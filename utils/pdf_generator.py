"""
pdf_generator.py
Generates a structured PDF research report.
Signature: generate_pdf(report_content: dict, session_id: str) -> str
"""
import os
import logging
from typing import Dict, Any
from config.settings import get_settings

logger = logging.getLogger(__name__)


def generate_pdf(report_content: Dict[str, Any], session_id: str) -> str:
    """
    Generate a PDF report from report_content and save it under the
    configured report output directory, named by session_id.

    Returns the absolute path of the generated file.
    """
    settings = get_settings()
    os.makedirs(settings.report_output_dir, exist_ok=True)
    output_path = os.path.join(settings.report_output_dir, f"{session_id}.pdf")

    try:
        # ── Real implementation (uncomment after: pip install reportlab) ─────
        # from reportlab.lib.pagesizes import A4
        # from reportlab.lib.styles import getSampleStyleSheet
        # from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        #
        # doc = SimpleDocTemplate(output_path, pagesize=A4)
        # styles = getSampleStyleSheet()
        # story = []
        # story.append(Paragraph(report_content.get("title", "Research Report"), styles["Title"]))
        # story.append(Spacer(1, 12))
        # for section in ["abstract", "introduction", "key_findings",
        #                  "analysis", "research_gaps", "emerging_trends", "conclusion"]:
        #     if report_content.get(section):
        #         story.append(Paragraph(section.replace("_", " ").title(), styles["Heading2"]))
        #         story.append(Paragraph(str(report_content[section]), styles["Normal"]))
        #         story.append(Spacer(1, 8))
        # doc.build(story)

        # ── Placeholder: minimal valid PDF stub ───────────────────────────────
        content = (
            "%PDF-1.4\n"
            "1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
            "2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
            "3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\n"
            "xref\n0 4\n0000000000 65535 f\n"
            "trailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n0\n%%EOF\n"
        )
        with open(output_path, "wb") as f:
            f.write(content.encode("latin-1"))

        logger.info("[pdf_generator] PDF written: %s", output_path)

    except Exception as exc:
        logger.error("[pdf_generator] Failed: %s", exc)
        raise

    return output_path
