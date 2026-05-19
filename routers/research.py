import os
from typing import List, Dict, Any
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from agents.state import create_initial_state
from agents.graph import get_graph
import uuid

router = APIRouter()

active_sessions = {}

class ResearchStartRequest(BaseModel):
    topic: str
    sources: List[str] = ["web"]

class ConfirmTopicRequest(BaseModel):
    confirmed_topic: str

@router.post("/research/start")
async def start_research(request: ResearchStartRequest, background_tasks: BackgroundTasks):
    session_id = str(uuid.uuid4())
    initial_state = create_initial_state(session_id, request.topic, request.sources)
    active_sessions[session_id] = {"status": "starting", "topic": request.topic}
    
    graph = get_graph()
    config = {"configurable": {"thread_id": session_id}}

    async def run_pipeline():
        try:
            active_sessions[session_id]["status"] = "running"
            await graph.ainvoke(initial_state, config=config)
            state = graph.get_state(config)
            if state and state.next:
                active_sessions[session_id]["status"] = "awaiting_confirmation"
            else:
                active_sessions[session_id]["status"] = "completed"
        except Exception as e:
            active_sessions[session_id]["status"] = "failed"
            active_sessions[session_id]["error"] = str(e)

    background_tasks.add_task(run_pipeline)
    return {"session_id": session_id, "message": "Research pipeline started."}


@router.post("/research/{session_id}/confirm")
async def confirm_research(session_id: str, request: ConfirmTopicRequest, background_tasks: BackgroundTasks):
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    graph = get_graph()
    config = {"configurable": {"thread_id": session_id}}

    async def resume_pipeline():
        try:
            active_sessions[session_id]["status"] = "running"
            await graph.aupdate_state(config, {"confirmed_topic": request.confirmed_topic})
            await graph.ainvoke(None, config=config)
            active_sessions[session_id]["status"] = "completed"
        except Exception as e:
            active_sessions[session_id]["status"] = "failed"
            active_sessions[session_id]["error"] = str(e)

    background_tasks.add_task(resume_pipeline)
    return {"session_id": session_id, "message": "Research pipeline resumed."}


@router.get("/research/{session_id}/results")
async def get_results(session_id: str):
    graph = get_graph()
    config = {"configurable": {"thread_id": session_id}}
    state = graph.get_state(config)
    if not state or not state.values:
        raise HTTPException(status_code=404, detail="Results not found")
    return {"analysis": state.values.get("analysis", {})}


@router.post("/research/{session_id}/report")
async def generate_report(session_id: str):
    graph = get_graph()
    config = {"configurable": {"thread_id": session_id}}
    state = graph.get_state(config)
    if not state or not state.values:
        raise HTTPException(status_code=404, detail="State not found")
    return {"report_paths": state.values.get("report_paths", {})}


@router.get("/research/{session_id}/download/{format}")
async def download_report(session_id: str, format: str):
    graph = get_graph()
    config = {"configurable": {"thread_id": session_id}}
    state = graph.get_state(config)
    if not state or not state.values:
        raise HTTPException(status_code=404, detail="State not found")
        
    paths = state.values.get("report_paths", {})
    if format not in paths or not os.path.exists(paths[format]):
        raise HTTPException(status_code=404, detail=f"Report format '{format}' not found")
        
    return FileResponse(paths[format])


@router.get("/research/{session_id}/status")
async def get_status(session_id: str):
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
        
    graph = get_graph()
    config = {"configurable": {"thread_id": session_id}}
    state = graph.get_state(config)
    
    return {
        "session_id": session_id,
        "status": active_sessions[session_id]["status"],
        "graph_state": state.values if state else {},
        "next_nodes": state.next if state else []
    }
