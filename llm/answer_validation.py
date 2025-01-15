from llm.llm_loader import llm_pipeline

def validate_and_refine_answer(query, initial_answer, documents_text):
    if "what is" in query.lower():
        validation_prompt = f"""
        Query: {query}
        Initial Answer: {initial_answer}

        Validate whether the above answer provides a clear description of GEM based on the following content:
        {documents_text}

        If the answer is incomplete or incorrect, provide a more accurate and detailed description.
        """
        refined_answer = llm_pipeline(validation_prompt)
        return refined_answer

    # General fallback refinement
    validation_prompt = f"""
    Query: {query}
    Initial Answer: {initial_answer}

    Validate whether the above answer is accurate and consistent with the following content:
    {documents_text}

    If the answer is inaccurate or incomplete, refine it to provide a better response.
    """
    refined_answer = llm_pipeline(validation_prompt)
    return refined_answer
