import { createShortLink, formatAutocannonResult } from "./util.js";
import autocannon from "autocannon";

const DURATION = 15;
const CONNECTIONS = 20;
const EXPECTED_STATUS = 301;

const BASE_URL = "http://localhost";

function printStatusSummary(result) {
  const stats = result.statusCodeStats;
  const total = Object.values(stats).reduce((sum, item) => sum + item.count, 0);
  const expected = stats[EXPECTED_STATUS]?.count || 0;
  const expectedRate = total > 0 ? (expected / total) * 100 : 0;

  console.log("\nStatus code breakdown:");
  Object.entries(stats)
    .sort(([a], [b]) => Number(a) - Number(b))
    .forEach(([status, { count }]) => {
      const marker = Number(status) === EXPECTED_STATUS ? " (expected redirect)" : "";
      console.log(`  ${status}${marker}: ${count}`);
    });

  console.log(
    `\nSuccessful redirects (${EXPECTED_STATUS}): ${expected}/${total} (${expectedRate.toFixed(2)}%)`,
  );

  return { total, expected };
}

function printHints(result) {
  const stats = result.statusCodeStats;
  const tooManyRequests = stats[429]?.count || 0;
  const notFound = stats[404]?.count || 0;

  if (tooManyRequests > 0) {
    console.log(
      "\nHint: some requests were rate limited (429). The GET /link/{code} " +
        "endpoint is limited by RATE_LIMIT_READ (default: 120/minute). " +
        "Raise it in backend/.env and recreate the containers for a realistic load test.",
    );
  }

  if (notFound > 0) {
    console.log(
      "\nHint: some requests returned 404. Check that SHORT_LINK points to an existing link.",
    );
  }
}

function runReadLoadTest(path) {
  const instance = autocannon({
    url: `${BASE_URL}${path}`,
    connections: CONNECTIONS,
    duration: DURATION,
    pipelining: 1,
  });

  instance.on("done", (result) => {
    const { total, expected } = printStatusSummary(result);

    console.log(formatAutocannonResult(autocannon, result));
    printHints(result);

    if (total === 0) {
      console.error("\nNo responses were received; the load test did not run.");
      process.exitCode = 1;
    } else if (expected === 0) {
      console.error(
        `\nNo ${EXPECTED_STATUS} responses were received; the redirect path was not exercised.`,
      );
      process.exitCode = 1;
    }
  });
}

(async () => {
  try {
    const path = await createShortLink();

    console.log(`Running read load test against ${BASE_URL}${path} ...`);

    runReadLoadTest(path);

  } catch (error) {
    console.error(`\nError: ${error.message}`);
    console.error(
      "Make sure the application is running (docker compose up --build -d) and accessible at BASE_URL.",
    );
    process.exit(1);
  }
})();
