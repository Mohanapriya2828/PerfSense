import json
from pathlib import Path
from fastapi import FastAPI
from prometheus_client import Gauge
from prometheus_fastapi_instrumentator import Instrumentator
import time

app = FastAPI(
    title="PerfSense AI",
    version="1.0.0",
    description="AI-Driven Performance Testing Platform"
)

# Prometheus monitoring
Instrumentator().instrument(app).expose(app)
# AI Performance Analysis Metrics
ai_health_score = Gauge(
    "perfsense_ai_health_score",
    "Overall AI-generated performance health score"
)

ai_bottleneck_severity = Gauge(
    "perfsense_ai_bottleneck_severity",
    "AI bottleneck severity: 1=Low, 2=Moderate, 3=High, 4=Critical"
)

ai_p95_latency = Gauge(
    "perfsense_ai_p95_latency_ms",
    "AI analyzed P95 latency in milliseconds"
)

# AI-generated bottleneck recommendation information
ai_recommendation_info = Gauge(
    "perfsense_ai_recommendation_info",
    "AI-generated bottleneck diagnosis and optimization recommendation",
    ["bottleneck_id", "severity", "reason", "recommendation"]
)

ai_recommendation_info.labels(
    bottleneck_id="BOT001",
    severity="Moderate",
    reason="P95 latency remains around 49-50 ms across all tests, indicating a latency bottleneck rather than throughput or resource exhaustion.",
    recommendation="Investigate request handling, optimize serialization and database queries, implement caching, reduce blocking I/O, and monitor CPU and memory usage."
).set(1)

AI_METRICS_FILE = Path("analysis/output/grafana_ai_metrics.json")


def load_ai_metrics():
    if not AI_METRICS_FILE.exists():
        return

    with open(AI_METRICS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    ai_health_score.set(data.get("health_score", 0))
    ai_bottleneck_severity.set(data.get("severity_value", 0))
    ai_p95_latency.set(data.get("p95_latency_ms", 0))

    ai_recommendation_info.clear()

    ai_recommendation_info.labels(
        bottleneck_id=data.get("bottleneck_id", "UNKNOWN"),
        severity=data.get("severity", "Unknown"),
        reason=data.get("reason", ""),
        recommendation=data.get("recommendation", "")
    ).set(1)


load_ai_metrics()


@app.get("/")
def home():
    return {"message": "Welcome to PerfSense AI 🚀"}


@app.get("/users")
def users():
    return [
        {
            "id": i,
            "name": f"User {i}",
            "email": f"user{i}@example.com",
            "age": 20 + (i % 40),
            "city": f"City {i % 10}"
        }
        for i in range(1, 5001)
    ]


@app.get("/products")
def products():
    return [
        {
            "id": i,
            "name": f"Product {i}",
            "price": 100 + (i * 10),
            "category": f"Category {i % 10}",
            "stock": i % 100
        }
        for i in range(1, 5001)
    ]


@app.get("/slow")
def slow():
    time.sleep(2)
    return {
        "message": "This endpoint intentionally responds slowly."
    }
