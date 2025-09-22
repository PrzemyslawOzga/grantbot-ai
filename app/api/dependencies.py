from app.core.search import GrantContextRetriever
from app.core.storage import HistoryStorage
from app.config import SEED_JSON


class AppDepends:
    def __init__(self, seed_path=SEED_JSON):
        self.retriever = None
        self.history_store = None
        self.seed_path = seed_path

    def get_retriever(self):
        """
        Return a singleton GrantContextRetriever with build index.
        """
        if self.retriever is None:
            self.retriever = GrantContextRetriever()
            self.build_retriever_index()

        return self.retriever

    def build_retriever_index(self):
        """
        Build index for returned a singleton GrantContextRetriever.
        """
        self.retriever.build_index(self.seed_path)

    def get_history_storage(self):
        """
        Return a singleton HistoryStore.
        """
        if self.history_store is None:
            self.history_store = HistoryStorage()

        return self.history_store
