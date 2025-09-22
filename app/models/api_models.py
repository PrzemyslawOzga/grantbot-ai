from pydantic import BaseModel, Field
from typing import List


class GenerateRequest(BaseModel):
    """Request model for generating a section."""

    company_id: str
    section_type: str
    text: str = Field(..., min_length=1)


class GenerateResponse(BaseModel):
    """Response model with generated text and sources."""

    company_id: str
    section_type: str
    generated_text: str
    sources: List[str]
    request_id: str
    created_at: str


class HistoryEntry(BaseModel):
    """Single history entry for generated sections."""

    request_id: str
    company_id: str
    section_type: str
    created_at: str
