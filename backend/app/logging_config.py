import logging
import json
from pathlib import Path
from datetime import datetime
from .config import LOG_FILE
# Ensure log directory exists
Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

# Set up logger
logger = logging.getLogger("post_discharge_ai")
logger.setLevel(logging.INFO)
# Create formatter
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
# Create file handler
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# Create console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Function to log interactions
def log_interaction(entry_type: str, data: dict):
    # Create log entry
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "type": entry_type,
        "data": data
    }

    # Append log entry to log file
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    
    logger.info(f"{entry_type}: {data.get('message', '')}")
