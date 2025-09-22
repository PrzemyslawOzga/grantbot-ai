from pydantic import BaseModel
from typing import Optional, List


class KBDocument(BaseModel):
    """
    Model representing a single document in the Knowledge Base (KB).
    """

    id: str
    company_id: Optional[str]
    section_type: Optional[str]
    language: Optional[str]
    tags: Optional[List[str]]
    source_type: Optional[str]
    source_url: Optional[str]
    created_at: Optional[str]
    text: str
