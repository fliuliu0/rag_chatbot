from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_content_into_chunks(docs):
    """Splits LangChain `Document` objects into smaller chunks."""
    # Initialize a text splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    # Ensure `docs` is a list of LangChain `Document` objects
    if not all(isinstance(doc, Document) for doc in docs):
        raise ValueError("All items in `docs` must be instances of LangChain `Document`.")

    # Split each document into smaller chunks
    chunks = []
    for doc in docs:
        # Split the page_content of the Document
        split_texts = text_splitter.split_text(doc.page_content)

        # Create new `Document` objects for each chunk
        for split_text in split_texts:
            chunks.append(Document(page_content=split_text, metadata=doc.metadata))

    return chunks
