from fastapi import FastAPI

app = FastAPI(
    title="OSINT Correlation Framework",
    description="Multi-signal cross-source entity correlation API",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "OSINT Correlation Framework API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }