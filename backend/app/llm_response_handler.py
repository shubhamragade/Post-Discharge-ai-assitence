import os
import logging
import requests
from dotenv import load_dotenv
from backend.app.rag.retriever import retrieve_relevant_chunks
# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)
# Groq API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_ID = os.getenv("GROQ_MODEL_ID", "llama-3.1-8b-instant")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
# Function to generate LLM response using Groq API
def generate_llm_response(user_query: str) -> str:
    try:
        # retrieve relevant chunks from ChromaDB
        results = retrieve_relevant_chunks(user_query)
        logger.info(f"Retrieved {len(results)} chunks from ChromaDB")

        # Prepare context from retrieved chunks
        if results and isinstance(results[0], dict):
            context = "\n".join(r.get("content", "") for r in results)
        # If results are not in expected format, fallback to another method
        else:
            context = "\n".join(getattr(r, "page_content", "") for r in results)
        context = context[:1500]

        # Build final prompt
        prompt = (
            f"You are a clinical AI assistant helping post-discharge nephrology patients.\n"
            f"Use the provided reference context and answer clearly, medically accurate, and concise.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {user_query}\n"
            f"Answer:"
        )
        # Prepare payload for Groq API
        payload = {
            "model": GROQ_MODEL_ID,
            "messages": [
                {"role": "system", "content": "You are a professional clinical assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.4,
            "max_tokens": 250,
        }
        # Set up headers for Groq API request
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        # Make request to Groq API
        response = requests.post(
            f"{GROQ_BASE_URL}/chat/completions", headers=headers, json=payload, timeout=60
        )
        # Handle non-200 responses
        if response.status_code != 200:
            logger.error("Groq API Error: %s", response.text)
            return f"Groq API error: {response.text}"
        # Parse response
        data = response.json()
        answer = data["choices"][0]["message"]["content"].strip()
        # Log successful response
        logger.info("llm_response_success: %s", answer[:120])
        return answer
    # Handle exceptions during API call or response parsing
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        logger.exception("llm_response_error")
        return f"Error: {e}\n\nTraceback:\n{tb}"
