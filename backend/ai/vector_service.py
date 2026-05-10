# MEMORY LAYER

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# In-memory store (MVP)
documents = []
index = None


def create_embedding(text: str):
    return model.encode([text])[0]


def add_document(text: str):
    global index

    embedding = create_embedding(text)

    documents.append(text)

    if index is None:
        dim = len(embedding)
        index = faiss.IndexFlatL2(dim)

    index.add(np.array([embedding]).astype("float32"))


def search_similar(query: str, k=3):
    if index is None or len(documents) == 0:
        return []

    query_embedding = create_embedding(query)

    distances, indices = index.search(
        np.array([query_embedding]).astype("float32"), k
    )

    results = []
    for idx in indices[0]:
        if idx < len(documents):
            results.append(documents[idx])

    return results