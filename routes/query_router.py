import sys
import os

# Add the project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from llm.llm_loader import llm_pipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def route_query(query):
    # Simple keyword-based routing as fallback
    keywords_vectorstore = ["location", "address", "year", "services", "details", "countries"]
    keywords_web_search = ["general", "external", "founder"]

    # Match keywords to decide routing
    if any(keyword in query.lower() for keyword in keywords_vectorstore):
        return "vectorstore"
    elif any(keyword in query.lower() for keyword in keywords_web_search):
        return "web_search"

    # Default to vectorstore if no clear routing
    return "vectorstore"

