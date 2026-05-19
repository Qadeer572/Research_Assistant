# AI Research Agent

> A production-ready AI research pipeline built with **FastAPI**, **LangGraph**, and **LangChain**.  
> Performs multi-source research (Tavily · ArXiv · NewsAPI), synthesizes findings with an LLM, and generates PDF + DOCX reports.

---

## Features

- **Topic Refinement & Validation** — LLM refines and validates the user's topic before research begins
- **Multi-Source Research** — Tavily (web), ArXiv (papers), NewsAPI (news)
- **LangGraph Pipeline** — Stateful, resumable agent graph with conditional routing
- **Analysis & Synthesis** — LLM-powered summary, key findings, themes, and recommendations
- **Report Generation** — PDF (ReportLab) and DOCX (python-docx) output
- **SSE Streaming** — Live progress updates via Server-Sent Events
- **Human-in-the-loop ready** — Graph can be paused awaiting user confirmation

---

## Project Structure

```
research_agent/
├── agents/          # LangGraph graph definition and all node implementations
├── routers/         # FastAPI route handlers
├── models/          # Pydantic request/response schemas
├── tools/           # LangChain tool wrappers for external APIs
├── utils/           # PDF/DOCX generators and shared helpers
├── config/          # Pydantic settings loaded from .env
├── outputs/         # Runtime output (auto-created)
│   ├── research/    # Raw JSON/CSV research datasets
│   └── reports/     # Generated PDF and DOCX reports
├── tests/           # pytest test suite
├── main.py          # FastAPI app entrypoint
└── requirements.txt
```

---

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/your-org/research-agent
cd research-agent
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

Visit **http://localhost:8000/docs** for the interactive API documentation.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Liveness check |
| `GET` | `/health` | Readiness probe |
| `POST` | `/research/start` | Start a research pipeline run |
| `GET` | `/research/status/{session_id}` | Poll session status |
| `GET` | `/research/stream/{session_id}` | SSE live progress stream |

### Example Request

```bash
curl -X POST http://localhost:8000/research/start \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Large Language Models in Healthcare",
    "max_sources": 10,
    "include_arxiv": true,
    "include_news": true,
    "include_web": true,
    "generate_pdf": true,
    "generate_docx": true
  }'
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## LangGraph Pipeline

```
refine_topic → validate_topic ──(invalid)──► END
                    │
                (valid)
                    ▼
               research ──► analyze ──► generate_report ──► END
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | required |
| `TAVILY_API_KEY` | Tavily Search API key | required |
| `NEWSAPI_KEY` | NewsAPI key | required |
| `LLM_MODEL` | OpenAI model name | `gpt-4o-mini` |
| `LLM_TEMPERATURE` | LLM temperature | `0.3` |
| `OUTPUT_RESEARCH_DIR` | Path for dataset output | `outputs/research` |
| `OUTPUT_REPORTS_DIR` | Path for report output | `outputs/reports` |

---

## License

MIT
