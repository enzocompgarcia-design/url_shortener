const TARGET_URL = "https://example.com";
const BASE_URL = "http://localhost";


export async function createShortLink() {
  const response = await fetch(`${BASE_URL}/link/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ long_link: TARGET_URL }),
  });

  if (response.status === 429) {
    throw new Error(
      "Rate limit reached while creating a short link (HTTP 429). " +
        "The POST /link/ endpoint is limited by RATE_LIMIT_WRITE (default: 10/minute). " +
        "Wait about 60 seconds and try again, or raise RATE_LIMIT_WRITE in backend/.env " +
        "and recreate the containers.",
    );
  }

  if (!response.ok) {
    throw new Error(
      `Failed to create a short link (HTTP ${response.status}). Is the stack running?`,
    );
  }

  const data = await response.json();

  console.log(`Created short link: ${data.short_link}`);

  return new URL(data.short_link).pathname;
}

export function formatAutocannonResult(autocannon, result) {
  return autocannon
    .printResult(result)
    .split("\n")
    .filter((line) => !/2xx responses,.*non 2xx responses/.test(line))
    .join("\n");
}