import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from llm.llm_loader import llm_pipeline

def rewrite_query(query):
    prompt = PromptTemplate(
        input_variables=["query"],
        template="Rewrite the following query to make it more effective for search engines.\n\nQuery: {query}\nRewritten Query:"
    )
    chain = LLMChain(llm=llm_pipeline, prompt=prompt)
    return chain.run(query).strip()
