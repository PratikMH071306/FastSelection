# # vector_store.py
# import chromadb
# from sentence_transformers import SentenceTransformer

# client = chromadb.Client()
# collection = client.get_or_create_collection("chat_queries")
# model = SentenceTransformer("all-MiniLM-L6-v2")

# def store_query(text: str, metadata: dict):
#     embedding = model.encode(text).tolist()
#     collection.add(documents=[text], embeddings=[embedding], metadatas=[metadata], ids=[text])

# def search_similar(text: str, top_k: int = 3):
#     embedding = model.encode(text).tolist()
#     return collection.query(query_embeddings=[embedding], n_results=top_k)
