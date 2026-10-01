from pydantic import BaseModel, Field


class InvestigationCreate(BaseModel):
    query: str = Field(min_length=2, max_length=200)
    sources: list[str] = Field(min_length=1)


class InvestigationResponse(BaseModel):
    id: int
    query: str
    sources: list[str]
    status: str
    created_at: str