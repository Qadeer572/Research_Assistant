import asyncio
import os
import uuid
from dotenv import load_dotenv
load_dotenv()

from agents.graph import get_graph
from agents.state import create_initial_state
from unittest.mock import patch
from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable

class MockResponse:
    @property
    def content(self):
        return '''```json\n{"status": "valid", "suggestions": ["Mock Suggestion"], "key_findings": [{"title": "Mock", "description": "Desc"}], "themes": ["Mock"], "source_count": 1, "title": "Mock", "abstract": "Mock", "introduction": "Mock", "analysis": "Mock", "research_gaps": "Mock", "emerging_trends": "Mock", "conclusion": "Mock", "references": ["Mock"]}```'''

class MockLLM(Runnable):
    def invoke(self, input, config=None, **kwargs):
        return MockResponse()
    
    async def ainvoke(self, input, config=None, **kwargs):
        return MockResponse()

def mock_get_llm():
    return MockLLM()

async def mock_agent_ainvoke(*args, **kwargs):
    return {"messages": [AIMessage(content="Mock valid source that is very long " * 20)]}

def mock_create_react_agent(*args, **kwargs):
    class DummyAgent(Runnable):
        def invoke(self, input, config=None, **kwargs):
            return {"messages": [AIMessage(content="Mock valid source that is very long " * 20)]}
            
        async def ainvoke(self, input, config=None, **kwargs):
            return await mock_agent_ainvoke(*args, **kwargs)
    return DummyAgent()

async def run_test():
    print("=== AI Research Agent Pipeline Test ===\n")
    
    graph = get_graph()
    session_id = str(uuid.uuid4())
    topic = "Impact of transformer models on NLP benchmarks"
    config = {"configurable": {"thread_id": session_id}}
    
    print(f"Session ID: {session_id}")
    print(f"Test topic: {topic}\n")
    
    state = create_initial_state(
        session_id=session_id,
        raw_input=topic,
        selected_sources=["web", "academic", "wiki"]
    )
    
    with patch("agents.nodes.topic_refiner.get_llm", new=mock_get_llm), \
         patch("agents.nodes.topic_validator.get_llm", new=mock_get_llm), \
         patch("agents.nodes.analyst_agent.get_llm", new=mock_get_llm), \
         patch("agents.nodes.report_generator.get_llm", new=mock_get_llm), \
         patch("agents.nodes.research_agent.get_llm", new=mock_get_llm), \
         patch("agents.nodes.research_agent.create_react_agent", new=mock_create_react_agent):

        print("Step 1: Running until HITL interrupt...")
        snapshot = await graph.ainvoke(state, config)
        print(f"Refined topic: {snapshot.get('refined_topic', '')}")
        print(f"Status: {snapshot.get('topic_status', '')}")
        print(f"Suggestions: {snapshot.get('suggestions', [])}\n")
        
        confirmed = snapshot.get("suggestions")[0] if snapshot.get("suggestions") else snapshot.get("refined_topic", "Fallback Topic")
        print(f"Step 2: Confirming topic: {confirmed}")
        await graph.aupdate_state(config, {"confirmed_topic": confirmed})
        
        print("\nStep 3: Running full pipeline...")
        final = await graph.ainvoke(None, config)
        print(f"Sources collected: {len(final.get('research_data', []))}")
        print(f"Themes: {final.get('analysis', {}).get('themes', [])}")
        print(f"Key findings: {len(final.get('analysis', {}).get('key_findings', []))}")
        print(f"DOCX: {final.get('report_paths', {}).get('docx')}")
        print(f"PDF: {final.get('report_paths', {}).get('pdf')}")
        
        assert len(final["research_data"]) > 0, "No research data"
        assert final["analysis"], "No analysis"
        assert "docx" in final["report_paths"], "No DOCX"
        assert "pdf" in final["report_paths"], "No PDF"
        assert os.path.exists(final["report_paths"]["docx"]), "DOCX file missing"
        
        print("\n=== ALL TESTS PASSED ===")

if __name__ == "__main__":
    asyncio.run(run_test())
