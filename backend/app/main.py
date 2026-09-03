
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

ai_health_score.set(78)
ai_bottleneck_severity.set(2)
ai_p95_latency.set(49.29)


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
