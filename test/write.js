
const autocannon = require("autocannon");

const instance = autocannon({
  url: "http://localhost/link/",
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    long_link: "https://google.com",
  }),
  connections: 20,
  duration: 15,
  pipelining: 1,
});

const statusCounts = {};

instance.on("response", (client, statusCode) => {
  statusCounts[statusCode] = (statusCounts[statusCode] || 0) + 1;
});

instance.on("done", (result) => {
  console.log("Status HTTP:", statusCounts);
  console.log(autocannon.printResult(result));
});

instance.on("done", (result) => {
  console.log(autocannon.printResult(result));
});
