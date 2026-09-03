from fastapi import FastAPI, Response
from prometheus_fastapi_instrumentator import Instrumentator
import time
import json

app = FastAPI(
    title="PerfSense AI",
    version="1.0.0",
    description="AI-Driven Performance Testing Platform"
)

Instrumentator().instrument(app).expose(app)

USERS_JSON = json.dumps([
    {
        "id": i,
        "name": f"User {i}",
        "email": f"user{i}@example.com",
        "age": 20 + (i % 40),
        "city": f"City {i % 10}"
    }
    for i in range(1, 5001)
])

PRODUCTS_JSON = json.dumps([
    {
        "id": i,
        "name": f"Product {i}",
        "price": 100 + (i * 10),
        "category": f"Category {i % 10}",
        "stock": i % 100
    }
    for i in range(1, 5001)
])

@app.get("/")
def home():
    return {"message": "Welcome to PerfSense AI 🚀"}

@app.get("/users")
def users():
    return Response(
        content=USERS_JSON,
        media_type="application/json"
    )

@app.get("/products")
def products():
    return Response(
        content=PRODUCTS_JSON,
        media_type="application/json"
    )

@app.get("/slow")
def slow():
    time.sleep(2)
    return {"message": "This endpoint intentionally responds slowly."}