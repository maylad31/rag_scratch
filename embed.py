from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "jinaai/jina-embeddings-v2-small-en", # switch to en/zh for English or Chinese
    trust_remote_code=True
)
model.max_seq_length = 8192

def embed_docs(docs:list):
    return model.encode(docs,normalize_embeddings=True)