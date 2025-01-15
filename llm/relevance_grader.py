import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from llm.llm_loader import llm_pipeline

def grade_relevance(query, document):
    prompt = PromptTemplate(
        input_variables=["query", "document"],
        template=(
            "You are a relevance grader. Given a query and a document, decide if the document is relevant to the query.\n"
            "Respond with 'yes' if relevant and 'no' if not. Do not provide any additional text.\n\n"
            "Query: {query}\nDocument: {document}\nRelevance (yes/no):"
        )
    )
    chain = LLMChain(llm=llm_pipeline, prompt=prompt)
    
    try:
        print(f"Grading relevance for query: {query}")
        print(f"Grading relevance for document: {document[:500]}...")  # Limit document length in logs
        relevance = chain.run(query=query, document=document).strip().lower()
        print(f"Relevance result: {relevance}")
        
        # Fallback for unclear responses
        if relevance not in {"yes", "no"}:
            print(f"Unexpected relevance result: {relevance}. Defaulting to 'no'.")
            return False
        return relevance == "yes"
    except Exception as e:
        print(f"Error grading relevance: {e}")
        return False


# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from llm.llm_loader import llm_pipeline

# def grade_relevance(query, document):
#     prompt = PromptTemplate(
#         input_variables=["query", "document"],
#         template="""
#         Query: {query}
#         Document: {document}
#         Is this document relevant to the query? Answer strictly yes or no. If the document is too short or meaningless, answer no.
#         """
#     )
#     chain = LLMChain(llm=llm_pipeline, prompt=prompt)

#     try:
#         print(f"Grading relevance for query: {query}")
#         print(f"Grading relevance for document: {document[:200]}...")  # Print first 200 chars
#         relevance = chain.run(query=query, document=document).strip().lower()
#         print(f"Relevance result: {relevance}")
#         return relevance == "yes"
#     except Exception as e:
#         print(f"Error grading relevance: {e}")
#         return False
