import logging
from backend.app.agents.receptionist_agent import ReceptionistAgent
from backend.app.agents.clinical_agent import ClinicalAgent
from backend.app.logging_config import log_interaction
# Configure logger
logger = logging.getLogger(__name__)
# AgentManager class definition
class AgentManager:
    # Initialize the AgentManager
    def __init__(self):
        self.receptionist = ReceptionistAgent()
        self.clinical = ClinicalAgent()
        self.active_agent = "receptionist"
        logger.info("AgentManager initialized with ReceptionistAgent active.")
    # Process user message
    def process_user_message(self, user_message: str) -> str:
        # Handle message routing between agents
        try:
            logger.info(f"Processing message via {self.active_agent}: {user_message}")
            log_interaction("agent_manager_input", {"agent": self.active_agent, "message": user_message})
            # Route message to the appropriate agent
            if self.active_agent == "receptionist":
                response = self.receptionist.handle_message(user_message)

                # Check if escalation to clinical is needed
                if isinstance(response, dict) and response.get("route") == "clinical":
                    logger.info("Escalating to ClinicalAgent.")
                    self.active_agent = "clinical"
                    query = response["query"]
                    # Call ClinicalAgent for the query
                    clinical_response = self.clinical.handle_query(query)

                    preamble = (
                        'Receptionist Agent: "This sounds like a medical concern. '
                        'Let me connect you with our Clinical AI Agent."\n\n'
                    )
                    clinical_response = self.clinical.handle_query(query)
                    return preamble + f"Clinical Agent: {clinical_response}"

               # If still with receptionist, return its response
                return f"Receptionist Agent: {response}"

            # If active agent is clinical
            elif self.active_agent == "clinical":
                clinical_response = self.clinical.handle_query(user_message)

                # Check if escalation to web search is needed
                if "Web Insight" in clinical_response:
                    return f"Clinical Agent (Web Search): {clinical_response}"
                else:
                    return f"Clinical Agent: {clinical_response}"

        except Exception as e:
            logger.exception("AgentManager encountered an error.")
            log_interaction("agent_manager_error", {"error": str(e)})
            return "Sorry, an internal error occurred while processing your message."
