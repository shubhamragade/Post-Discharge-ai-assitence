from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader
from ..config import REF_PDF
from ..logging_config import log_interaction

# In This File I load data from a reference PDF document for RAG purposes.
def load_reference_document() -> str:
    pdf_path = Path(REF_PDF)
    # Check if the PDF exists
    if not pdf_path.exists():
        log_interaction("rag_loader_error", {"message": f"Reference file not found: {pdf_path}"})
        raise FileNotFoundError(f"Reference PDF not found at {pdf_path}")
    # Load the PDF using PyMuPDFLoader
    try:
        loader = PyMuPDFLoader(str(pdf_path))
        documents = loader.load()
    # Check if any text was extracted
        if not documents:
            log_interaction("rag_loader_warning", {"message": f"No text extracted from {pdf_path}"})
            return []
    # Log success and return documents
        log_interaction("rag_loader_success", {"message": f"Loaded {len(documents)} pages from reference PDF"})
        return documents
    # Handle exceptions during loading
    except Exception as e:
        log_interaction("rag_loader_exception", {"message": str(e)})
        raise RuntimeError(f"Failed to load reference document: {str(e)}")
