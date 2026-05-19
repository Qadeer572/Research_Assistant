import os
import json
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langgraph.prebuilt import create_react_agent
from agents.state import ResearchState
from config.settings import get_llm, get_settings

# Ensure .env is loaded into os.environ so tool constructors can read API keys
load_dotenv(override=False)

logger = logging.getLogger(__name__)


async def research_agent_node(state: ResearchState) -> dict:
    logger.info(f"Research started: {state['confirmed_topic']}")
    try:
        settings = get_settings()

        # Explicitly set TAVILY_API_KEY in env so TavilySearchResults picks it up
        os.environ.setdefault("TAVILY_API_KEY", settings.tavily_api_key)

        tools = [
            TavilySearchResults(
                max_results=5,
                tavily_api_key=settings.tavily_api_key,
            ),
            ArxivQueryRun(),
            WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
        ]
        llm = get_llm()
        agent = create_react_agent(llm, tools)
        result = await agent.ainvoke({
            "messages": [{
                "role": "user",
                "content": (
                    f"Research this topic using all tools: {state['confirmed_topic']}. "
                    "Collect at least 10 sources."
                )
            }]
        })
        research_data = []
        for msg in result.get("messages", []):
            if hasattr(msg, "content") and isinstance(msg.content, str):
                if len(msg.content) > 100:
                    research_data.append({
                        "title": msg.content[:100],
                        "url": "",
                        "summary": msg.content[:500],
                        "source_type": "web",
                        "date": ""
                    })

        os.makedirs(settings.research_output_dir, exist_ok=True)
        path = f"{settings.research_output_dir}/{state['session_id']}.json"
        with open(path, "w") as f:
            json.dump(research_data, f, indent=2)

        logger.info(f"Collected {len(research_data)} sources")
        return {
            "research_data": research_data,
            "dataset_path": path,
            "current_node": "research_agent"
        }
    except Exception as e:
        logger.error(f"Research agent error: {e}")
        return {
            "research_data": [],
            "dataset_path": "",
            "current_node": "research_agent",
            "error": str(e)
        }
