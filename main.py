from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.research import router as research_router
from config.settings import get_settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting AI Research Agent API")
    logger.info(f"Model: {settings.hf_model_id}")
    yield
    logger.info("Shutting down")

app = FastAPI(
    title="AI Research Agent API",
    description="Agentic research using LangGraph and Hugging Face free models",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(research_router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "model": settings.hf_model_id,
        "env": settings.app_env
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.app_host,
                port=settings.app_port, reload=True)
