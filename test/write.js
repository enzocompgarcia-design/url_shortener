const autocannon = require("autocannon");

const BASE_URL = process.env.BASE_URL || "http://localhost";
const DURATION = Number(process.env.DURATION || 15);
const CONNECTIONS = Number(process.env.CONNECTIONS || 20);
const TARGET_URL = "https://example.com";

const statusCounts = {};

const instance = autocannon({
  url: `${BASE_URL}/link/`,
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    long_link: TARGET_URL,
  }),
  connections: CONNECTIONS,
  duration: DURATION,
  pipelining: 1,
});

instance.on("response", (client, statusCode) => {
  statusCounts[statusCode] = (statusCounts[statusCode] || 0) + 1;
});

instance.on("done", (result) => {
  console.log("\nHTTP status counts:", statusCounts);
  console.log(autocannon.printResult(result));

  const tooManyRequests = statusCounts[429] || 0;

  if (tooManyRequests > 0) {
    console.log(
      "\nHint: some requests were rate limited (429). The POST /link/ endpoint " +
        "is limited by RATE_LIMIT_WRITE (default: 10/minute). " +
        "Raise it in backend/.env and recreate the containers for a realistic load test.",
    );
  }
});

autocannon.track(instance, { renderProgressBar: false });
