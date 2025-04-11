const http = require("http");

const postData = JSON.stringify({
  text: "the integral of cosine x from 0 to \\pi"
});

const options = {
  hostname: "localhost",
  port: 8000,
  path: "/latex",
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Content-Length": Buffer.byteLength(postData)
  }
};

const req = http.request(options, (res) => {
  let data = "";

  res.setEncoding("utf8");
  res.on("data", (chunk) => {
    data += chunk;
  });

  res.on("end", () => {
    console.log("Response from API:");
    try {
      const parsed = JSON.parse(data);
      console.log(parsed.latex);
    } catch (e) {
      console.error("Failed to parse response:", data);
    }
  });
});

req.on("error", (e) => {
  console.error(`Request error: ${e.message}`);
});

req.write(postData);
req.end();
