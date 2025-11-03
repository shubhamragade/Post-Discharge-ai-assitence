import logging
from backend.app.llm_response_handler import generate_llm_response
from backend.app.rag.retriever import retrieve_relevant_chunks
#Optional web search import
try:
    from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
    web_search_available = True
except ImportError:
    web_search_available = False
    DuckDuckGoSearchRun = None
# Set up logger
logger = logging.getLogger(__name__)
# ClinicalAgent class definition
class ClinicalAgent:
    def __init__(self):
        # Initialize web search tool if available
        self.web_search = DuckDuckGoSearchRun() if web_search_available else None
        logger.info("ClinicalAgent initialized (RAG + Web Search support)")
    # Handle clinical query
    def handle_query(self, query: str, patient_data=None) -> str:
        try:
            logger.info(f"ClinicalAgent received query: {query}")
            # Prepare patient info if available
            patient_info = ""
            if patient_data:
                name = patient_data.get("patient_name") or patient_data.get("name", "the patient")
                diagnosis = patient_data.get("primary_diagnosis") or patient_data.get("diagnosis", "")
                patient_info = f"Patient: {name}\nDiagnosis: {diagnosis}\n"
            # Determine if web search is needed based on keywords   
            recent_keywords = [
                "latest", "recent", "update", "research", "study", "trial",
                "fda", "new", "2023", "2024", "2025", "innovation"
            ]
            use_web = any(k in query.lower() for k in recent_keywords)
            # Retrieve relevant chunks using RAG
            results = retrieve_relevant_chunks(query)
            logger.info(f"Retrieved {len(results)} chunks for query.")
            # Prepare context from retrieved chunks
            context = "\n".join(
                r.get("content", "") if isinstance(r, dict) else getattr(r, "page_content", "")
                for r in results
            )[:1500]
            # Prepare citations for retrieved chunks
            citations = []
            for r in results:
                if isinstance(r, dict) and "metadata" in r:
                    meta = r["metadata"]
                    if "page" in meta and "file_path" in meta:
                        citations.append(f"p.{meta['page']} ({meta['file_path']})")
                # Handle non-dict result format
            rag_response = ""
            if context:
                prompt = (
                    f"You are a clinical nephrology assistant.\n"
                    f"{patient_info}\n"
                    f"Use the following medical reference to answer clinically and safely.\n\n"
                    f"Reference Context:\n{context}\n\n"
                    f"Question: {query}\n"
                    f"Answer concisely and clearly for a post-discharge patient."
                )
                rag_response = generate_llm_response(prompt)

            # Decide on web search if RAG response is insufficient
            if (not rag_response or len(rag_response) < 80) or use_web:
                if self.web_search:
                    logger.info("Performing web search due to insufficient RAG data or research topic.")
                    web_result = self.web_search.run(query)
                    return f"Web Insight (Latest Research)\n{web_result}"
                else:
                    return (
                        "I couldn’t find relevant data in your medical reference. "
                        "Please enable web search for up-to-date research results."
                    )

            # Append citations to RAG response
            citation_text = (
                "\n\n[RAG response with citations: " + "; ".join(citations) + "]"
                if citations else ""
            )
            # Return final response
            
            return f"Clinical AI Response (RAG)\n{rag_response.strip()}{citation_text}"
        # Handle exceptions
        except Exception as e:
            logger.exception("Error in ClinicalAgent.handle_query")
            return f"Clinical Agent Error: {e}"
