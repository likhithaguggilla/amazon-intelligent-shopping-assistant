# AI-Powered E-commerce Shopping Assistant

An intelligent shopping assistant that helps users find products through natural language conversations. Built with **LangGraph agentic AI** and **vector search capabilities**.

## Overview

This project implements a **conversational AI assistant** for e-commerce that understands user queries, searches through product catalogs, retrieves relevant reviews, and provides personalized recommendations. The system uses a **supervisor-worker architecture powered by LLMs** to deliver **context-aware responses**.

## Key Features

- **Natural Language Understanding**: Interprets user queries and determines intent
- **Intelligent Product Search**: Vector-based semantic search using Qdrant
- **Review Analysis**: Fetches and analyzes product reviews for better recommendations
- **Conversational Memory**: Maintains conversation context using PostgreSQL checkpointing
- **Real-time Streaming**: Server-sent events (SSE) for live response streaming
- **User Feedback System**: Collects positive/negative feedback with optional detailed comments
- **Dockerized Deployment**: Complete containerized setup for easy deployment

## Architecture

### Application Layer
- **Streamlit UI**: Interactive chat interface for users
- **FastAPI Backend**: RESTful API handling agent orchestration

### Agentic AI System (Powered by LLM)
The core intelligence is built using **LangGraph**, which orchestrates multiple specialized agents:

1. **Planner & Orchestrator Agent**: 
   - Detects query intent and generates multi-step execution plans
   - Routes requests to appropriate tools and agents

2. **RAG-based System**:
   - **Vector DB (Qdrant)**: Stores product metadata, descriptions, and embeddings
   - **External APIs**: Integrates cart tools like ```addToCart, removeFromCart, readTheCart``` etc.

3. **Task Execution Agents + Tools**:
   - Execute specific tasks like product search and review retrieval
   - Iterative refinement based on intermediate results

4. **LLM Synthesis**: Generates final coherent responses

### Data Flow
```
User Query → Streamlit UI → FastAPI Backend → Intent Router → Agent Planner
                                                                    ↓
                                                            Tool Selection
                                                                    ↓
                                                    ┌───────────────┴───────────────┐
                                                    ↓                               ↓
                                            Vector Search                    Review Retrieval
                                            (Qdrant DB)                      (Qdrant DB)
                                                    ↓                               ↓
                                                    └───────────────┬───────────────┘
                                                                    ↓
                                                            LLM Synthesis
                                                                    ↓
                                                            Final Response
```


## Tech Stack

### Core Frameworks
- **LangGraph**: Agentic workflow orchestration
- **FastAPI**: High-performance async API
- **Streamlit**: Interactive web UI
- **OpenAI**: LLM and embeddings

### Data & Storage
- **Qdrant**: Vector database for semantic search
- **PostgreSQL**: Conversation state persistence
- **Pydantic**: Data validation and settings management

### Evaluation & Monitoring
- **RAGAS**: RAG system evaluation
- **LangSmith**: Agent tracing and debugging

### DevOps
- **Docker**: Containerization
- **UV**: Fast Python package management

## Key Components

### Agent System
- **Intent Router**: Determines if query is product-related
- **Planner Agent**: Creates execution plans and selects tools
- **Tool Executor**: Runs search and retrieval operations
- **Response Synthesizer**: Generates natural language responses

### Tools
- `get_formatted_context`: Semantic product search
- `get_formatted_reviews_context`: Review retrieval and analysis

### Feedback System
- Thumbs up/down feedback collection
- Optional detailed feedback for negative responses
- Trace ID tracking for debugging

## API Endpoints

- `POST /rag`: Main chat endpoint (streaming SSE)
- `POST /submit_feedback`: Submit user feedback
- `GET /`: Health check

## Products Ingestion Pipeline

The products pipeline processes product data and creates vector embeddings:

1. **Data Format**: JSONL files with product information (title, features, description, price, images, reviews)
2. **Preprocessing**: Combines product metadata into searchable text
3. **Embedding Generation**: Uses OpenAI's `text-embedding-3-small` model
4. **Vector Storage**: Uploads to Qdrant with metadata payloads


## Evaluation

The project includes a comprehensive evaluation framework to assess the quality and performance of the RAG system using industry-standard metrics.

### Evaluation Framework

The evaluation system is built on:
- **RAGAS (Retrieval-Augmented Generation Assessment)**: Framework for evaluating RAG pipelines
- **LangSmith**: Experiment/prompt tracking and golden dataset management
- **OpenAI GPT-4o-mini**: LLM judge for metric computation
- **Format**: Question-answer pairs with expected outputs
- **Purpose**: Consistent benchmarking across experiments

### Evaluation Process

1.  Fetches test questions from LangSmith dataset
2.  Runs each question through the full RAG pipeline
3. **Metric Computation**: 
   - Faithfulness scorer analyzes answer-context alignment
   - Response Relevancy scorer evaluates answer-question relevance
4. Computes average scores across all test cases
5. Results logged to LangSmith with experiment prefix `retriever`


## Getting Started

### Prerequisites

- Python 3.12
- Docker & Docker Compose
- OpenAI API key (for embeddings and LLM)
- UV package manager (recommended) or pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai_engineering
   ```

2. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=http://qdrant:6333
   API_URL=http://api:8000
   ```

3. **Install dependencies**
   ```bash
   uv sync
   # or
   pip install -e .
   ```

### Running the Application

#### Using Docker Compose

```bash
make run-docker-compose
# or
uv sync && docker compose up --build
```

This will start:
- Streamlit UI at `http://localhost:8501`
- FastAPI backend at `http://localhost:8000`
- Qdrant vector DB at `http://localhost:6333`
- PostgreSQL at `localhost:5433`


### Running Evaluations

```bash
make run-evals-retriever
```

## Project Structure

```
ai_engineering/
├── src/
│   ├── api/                      # FastAPI backend
│   │   ├── agent/                # LangGraph agent implementation
│   │   │   ├── agents.py         # Agent nodes (intent router, planner)
│   │   │   ├── graph.py          # LangGraph workflow definition
│   │   │   ├── tools.py          # Tool implementations (search, reviews)
│   │   │   └── utils/            # Prompt management and utilities
│   │   ├── api/                  # API endpoints and middleware
│   │   ├── core/                 # Configuration management
│   │   └── app.py                # FastAPI application entry point
│   │
│   ├── chatbot_ui/               # Streamlit frontend
│   │   └── app.py                # Chat interface with feedback system
│   │
│   └── data_pipeline/            # Data ingestion pipeline
│       ├── pipeline.py           # ETL pipeline for product data
│       └── verify_ingestion.py  # Data validation scripts
│
├── data/                         # Product data (JSONL format)
├── evals/                        # Evaluation scripts
│   └── eval_retriever.py         # Retrieval quality evaluation
├── experiments/                  # Experimental notebooks and scripts
├── docker-compose.yml            # Service orchestration
├── Dockerfile.fastapi            # API container definition
├── Dockerfile.streamlit          # UI container definition
├── pyproject.toml                # Python dependencies
└── system-architecture.png       # Architecture diagram
```



## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.




