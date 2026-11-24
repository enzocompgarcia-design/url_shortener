import { formatAutocannonResult, createShortLink } from "./util.js";
import { randomBytes } from "node:crypto";

import autocannon from "autocannon";

const DURATION = 15;
const CONNECTIONS = 20;

const BASE_URL = "http://localhost";

const BATCH_SIZE = 10;
const CACHED_REQUESTS = 8;
const MISSING_REQUESTS = BATCH_SIZE - CACHED_REQUESTS;

const CACHED_STATUS = 301;
const MISSING_STATUS = 404;
const EXPECTED_CACHED_RATE = 80;
const RATE_TOLERANCE = 5; // pontos percentuais

function missingCode() {
  return `inexistente-${randomBytes(4).toString("hex")}`;
}

async function warmCache(path) {
  const response = await fetch(`${BASE_URL}${path}`, { redirect: "manual" });

  if (response.status !== CACHED_STATUS) {
    throw new Error(
      `Cache warm-up failed: expected ${CACHED_STATUS} for ${path}, got ${response.status}.`,
    );
  }

  console.log(`Cache warmed: ${path} -> ${response.headers.get("location")}`);
}

function buildRequests(validPath) {
  const requests = [];

  for (let i = 0; i < CACHED_REQUESTS; i++) {
    requests.push({ path: validPath });
  }

  for (let i = 0; i < MISSING_REQUESTS; i++) {
    requests.push({ path: `/link/${missingCode()}` });
  }

  for (let i = requests.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [requests[i], requests[j]] = [requests[j], requests[i]];
  }

  return requests;
}

function printStatusSummary(result) {
  const stats = result.statusCodeStats;
  const total = Object.values(stats).reduce((sum, item) => sum + item.count, 0);
  const cached = stats[CACHED_STATUS]?.count || 0;
  const missing = stats[MISSING_STATUS]?.count || 0;
  const classified = cached + missing;
  const cachedRate = classified > 0 ? (cached / classified) * 100 : 0;
  const missingRate = classified > 0 ? (missing / classified) * 100 : 0;

  console.log("\nStatus code breakdown:");
  Object.entries(stats)
    .sort(([a], [b]) => Number(a) - Number(b))
    .forEach(([status, { count }]) => {
      let marker = "";
      if (Number(status) === CACHED_STATUS) marker = " (cached short link)";
      if (Number(status) === MISSING_STATUS) marker = " (nonexistent link)";
      console.log(`  ${status}${marker}: ${count}`);
    });

  console.log(
    `\nCached short links (${CACHED_STATUS}): ${cached}/${classified} ` +
      `(${cachedRate.toFixed(2)}%, target ${EXPECTED_CACHED_RATE}%)`,
  );
  console.log(
    `Nonexistent links (${MISSING_STATUS}): ${missing}/${classified} ` +
      `(${missingRate.toFixed(2)}%, target ${100 - EXPECTED_CACHED_RATE}%)`,
  );

  return { total, cached, missing, cachedRate };
}

function printHints(result) {
  const stats = result.statusCodeStats;
  const tooManyRequests = stats[429]?.count || 0;

  if (tooManyRequests > 0) {
    console.log(
      "\nHint: some requests were rate limited (429). The GET /link/{code} " +
        "endpoint is limited by RATE_LIMIT_READ (default: 120/minute). " +
        "Raise it in backend/.env and recreate the containers for a realistic load test.",
    );
  }
}

function runHybridLoadTest(validPath) {
  const requests = buildRequests(validPath);

  console.log(
    `\nRunning hybrid load test: 80% valid links and 20% invalid links ...`,
  );

  const instance = autocannon({
    url: BASE_URL,
    connections: CONNECTIONS,
    duration: DURATION,
    pipelining: 1,
    requests,
  });

  instance.on("done", (result) => {
    const { total, cached, missing, cachedRate } = printStatusSummary(result);

    console.log(formatAutocannonResult(autocannon, result));
    printHints(result);

    if (total === 0) {
      console.error("\nNo responses were received; the load test did not run.");
      process.exitCode = 1;
    } else if (cached === 0 || missing === 0) {
      console.error(
        `\nThe mix was not exercised: expected both ${CACHED_STATUS} and ${MISSING_STATUS} responses.`,
      );
      process.exitCode = 1;
    } else if (Math.abs(cachedRate - EXPECTED_CACHED_RATE) > RATE_TOLERANCE) {
      console.error(
        `\nObserved cached-link rate (${cachedRate.toFixed(2)}%) is off target ` +
          `(expected ${EXPECTED_CACHED_RATE}% +/- ${RATE_TOLERANCE} points).`,
      );
      process.exitCode = 1;
    }
  });
}

(async () => {
  try {
    const path = await createShortLink();

    await warmCache(path);

    runHybridLoadTest(path);
  } catch (error) {
    console.error(`\nError: ${error.message}`);
    console.error(
      "Make sure the application is running (docker compose up --build -d) and accessible at BASE_URL.",
    );
    process.exit(1);
  }
})();
