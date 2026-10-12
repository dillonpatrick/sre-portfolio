import time
from flask import Flask, Response, request, g
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

app = Flask(__name__)

http_request_total = Counter(
    name="http_request_total",
    documentation="Total number of HTTP requests",
    labelnames=["method", "endpoint", "status_code"],
)

http_request_duration_seconds = Histogram(
    name="http_request_duration_seconds",
    documentation="HTTP request duration in seconds",
    labelnames=["method", "endpoint"],
)


@app.before_request
def before_request():
    g.start_time = time.perf_counter()


@app.after_request
def after_request(response):
    duration = time.perf_counter() - g.start_time

    http_request_total.labels(
        method=request.method,
        endpoint=request.path,
        status_code=str(response.status_code),
    ).inc()

    http_request_duration_seconds.labels(
        method=request.method, endpoint=request.path
    ).observe(duration)

    return response


@app.get("/")
def home():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/simulate-error")
def simulate_error():
    return {"status": "error"}, 500


@app.get("/simulate-slow")
def simutale_slow():
    time.sleep(0.3)
    return {"status": "slow"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
