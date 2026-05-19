"""
main.py
FastAPI application entrypoint for the AI Research Agent.
Run with: uvicorn main:app --reload
"""
import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config.settings import get_settings
settings = get_settings()
from routers.research import router as research_router

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL, logging.INFO) if hasattr(settings, "LOG_LEVEL") else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


# ── Lifespan (startup / shutdown) ─────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create required output directories on startup."""
    for path in [settings.OUTPUT_RESEARCH_DIR, settings.OUTPUT_REPORTS_DIR]:
        os.makedirs(path, exist_ok=True)
        logger.info("Ensured directory exists: %s", path)
    logger.info("🚀  %s v%s is starting up", settings.APP_NAME, settings.APP_VERSION)
    yield
    logger.info("🛑  %s is shutting down", settings.APP_NAME)


# ── App Factory ────────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "AI Research Agent powered by FastAPI + LangGraph + LangChain. "
        "Supports multi-source research (Tavily, ArXiv, NewsAPI), "
        "topic refinement, analysis, and PDF/DOCX report generation."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(research_router)


# ── Root endpoint ──────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    """Liveness check — returns service name and version."""
    return JSONResponse({
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    })


@app.get("/health", tags=["Health"])
async def health():
    """Readiness probe for Docker / Kubernetes."""
    return JSONResponse({"status": "healthy"})
