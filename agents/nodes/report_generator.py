"""
report_generator.py
Node: Generates PDF and DOCX reports from the structured analysis stored in state.
Delegates actual file creation to utils/pdf_generator.py and utils/docx_generator.py.
"""
import logging
import os
from datetime import datetime
from agents.state import ResearchState as AgentState
from config.settings import get_settings
settings = get_settings()
from utils.pdf_generator import generate_pdf
from utils.docx_generator import generate_docx

logger = logging.getLogger(__name__)


def report_generator_node(state: AgentState) -> AgentState:
    """
    LangGraph node — generates PDF and/or DOCX reports and stores their
    file paths in `pdf_path` and `docx_path` state keys.
    """
    session_id = state.get("session_id", "unknown")
    refined_topic = state.get("refined_topic", "Research Report")
    generate_pdf_flag = state.get("generate_pdf", True)
    generate_docx_flag = state.get("generate_docx", True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c if c.isalnum() else "_" for c in refined_topic)[:50]
    base_filename = f"{safe_name}_{timestamp}"

    pdf_path: str | None = None
    docx_path: str | None = None

    os.makedirs(settings.OUTPUT_REPORTS_DIR, exist_ok=True)

    report_data = {
        "session_id": session_id,
        "topic": refined_topic,
        "summary": state.get("summary", ""),
        "key_findings": state.get("key_findings", []),
        "themes": state.get("themes", []),
        "recommendations": state.get("recommendations", []),
        "confidence_score": state.get("confidence_score", 0.0),
        "sources": state.get("sources", []),
        "generated_at": timestamp,
    }

    if generate_pdf_flag:
        pdf_path = os.path.join(settings.OUTPUT_REPORTS_DIR, f"{base_filename}.pdf")
        generate_pdf(report_data, pdf_path)
        logger.info("[report_generator] PDF written to %s", pdf_path)

    if generate_docx_flag:
        docx_path = os.path.join(settings.OUTPUT_REPORTS_DIR, f"{base_filename}.docx")
        generate_docx(report_data, docx_path)
        logger.info("[report_generator] DOCX written to %s", docx_path)

    return {
        **state,
        "pdf_path": pdf_path,
        "docx_path": docx_path,
        "status": "completed",
        "messages": [f"Reports generated. PDF={pdf_path} | DOCX={docx_path}"],
    }
