import json
import numpy as np

from sentence_transformers import SentenceTransformer
from app.config import TOP_K, EMBEDDING_MODEL_NAME
from app.models.db_models import KBDocument


class GrantContextRetriever:
    """
    Responsible for retrieving context (document fragments).
    GrantContextRetriever workflow:
        1. Load source documents from JSON files.
        2. Create embeddings for document texts.
        3. Finds the most similar fragments to a given query.
    """

    def __init__(self, model_name=EMBEDDING_MODEL_NAME):
        self.model_name = model_name
        self.model = None
        self.embeddings = None
        self.docs = []

    def load_model(self, model_name):
        """Load a SentenceTransformer model for creating embeddings."""
        if model_name:
            self.model_name = model_name
        if not self.model_name:
            raise ValueError("No embedding model specified.")
        self.model = SentenceTransformer(model_name)

    def build_index(self, seed_path):
        """
        Load documents from a JSON seed file and build embeddings.
        """
        try:
            with open(seed_path, "r", encoding="utf-8") as seed_file:
                lines = [
                    json.loads(line) for line in seed_file if line.strip()
                ]
        except FileNotFoundError:
            print(f"Couldn't find seed file: {seed_path}.")
            raise

        self.docs = []
        for line in lines:
            doc = KBDocument(**line)
            self.docs.append(doc)

        texts = []
        for doc in self.docs:
            texts.append(doc.text)

        if texts:
            if self.model is None:
                self.load_model(self.model_name)
                self.embeddings = np.array(self.model.encode(texts))
            else:
                self.embeddings = np.zeros((0, 1))

    def search(self, query, top_k=TOP_K, company_id=None):
        """
        Search for the top_k most similar documents to the query. Optionally filter by company_id.
        """
        if self.model is None:
            self.load_model(self.model_name)

        if self.embeddings is None or len(self.docs) == 0:
            print(f"No documents in index. Returning empty results.")
            return []

        results = []
        threshold = 0.1

        if company_id:
            candidate_docs = []
            for doc in self.docs:
                if doc.company_id == company_id:
                    candidate_docs.append(doc)

            texts = []
            for doc in candidate_docs:
                texts.append(doc.text)

            embeddings = self.model.encode(texts, show_progress_bar=False)

        else:
            candidate_docs = self.docs
            embeddings = self.embeddings

        embeddings_normalization = embeddings / np.linalg.norm(
            embeddings, axis=1, keepdims=True
        )

        query_embeddings = self.model.encode([query])[0]
        query_normalization = query_embeddings / np.linalg.norm(
            query_embeddings
        )

        similarity = embeddings_normalization.dot(query_normalization)
        idx = np.argsort(-similarity)[:top_k]
        for i in idx:
            if similarity[i] >= threshold:
                doc = candidate_docs[i]
                sim_score = float(similarity[i])
                results.append((doc, sim_score))

        return results
