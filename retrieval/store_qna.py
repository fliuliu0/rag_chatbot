# Load Q&A dataset
import json
from xml.dom.minidom import Document

from text_processing import split_content_into_chunks
from vectorstore_manager import add_documents_to_vectorstore


def load_qna_dataset(qna_file):
    with open(qna_file, "r") as f:
        qna_data = json.load(f)
    documents = [
        Document(
            page_content=f"Question: {entry['question']}\nAnswer: {entry['answer']}",
            metadata={"context": entry["context"]}
        )
        for entry in qna_data
    ]
    return documents

# Add Q&A to vector store
def index_qna_data(qna_file):
    qna_documents = load_qna_dataset(qna_file)
    chunks = split_content_into_chunks(qna_documents)
    add_documents_to_vectorstore([chunk.page_content for chunk in chunks])
