import json
import os
from backend.app.logging_config import log_interaction
# Path to the patient data JSON file
DATA_PATH = os.path.join("backend", "data", "patients_data.json")
# Function to get patient data by name
def get_patient_by_name(patient_name: str, case_sensitive: bool = True):
    # Load patient data from JSON file
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as file:
            patients = json.load(file)
        # Search for the patient by name
        for patient in patients:
            if case_sensitive:
                if patient["patient_name"] == patient_name:
                    log_interaction("patient_lookup", patient)
                    return patient
            # Non-case-sensitive search
            else:
                if patient["patient_name"].lower() == patient_name.lower():
                    log_interaction("patient_lookup", patient)
                    return patient
        # Log if patient not found
        log_interaction("patient_not_found", {"query": patient_name})
        return None
    # Handle exceptions during file read or JSON parsing
    except Exception as e:
        log_interaction("patient_lookup_error", {"error": str(e)})
        return None
