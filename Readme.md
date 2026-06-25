♻️ EcoDispose AI — Intelligent Urban Waste Management RAG Platform
An enterprise-grade, localized Retrieval-Augmented Generation (RAG) platform engineered to solve critical source-segregation visibility, compliance tracing, and regional recycling logistics within the Greater Chennai Corporation (GCC) footprint.

This platform eliminates general large language model hallucinations regarding hyper-local urban geography, regional jurisdiction boundaries, and specialized hazardous material workflows. By utilizing a decoupled microservices setup, it matches an asynchronous FastAPI backend orchestrating a LangChain-Classic production workflow with an isolated local ChromaDB vector database, interfacing seamlessly through a responsive, state-managed Streamlit user application interface.

🏗️ Technical Stack & Architectural Core
Backend Architecture & RAG Orchestration
FastAPI Framework: Implements high-performance, asynchronous RESTful API routing, using Pydantic schemas for request validation payloads to handle stream communication under sub-second latency.

LangChain-Classic Engine: Orchestrates document chunking pipelines, vector store context injection, and structural prompt formatting template wrappers to build a deterministic Retrieval-Augmented pipeline.

ChromaDB Vector Store: Embedded, high-efficiency, disk-persistent vector database configured with localized directory mapping (./chroma_db_store) to isolate document indices.

Google Developer Core AI API: Employs gemini-embedding-001 for highly dense mathematical tokenization vectors and gemini-2.5-flash via advanced safety system definitions for contextual response orchestration.

UI & Pipeline Communication
Streamlit Framework: Python-native web application serving a stateful conversational user interface via session token memory tracking hooks.

Dynamic URL Router & Cloud Isolation: Configured with decoupled runtime environment detection blocks. It programmatically identifies infrastructure properties to toggle API requests seamlessly between local dev server clusters (localhost:8000) and secure live cloud instances (Render Web Services) without altering code.

the file structure : 

EcoDisposeAI/
│
├── env/                         # Isolated Python 3 Local Virtual Runtime Environment
├── chroma_db_store/             # Persistent Disk-Level Hex-Indexed Vector Database
│
├── backend.py                   # FastAPI Application Engine, Embedding Workflows & Core Chain
├── frontend.py                  # Stateful Streamlit Client Browser User Interface
├── ewaste_policy.pdf            # Curated Chennai Waste Infrastructure Policy Document
└── requirements.txt             # Unified System Dependency Blueprint Profile