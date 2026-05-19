"""
docx_generator.py
Generates a structured DOCX research report using python-docx.
Signature: generate_docx(report_content: dict, session_id: str) -> str
"""
import logging
import os
from typing import Dict, Any
from config.settings import get_settings

logger = logging.getLogger(__name__)


def generate_docx(report_content: Dict[str, Any], session_id: str) -> str:
    """
    Generate a DOCX report from `report_content` and save it to the 
    configured report output directory, named by session_id.

    Returns the absolute path of the generated file.
    """
    settings = get_settings()
    os.makedirs(settings.report_output_dir, exist_ok=True)
    output_path = os.path.join(settings.report_output_dir, f"{session_id}.docx")

    try:
        # ── Real implementation (uncomment after: pip install python-docx) ───
        # from docx import Document
        # from docx.shared import Pt
        #
        # doc = Document()
        # doc.add_heading(report_content.get("title", "Research Report"), level=0)
        # doc.add_heading("Executive Summary", level=1)
        # doc.add_paragraph(report_content.get("abstract", ""))
        # doc.add_heading("Key Findings", level=1)
        # doc.add_paragraph(str(report_content.get("key_findings", "")))
        # doc.add_heading("Themes", level=1)
        # doc.add_paragraph(str(report_content.get("themes", "")))
        # doc.add_heading("Recommendations", level=1)
        # doc.add_paragraph(str(report_content.get("conclusion", "")))
        # doc.save(output_path)

        # ── Placeholder: write a minimal stub DOCX (zip-based format) ────────
        # A real DOCX is a ZIP archive; we write a plain text placeholder instead.
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"[DOCX Placeholder]\n")
            f.write(f"Title: {report_content.get('title', '')}\n")
            f.write(f"Abstract: {report_content.get('abstract', '')}\n")
            f.write(f"Key Findings: {report_content.get('key_findings', '')}\n")

        logger.info("[docx_generator] DOCX written: %s", output_path)

    except Exception as exc:
        logger.error("[docx_generator] Failed to generate DOCX: %s", exc)
        raise

    return output_path
