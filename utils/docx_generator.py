"""
docx_generator.py
Generates a structured DOCX research report using python-docx.
Accepts a report_data dict and writes the file to the given output_path.
"""
import logging
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)


def generate_docx(report_data: Dict[str, Any], output_path: str) -> str:
    """
    Generate a DOCX report from `report_data` and save it to `output_path`.

    Args:
        report_data: Dictionary containing topic, summary, findings, etc.
        output_path: Absolute path where the DOCX should be saved.

    Returns:
        The output_path of the generated file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        # ── Real implementation (uncomment after: pip install python-docx) ───
        # from docx import Document
        # from docx.shared import Pt
        #
        # doc = Document()
        # doc.add_heading(report_data.get("topic", "Research Report"), level=0)
        # doc.add_heading("Executive Summary", level=1)
        # doc.add_paragraph(report_data.get("summary", ""))
        # doc.add_heading("Key Findings", level=1)
        # for finding in report_data.get("key_findings", []):
        #     doc.add_paragraph(finding, style="List Bullet")
        # doc.add_heading("Themes", level=1)
        # for theme in report_data.get("themes", []):
        #     doc.add_paragraph(theme, style="List Bullet")
        # doc.add_heading("Recommendations", level=1)
        # for rec in report_data.get("recommendations", []):
        #     doc.add_paragraph(rec, style="List Bullet")
        # doc.save(output_path)

        # ── Placeholder: write a minimal stub DOCX (zip-based format) ────────
        # A real DOCX is a ZIP archive; we write a plain text placeholder instead.
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"[DOCX Placeholder]\n")
            f.write(f"Topic: {report_data.get('topic', '')}\n")
            f.write(f"Summary: {report_data.get('summary', '')}\n")
            f.write("Key Findings:\n")
            for finding in report_data.get("key_findings", []):
                f.write(f"  - {finding}\n")

        logger.info("[docx_generator] DOCX written: %s", output_path)

    except Exception as exc:
        logger.error("[docx_generator] Failed to generate DOCX: %s", exc)
        raise

    return output_path
