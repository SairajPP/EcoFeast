# EcoFeast 2.0 — Real-Time Food Waste Redistribution Platform
### Autonomous, Multi-Agent Food Rescue Orchestration System

**Status: Production-Ready ✅ (91/91 Tests Passing, CI Integrated)**

**EcoFeast 2.0** is a web-based, agentic platform that tackles food waste by automating the redistribution of surplus food from donors (restaurants, grocery stores, event organizers) to NGOs. 

Evolving from a baseline Django web application, EcoFeast 2.0 integrates **classical Machine Learning** for freshness prediction, **Generative AI** for unstructured data intake, **RAG** for constraint-based NGO matching, and **LangGraph** for autonomous routing.

---

## 🌟 Key Features

* **Multimodal GenAI Intake:** Donors can submit food listings using a photo (Vision Intake using Groq Llama Vision) or a simple conversational description (Chat Intake using Groq Llama 3 70B). The system extracts structured fields automatically with donor verification.
* **XGBoost Freshness Prediction:** A machine learning model predicts a precise freshness score based on temporal parameters and sensory details (smell, texture, moisture).
* **SHAP Explainability:** Surfaces feature contributions (e.g., storage time, cooking method) explaining *why* the model predicted a freshness score, translated into natural language by an LLM for NGOs.
* **RAG-based NGO Matching:** Combines semantic profiles (dietary restrictions, operating hours, capacity) embedded via SentenceTransformers (`all-MiniLM-L6-v2`) in Qdrant with real-world distance (Haversine formula), capacity, and reliability rankings.
* **LangGraph Multi-Agent Orchestration:** Runs an autonomous pipeline of specialized agents (Intake, Verification, Matching, Logistics) with conditional routing and self-loop escalations to re-route offers if an NGO times out or rejects the assignment.
* **Observability Dashboard:** A real-time monitoring dashboard displaying pipeline status distributions, agent performance charts, and step-by-step decision trails.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      OBSERVABILITY DASHBOARD                    │
│           (Django Templates + Chart.js Pipeline Auditing)       │
└────────────────────────────────┬────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│             LANGGRAPH MULTI-AGENT STATE MACHINE                 │
│  [Intake Agent] ──► [Verify Agent] ──► [Match] ──► [Logistics]  │
└───────┬────────────────────┬─────────────┬─────────────▲────────┘
        │                    │             │             │
┌───────▼───────┐    ┌───────▼───────┐     │     ┌───────┴────────┐
│   ML LAYER    │    │  GENAI LAYER  │     │     │   RAG LAYER    │
│  XGBoost +    │    │ Llama Vision  │     │     │  SentenceTrans │
│  SHAP Engine  │    │ + JSON Mode   │     │     │   + Qdrant     │
└───────────────┘    └───────────────┘     │     └────────────────┘
                                           │
┌──────────────────────────────────────────▼──────────────────────┐
│                  DJANGO REST API + POSTGRESQL                   │
│          (Data Persistence, User Auth, and API Routing)         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```bash
EcoFeast/
├── config/             # Django project configuration
├── donations/          # Core donation models, serializers, and views
├── users/              # Custom user roles (Donors/NGOs) and capability profiles
├── ml_service/         # Feature engineering, XGBoost training, and SHAP explainability
├── genai_service/      # LLM-based image/text information extraction
├── rag_service/        # Qdrant NGO profile embeddings and weighted matching
├── agents/             # LangGraph state definition and agent node handlers
├── templates/          # HTML templates (Dashboard, Maps, and Agent Monitoring)
├── tests/              # Pytest test suite for ML, GenAI, RAG, and Agents
├── Dockerfile          # Production web service dockerfile
└── docker-compose.yml  # Local services (Django, Postgres, Redis, Qdrant)
```

---

## 🚀 Getting Started

### Prerequisites
* Docker and Docker Compose
* Python 3.10+ (if running locally without Docker)
* A [Groq API Key](https://console.groq.com/) for GenAI features

### Running with Docker (Recommended)

1. **Clone the repository and enter the directory:**
   ```bash
   git clone https://github.com/SairajPP/EcoFeast.git
   cd EcoFeast
   ```

2. **Create a `.env` file in the project root:**
   ```env
   DEBUG=1
   SECRET_KEY=your_django_secret_key
   GROQ_API_KEY=your_groq_api_key
   POSTGRES_DB=ecofeast
   POSTGRES_USER=ecofeast
   POSTGRES_PASSWORD=ecofeast_dev_2026
   QDRANT_URL=http://qdrant:6333
   ```

3. **Build and start the container services:**
   ```bash
   docker-compose up --build
   ```
   This will spin up:
   * **Django Web Server** at `http://localhost:8000`
   * **PostgreSQL Database** at `localhost:5432`
   * **Redis Cache/Broker** at `localhost:6379`
   * **Qdrant Vector DB** at `localhost:6333`

4. **Run migrations and populate mock data:**
   ```bash
   docker-compose exec web python manage.py migrate
   # Optional: Sync RAG profiles
   docker-compose exec web python manage.py shell -c "from rag_service.matcher import sync_all_ngos; sync_all_ngos()"
   ```

---

## 🧪 Verification & Testing

The project uses `pytest` for unit and integration testing.

Run all tests inside the Docker container:
```bash
docker-compose exec web pytest
```

The test suite covers:
* **Models:** CustomUser profiles and Donation constraints.
* **ML Service:** Feature transform pipelines, model predictions, and SHAP explainer runs.
* **GenAI Service:** Llama extraction correctness and explainers (mocked API).
* **RAG Service:** Qdrant upserts and combined distance/capacity matcher.
* **Agents:** LangGraph StateGraph state updates, validation filters, and routing loops.
