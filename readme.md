# Lexi RAG Backend – Legal Query Assistant

This is a production-ready Retrieval-Augmented Generation (RAG) backend service for legal queries. It accepts a natural language question, retrieves relevant legal document snippets, and generates an answer along with citation metadata.

## Features

- Built with **FastAPI**
- Uses **sentence-transformers** for embedding
- Vector search powered by **FAISS**
- Text extraction from **PDF** and **DOCX**
- **Together AI** integration for answer generation
- Citation support with metadata (filename, chunk text)
- Simple and modular structure

---

## Folder Structure
    lexi-rag-backend/
    ├── data/ # Stores index.faiss and metadata.json
    ├── docs/ # Raw PDF/DOCX legal documents
    ├── utils/ # Core logic (embedder, loader, vectorstore)
    │ ├── embedder.py
    │ ├── loader.py
    │ ├── vectorstore.py
    ├── build_index.py # Script to build vector index
    ├── main.py # FastAPI app
    ├── .env # API keys and config
    ├── requirements.txt
    └── README.md


---

## Setup Instructions

1. **Clone the repository**


2. **Install dependencies**

      Ensure Python 3.10+ is installed.

      ```bash
      pip install -r requirements.txt
      ```

3. **create a .env file**

      TOGETHER_API_KEY=your_together_ai_key

4. **Add legal documents**

      Place .pdf and .docx files inside the docs/ folder.

4. **Build the index**

      ```bash
      python build_index.py
      ```
4. **Run the server**

      ```bash
      uvicorn main:app --reload
      ```

The API will be available at http://localhost:8000


POST /query
{
  "query": "Is an insurance company liable if a transport vehicle is used without a valid permit?"
}

Response Format:

{
  "answer": "No, the insurance company is not liable...",
  "citations": [
    {
      "text": "Relevant legal excerpt...",
      "source": "case_law.docx"
    }
  ]
}






