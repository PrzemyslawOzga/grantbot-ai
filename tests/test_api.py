from fastapi.testclient import TestClient
from app.main import app
from app.core.storage import HistoryStorage

def test_api_generate_section():
    """Test that the generate-section endpoint returns generated text."""
    client = TestClient(app)
    payload = {
        "company_id": "123",
        "section_type": "market_analysis",
        "text": "Describe market.",
    }
    response = client.post("/api/generate-section", json=payload)
    data = response.json()
    assert response.status_code == 200
    assert "generated_text" in data
    assert data["company_id"] == "123"

def test_api_get_history(retriever):
    """Test that the history endpoint returns history entries for a company."""
    storage = HistoryStorage()
    company_id = retriever.docs[0].company_id
    section_type = retriever.docs[0].section_type
    storage.add(company_id, section_type)
    client = TestClient(app)
    response = client.get("/api/history/123")
    data = response.json()
    assert response.status_code == 200
    assert len(data) > 0
    assert data[0]["company_id"] == "123"
