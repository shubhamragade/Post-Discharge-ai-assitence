from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from ..config import CHROMA_PATH
from ..logging_config import log_interaction
import os
# In This File : I retrieve relevant document chunks from the ChromaDB based on user queries.
# I load the Chroma vector store and perform similarity search to get relevant chunks.
# I log interactions for monitoring and debugging.
def load_vector_store():
    # Check if ChromaDB exists
    if not os.path.exists(CHROMA_PATH):
        log_interaction("retriever_error", {"message": f"ChromaDB not found at {CHROMA_PATH}"})
        raise FileNotFoundError(f"No Chroma database found at {CHROMA_PATH}")
    # Load the Chroma vector store
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
        log_interaction("retriever_load_success", {"message": "ChromaDB loaded successfully"})
        return vector_store
    # Handle exceptions during loading
    except Exception as e:
        log_interaction("retriever_load_exception", {"message": str(e)})
        raise RuntimeError(f"Failed to load ChromaDB: {str(e)}")


def retrieve_relevant_chunks(query: str, top_k: int = 4):
    # Load the vector store
    vector_store = load_vector_store()
    # Perform similarity search
    try:
        results = vector_store.similarity_search(query, k=top_k)
        # Log the retrieval interaction
        log_interaction("retriever_query", {
            "query": query,
            "results_count": len(results),
            "message": f"Retrieved top {len(results)} chunks for query."
        })
        # Format results
        formatted_results = []
        for doc in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })
        # return formatted results
        return formatted_results
        # Handle exceptions during retrieval
    except Exception as e:
        log_interaction("retriever_query_error", {"message": str(e)})
        raise RuntimeError(f"Error retrieving chunks: {str(e)}")
