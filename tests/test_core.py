import pytest
from app.core.storage import HistoryStorage
from app.core.generator import generator
from app.api.dependencies import AppDepends

TEST_JSON_PATH = "./tests/test_data/test_data.json"

@pytest.fixture
def retriever():
    """Create a GrantContextRetriever and build index from test JSON."""
    app_depends = AppDepends(seed_path=TEST_JSON_PATH)
    retriever = app_depends.get_retriever()
    return retriever

def test_core_generator(retriever):
    """Test generator output contains input text and document references."""
    input_text = "input text"
    contexts = retriever.docs
    output = generator(input_text, contexts)
    assert "input text" in output
    assert "doc-" in output

def test_core_search_load_model_and_build_index(retriever):
    """Check that documents are loaded from JSON."""
    assert len(retriever.docs) > 0
    assert any(doc.id.startswith("doc-") for doc in retriever.docs)

def test_core_search_search(retriever):
    """Search for 'AI' and expect at least one match."""
    results = retriever.search("AI")
    assert len(results) > 0
    assert any("AI" in doc.text for doc, _ in results)

def test_core_search_company_filter(retriever):
    """Search only within company_id='123'."""
    results = retriever.search("market", company_id="123")
    assert len(results) > 0
    assert all(doc.company_id == "123" for doc, _ in results)

def test_core_search_no_results(retriever):
    """Search for a nonsense query returns empty or zero results."""
    results = retriever.search("thisdoesnotexist123")
    assert isinstance(results, list) and len(results) == 0

def test_core_storage(tmp_path, retriever):
    """Test adding and retrieving entries in HistoryStorage."""
    history_file = tmp_path / "history.json"
    storage = HistoryStorage(path=history_file)
    company_id = retriever.docs[0].company_id
    section_type = retriever.docs[0].section_type
    entry = storage.add(company_id, section_type)
    entries = storage.list_for_company("123")
    assert entry["company_id"] == "123"
    assert entry["section_type"] == "market_analysis"
    assert "request_id" in entry
    assert "created_at" in entry
    assert len(entries) == 1
    assert entries[0]["request_id"] == entry["request_id"]
    assert storage.list_for_company("999") == []
