from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import time

app = FastAPI(
    title="PerfSense AI",
    version="1.0.0",
    description="AI-Driven Performance Testing Platform"
)

Instrumentator().instrument(app).expose(app)

@app.get("/")
def home():
    return {"message": "Welcome to PerfSense AI 🚀"}

@app.get("/users")
def users():
    return [
        {"id": 1, "name": "John"},
        {"id": 2, "name": "Alice"},
        {"id": 3, "name": "Bob"}
    ]

@app.get("/products")
def products():
    return [
        {"id": 101, "name": "Laptop", "price": 65000},
        {"id": 102, "name": "Phone", "price": 30000},
        {"id": 103, "name": "Headphones", "price": 2000}
    ]

@app.get("/slow")
def slow():
    time.sleep(2)
    return {"message": "This endpoint intentionally responds slowly."}