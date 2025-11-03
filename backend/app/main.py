from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.app.agents.agent_manager import AgentManager

# Initialize FastAPI and AgentManager
app = FastAPI(title="Post-Discharge Medical AI Assistant")
agent_manager = AgentManager()

# Enable CORS (for Streamlit frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class QueryRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: QueryRequest):
    # Process user message through AgentManager
    response = agent_manager.process_user_message(request.message)
    return {"response": response}
# Root endpoint for health check
@app.get("/")
def root():
    return {"status": "ok", "message": "Medical AI backend is running 🚀"}
