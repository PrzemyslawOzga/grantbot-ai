# GrantBot.ai Backend

This project is a backend service for generating sections of grant applications using 
contextual information from a knowledge base. It implements a **RAG-style approach**: 
retrieving relevant document fragments to support section generation. In this version, 
the program does not use artificial intelligence text completion – this is a plan 
for future development.

---

## Project overview

- `app/main.py` – FastAPI app with endpoints and a simple HTML form.
- `app/config.py` – Project configuration (paths, model name, top-k results, seed path).
- `app/api/dependencies.py` – AppDepends class providing singleton access to retriever and 
history storage.
- `app/api/endpoints.py` – API routes for generating sections and viewing history.
- `app/core/search.py` – GrantContextRetriever for embedding-based context search.
- `app/core/generator.py` – Generates HTML-based sections using input and context.
- `app/core/storage.py` – HistoryStorage class for JSON-based request history.
- `app/models/` – Pydantic models for API requests/responses and database documents.
- `app/utils/` – Utility functions, e.g., for timestamps and UUID generation.
- `data/` – Seed data (knowledge base JSON or CSV files).
- `tests/` – Unit and integration tests for API and core modules.

### Assumptions & simplifications

Grantbot.ai uses SentenceTransformer embeddings (`paraphrase-multilingual-mpnet-base-v2`) 
to find documents that are similar to the user’s input. This works in a RAG-style way, 
meaning it retrieves the top most relevant fragments from the knowledge base. The history 
of API calls (company ID, section type, timestamp, request UUID) is stored locally in a 
JSON file (history.json).

Users can submit text via the `/submit` form, and the system returns a ready-made section 
in HTML, showing both the input text and the retrieved context snippets. For developers, 
the `/api/generate-section` endpoint provides structured JSON output.

Grantbot.ai uses seed data located in the data/ directory in .json format. The generator 
simply combines the input text with the retrieved fragments into formatted HTML. Currently, 
the project does not use AI-based text completion – this is planned for future development. 
By default, only the top three most relevant documents are used.

### Justification

**FastAPI architecture** – FastAPI was chosen due to my familiarity with it. It allows
for clear, modular endpoint definitions, automatic validation, and clean project 
structure, making the backend easy to navigate, maintain, and extend.

**SentenceTransformer embeddings (`paraphrase-multilingual-mpnet-base-v2`)** - this model 
provides multilingual semantic embeddings, enabling highly accurate similarity-based 
retrieval of document fragments. Compared to lightweight MiniLLM-style models, it 
captures semantic nuances more reliably, making it better suited for retrieving relevant
context from a knowledge base while still being lightweight enough to run locally.

---

## Local setup, run steps & application support

### Setup by terminal
```
# Preferred python version is Python 3.10.x
python --version

# Clone repository
git clone https://github.com/PrzemyslawOzga/grantbot-ai.git
cd grantbot-ai

# Create virtual env
python -m venv venv
venv\Scripts\activate  # for Windows systems

# Install all requirements
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-test.txt  # if you would like to run tests

# Ensure data/grantbot_vector_seed.json is available, then please run in terminal:
uvicorn app.main:app --reload
```

### Setup by dockerfile
```
# Flag -t grantbot-ai - add name for docker image
docker build -t grantbot-ai .

# When container build successful, run container
docker run -p 8000:8000 grantbot-ai

# If you run containter in Docker Desktop App please configure port = 8000
# In console you should see below log:
# Uvicorn running on http://0.0.0.0:8000
# But please use url - http://localhost:8000/
# In powershell you can read dockerfile logs by:
# docker ps
# docker logs <container_id>
```

### Application support
Once the server is running, the backend API is available at: http://127.0.0.1:8000 .
You can interact with the API directly through HTTP requests, or explore the 
automatically generated interactive documentation provided by FastAPI at: http://127.0.0.1:8000/docs .
