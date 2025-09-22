from app.core.search import GrantContextRetriever
from app.core.storage import HistoryStore


class AppDepends:
    def __init__(self):
        self.retriever = None
        self.history_store = None

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
        self.retriever.build_index()

    def get_history_store(self):
        """
        Return a singleton HistoryStore.
        """
        if self.history_store is None:
            self.history_store = HistoryStore()

        return self.history_store
