from utils.loader import load_documents
from utils.embedder import embed_texts
from utils.vectorstore import build_faiss_index, save_index

docs = load_documents("docs")
print(f"[DEBUG] Loaded {len(docs)} chunks")

texts = [doc["chunk"] for doc in docs]
if not texts:
    print("[ERROR] No texts found for embedding. Check your docs folder and file types.")
    exit(1)

embeddings = embed_texts(texts)
print(f"[DEBUG] Got {len(embeddings)} embeddings")

index = build_faiss_index(embeddings)
save_index(index, docs)

print(f"Indexed {len(docs)} chunks.")
