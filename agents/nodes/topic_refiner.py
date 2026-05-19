import logging
from langchain_core.prompts import ChatPromptTemplate
from agents.state import ResearchState
from config.settings import get_llm

logger = logging.getLogger(__name__)

async def topic_refiner_node(state: ResearchState) -> dict:
    logger.info(f"Topic refiner started: {state['raw_input'][:50]}")
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a research topic specialist. 
            Rewrite the user input as a clear focused academic 
            research question. Return only the refined topic. 
            Nothing else. No explanation. No quotes."""),
            ("human", "Raw input: {raw_input}")
        ])
        llm = get_llm()
        chain = prompt | llm
        response = await chain.ainvoke({"raw_input": state["raw_input"]})
        refined = response.content.strip().strip('"').strip("'")
        if refined.lower().startswith("refined topic:"):
            refined = refined[14:].strip()
        logger.info(f"Refined topic: {refined}")
        return {"refined_topic": refined, "current_node": "topic_refiner"}
    except Exception as e:
        logger.error(f"Topic refiner error: {e}")
        return {
            "refined_topic": state["raw_input"],
            "current_node": "topic_refiner",
            "error": str(e)
        }
