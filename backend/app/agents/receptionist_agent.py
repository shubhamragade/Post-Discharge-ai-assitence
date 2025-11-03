from backend.app.patient_data_tool import get_patient_by_name
from backend.app.logging_config import log_interaction
# ReceptionistAgent class definition
class ReceptionistAgent:
    # Initialize the agent
    def __init__(self):
        self.patient_data = None
        self.state = "GREETING"
    # Handle user message
    def handle_message(self, user_message: str):
        # Process message based on current state
        try:
            user_message = user_message.strip()
            log_interaction("receptionist_input", {"message": user_message})
            if self.state == "GREETING":
                self.state = "ASK_NAME"
                return (
                    "Hello! I’m your Post-Discharge Assistant. "
                    "May I know the patient's full name, please?"
                )

            # Ask for patient name
            elif self.state == "ASK_NAME":
                patient_info = get_patient_by_name(user_message)
                if not patient_info:
                    log_interaction("receptionist_no_match", {"name": user_message})
                    return (
                        f"I couldn’t find any record for '{user_message}'. "
                        "Please check the spelling or try the full name."
                    )
                # Load patient data and transition to READY state
                self.patient_data = patient_info
                self.state = "READY"
                log_interaction("receptionist_patient_loaded", patient_info)
                # Provide basic patient info
                response = (
                    f"Patient record found for *{patient_info['patient_name']}*.\n"
                    f"Primary Diagnosis: {patient_info['primary_diagnosis']}\n"
                    f"Follow-up: {patient_info['follow_up']}\n\n"
                    "You can now ask any questions about the discharge, "
                    "medications, or warning signs."
                )
                return response

            # Handle medical queries
            elif self.state == "READY":
                if self.is_medical_query(user_message):
                    log_interaction("receptionist_escalate", {"query": user_message})
                    return {
                        "route": "clinical",
                        "query": user_message,
                        "patient_data": self.patient_data
                    }
                else:
                    return (
                        "I’m here to help with medical or discharge-related questions. "
                        "Could you please clarify your concern?"
                    )
        # Handle unexpected states
        except Exception as e:
            log_interaction("receptionist_error", {"error": str(e)})
            return "Something went wrong while processing your request."
    # Static method to identify medical queries
    @staticmethod
    def is_medical_query(message: str) -> bool:
        keywords = [
            "pain", "swelling", "fever", "medication", "dose", "symptom",
            "diet", "exercise", "follow up", "side effect", "blood pressure",
            "urine", "kidney", "warning", "instruction", "advice", "discharge","Sick","Ill","Emergency"
        ]
        msg_lower = message.lower()
        return any(keyword in msg_lower for keyword in keywords)
