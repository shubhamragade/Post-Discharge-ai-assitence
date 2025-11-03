from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..logging_config import log_interaction
# In This File : We split loaded documents into smaller chunks for embedding and retrieval.
# for this we use RecursiveCharacterTextSplitter from langchain_text_splitters
# The splitter uses a hierarchy of separators to split text into chunks of specified size with overlap.
def split_documents(documents, chunk_size=800, chunk_overlap=100):
    # Checking if documents list is empty
    if not documents:
        log_interaction("splitter_warning", {"message": "No documents provided for splitting."})
        return []
    # Initialize the text splitter
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        # Split the documents into chunks
        chunks = splitter.split_documents(documents)
        # HERE we Add metadata to each chunk
        for idx, chunk in enumerate(chunks):
            meta = chunk.metadata
            meta["chunk_id"] = idx
            meta["domain"] = "nephrology_reference"
        # Log the successful splitting
        log_interaction(
            "splitter_success",
            {"message": f"Split {len(documents)} documents into {len(chunks)} chunks."}
        )
        # Return the split chunks
        return chunks
    # here we handle exceptions during splitting
    except Exception as e:
        log_interaction("splitter_exception", {"message": str(e)})
        raise RuntimeError(f"Error while splitting documents: {str(e)}")
