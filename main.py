from flask import Flask, request, Response
import requests

ORIGIN = "https://announcement-amsterdam-0-alpaca.dynast.cloud"

app = Flask(__name__)

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
def proxy(path):
    target_url = f"{ORIGIN}/{path}"

    headers = dict(request.headers)
    headers["Host"] = "announcement-amsterdam-0-alpaca.dynast.cloud"
    headers["X-Forwarded-Host"] = request.host

    resp = requests.request(
        method=request.method,
        url=target_url,
        headers=headers,
        params=request.args,
        data=request.get_data(),
        allow_redirects=False
    )

    excluded = {"content-encoding", "content-length", "transfer-encoding", "connection"}
    response_headers = [
        (k, v) for k, v in resp.headers.items()
        if k.lower() not in excluded
    ]

    return Response(resp.content, resp.status_code, response_headers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
