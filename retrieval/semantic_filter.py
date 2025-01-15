# from ctypes import util
# from sentence_transformers import SentenceTransformer


from sentence_transformers.util import pytorch_cos_sim  # Correct import

def semantic_filter(query, documents):
    from sentence_transformers import SentenceTransformer, util

    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode(query, convert_to_tensor=True)
    document_embeddings = model.encode([doc.page_content for doc in documents], convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(query_embedding, document_embeddings).squeeze(0)
    unique_docs = {}
    for idx, sim_score in enumerate(similarities):
        content = documents[idx].page_content.strip()
        if content not in unique_docs:
            unique_docs[content] = (documents[idx], sim_score.item())

    # Sort by similarity score
    sorted_docs = sorted(unique_docs.values(), key=lambda x: x[1], reverse=True)
    if not sorted_docs:
        print("No relevant documents found.")
        return []

    print("Top filtered docs:", [doc[0].page_content for doc in sorted_docs[:5]])
    return [doc[0] for doc in sorted_docs[:5]]
