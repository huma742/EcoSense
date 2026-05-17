import os

file_path = r"d:\humaa\EconoSense-pk\backend\main.py"

new_main_code = """import time
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

# Initialize the agents
ingestion_agent = IngestionAgent()
insight_agent = InsightAgent()
action_agent = ActionAgent()
simulation_agent = SimulationAgent()
chain_agent = ChainAgent()
constraint_agent = ConstraintAgent()
contradiction_agent = ContradictionAgent()
temporal_agent = TemporalAgent()

def calculate_autonomy_score(timeline: List[dict]) -> int:
    score = 100
    for item in timeline:
        retries = item.get("retries", 0)
        score -= (retries * 5)
    return max(0, score)

# Define the request body schema
class AnalyzeRequest(BaseModel):
    news_text: str

@app.post("/analyze")
async def analyze_news(request: AnalyzeRequest):
    try:
        start_total = time.time()
        agent_timeline = []

        # 1. IngestionAgent -> clean the text
        t0 = time.time()
        clean_text, ret0, trace0 = ingestion_agent.process(request.news_text)
        agent_timeline.append({"agent": "IngestionAgent", "time_ms": round((time.time() - t0) * 1000, 2), "retries": ret0, "reasoning_trace": trace0})

        # 2. InsightAgent -> get insights
        t1 = time.time()
        insights, ret1, trace1 = insight_agent.analyze(clean_text)
        agent_timeline.append({"agent": "InsightAgent", "time_ms": round((time.time() - t1) * 1000, 2), "retries": ret1, "reasoning_trace": trace1})

        # 3. ActionAgent -> get 3 actions
        t2 = time.time()
        actions, ret2, trace2 = action_agent.get_actions(insights)
        agent_timeline.append({"agent": "ActionAgent", "time_ms": round((time.time() - t2) * 1000, 2), "retries": ret2, "reasoning_trace": trace2})

        # 4. ChainAgent -> chain top action
        t3 = time.time()
        action_chain, ret3, trace3 = chain_agent.create_chain(insights, actions)
        agent_timeline.append({"agent": "ChainAgent", "time_ms": round((time.time() - t3) * 1000, 2), "retries": ret3, "reasoning_trace": trace3})

        # 5. ConstraintAgent -> check constraints
        t4 = time.time()
        constraints = {}
        if actions and len(actions) > 0:
            top_action = actions[0]
            constraints, ret4, trace4 = constraint_agent.check_feasibility(top_action)
            agent_timeline.append({"agent": "ConstraintAgent", "time_ms": round((time.time() - t4) * 1000, 2), "retries": ret4, "reasoning_trace": trace4})

        # 6. SimulationAgent -> simulate top action
        t5 = time.time()
        simulation = {}
        if actions and len(actions) > 0:
            top_action = actions[0]
            simulation, ret5, trace5 = simulation_agent.simulate(top_action)
            agent_timeline.append({"agent": "SimulationAgent", "time_ms": round((time.time() - t5) * 1000, 2), "retries": ret5, "reasoning_trace": trace5})

        agent_timeline.append({"total_time_ms": round((time.time() - start_total) * 1000, 2)})

        return {
            "system_autonomy_score": calculate_autonomy_score(agent_timeline),
            "insights": insights,
            "actions": actions,
            "action_chain": action_chain,
            "constraints": constraints,
            "simulation": simulation,
            "agent_timeline": agent_timeline
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class AnalyzeUrlRequest(BaseModel):
    url: str

@app.post("/analyze-url")
async def analyze_url(request: AnalyzeUrlRequest):
    try:
        start_total = time.time()
        agent_timeline = []
        
        # 0. Fetch URL content
        t_fetch = time.time()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(request.url)
                response.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")
            
        soup = BeautifulSoup(response.text, "html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        extracted_text = soup.get_text(separator=' ')
        agent_timeline.append({"agent": "URLFetcher", "time_ms": round((time.time() - t_fetch) * 1000, 2), "retries": 0, "reasoning_trace": ["Extracted text from URL", "Cleaned HTML"]})

        # 1. IngestionAgent -> clean the text
        t0 = time.time()
        clean_text, ret0, trace0 = ingestion_agent.process(extracted_text)
        agent_timeline.append({"agent": "IngestionAgent", "time_ms": round((time.time() - t0) * 1000, 2), "retries": ret0, "reasoning_trace": trace0})

        # 2. InsightAgent -> get insights
        t1 = time.time()
        insights, ret1, trace1 = insight_agent.analyze(clean_text)
        agent_timeline.append({"agent": "InsightAgent", "time_ms": round((time.time() - t1) * 1000, 2), "retries": ret1, "reasoning_trace": trace1})

        # 3. ActionAgent -> get 3 actions
        t2 = time.time()
        actions, ret2, trace2 = action_agent.get_actions(insights)
        agent_timeline.append({"agent": "ActionAgent", "time_ms": round((time.time() - t2) * 1000, 2), "retries": ret2, "reasoning_trace": trace2})

        # 4. ChainAgent -> chain top action
        t3 = time.time()
        action_chain, ret3, trace3 = chain_agent.create_chain(insights, actions)
        agent_timeline.append({"agent": "ChainAgent", "time_ms": round((time.time() - t3) * 1000, 2), "retries": ret3, "reasoning_trace": trace3})

        # 5. ConstraintAgent -> check constraints
        t4 = time.time()
        constraints = {}
        if actions and len(actions) > 0:
            top_action = actions[0]
            constraints, ret4, trace4 = constraint_agent.check_feasibility(top_action)
            agent_timeline.append({"agent": "ConstraintAgent", "time_ms": round((time.time() - t4) * 1000, 2), "retries": ret4, "reasoning_trace": trace4})

        # 6. SimulationAgent -> simulate top action
        t5 = time.time()
        simulation = {}
        if actions and len(actions) > 0:
            top_action = actions[0]
            simulation, ret5, trace5 = simulation_agent.simulate(top_action)
            agent_timeline.append({"agent": "SimulationAgent", "time_ms": round((time.time() - t5) * 1000, 2), "retries": ret5, "reasoning_trace": trace5})

        agent_timeline.append({"total_time_ms": round((time.time() - start_total) * 1000, 2)})

        return {
            "system_autonomy_score": calculate_autonomy_score(agent_timeline),
            "insights": insights,
            "actions": actions,
            "action_chain": action_chain,
            "constraints": constraints,
            "simulation": simulation,
            "agent_timeline": agent_timeline
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class AnalyzeMultiRequest(BaseModel):
    sources: List[str]

@app.post("/analyze-multi")
async def analyze_multi(request: AnalyzeMultiRequest):
    try:
        start_total = time.time()
        agent_timeline = []
        
        # 0. ContradictionAgent -> check for conflicts
        t_conflict = time.time()
        contradiction_result, ret_c, trace_c = contradiction_agent.detect_contradictions(request.sources)
        agent_timeline.append({"agent": "ContradictionAgent", "time_ms": round((time.time() - t_conflict) * 1000, 2), "retries": ret_c, "reasoning_trace": trace_c})
        
        # Combine texts for downstream agents
        combined_text = "\\n\\n".join(request.sources)
        
        # 1. IngestionAgent -> clean the text
        t0 = time.time()
        clean_text, ret0, trace0 = ingestion_agent.process(combined_text)
        agent_timeline.append({"agent": "IngestionAgent", "time_ms": round((time.time() - t0) * 1000, 2), "retries": ret0, "reasoning_trace": trace0})

        # 2. InsightAgent -> get insights
        t1 = time.time()
        insights, ret1, trace1 = insight_agent.analyze(clean_text)
        agent_timeline.append({"agent": "InsightAgent", "time_ms": round((time.time() - t1) * 1000, 2), "retries": ret1, "reasoning_trace": trace1})

        # 3. ActionAgent -> get 3 actions
        t2 = time.time()
        actions, ret2, trace2 = action_agent.get_actions(insights)
        agent_timeline.append({"agent": "ActionAgent", "time_ms": round((time.time() - t2) * 1000, 2), "retries": ret2, "reasoning_trace": trace2})

        # 4. ChainAgent -> chain top action
        t3 = time.time()
        action_chain, ret3, trace3 = chain_agent.create_chain(insights, actions)
        agent_timeline.append({"agent": "ChainAgent", "time_ms": round((time.time() - t3) * 1000, 2), "retries": ret3, "reasoning_trace": trace3})

        # 5. ConstraintAgent -> check constraints
        t4 = time.time()
        constraints = {}
        if actions and len(actions) > 0:
            top_action = actions[0]
            constraints, ret4, trace4 = constraint_agent.check_feasibility(top_action)
            agent_timeline.append({"agent": "ConstraintAgent", "time_ms": round((time.time() - t4) * 1000, 2), "retries": ret4, "reasoning_trace": trace4})

        # 6. SimulationAgent -> simulate top action
        t5 = time.time()
        simulation = {}
        if actions and len(actions) > 0:
            top_action = actions[0]
            simulation, ret5, trace5 = simulation_agent.simulate(top_action)
            agent_timeline.append({"agent": "SimulationAgent", "time_ms": round((time.time() - t5) * 1000, 2), "retries": ret5, "reasoning_trace": trace5})

        agent_timeline.append({"total_time_ms": round((time.time() - start_total) * 1000, 2)})

        return {
            "system_autonomy_score": calculate_autonomy_score(agent_timeline),
            "contradiction_analysis": contradiction_result,
            "insights": insights,
            "actions": actions,
            "action_chain": action_chain,
            "constraints": constraints,
            "simulation": simulation,
            "agent_timeline": agent_timeline
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class AnalyzeCsvRequest(BaseModel):
    csv_data: str

@app.post("/analyze-csv")
async def analyze_csv(request: AnalyzeCsvRequest):
    try:
        start_total = time.time()
        agent_timeline = []
        
        # 0. TemporalAgent -> Analyze trends
        t_temp = time.time()
        temporal_analysis, ret_t, trace_t = temporal_agent.analyze_trend(request.csv_data)
        agent_timeline.append({"agent": "TemporalAgent", "time_ms": round((time.time() - t_temp) * 1000, 2), "retries": ret_t, "reasoning_trace": trace_t})
        
        # Generate insight text from temporal summary
        text_from_csv = f"Data Analysis Report: {temporal_analysis.get('summary', 'Data analyzed.')} The trend direction is {temporal_analysis.get('trend_direction', 'stable')} with a percentage change of {temporal_analysis.get('percentage_change', '0%')}. Forecast: {temporal_analysis.get('forecast', 'N/A')}."

        # 1. IngestionAgent -> clean the text
        t0 = time.time()
        clean_text, ret0, trace0 = ingestion_agent.process(text_from_csv)
        agent_timeline.append({"agent": "IngestionAgent", "time_ms": round((time.time() - t0) * 1000, 2), "retries": ret0, "reasoning_trace": trace0})

        # 2. InsightAgent -> get insights
        t1 = time.time()
        insights, ret1, trace1 = insight_agent.analyze(clean_text)
        agent_timeline.append({"agent": "InsightAgent", "time_ms": round((time.time() - t1) * 1000, 2), "retries": ret1, "reasoning_trace": trace1})

        # 3. ActionAgent -> get 3 actions
        t2 = time.time()
        actions, ret2, trace2 = action_agent.get_actions(insights)
        agent_timeline.append({"agent": "ActionAgent", "time_ms": round((time.time() - t2) * 1000, 2), "retries": ret2, "reasoning_trace": trace2})

        # 4. ChainAgent -> chain top action
        t3 = time.time()
        action_chain, ret3, trace3 = chain_agent.create_chain(insights, actions)
        agent_timeline.append({"agent": "ChainAgent", "time_ms": round((time.time() - t3) * 1000, 2), "retries": ret3, "reasoning_trace": trace3})

        # 5. ConstraintAgent -> check constraints
        t4 = time.time()
        constraints = {}
        if actions and len(actions) > 0:
            top_action = actions[0]
            constraints, ret4, trace4 = constraint_agent.check_feasibility(top_action)
            agent_timeline.append({"agent": "ConstraintAgent", "time_ms": round((time.time() - t4) * 1000, 2), "retries": ret4, "reasoning_trace": trace4})

        # 6. SimulationAgent -> simulate top action
        t5 = time.time()
        simulation = {}
        if actions and len(actions) > 0:
            top_action = actions[0]
            simulation, ret5, trace5 = simulation_agent.simulate(top_action)
            agent_timeline.append({"agent": "SimulationAgent", "time_ms": round((time.time() - t5) * 1000, 2), "retries": ret5, "reasoning_trace": trace5})

        agent_timeline.append({"total_time_ms": round((time.time() - start_total) * 1000, 2)})

        return {
            "system_autonomy_score": calculate_autonomy_score(agent_timeline),
            "temporal_analysis": temporal_analysis,
            "insights": insights,
            "actions": actions,
            "action_chain": action_chain,
            "constraints": constraints,
            "simulation": simulation,
            "agent_timeline": agent_timeline
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # Run on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
"""

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_main_code)

print("Updated main.py successfully.")
