import sys
import os
# Add the project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_community.document_loaders import WebBaseLoader
import bs4
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from config import VECTOR_DB_DIR, EMBEDDING_MODEL
from retrieval.vectorstore_manager import add_documents_to_vectorstore, clear_vectorstore

def extract_content_from_gem():
    loader = WebBaseLoader(
        web_paths=["https://gem-corp.tech/"],
        bs_kwargs={"parse_only": bs4.SoupStrainer("body")}
    )
    docs = loader.load()

    # Filter out empty or irrelevant content
    valid_docs = [
        doc for doc in docs if len(doc.page_content.strip()) > 50
    ]
    return valid_docs

    
def add_documents_to_vectorstore(docs):
    valid_docs = [
        doc for doc in docs 
        if hasattr(doc, 'page_content') and len(doc.page_content.strip()) > 20
    ]
    unique_docs = {doc.page_content: doc for doc in valid_docs}.values()  # Remove duplicates
    print("Unique documents being added to vectorstore:", [doc.page_content[:200] for doc in unique_docs])

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)
    vectorstore.add_texts([doc.page_content for doc in unique_docs])
    print("Documents successfully indexed.")


def filter_relevant_sections(documents, query):
    """
    Filters documents to extract only the sections most relevant to the query.
    """
    relevant_docs = []
    for doc in documents:
        content = doc.page_content.lower()
        if query.lower() in content or any(keyword in content for keyword in ["address", "services", "location"]):
            relevant_docs.append(doc)
    return relevant_docs

def get_vectorstore_retriever():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)

    # Debug print the contents of the vectorstore
    docs = vectorstore._collection.get()
    print("Vectorstore contents (debug):", docs['documents'])

    return vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5})

def extract_and_store():
    # Step 1: Clear the vectorstore
    clear_vectorstore()
    
    # Step 2: Extract content from the website
    docs = extract_content_from_gem()
    print("Extracted documents:", [doc.page_content[:200] for doc in docs])  # Debug print
    
    # Step 3: Add documents to the vectorstore
    add_documents_to_vectorstore(docs)
    print("Documents successfully stored in the vectorstore.")