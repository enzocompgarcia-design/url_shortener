const autocannon = require("autocannon");
const crypto = require("crypto");

const statusCounts = {};
let requestCount = 0;

const instance = autocannon({
  url: "http://localhost",
  connections: 20,
  duration: 15,
  pipelining: 1,

  setupRequest: (req) => {
    requestCount++;

    if (requestCount % 100 === 0) {
      req.path = "/link/b7gJ7";
    } else {
      req.path = `/link/${crypto.randomBytes(5).toString("base64url")}`;
    }

    return req;
  },
});

instance.on("response", (client, statusCode) => {
  statusCounts[statusCode] = (statusCounts[statusCode] || 0) + 1;
});

instance.on("done", (result) => {
  console.log("HTTP status counts:", statusCounts);
  console.log("Total de requisições geradas:", requestCount);
  console.log(autocannon.printResult(result));
});