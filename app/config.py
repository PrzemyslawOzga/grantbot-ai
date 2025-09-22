from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
HISTORY_FILE = DATA_DIR / "history.json"
SEED_JSON = DATA_DIR / "grantbot_vector_seed.json"
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-mpnet-base-v2"
TOP_K = 3
