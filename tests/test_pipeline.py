"""
test_pipeline.py
Integration tests for the full research agent pipeline.
Run with: pytest tests/ -v
"""
import pytest
from fastapi.testclient import TestClient


# ── App import (deferred so pytest collects even without all deps) ─────────────

@pytest.fixture(scope="module")
def client():
    from main import app
    return TestClient(app)


# ── Health check ───────────────────────────────────────────────────────────────

def test_health_check(client: TestClient):
    """Root endpoint should return 200 with service info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data


# ── Research start ─────────────────────────────────────────────────────────────

def test_start_research_returns_session_id(client: TestClient):
    """POST /research/start should return a session_id and pending status."""
    payload = {
        "topic": "Artificial Intelligence in Healthcare",
        "max_sources": 5,
        "include_arxiv": True,
        "include_news": True,
        "include_web": True,
        "generate_pdf": False,
        "generate_docx": False,
    }
    response = client.post("/research/start", json=payload)
    assert response.status_code == 202
    data = response.json()
    assert "session_id" in data
    assert data["status"] in ("pending", "researching", "completed")


def test_start_research_invalid_topic(client: TestClient):
    """Very short topic should fail validation (min_length=3)."""
    payload = {"topic": "AI"}
    response = client.post("/research/start", json=payload)
    assert response.status_code == 422


# ── Status check ───────────────────────────────────────────────────────────────

def test_status_not_found(client: TestClient):
    """Unknown session_id should return 404."""
    response = client.get("/research/status/nonexistent-session-id")
    assert response.status_code == 404


# ── Unit: topic refiner ────────────────────────────────────────────────────────

def test_topic_refiner_node():
    """topic_refiner_node should return refined_topic and search_queries."""
    from agents.nodes.topic_refiner import topic_refiner_node
    state = {"original_topic": "quantum computing"}
    result = topic_refiner_node(state)
    assert "refined_topic" in result
    assert "search_queries" in result
    assert len(result["search_queries"]) > 0


# ── Unit: topic validator ──────────────────────────────────────────────────────

def test_topic_validator_passes_clean_topic():
    """Clean topics should be marked valid."""
    from agents.nodes.topic_validator import topic_validator_node
    state = {"refined_topic": "machine learning applications"}
    result = topic_validator_node(state)
    assert result["is_valid"] is True


def test_topic_validator_blocks_harmful_topic():
    """Topics containing blocked keywords should be marked invalid."""
    from agents.nodes.topic_validator import topic_validator_node
    state = {"refined_topic": "illegal activities guide"}
    result = topic_validator_node(state)
    assert result["is_valid"] is False


# ── Unit: research agent ───────────────────────────────────────────────────────

def test_research_agent_returns_sources():
    """research_agent_node should return at least one source."""
    from agents.nodes.research_agent import research_agent_node
    state = {
        "search_queries": ["AI ethics"],
        "refined_topic": "AI ethics",
        "include_web": True,
        "include_arxiv": True,
        "include_news": True,
        "max_sources": 10,
        "sources": [],
    }
    result = research_agent_node(state)
    assert "sources" in result
    assert len(result["sources"]) > 0


# ── Unit: analyst agent ────────────────────────────────────────────────────────

def test_analyst_agent_produces_summary():
    """analyst_agent_node should produce a non-empty summary."""
    from agents.nodes.analyst_agent import analyst_agent_node
    state = {
        "sources": [
            {"title": "Test Source", "content": "Some content.", "url": "", "source_type": "web"}
        ],
        "refined_topic": "AI ethics",
    }
    result = analyst_agent_node(state)
    assert "summary" in result
    assert len(result["summary"]) > 0
    assert "key_findings" in result
