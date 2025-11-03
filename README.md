
# 🏥 **Post-Discharge Medical AI Assistant**

## 📘 **Overview**

**Post-Discharge Medical AI Assistant** is an intelligent **multi-agent healthcare system** designed to support patients after hospital discharge.  
It leverages **Retrieval-Augmented Generation (RAG)**, **LLM reasoning**, and **real-time medical web search** to provide **accurate, grounded, and context-aware medical responses**.

---

## 💡 **Core Capabilities**

- ✅ Patient lookup & verification  
- ✅ Context-aware medical responses (RAG)  
- ✅ Real-time medical literature web search  
- ✅ Multi-agent dialogue (Receptionist + Clinical AI)  
- ✅ Interactive Streamlit chat interface  

---

## 🧩 **System Architecture**


flowchart TD
A[👤 Patient] -->|Query| B[🤖 Receptionist Agent]
B -->|Medical Query Detected| C[🩺 Clinical Agent]
C -->|RAG Context Retrieval| D[(📚 ChromaDB - Nephrology PDF)]
C -->|If Not Found| E[🌍 Web Search (DuckDuckGo)]
C -->|Response| F[💬 Streamlit Chat UI]


⚙️ Tech Stack
LayerTechnologyFrontendStreamlitBackendFastAPILLMGroq API (Llama-3.1-8b-instant)RAG EngineLangChain + ChromaDBEmbeddingssentence-transformers/all-MiniLM-L6-v2Web Searchddgs (DuckDuckGo Search)Data SourceComprehensive Clinical Nephrology (PDF)LoggingPython logging + JSON
🧠 LLM Selection
Model: llama-3.1-8b-instant (via Groq API)
Why this model?

* 🚀 Lightweight & ultra-fast inference

* 🧩 Ideal for retrieval-based medical reasoning

* 💰 Free API access and low latency

🧮 Vector Database Selection
Database: ChromaDB
Why ChromaDB?

* ⚡ Lightweight, local, and open-source

* 🔗 Integrates seamlessly with LangChain

* 💾 Supports persistent offline vector storage

Embeddings Model: sentence-transformers/all-MiniLM-L6-v2
🧩 RAG Implementation Pipeline

1. Text Splitting → Chunk PDF text

2. Embedding Generation → Encode using MiniLM model

3. Vector Storage → Save in backend/data/chroma_db/

4. Retrieval → Fetch top-k relevant chunks

5. LLM Fusion → Combine retrieved context + query

6. Response Generation → Produce grounded answers with citations

🌍 Web Search Integration
When RAG confidence is low or the user requests recent information,\
the Clinical Agent triggers DuckDuckGo Search (ddgs).
Example:
👤 Patient: “What's the latest research on SGLT2 inhibitors for kidney disease?”\
🤖 Clinical Agent: “This requires recent information. Let me search for you...\
According to recent studies, SGLT2 inhibitors significantly reduce CKD progression and cardiovascular mortality.”\
📚 Sources: Nature 2025, PubMed 2024, NEJM 2025
🧬 Multi-Agent Framework
AgentResponsibilityReceptionist AgentGreets patient, verifies ID, routes medical queriesClinical AgentAnswers using RAG + Web SearchAgent ManagerControls flow between agents and maintains state
🧾 Logging & Traceability
All agent interactions are recorded for auditing and debugging.
📂 Location: backend/logs/chat_memory.json
Sample Log:

{
  "timestamp": "2025-11-02T10:01:00",
  "agent": "clinical",
  "event": "RAG_response",
  "query": "I'm having swelling in my legs",
  "response": "Based on CKD guidelines..."
}

🧠 Patient Data Retrieval

* Stored in patients_data.json

* Receptionist Agent retrieves patient details (diagnosis, meds, follow-up info)

* Context is passed to Clinical Agent for response generation

🏗️ Project Structure


