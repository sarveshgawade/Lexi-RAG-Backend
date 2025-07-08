from fastapi import FastAPI
from pydantic import BaseModel
from utils.embedder import embed_texts
from utils.vectorstore import load_index
import numpy as np
from dotenv import load_dotenv
import os
import requests

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

app = FastAPI()
index, metadata = load_index()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query(data: QueryRequest):
    query_text = data.query
    query_embedding = embed_texts([query_text])[0]

    # Search top-5 relevant chunks
    D, I = index.search(np.array([query_embedding]).astype("float32"), k=5)
    top_chunks = [metadata[i] for i in I[0]]

    # Build context
    context = "\n\n".join([chunk["chunk"] for chunk in top_chunks])

    prompt = f"""
You are a legal assistant. Based only on the legal documents below, answer the user's question clearly and concisely.

Documents:
{context}

Question:
{query_text}

Answer:
""".strip()

    try:
        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",  
                "messages": [
                    {"role": "system", "content": "You are a helpful legal assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 500
            }
        )

        result = response.json()

        answer = result["choices"][0]["message"]["content"].strip()

        return {
            "answer": answer,
            "citations": [
                {
                    "text": chunk["chunk"],
                    "source": chunk["filename"]
                }
                for chunk in top_chunks
            ]
        }

    except Exception as e:
        return {"error": str(e)}
