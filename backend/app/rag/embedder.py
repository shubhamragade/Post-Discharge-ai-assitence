from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from ..config import CHROMA_PATH
from ..logging_config import log_interaction
from pathlib import Path
# In This File I create embeddings for document chunks and store them in ChromaDB.
# I use a local sentence transformer model to generate embeddings.
# The embeddings are then stored in a Chroma vector store for efficient retrieval.

def create_and_store_embeddings(chunks, rebuild=False):
    # Checking if chunks list is empty
    if not chunks:
        log_interaction("embedder_warning", {"message": "No chunks provided for embedding."})
        return None
    # Ensure ChromaDB directory exists
    db_path = Path(CHROMA_PATH)
    db_path.mkdir(parents=True, exist_ok=True)
    # Rebuild the database if specified
    if rebuild and db_path.exists():
        for file in db_path.glob("*"):
            file.unlink()
        log_interaction("embedder_info", {"message": "Rebuilt Chroma database from scratch."})
    # Create embeddings and store in ChromaDB
    try:
        log_interaction("embedder_start", {"message": "Creating embeddings using local model."})
        # Load local sentence transformer model
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        # Create or load Chroma vector store

        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(db_path)
        )
        # Persist the vector store to disk
        vector_store.persist()
        log_interaction("embedder_success", {"message": f"ChromaDB created at {db_path}"})
        # Return the vector store
        return vector_store
    # Handle exceptions during embedding creation
    except Exception as e:
        log_interaction("embedder_error", {"message": str(e)})
        raise RuntimeError(f"Failed to create embeddings: {str(e)}")
