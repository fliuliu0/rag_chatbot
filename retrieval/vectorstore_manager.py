
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from config import VECTOR_DB_DIR, EMBEDDING_MODEL

def deduplicate_documents(docs):
    seen = set()
    deduplicated_docs = []
    for doc in docs:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            deduplicated_docs.append(doc)
    return deduplicated_docs

def batch_documents(docs, batch_size):
    """Yield successive n-sized chunks from docs."""
    for i in range(0, len(docs), batch_size):
        yield docs[i:i + batch_size]

def add_documents_to_vectorstore(documents):
    print("Documents received for vectorstore addition:", documents)
    if not documents:
        print("No documents to add to the vectorstore.")
        return
    
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)
    
    # Add texts
    vectorstore.add_texts(documents)
    print("Documents successfully added to vectorstore.")
    
    # Persist changes
    vectorstore.persist()
    print("Vectorstore contents after addition:", vectorstore._collection.get())


def get_vectorstore_retriever():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)

    # Debug print the contents of the vectorstore
    docs = vectorstore._collection.get()
    print("Vectorstore contents (debug):", docs['documents'])

    # Ensure documents are valid
    valid_docs = [
        doc for doc in docs['documents']
        if isinstance(doc, str) and len(doc.strip()) > 20  # Ensure valid text
    ]
    print("Valid documents:", valid_docs)

    if not valid_docs:
        print("No valid documents found in vectorstore.")

    return vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5})


from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from config import VECTOR_DB_DIR, EMBEDDING_MODEL

def clear_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)

    # Retrieve all document IDs to delete
    docs = vectorstore._collection.get()  # Get the current documents
    doc_ids = docs.get("ids", [])
    
    if doc_ids:  # Only delete if there are documents
        for doc_id in doc_ids:
            vectorstore._collection.delete(where={"id": doc_id})  # Delete by ID
        print(f"Deleted {len(doc_ids)} documents from the vectorstore.")
    else:
        print("Vectorstore is already empty.")

    print("Vectorstore cleared.")
