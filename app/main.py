import json
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException

from app.database import create_tables, get_connection
from app.schemas import InvestigationCreate, InvestigationResponse


app = FastAPI(
    title="OSINT Correlation Framework",
    description="Multi-signal cross-source entity correlation API",
    version="0.1.0",
)


create_tables()


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


@app.post(
    "/api/investigations",
    response_model=InvestigationResponse,
    status_code=201,
)
def create_investigation(investigation: InvestigationCreate):
    created_at = datetime.now(timezone.utc).isoformat()

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO investigations (query, sources, status, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            investigation.query,
            json.dumps(investigation.sources),
            "created",
            created_at,
        ),
    )

    connection.commit()

    investigation_id = cursor.lastrowid

    connection.close()

    return {
        "id": investigation_id,
        "query": investigation.query,
        "sources": investigation.sources,
        "status": "created",
        "created_at": created_at,
    }