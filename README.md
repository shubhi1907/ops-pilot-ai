# OpsPilot AI

Agentic AI workflow automation platform for enterprise support operations.

The platform processes customer issues, performs AI-driven operational decisioning, retrieves contextual memory using vector search (RAG), generates intelligent responses, tracks workflow lifecycle, and supports human approval flows.

## Features

- Multi-agent AI architecture
- Risk scoring engine
- AI escalation logic
- Human approval workflows
- Workflow lifecycle tracking
- Retrieval-Augmented Generation (RAG)
- Operational analytics dashboard
- Streamlit frontend
- FastAPI backend

## Architecture

![Architecture Diagram](architecture.png)

## Tech Stack

- Python
- FastAPI
- Streamlit
- OpenAI API
- FAISS Vector Search
- SQLite
- SQLAlchemy

## Demo Workflow

1. Customer email submitted
2. Classification agent categorizes issue
3. Decision agent determines escalation + risk
4. RAG memory retrieves similar incidents
5. Response agent generates customer communication
6. Human approval workflow triggered
7. Analytics dashboard updated