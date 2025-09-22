import os
import pytest
from app.api.dependencies import AppDepends

TEST_JSON_PATH = os.path.join(os.path.dirname(__file__), "test_data", "test_data.json")

@pytest.fixture
def retriever():
    """Create a GrantContextRetriever and build index from test JSON."""
    app_depends = AppDepends(seed_path=TEST_JSON_PATH)
    retriever = app_depends.get_retriever()
    return retriever
