import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.storage import HistoryStorage

@pytest.mark.integration
def test_grantbot_ai_full_flow(retriever, tmp_path):
    """Test generating a section via API and storing it in a temporary history."""
    client = TestClient(app)

    history_file = tmp_path / "history.json"
    storage = HistoryStorage(path=history_file)

    company_id = retriever.docs[0].company_id
    section_type = retriever.docs[0].section_type
    text = retriever.docs[0].text

    payload = {
        'company_id': company_id,
        'section_type': section_type,
        'text': text
    }
    response_generate = client.post('/api/generate-section', json=payload)
    data_generate = response_generate.json()

    storage.add(company_id, section_type)

    history = storage.list_for_company(company_id)

    assert response_generate.status_code == 200
    assert 'generated_text' in data_generate
    assert data_generate['company_id'] == company_id
    assert len(history) == 1
    assert history[0]['company_id'] == company_id
    assert history[0]['section_type'] == section_type
