from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class ResearchStatus(str, Enum):
    PENDING = "pending"
    REFINING = "refining"
    VALIDATING = "validating"
    RESEARCHING = "researching"
    ANALYZING = "analyzing"
    GENERATING_REPORT = "generating_report"
    COMPLETED = "completed"
    FAILED = "failed"


# ── Request Schemas ────────────────────────────────────────────────────────────

class ResearchRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=500, description="Research topic submitted by the user")
    max_sources: int = Field(default=10, ge=1, le=50, description="Maximum number of sources to retrieve")
    include_arxiv: bool = Field(default=True, description="Include ArXiv academic papers")
    include_news: bool = Field(default=True, description="Include news articles")
    include_web: bool = Field(default=True, description="Include general web search via Tavily")
    generate_pdf: bool = Field(default=True, description="Generate a PDF report")
    generate_docx: bool = Field(default=True, description="Generate a DOCX report")


# ── Internal Result Schemas ────────────────────────────────────────────────────

class TopicRefinementResult(BaseModel):
    original_topic: str
    refined_topic: str
    search_queries: List[str] = Field(default_factory=list)
    is_valid: bool = True
    validation_message: str = ""


class SourceItem(BaseModel):
    title: str
    url: str
    content: str
    source_type: str  # "web" | "arxiv" | "news"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ResearchResult(BaseModel):
    query: str
    sources: List[SourceItem] = Field(default_factory=list)
    total_sources: int = 0


class AnalysisResult(BaseModel):
    summary: str = ""
    key_findings: List[str] = Field(default_factory=list)
    themes: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    confidence_score: float = 0.0


class ReportResult(BaseModel):
    pdf_path: Optional[str] = None
    docx_path: Optional[str] = None
    generated_at: Optional[str] = None


# ── Response Schemas ───────────────────────────────────────────────────────────

class ResearchResponse(BaseModel):
    session_id: str
    status: ResearchStatus = ResearchStatus.PENDING
    topic: str
    refined_topic: Optional[str] = None
    research: Optional[ResearchResult] = None
    analysis: Optional[AnalysisResult] = None
    report: Optional[ReportResult] = None
    error: Optional[str] = None

    class Config:
        use_enum_values = True
