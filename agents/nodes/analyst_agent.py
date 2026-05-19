"""
analyst_agent.py
Node: Synthesizes all collected sources into a structured analysis —
summary, key findings, themes, and recommendations using an LLM.
"""
import logging
from typing import List, Dict, Any
from agents.state import ResearchState as AgentState

logger = logging.getLogger(__name__)


def _build_context(sources: List[Dict[str, Any]]) -> str:
    """Concatenate source contents into a single context block for the LLM."""
    snippets = []
    for i, src in enumerate(sources, 1):
        snippets.append(f"[{i}] {src.get('title', 'Untitled')}\n{src.get('content', '')}")
    return "\n\n".join(snippets)


def analyst_agent_node(state: AgentState) -> AgentState:
    """
    LangGraph node — reads `sources` from state and produces structured analysis.
    """
    sources = state.get("sources", [])
    refined_topic = state.get("refined_topic", "")
    logger.info("[analyst_agent] Analyzing %d sources for topic: %s", len(sources), refined_topic)

    # ── Placeholder: replace with real LLM synthesis ─────────────────────────
    # from langchain_openai import ChatOpenAI
    # context = _build_context(sources)
    # llm = ChatOpenAI(model=settings.LLM_MODEL)
    # response = llm.invoke(f"Analyze the following research on '{refined_topic}':\n{context}")

    summary = (
        f"This is a placeholder summary for the topic '{refined_topic}'. "
        f"A total of {len(sources)} sources were analyzed."
    )
    key_findings = [
        f"Finding 1: Placeholder insight about {refined_topic}.",
        f"Finding 2: Another placeholder insight from {len(sources)} sources.",
        "Finding 3: Further details to be filled by real LLM analysis.",
    ]
    themes = ["Theme A", "Theme B", "Theme C"]
    recommendations = [
        "Recommendation 1: Explore topic further.",
        "Recommendation 2: Cross-reference with domain experts.",
    ]
    confidence_score = round(min(1.0, len(sources) / 10), 2)

    logger.info("[analyst_agent] Analysis complete. Confidence: %s", confidence_score)

    return {
        **state,
        "summary": summary,
        "key_findings": key_findings,
        "themes": themes,
        "recommendations": recommendations,
        "confidence_score": confidence_score,
        "status": "analyzing",
        "messages": ["Analysis complete."],
    }
