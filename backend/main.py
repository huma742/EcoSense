import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import httpx
from bs4 import BeautifulSoup

# Import our AI Agents
from agents import IngestionAgent, InsightAgent, ActionAgent, SimulationAgent

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

# Initialize the 4 agents
ingestion_agent = IngestionAgent()
insight_agent = InsightAgent()
action_agent = ActionAgent()
simulation_agent = SimulationAgent()

# Define the request body schema
class AnalyzeRequest(BaseModel):
    news_text: str

@app.post("/analyze")
async def analyze_news(request: AnalyzeRequest):
    try:
        start_total = time.time()
        agent_trace = []

        # 1. IngestionAgent -> clean the text
        t0 = time.time()
        clean_text = ingestion_agent.process(request.news_text)
        agent_trace.append({"agent": "IngestionAgent", "time_ms": round((time.time() - t0) * 1000, 2)})

        # 2. InsightAgent -> get insights
        t1 = time.time()
        insights = insight_agent.analyze(clean_text)
        agent_trace.append({"agent": "InsightAgent", "time_ms": round((time.time() - t1) * 1000, 2)})

        # 3. ActionAgent -> get 3 actions
        t2 = time.time()
        actions = action_agent.get_actions(insights)
        agent_trace.append({"agent": "ActionAgent", "time_ms": round((time.time() - t2) * 1000, 2)})

        # 4. SimulationAgent -> simulate top action
        t3 = time.time()
        simulation = {}
        if actions and len(actions) > 0:
            top_action = actions[0]  # Assuming the first action is the highest priority
            simulation = simulation_agent.simulate(top_action)
        agent_trace.append({"agent": "SimulationAgent", "time_ms": round((time.time() - t3) * 1000, 2)})

        agent_trace.append({"total_time_ms": round((time.time() - start_total) * 1000, 2)})

        # Return all results as JSON
        return {
            "clean_text": clean_text,
            "insights": insights,
            "actions": actions,
            "simulation": simulation,
            "agent_trace": agent_trace
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class AnalyzeUrlRequest(BaseModel):
    url: str

@app.post("/analyze-url")
async def analyze_url(request: AnalyzeUrlRequest):
    try:
        start_total = time.time()
        agent_trace = []
        
        # 0. Fetch URL content
        t_fetch = time.time()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(request.url)
                response.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")
            
        soup = BeautifulSoup(response.text, "html.parser")
        # Basic string cleaning: remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        extracted_text = soup.get_text(separator=' ')
        agent_trace.append({"agent": "URLFetcher", "time_ms": round((time.time() - t_fetch) * 1000, 2)})

        # 1. IngestionAgent -> clean the text
        t0 = time.time()
        clean_text = ingestion_agent.process(extracted_text)
        agent_trace.append({"agent": "IngestionAgent", "time_ms": round((time.time() - t0) * 1000, 2)})

        # 2. InsightAgent -> get insights
        t1 = time.time()
        insights = insight_agent.analyze(clean_text)
        agent_trace.append({"agent": "InsightAgent", "time_ms": round((time.time() - t1) * 1000, 2)})

        # 3. ActionAgent -> get 3 actions
        t2 = time.time()
        actions = action_agent.get_actions(insights)
        agent_trace.append({"agent": "ActionAgent", "time_ms": round((time.time() - t2) * 1000, 2)})

        # 4. SimulationAgent -> simulate top action
        t3 = time.time()
        simulation = {}
        if actions and len(actions) > 0:
            top_action = actions[0]
            simulation = simulation_agent.simulate(top_action)
        agent_trace.append({"agent": "SimulationAgent", "time_ms": round((time.time() - t3) * 1000, 2)})

        agent_trace.append({"total_time_ms": round((time.time() - start_total) * 1000, 2)})

        # Return all results as JSON
        return {
            "clean_text": clean_text,
            "insights": insights,
            "actions": actions,
            "simulation": simulation,
            "agent_trace": agent_trace
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
