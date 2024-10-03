# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World! From K8s!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# Liveness Probe Endpoint
@app.get("/healthz")
def healthz():
    # Add logic here to check application health if needed
    return {"status": "ok"}

# Readiness Probe Endpoint
@app.get("/ready")
def ready():
    # Add logic here to check if the application is ready to accept traffic
    return {"status": "ready"}
