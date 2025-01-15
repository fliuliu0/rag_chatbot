# def construct_llm_query(query, documents_text):
#     if "what is" in query.lower():
#         return f"Based on the following content, provide a detailed description of GEM:\n{documents_text}"
#     elif "year" in query.lower() or "founded" in query.lower():
#         return f"Based on the following content, identify the year GEM was founded:\n{documents_text}\nIf the founding year is not mentioned, respond with 'Information not available.'"
#     elif "location" in query.lower() or "address" in query.lower():
#         return f"Extract the location details from the following content:\n{documents_text}"
#     elif "services" in query.lower():
#         return f"List all the services mentioned in the following content:\n{documents_text}"
#     elif "countries" in query.lower():
#         return f"List the countries where GEM operates based on the following content:\n{documents_text}"
#     else:
#         return f"Answer the following query based on the content provided:\nQuery: {query}\nContent: {documents_text}"

def construct_llm_query(query, context, max_context_tokens=400):
    # Truncate context to fit within the max token limit
    truncated_context = context[:max_context_tokens]
    return f"You are an expert assistant. Use the following context to answer the user's query concisely and accurately.\n\nContext:\n{truncated_context}\n\nQuestion: {query}"
