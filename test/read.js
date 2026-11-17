const autocannon = require("autocannon");

const BASE_URL = process.env.BASE_URL || "http://localhost";
const DURATION = Number(process.env.DURATION || 15);
const CONNECTIONS = Number(process.env.CONNECTIONS || 20);
const TARGET_URL = "https://example.com";
// Optional: reuse an existing short link instead of creating a new one.
// Accepts a full URL (http://localhost/link/abc123) or just a path (/link/abc123).
const SHORT_LINK = process.env.SHORT_LINK;
// The read endpoint redirects with 301, so that is the successful response.
const EXPECTED_STATUS = Number(process.env.EXPECTED_STATUS || 301);

function toPath(value) {
  return value.startsWith("http") ? new URL(value).pathname : value;
}

async function createShortLink() {
  const response = await fetch(`${BASE_URL}/link/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ long_link: TARGET_URL }),
  });

  if (response.status === 429) {
    throw new Error(
      "Rate limit reached while creating a short link (HTTP 429). " +
        "The POST /link/ endpoint is limited by RATE_LIMIT_WRITE (default: 10/minute). " +
        "Wait about 60 seconds and try again, raise RATE_LIMIT_WRITE in backend/.env " +
        "and recreate the containers, or pass SHORT_LINK=/link/<code> to reuse an existing link.",
    );
  }

  if (!response.ok) {
    throw new Error(
      `Failed to create a short link (HTTP ${response.status}). Is the stack running?`,
    );
  }

  const data = await response.json();

  console.log(`Created short link: ${data.short_link}`);
  return toPath(data.short_link);
}

function getStatusCodeStats(result) {
  return result.statusCodeStats || {};
}

function printStatusSummary(result) {
  const stats = getStatusCodeStats(result);
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
  const stats = getStatusCodeStats(result);
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

// autocannon only treats 2xx as successful, which is misleading for this API:
// the expected response here is a 301 redirect. We print the tables ourselves
// and drop the "0 2xx responses, N non 2xx responses" line.
function formatAutocannonResult(result) {
  return autocannon
    .printResult(result)
    .split("\n")
    .filter((line) => !/2xx responses,.*non 2xx responses/.test(line))
    .join("\n");
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

    console.log(formatAutocannonResult(result));
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

  autocannon.track(instance, {
    renderProgressBar: false,
    renderResultsTable: false,
  });
}

(async () => {
  try {
    const path = SHORT_LINK ? toPath(SHORT_LINK) : await createShortLink();
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
