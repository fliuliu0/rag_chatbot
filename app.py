print("Importing modules...")

import json
import sys
import os

from llm.query_utils import construct_llm_query
# Add the project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from config import API_KEY, CSE_ID
from retrieval.text_processing import split_content_into_chunks
from routes.query_router import route_query
from retrieval.semantic_filter import semantic_filter
from retrieval.vectorstore_manager import add_documents_to_vectorstore, clear_vectorstore
from retrieval.content_extraction import extract_content_from_gem, get_vectorstore_retriever
# from llm.query_rewriter import rewrite_query
# from llm.relevance_grader import grade_relevance
# from llm.answer_validation import validate_and_refine_answer
from llm.llm_loader import llm_pipeline
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Add the home route here
@app.route("/")
def home():
    return "Welcome to the Query API! Use POST /query to interact."

from bs4 import BeautifulSoup
import requests
from langchain.schema import Document  # Import Document class

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

@app.route("/add_documents", methods=["POST"])
def add_documents():
    try:
        # Load the list of URLs from the JSON file
        with open("gem_urls.json") as f:
            urls = json.load(f).get("post", [])
        
        if not urls:
            return jsonify({"error": "No URLs found in the JSON file."}), 400

        all_content = []
        print(f"Scraping {len(urls)} URLs...")

        # Scrape content from all URLs
        for url in urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code != 200:
                    print(f"Failed to fetch {url}: Status code {response.status_code}")
                    continue
                
                # Validate content type
                if "text/html" not in response.headers.get("Content-Type", ""):
                    print(f"Skipping non-HTML content from {url}")
                    continue

                # Handle encoding issues
                response.encoding = response.apparent_encoding or "utf-8"

                # Use a robust parser
                soup = BeautifulSoup(response.text, "html5lib")

                # Extract text from relevant tags
                page_content = []
                for tag in soup.find_all(["p", "h1", "h2", "h3", "li", "ul", "ol"]):  # Include list items
                    text = tag.get_text(strip=True)
                    if text:
                        page_content.append(text)

                # Add to the overall content if the page has text
                if page_content:
                    all_content.append({
                        "url": url,
                        "content": " ".join(page_content)
                    })

            except Exception as e:
                print(f"Error scraping {url}: {e}")
                continue  # Skip to the next URL if this one fails

        if not all_content:
            return jsonify({"error": "No content could be scraped from the provided URLs."}), 400

        # Log the first 500 characters of content from each URL for debugging
        for item in all_content[:5]:  # Limit logging to the first 5 items
            print(f"Scraped content from {item['url']}:\n{item['content'][:500]}...\n")

        # Convert content to LangChain Document format
        documents = [Document(page_content=item["content"], metadata={"url": item["url"]}) for item in all_content]

        # Split content into chunks
        chunks = split_content_into_chunks(documents)
        print("Split chunks:", [chunk.page_content[:100] for chunk in chunks[:5]])  # Log first 100 chars of first 5 chunks

        # Clear vectorstore and add new documents
        clear_vectorstore()
        add_documents_to_vectorstore([chunk.page_content for chunk in chunks])  # Add only content to vectorstore
        print("Documents successfully added to vectorstore.")
        return jsonify({"message": "Documents successfully scraped and added to vectorstore."})

    except Exception as e:
        print(f"Error adding documents: {e}")
        return jsonify({"error": str(e)})

@app.route("/add_qna_data", methods=["POST"])  
def add_qna_data():
    try:
        qna_file = "qna_dataset.json"
        
        # Load Q&A dataset
        with open(qna_file, "r") as f:
            qna_data = json.load(f)

        # Convert Q&A dataset into LangChain Document format
        qna_documents = [
            Document(
                page_content=f"Question: {entry['question']}\nAnswer: {entry['answer']}",
                metadata={"context": entry["context"]}
            )
            for entry in qna_data
        ]

        # Split Q&A content into chunks
        chunks = split_content_into_chunks(qna_documents)
        add_documents_to_vectorstore([chunk.page_content for chunk in chunks])
        print("Q&A data successfully added to vectorstore.")
        return jsonify({"message": "Q&A data successfully added to vectorstore."})

    except Exception as e:
        print(f"Error adding Q&A data: {e}")
        return jsonify({"error": str(e)})


def serialize_documents(documents):
    return [
        {
            "page_content": doc.page_content,
            "metadata": doc.metadata,
        }
        for doc in documents
    ]

@app.route("/query", methods=["POST"])
def query_pipeline():
    try:
        data = request.get_json()
        query = data.get("query", "").strip()

        if not query:
            return jsonify({"error": "No query provided."}), 400

        # Check if "elaborate" is in the query
        is_elaborate = "elaborate" in query.lower()

        # Retrieve relevant documents
        retriever = get_vectorstore_retriever()

        results = retriever.get_relevant_documents(query)
        filtered_docs = semantic_filter(query, results) if results else []

        if not filtered_docs:
            return jsonify({
                "answer": "I couldn't find sufficient information about GEM.",
                "source": []
            })

        # Construct the context for the LLM
        documents_text = "\n".join([doc.page_content for doc in filtered_docs])
        
        # Modify LLM query based on the keyword "elaborate"
        if is_elaborate:
            llm_query = f"You are an expert assistant. Use the following context to provide a detailed explanation to the user's query. The purpose is to educate them with GEM's information efficiently.\n\nContext:\n{documents_text}\n\nQuestion: {query}"
        else:
            llm_query = f"You are an expert assistant. Use the following context to answer the user's query concisely and accurately.\n\nContext:\n{documents_text}\n\nQuestion: {query}"

        print("LLM Query:", llm_query)

        # Pass to LLM pipeline
        raw_output = llm_pipeline(llm_query, max_length=1000 if is_elaborate else 300)  # Increase max tokens if "elaborate"
        
        print("Raw LLM Output:", raw_output)

        # Parse the LLM output
        if isinstance(raw_output, list) and len(raw_output) > 0 and isinstance(raw_output[0], dict):
            answer = raw_output[0].get('generated_text', '').strip()
        elif isinstance(raw_output, str):
            answer = raw_output.strip()
        else:
            answer = "I could not generate a valid response."

        # Final fallback
        if not answer or answer.strip() in ["True", "False", "1).", "a).", "Error", ""]:
            answer = f"Based on the provided information: {documents_text[:512]}..."

        serialized_docs = serialize_documents(filtered_docs)
        return jsonify({"answer": answer, "source": serialized_docs})

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Flask server is about to start...")
    app.run(debug=False, port=5001)
