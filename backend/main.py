import time
import os
import json
import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import httpx
from bs4 import BeautifulSoup
from typing import List, Optional

# Import our AI Agents
from agents import (
    IngestionAgent, 
    InsightAgent, 
    ActionAgent, 
    SimulationAgent,
    ChainAgent,
    ConstraintAgent,
    ContradictionAgent,
    TemporalAgent
)

# Initialize FastAPI app
app = FastAPI(title="EconoSense PK API", description="Pakistan Economy News Analysis")

# Add CORS middleware so Flutter app can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AntigravityOrchestrator:
    def __init__(self):
        self.agents = {}
        self.active_tasks = []
        self.execution_log = []
        
        # Initialize all 8 agents
        self.spawn_agent("IngestionAgent", IngestionAgent())
        self.spawn_agent("InsightAgent", InsightAgent())
        self.spawn_agent("ActionAgent", ActionAgent())
        self.spawn_agent("ChainAgent", ChainAgent())
        self.spawn_agent("ConstraintAgent", ConstraintAgent())
        self.spawn_agent("SimulationAgent", SimulationAgent())
        self.spawn_agent("ContradictionAgent", ContradictionAgent())
        self.spawn_agent("TemporalAgent", TemporalAgent())
    
    def spawn_agent(self, agent_name, agent_instance):
        self.agents[agent_name] = agent_instance
        self.execution_log.append({
            "event": f"Antigravity Orchestrator spawned {agent_name}",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    
    def assign_task(self, agent_name, task_name, func, *args, **kwargs):
        self.execution_log.append({
            "event": f"Task assigned: {task_name} to {agent_name}",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
        
        t0 = time.time()
        try:
            result = func(*args, **kwargs)
            time_ms = round((time.time() - t0) * 1000, 2)
            
            # The agents in EconoSense usually return (output, retries, trace)
            if isinstance(result, tuple) and len(result) == 3:
                output, retries, trace = result
                
                self.execution_log.append({
                    "event": f"Agent completed: {agent_name}",
                    "agent": agent_name,
                    "time_ms": time_ms,
                    "retries": retries,
                    "reasoning_trace": trace,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })
                return output, retries, trace, time_ms
            else:
                self.execution_log.append({
                    "event": f"Agent completed: {agent_name}",
                    "agent": agent_name,
                    "time_ms": time_ms,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })
                return result, 0, [], time_ms
                
        except Exception as e:
            self.handle_failure(agent_name, e)
            raise e
    
    def handle_failure(self, agent_name, error):
        self.execution_log.append({
            "event": f"Agent failed: {agent_name}",
            "error": str(error),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
        print(f"Orchestrator caught failure in {agent_name}: {error}")
    
    def monitor_agents(self):
        return {name: "Active" for name in self.agents.keys()}
        
    def calculate_autonomy_score(self, timeline: List[dict]) -> int:
        score = 100
        for item in timeline:
            retries = item.get("retries", 0)
            score -= (retries * 5)
        return max(0, score)

    def save_trace_log(self, input_text, agent_timeline, action_chain, constraints, final_output, total_time_ms):
        try:
            log_dir = r"D:\humaa\EconoSense-pk\antigravity-artifacts-logs"
            os.makedirs(log_dir, exist_ok=True)
            
            trace_id = str(uuid.uuid4())
            filename = f"analysis_trace_{trace_id}.json"
            filepath = os.path.join(log_dir, filename)
            
            agent_decisions = {item["agent"]: item.get("reasoning_trace", []) for item in agent_timeline if "agent" in item}
            
            # Extract only orchestrator events for decisions trace
            orchestrator_decisions = [item for item in agent_timeline if "event" in item]
            
            trace_data = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "input_text": input_text,
                "orchestrator_decisions": orchestrator_decisions,
                "agent_decisions": agent_decisions,
                "action_chain": action_chain,
                "constraint_check": constraints,
                "final_output": final_output,
                "total_time_ms": total_time_ms
            }
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(trace_data, f, indent=2)
        except Exception as e:
            print(f"Failed to save trace log: {e}")

    async def coordinate_pipeline(self, input_data, pipeline_type: str = "text"):
        # Reset execution log for this run
        self.execution_log = []
        self.execution_log.append({
            "event": f"Antigravity Orchestrator starting {pipeline_type} pipeline",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
        
        start_total = time.time()
        
        contradiction_result = None
        temporal_analysis = None
        current_text = input_data
        
        # Pipeline Type specific initial steps
        if pipeline_type == "url":
            t_fetch = time.time()
            self.execution_log.append({"event": "Task assigned: Fetch URL to URLFetcher", "timestamp": datetime.utcnow().isoformat() + "Z"})
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(input_data)
                    response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                for script in soup(["script", "style"]):
                    script.extract()
                current_text = soup.get_text(separator=' ')
                fetch_time = round((time.time() - t_fetch) * 1000, 2)
                self.execution_log.append({
                    "event": "Agent completed: URLFetcher",
                    "agent": "URLFetcher", 
                    "time_ms": fetch_time, 
                    "retries": 0, 
                    "reasoning_trace": ["Extracted text from URL", "Cleaned HTML"],
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })
            except Exception as e:
                self.handle_failure("URLFetcher", e)
                raise e
                
        elif pipeline_type == "multi":
            contradiction_result, ret_c, trace_c, time_c = self.assign_task(
                "ContradictionAgent", "Check for conflicts",
                self.agents["ContradictionAgent"].detect_contradictions, input_data
            )
            current_text = "\n\n".join(input_data)
            
        elif pipeline_type == "csv":
            temporal_analysis, ret_t, trace_t, time_t = self.assign_task(
                "TemporalAgent", "Analyze trends",
                self.agents["TemporalAgent"].analyze_trend, input_data
            )
            current_text = f"Data Analysis Report: {temporal_analysis.get('summary', 'Data analyzed.')} The trend direction is {temporal_analysis.get('trend_direction', 'stable')} with a percentage change of {temporal_analysis.get('percentage_change', '0%')}. Forecast: {temporal_analysis.get('forecast', 'N/A')}."

        # Standard 6-agent pipeline
        clean_text, ret0, trace0, time0 = self.assign_task(
            "IngestionAgent", "Clean text",
            self.agents["IngestionAgent"].process, current_text
        )

        insights, ret1, trace1, time1 = self.assign_task(
            "InsightAgent", "Extract insights",
            self.agents["InsightAgent"].analyze, clean_text
        )

        actions, ret2, trace2, time2 = self.assign_task(
            "ActionAgent", "Generate actions",
            self.agents["ActionAgent"].get_actions, insights
        )

        action_chain, ret3, trace3, time3 = self.assign_task(
            "ChainAgent", "Create action chain",
            self.agents["ChainAgent"].create_chain, insights, actions
        )

        constraints = {}
        if actions and len(actions) > 0:
            top_action = actions[0]
            constraints, ret4, trace4, time4 = self.assign_task(
                "ConstraintAgent", "Check feasibility",
                self.agents["ConstraintAgent"].check_feasibility, top_action
            )

        simulation = {}
        if actions and len(actions) > 0:
            top_action = actions[0]
            simulation, ret5, trace5, time5 = self.assign_task(
                "SimulationAgent", "Simulate top action",
                self.agents["SimulationAgent"].simulate, top_action
            )

        total_time = round((time.time() - start_total) * 1000, 2)
        
        self.execution_log.append({
            "event": "Antigravity Orchestrator pipeline complete",
            "total_time_ms": total_time,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
        
        final_output = {
            "system_autonomy_score": self.calculate_autonomy_score(self.execution_log),
            "insights": insights,
            "actions": actions,
            "action_chain": action_chain,
            "constraints": constraints,
            "simulation": simulation,
            "agent_timeline": self.execution_log
        }
        
        if pipeline_type == "multi":
            final_output["contradiction_analysis"] = contradiction_result
        elif pipeline_type == "csv":
            final_output["temporal_analysis"] = temporal_analysis
            
        # For trace logging input representation
        trace_input = input_data
        if pipeline_type == "multi":
            trace_input = "\n\n".join(input_data)
            
        self.save_trace_log(trace_input, self.execution_log, action_chain, constraints, final_output, total_time)

        return final_output

# Initialize the orchestrator
orchestrator = AntigravityOrchestrator()

# Define the request body schemas
class AnalyzeRequest(BaseModel):
    news_text: str

class AnalyzeUrlRequest(BaseModel):
    url: str

class AnalyzeMultiRequest(BaseModel):
    sources: List[str]

class AnalyzeCsvRequest(BaseModel):
    csv_data: str

@app.post("/analyze")
async def analyze_news(request: AnalyzeRequest):
    try:
        return await orchestrator.coordinate_pipeline(request.news_text, "text")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-url")
async def analyze_url(request: AnalyzeUrlRequest):
    try:
        return await orchestrator.coordinate_pipeline(request.url, "url")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-multi")
async def analyze_multi(request: AnalyzeMultiRequest):
    try:
        return await orchestrator.coordinate_pipeline(request.sources, "multi")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-csv")
async def analyze_csv(request: AnalyzeCsvRequest):
    try:
        return await orchestrator.coordinate_pipeline(request.csv_data, "csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
