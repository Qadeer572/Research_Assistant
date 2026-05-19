from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from agents.state import ResearchState
from agents.nodes.topic_refiner import topic_refiner_node
from agents.nodes.topic_validator import topic_validator_node
from agents.nodes.research_agent import research_agent_node
from agents.nodes.analyst_agent import analyst_agent_node
from agents.nodes.report_generator import report_generator_node

def route_after_validation(state: ResearchState) -> str:
    if state["topic_status"] == "valid":
        return "research_agent"
    return END

def build_graph():
    graph = StateGraph(ResearchState)
    
    graph.add_node("topic_refiner", topic_refiner_node)
    graph.add_node("topic_validator", topic_validator_node)
    graph.add_node("research_agent", research_agent_node)
    graph.add_node("analyst_agent", analyst_agent_node)
    graph.add_node("report_generator", report_generator_node)
    
    graph.set_entry_point("topic_refiner")
    graph.add_edge("topic_refiner", "topic_validator")
    graph.add_conditional_edges(
        "topic_validator",
        route_after_validation,
        {"research_agent": "research_agent", END: END}
    )
    graph.add_edge("research_agent", "analyst_agent")
    graph.add_edge("analyst_agent", "report_generator")
    graph.add_edge("report_generator", END)
    
    checkpointer = MemorySaver()
    return graph.compile(
        checkpointer=checkpointer,
        interrupt_before=["research_agent"]
    )

research_graph = build_graph()

def get_graph():
    return research_graph
