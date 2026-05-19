"""
routers/research.py
FastAPI router for the research pipeline.

Endpoints:
  POST /research/start   — submit a research request and run the full pipeline
  GET  /research/status  — check current status of a pipeline run
  GET  /research/stream  — SSE stream for live pipeline progress (placeholder)
"""
import uuid
import logging
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from models.schemas import ResearchRequest, ResearchResponse, ResearchStatus
from agents.graph import run_pipeline
from agents.state import ResearchState as AgentState

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/research", tags=["Research"])

# In-memory session store (replace with Redis in production)
_sessions: dict[str, dict] = {}


# ── POST /research/start ───────────────────────────────────────────────────────

@router.post("/start", response_model=ResearchResponse, status_code=202)
async def start_research(
    request: ResearchRequest,
    background_tasks: BackgroundTasks,
) -> ResearchResponse:
    """
    Accept a research topic and kick off the full LangGraph pipeline.
    Returns a session_id immediately; use /status or /stream to track progress.
    """
    session_id = str(uuid.uuid4())
    logger.info("[router] New research session: %s | Topic: %s", session_id, request.topic)

    # Store initial session state
    _sessions[session_id] = {
        "status": ResearchStatus.PENDING,
        "topic": request.topic,
        "result": None,
        "error": None,
    }

    # Build initial agent state
    initial_state: AgentState = {
        "session_id": session_id,
        "original_topic": request.topic,
        "max_sources": request.max_sources,
        "include_arxiv": request.include_arxiv,
        "include_news": request.include_news,
        "include_web": request.include_web,
        "generate_pdf": request.generate_pdf,
        "generate_docx": request.generate_docx,
        "sources": [],
        "messages": [],
        "status": "pending",
        "error": None,
    }

    # Run pipeline in background
    background_tasks.add_task(_run_pipeline_task, session_id, initial_state)

    return ResearchResponse(
        session_id=session_id,
        status=ResearchStatus.PENDING,
        topic=request.topic,
    )


# ── GET /research/status/{session_id} ─────────────────────────────────────────

@router.get("/status/{session_id}", response_model=ResearchResponse)
async def get_status(session_id: str) -> ResearchResponse:
    """Return the current status and results of a research session."""
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")

    result = session.get("result") or {}

    return ResearchResponse(
        session_id=session_id,
        status=session["status"],
        topic=session["topic"],
        refined_topic=result.get("refined_topic"),
        error=session.get("error"),
    )


# ── GET /research/stream/{session_id} — SSE ────────────────────────────────────

@router.get("/stream/{session_id}")
async def stream_progress(session_id: str):
    """
    SSE endpoint — streams pipeline progress events for a given session.
    Replace the placeholder generator with a real pub/sub (e.g. Redis Streams).
    """
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")

    async def event_generator():
        yield f"data: {{\"session_id\": \"{session_id}\", \"status\": \"connected\"}}\n\n"
        # ── Real implementation: subscribe to Redis channel and yield events ──
        # async for message in redis_subscribe(session_id):
        #     yield f"data: {message}\n\n"
        yield f"data: {{\"session_id\": \"{session_id}\", \"status\": \"streaming_placeholder\"}}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# ── Internal background task ───────────────────────────────────────────────────

def _run_pipeline_task(session_id: str, initial_state: AgentState) -> None:
    """Background task that executes the LangGraph pipeline and updates session state."""
    try:
        _sessions[session_id]["status"] = ResearchStatus.RESEARCHING
        final_state = run_pipeline(initial_state)
        _sessions[session_id]["status"] = ResearchStatus.COMPLETED
        _sessions[session_id]["result"] = final_state
        logger.info("[router] Pipeline completed for session: %s", session_id)
    except Exception as exc:
        logger.error("[router] Pipeline failed for session %s: %s", session_id, exc)
        _sessions[session_id]["status"] = ResearchStatus.FAILED
        _sessions[session_id]["error"] = str(exc)
