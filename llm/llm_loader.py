import logging
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from langchain.llms import HuggingFacePipeline
import torch

logging.basicConfig(level=logging.DEBUG)

try:
    print("Initializing language model pipeline...")
    model_name = "google/flan-t5-small"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir="./model_cache")
    print("Model loaded.")
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir="./model_cache")
    print("Tokenizer loaded.")
    
    hf_pipeline = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1,
        max_length=256,
        temperature=0.1,
        do_sample=True,
        batch_size=8  # Adjust batch size to avoid exceeding limits
    )
    
    print("Pipeline created.")
    
    # Wrap the pipeline in a LangChain-compatible class
    llm_pipeline = HuggingFacePipeline(pipeline=hf_pipeline)
    print("Pipeline wrapped for LangChain.")
except Exception as e:
    print(f"Error initializing pipeline: {e}")
    llm_pipeline = None
