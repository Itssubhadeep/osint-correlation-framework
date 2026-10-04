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


# Create database tables when the application starts
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


# --------------------------------------------------
# CREATE AN INVESTIGATION
# --------------------------------------------------

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


# --------------------------------------------------
# GET ALL INVESTIGATIONS
# --------------------------------------------------

@app.get(
    "/api/investigations",
    response_model=list[InvestigationResponse],
)
def get_investigations():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, query, sources, status, created_at
        FROM investigations
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    investigations = []

    for row in rows:
        investigations.append(
            {
                "id": row["id"],
                "query": row["query"],
                "sources": json.loads(row["sources"]),
                "status": row["status"],
                "created_at": row["created_at"],
            }
        )

    return investigations


# --------------------------------------------------
# GET ONE INVESTIGATION
# --------------------------------------------------

@app.get(
    "/api/investigations/{investigation_id}",
    response_model=InvestigationResponse,
)
def get_investigation(investigation_id: int):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT id, query, sources, status, created_at
        FROM investigations
        WHERE id = ?
        """,
        (investigation_id,),
    ).fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Investigation not found",
        )

    return {
        "id": row["id"],
        "query": row["query"],
        "sources": json.loads(row["sources"]),
        "status": row["status"],
        "created_at": row["created_at"],
    }