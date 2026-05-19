from typing import TypedDict, List, Dict, Any, Optional, Literal
from datetime import datetime
import uuid

class ResearchState(TypedDict):
    session_id: str
    raw_input: str
    refined_topic: str
    topic_status: Literal["valid","too_broad","too_narrow","pending"]
    suggestions: List[str]
    confirmed_topic: str
    selected_sources: List[str]
    research_data: List[Dict[str, Any]]
    dataset_path: str
    analysis: Dict[str, Any]
    report_content: Dict[str, Any]
    report_paths: Dict[str, str]
    error: Optional[str]
    current_node: str
    created_at: str

def create_initial_state(
    session_id: str,
    raw_input: str,
    selected_sources: List[str]
) -> ResearchState:
    return ResearchState(
        session_id=session_id,
        raw_input=raw_input,
        refined_topic="",
        topic_status="pending",
        suggestions=[],
        confirmed_topic="",
        selected_sources=selected_sources,
        research_data=[],
        dataset_path="",
        analysis={},
        report_content={},
        report_paths={},
        error=None,
        current_node="",
        created_at=datetime.now().isoformat()
    )
