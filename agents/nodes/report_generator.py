import json
import logging
from langchain_core.prompts import ChatPromptTemplate
from agents.state import ResearchState
from config.settings import get_llm
from utils.docx_generator import generate_docx
from utils.pdf_generator import generate_pdf

logger = logging.getLogger(__name__)

async def report_generator_node(state: ResearchState) -> dict:
    logger.info("Report generator started")
    try:
        analysis_str = json.dumps(state["analysis"])[:2000]
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an academic report writer.
            Write report content based strictly on provided data.
            Respond with raw JSON only. No markdown.
            JSON format:
            {{
                "title": str,
                "abstract": str,
                "introduction": str,
                "key_findings": str,
                "analysis": str,
                "research_gaps": str,
                "emerging_trends": str,
                "conclusion": str,
                "references": [str]
            }}"""),
            ("human", "Topic: {topic}\nAnalysis: {analysis}")
        ])
        llm = get_llm()
        chain = prompt | llm
        response = await chain.ainvoke({
            "topic": state["confirmed_topic"],
            "analysis": analysis_str
        })
        text = response.content.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        report_content = json.loads(text.strip())
        docx_path = generate_docx(report_content, state["session_id"])
        pdf_path = generate_pdf(report_content, state["session_id"])
        logger.info(f"Report saved: {docx_path}, {pdf_path}")
        return {
            "report_content": report_content,
            "report_paths": {"docx": docx_path, "pdf": pdf_path},
            "current_node": "report_generator"
        }
    except Exception as e:
        logger.error(f"Report generator error: {e}")
        return {
            "report_content": {},
            "report_paths": {},
            "current_node": "report_generator",
            "error": str(e)
        }
