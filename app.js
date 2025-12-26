import http from "http";
import { request as httpsRequest } from "https";
import { URL } from "url";

const ORIGIN = "https://announcement-amsterdam-0-alpaca.dynast.cloud";

http.createServer((req, res) => {
    const url = new URL(req.url, ORIGIN);

    const options = {
        protocol: url.protocol,
        hostname: url.hostname,
        port: 443,
        path: url.pathname + url.search,
        method: req.method,
        headers: {
            ...req.headers,
            host: url.hostname,
            "x-forwarded-host": req.headers.host
        }
    };

    const proxyReq = httpsRequest(options, proxyRes => {
        res.writeHead(proxyRes.statusCode, proxyRes.headers);
        proxyRes.pipe(res, { end: true });
    });

    proxyReq.on("error", err => {
        res.writeHead(502);
        res.end("Bad Gateway");
    });

    if (!["GET", "HEAD"].includes(req.method)) {
        req.pipe(proxyReq, { end: true });
    } else {
        proxyReq.end();
    }
}).listen(80, "0.0.0.0");
