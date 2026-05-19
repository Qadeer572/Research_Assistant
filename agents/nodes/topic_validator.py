import json
import logging
from langchain_core.prompts import ChatPromptTemplate
from agents.state import ResearchState
from config.settings import get_llm

logger = logging.getLogger(__name__)

async def topic_validator_node(state: ResearchState) -> dict:
    logger.info(f"Validating topic: {state['refined_topic']}")
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a research scope evaluator.
            Respond with raw JSON only. No markdown. No explanation.
            JSON format:
            {{
                "status": "valid" or "too_broad" or "too_narrow",
                "suggestions": ["s1", "s2", "s3", "s4"]
            }}
            valid = well scoped and researchable
            too_broad = covers too many areas
            too_narrow = too specific with limited sources
            Always provide 4 suggestions."""),
            ("human", "Research topic: {topic}")
        ])
        llm = get_llm()
        chain = prompt | llm
        response = await chain.ainvoke({"topic": state["refined_topic"]})
        text = response.content.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        parsed = json.loads(text.strip())
        status = parsed.get("status", "valid")
        suggestions = parsed.get("suggestions", [])
        logger.info(f"Status: {status}, Suggestions: {len(suggestions)}")
        return {
            "topic_status": status,
            "suggestions": suggestions,
            "current_node": "topic_validator"
        }
    except Exception as e:
        logger.error(f"Validator error: {e}")
        return {
            "topic_status": "valid",
            "suggestions": [],
            "current_node": "topic_validator",
            "error": str(e)
        }
