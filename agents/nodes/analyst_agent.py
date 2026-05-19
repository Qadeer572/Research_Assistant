import json
import logging
from langchain_core.prompts import ChatPromptTemplate
from agents.state import ResearchState
from config.settings import get_llm

logger = logging.getLogger(__name__)

async def analyst_agent_node(state: ResearchState) -> dict:
    logger.info("Analyst agent started")
    try:
        if not state["research_data"]:
            return {
                "analysis": {},
                "current_node": "analyst_agent",
                "error": "No research data to analyze"
            }
        formatted = ""
        for i, item in enumerate(state["research_data"][:15]):
            formatted += f"Source {i+1}: {item.get('title','')}\n"
            formatted += f"Summary: {item.get('summary','')[:300]}\n\n"
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a research analyst.
            Respond with raw JSON only. No markdown. No explanation.
            JSON format:
            {{
                "key_findings": [{{"title": str, "description": str}}],
                "research_gaps": [str, str, str],
                "emerging_trends": [str, str, str],
                "themes": [str, str, str, str],
                "source_count": int,
                "conclusion": str
            }}"""),
            ("human", "Topic: {topic}\n\nData:\n{data}")
        ])
        llm = get_llm()
        chain = prompt | llm
        response = await chain.ainvoke({
            "topic": state["confirmed_topic"],
            "data": formatted[:3000]
        })
        text = response.content.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        parsed = json.loads(text.strip())
        logger.info(f"Analysis complete: {len(parsed.get('key_findings',[]))} findings")
        return {"analysis": parsed, "current_node": "analyst_agent"}
    except Exception as e:
        logger.error(f"Analyst error: {e}")
        return {
            "analysis": {
                "key_findings": [],
                "research_gaps": [],
                "emerging_trends": [],
                "themes": [],
                "source_count": len(state["research_data"]),
                "conclusion": "Analysis could not be completed."
            },
            "current_node": "analyst_agent",
            "error": str(e)
        }