post_discharge_medical_ai_poc/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── receptionist_agent.py
│   │   │   ├── clinical_agent.py
│   │   │   └── agent_manager.py
│   │   ├── rag/
│   │   │   ├── embedder.py
│   │   │   └── retriever.py
│   │   ├── patient_data_tool.py
│   │   ├── llm_response_handler.py
│   │   ├── logging_config.py
│   │   └── main.py
│   └── data/
│       ├── patients_data.json
│       └── nephrology_refs/
│           └── comprehensive-clinical-nephrology.pdf
│
├── frontend/
│   ├── streamlit_app.py
│   ├── assets/
│   │   └── logo.png
│   └── components/
│       └── chat_ui.py
│
└── README.md


💬 Example Interaction
👤 Patient: “I'm having swelling in my legs. Should I be worried?”\
🤖 Receptionist Agent: “This sounds like a medical concern. Let me connect you with our Clinical AI Agent.”\
🩺 Clinical Agent (RAG): “Based on your CKD diagnosis and nephrology guidelines, leg swelling may indicate fluid retention.\
📚 [Citations: p.614, p.905]”
👤 Patient: “What's the latest research on SGLT2 inhibitors for kidney disease?”\
🩺 Clinical Agent (Web Search): “This requires recent information. Let me search for you...\
📖 [Results from PubMed 2025, NEJM 2024, Nature 2025]”
🚀 Running the Project
1️⃣ Create Virtual Environment


python -m venv .venv
.\.venv\Scripts\activate   # (Windows)
source .venv/bin/activate  # (Linux/Mac)


2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

3️⃣ Start Backend (FastAPI)

```
uvicorn backend.app.main:app --reload
```

4️⃣ Start Frontend (Streamlit)

```
streamlit run frontend/streamlit_app.py
```

🔐 Environment Variables (.env)

```
GROQ_API_KEY=your_groq_api_key_here
CHROMA_PATH=backend/data/chroma_db
```

🧱 System Workflow
1️⃣ Receptionist Agent receives user query\
2️⃣ If medical → escalates to Clinical Agent\
3️⃣ Clinical Agent performs RAG retrieval\
4️⃣ If context unavailable → triggers Web Search\
5️⃣ Returns grounded response with citations\
6️⃣ Logs interaction in JSON
📦 Requirements

```
fastapi
uvicorn
streamlit
langchain
langchain-community
langchain-chroma
langchain-huggingface
chromadb
sentence-transformers
ddgs
groq
pydantic
Pillow
python-dotenv
```

🔮 Future Enhancements

* 🔗 EHR / FHIR integration

* 📊 Confidence-based RAG response scoring

* 🧠 Explainable AI reasoning layer

* 🗣️ Voice-enabled interaction

* 🐳 Dockerized deployment

👨‍💻 Contributor
Shubham Ragade\
AI Developer | DataSmith AI (GenAI Internship 2025)\
📧 shubhamragade.ai@gmail.com
⭐ If you find this project useful, consider giving it a star on GitHub! ⭐

````

---

## 🧩 2. `requirements.txt`

```text
fastapi
uvicorn
streamlit
langchain
langchain-community
langchain-chroma
langchain-huggingface
chromadb
sentence-transformers
ddgs
groq
pydantic
Pillow
python-dotenv
````

🔐 3. .env.example

```
# === LLM Configuration ===
GROQ_API_KEY=your_groq_api_key_here

# === Vector Database Path ===
CHROMA_PATH=backend/data/chroma_db

# === App Configuration ===
LOG_PATH=backend/logs/chat_memory.json
PATIENT_DATA_PATH=backend/data/patients_data.json
NEPHROLOGY_PDF_PATH=backend/data/nephrology_refs/comprehensive-clinical-nephrology.pdf
```

📦 Copy Instructions
1️⃣ Create your folder → post_discharge_medical_ai_poc/\
2️⃣ Inside it, make these files:

# 1. Clone & Enter
git clone https://github.com/shubhamragade/Post-Discharge-ai-assitence.git
cd post_discharge_medical_ai_poc

# 2. Virtual Env
python -m venv .venv && source .venv/bin/activate   # mac/linux
# .\ .venv\Scripts\activate   # windows

# 3. Install
pip install -r requirements.txt

# 4. Add your key
cp .env.example .env
# → paste GROQ_API_KEY=gho_...

# 5. Launch
# Terminal 1
uvicorn backend.app.main:app --reload

# Terminal 2
streamlit run frontend/streamlit_app.py

