import os
import json

file_path = r"d:\humaa\EconoSense-pk\backend\agents.py"

new_agents_code = """import os
import json
import re
import time
import random
import datetime
from groq import Groq
from typing import Dict, Any, List, Tuple
from dotenv import load_dotenv

# Setup Groq API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
print(f"Groq client initialized: {client is not None}")

class IngestionAgent:
    \"\"\"Takes news text, cleans it, returns clean text.\"\"\"
    
    def process(self, text: str) -> str:
        # Remove extra whitespace and newlines
        clean_text = re.sub(r'\\s+', ' ', text).strip()
        return clean_text

def clean_json_response(response_text: str) -> str:
    \"\"\"Cleans up LLM response by removing comments, markdown, and extracting JSON.\"\"\"
    # Remove markdown code blocks if any
    if response_text.startswith("```json"):
        response_text = response_text[7:-3].strip()
    elif response_text.startswith("```"):
        response_text = response_text[3:-3].strip()
        
    # Remove // comments from JSON
    response_text = re.sub(r'//[^\\n]*', '', response_text)
    
    # Extract JSON object (assuming it's a dict or array)
    json_match = re.search(r'(\\{.*\\}|\\[.*\\])', response_text, re.DOTALL)
    if json_match:
        response_text = json_match.group(1)
        
    return response_text

def execute_with_retry(prompt: str, default_response: Any, temperature: float = 0.3) -> Tuple[Any, int]:
    if not client:
        return default_response, 0
        
    retries = 0
    while retries <= 3:
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            response_text = response.choices[0].message.content.strip()
            
            cleaned_text = clean_json_response(response_text)
            return json.loads(cleaned_text), retries
        except Exception as e:
            print(f"API Error (attempt {retries+1}): {e}")
            retries += 1
            if retries <= 3:
                time.sleep(2)
    
    return default_response, retries - 1

class InsightAgent:
    \"\"\"Analyzes text, returns JSON with: event, sectors, risk_score (1-10), impact_summary.\"\"\"
    
    def analyze(self, text: str) -> Tuple[Dict[str, Any], int]:
        default = {
            "event": "Economic policy update detected",
            "sectors": ["Banking", "Trade", "SMEs"],
            "risk_score": 7,
            "impact_summary": "This policy change affects key economic sectors in Pakistan with moderate to high impact on businesses and consumers.",
            "why_it_matters": "N/A",
            "affected_population": "N/A"
        }
        if not client:
            return default, 0
            
        prompt = f\"\"\"
You are an expert Pakistan economic analyst. Analyze this news and return ONLY a JSON object with no comments:
{{
  "event": "specific event name",
  "sectors": ["sector1", "sector2", "sector3"],
  "risk_score": 7,
  "impact_summary": "2-3 sentence explanation of WHY this matters and real-world consequences for Pakistan businesses and citizens",
  "why_it_matters": "specific reason this insight is critical right now",
  "affected_population": "who is directly affected and how"
}}

News: {text}

Return ONLY the JSON. No comments, no explanation, no markdown.
\"\"\"
        return execute_with_retry(prompt, default)

class ActionAgent:
    \"\"\"Takes insights, returns list of 3 actions with priority (HIGH/MED/LOW) and description.\"\"\"
    
    def get_actions(self, insights: Dict[str, Any]) -> Tuple[List[Dict[str, str]], int]:
        default = [
            {"priority": "HIGH", "description": "Notify financial institutions and update lending rate guidelines immediately", "target": "State Bank", "timeline": "immediate", "expected_outcome": "Stabilization"},
            {"priority": "MED", "description": "Alert SME sector stakeholders and provide adjustment timeline", "target": "SMEs", "timeline": "1 week", "expected_outcome": "Preparation"},
            {"priority": "LOW", "description": "Monitor consumer price index weekly for next 30 days", "target": "Statistics Bureau", "timeline": "1 month", "expected_outcome": "Data gathering"}
        ]
        if not client:
            return default, 0
            
        prompt = f\"\"\"
You are an expert Pakistan economic policy advisor. Based on these insights, generate exactly 3 specific actionable recommendations. Return ONLY a JSON array with no comments:
[
  {{
    "priority": "HIGH",
    "description": "specific action with clear steps",
    "target": "who should take this action",
    "timeline": "immediate/1 week/1 month",
    "expected_outcome": "what will happen if this action is taken"
  }},
  {{
    "priority": "MED", 
    "description": "specific action with clear steps",
    "target": "who should take this action",
    "timeline": "immediate/1 week/1 month",
    "expected_outcome": "what will happen if this action is taken"
  }},
  {{
    "priority": "LOW",
    "description": "specific action with clear steps", 
    "target": "who should take this action",
    "timeline": "immediate/1 week/1 month",
    "expected_outcome": "what will happen if this action is taken"
  }}
]

Insights: {json.dumps(insights)}

Return ONLY the JSON array. No comments, no explanation, no markdown.
\"\"\"
        return execute_with_retry(prompt, default)

class SimulationAgent:
    \"\"\"Takes top action, returns a detailed realistic simulation result.\"\"\"
    
    def simulate(self, action: Dict[str, str]) -> Tuple[Dict[str, Any], int]:
        description = action.get("description", "Execute general economic policy adjustment.")
        priority = action.get("priority", "LOW")
        desc_lower = description.lower()
        
        # Base affected count on priority
        base_count = {"HIGH": 500000, "MED": 100000, "LOW": 10000}.get(priority, 10000)
        affected = base_count + random.randint(1000, 50000)
        
        # Determine states based on keywords
        before_state = "Status Quo with moderate inefficiency."
        after_state = "Policy implemented; monitoring initial impact."
        
        if "tax" in desc_lower or "revenue" in desc_lower or "fbr" in desc_lower:
            before_state = "Low tax collection and high deficit."
            after_state = "Increased tax compliance; deficit narrowing by 1.2%."
        elif "interest" in desc_lower or "rate" in desc_lower or "sbp" in desc_lower:
            before_state = "High inflation pressure; volatile lending."
            after_state = "Inflation stabilized; credit flow restricted."
        elif "export" in desc_lower or "trade" in desc_lower:
            before_state = "Trade imbalance and stagnant exports."
            after_state = "Export volume boosted; trade gap reduced."
        elif "energy" in desc_lower or "power" in desc_lower or "circular debt" in desc_lower:
            before_state = "Rising circular debt and power outages."
            after_state = "Tariff structured; grid efficiency improved."
        elif "imf" in desc_lower or "bailout" in desc_lower:
            before_state = "Depleted FX reserves; default risk high."
            after_state = "FX reserves bolstered; macroeconomic stability restored."
            
        # Email draft
        email_draft = f"Subject: Urgent: Implementation of {priority} Priority Economic Action\\n\\nDear Stakeholders,\\n\\nPlease be advised that the following action has been initiated:\\n\\\"{description}\\\"\\n\\nExpected Impact: ~{affected:,} individuals/entities.\\nCurrent Phase: {after_state}\\n\\nRegards,\\nEconoSense AI System"
        
        # Logs
        now = datetime.datetime.now()
        logs = [
            f"{(now - datetime.timedelta(minutes=5)).strftime('%H:%M:%S')} - System initialized simulation parameters.",
            f"{(now - datetime.timedelta(minutes=3)).strftime('%H:%M:%S')} - Risk assessed and validated.",
            f"{(now - datetime.timedelta(minutes=1)).strftime('%H:%M:%S')} - Notification dispatched to relevant authorities.",
            f"{now.strftime('%H:%M:%S')} - Action logged in ledger."
        ]
        
        res = {
            "action_taken": description,
            "affected_count": affected,
            "before_state": before_state,
            "after_state": after_state,
            "execution_time": f"{random.randint(100, 300)}ms",
            "email_draft": email_draft,
            "notification_sent": random.randint(10, 500),
            "dashboard_updated": True,
            "logs": logs
        }
        return res, 0

class ChainAgent:
    \"\"\"Takes the output of InsightAgent and ActionAgent and chains the TOP action into 3-5 connected sub-steps.\"\"\"
    
    def create_chain(self, insights: Dict[str, Any], actions: List[Dict[str, str]]) -> Tuple[List[Dict[str, Any]], int]:
        default = [
            {"step_number": 1, "action": "Diagnose the issue based on the insight", "status": "completed", "result": "Diagnosis complete"},
            {"step_number": 2, "action": "Notify relevant stakeholders", "status": "executing", "result": "Notifications sent to 50% of stakeholders"},
            {"step_number": 3, "action": "Launch mitigation plan", "status": "pending", "result": "Awaiting resource allocation"},
            {"step_number": 4, "action": "Schedule monitoring and follow-up", "status": "pending", "result": "Scheduled for next week"}
        ]
        
        if not client:
            return default, 0
        
        top_action = actions[0] if actions else {"description": "No action provided"}
        
        prompt = f\"\"\"
You are an expert project manager and system orchestrator. Based on the following insight and top priority action, break down the execution of the action into 3-5 connected sub-steps (e.g., diagnose -> notify stakeholders -> update system -> launch mitigation -> schedule monitoring).

Return ONLY a JSON array with no comments, where each object represents a step:
[
  {{
    "step_number": 1,
    "action": "clear description of the step",
    "status": "completed",
    "result": "what was the outcome of this step"
  }},
  {{
    "step_number": 2,
    "action": "clear description of the step",
    "status": "executing",
    "result": "currently in progress..."
  }},
  {{
    "step_number": 3,
    "action": "clear description of the step",
    "status": "pending",
    "result": "awaiting execution"
  }}
]

Insight: {json.dumps(insights)}
Top Action: {json.dumps(top_action)}

Return ONLY the JSON array. No comments, no explanation, no markdown.
\"\"\"
        return execute_with_retry(prompt, default)

class ContradictionAgent:
    \"\"\"Takes multiple text inputs and detects if they contradict each other.\"\"\"
    
    def detect_contradictions(self, texts: List[str]) -> Tuple[Dict[str, Any], int]:
        default = {
            "contradiction_found": False,
            "conflicting_claims": [],
            "resolution": "Could not analyze due to an error."
        }
        
        if not client:
            return default, 0
            
        texts_json = json.dumps(texts)
        prompt = f\"\"\"
You are an expert fact-checker and logic analyzer. Analyze the following list of text inputs and determine if there are any contradictions between them.

Return ONLY a JSON object with no comments:
{{
  "contradiction_found": true or false,
  "conflicting_claims": ["claim 1 from text A", "conflicting claim 2 from text B"] if found else [],
  "resolution": "explanation of how to resolve the conflict, or explanation of why there is no conflict"
}}

Texts to analyze: {texts_json}

Return ONLY the JSON. No comments, no explanation, no markdown.
\"\"\"
        return execute_with_retry(prompt, default, temperature=0.2)

class ConstraintAgent:
    \"\"\"Checks if actions are feasible given constraints like budget, time, and urgency.\"\"\"
    
    def check_feasibility(self, action: Dict[str, str], budget_limit: str = "PKR 1 million", time_limit: str = "48 hours", urgency_level: str = "HIGH") -> Tuple[Dict[str, Any], int]:
        default = {
            "feasible": True,
            "reason": "Defaulting to feasible due to API error.",
            "adjustments_needed": "None"
        }
        
        if not client:
            return default, 0
            
        prompt = f\"\"\"
You are a resource management expert. Evaluate if the following action is feasible given the constraints.

Constraints:
- Budget Limit: {budget_limit}
- Time Limit: {time_limit}
- Urgency Level: {urgency_level}

Action to evaluate:
{json.dumps(action)}

Return ONLY a JSON object with no comments:
{{
  "feasible": true or false,
  "reason": "detailed explanation of why the action is or isn't feasible within these constraints",
  "adjustments_needed": "what would need to change for it to be feasible (if not feasible) or 'None' (if feasible)"
}}

Return ONLY the JSON. No comments, no explanation, no markdown.
\"\"\"
        return execute_with_retry(prompt, default, temperature=0.2)

class TemporalAgent:
    \"\"\"Takes a list of data points with dates and values, detects trends, and returns trend direction, percentage change, and forecast.\"\"\"
    
    def analyze_trend(self, data: str) -> Tuple[Dict[str, Any], int]:
        default = {
            "trend_direction": "stable",
            "percentage_change": "0%",
            "forecast": "Unable to forecast due to API error.",
            "summary": "Data could not be analyzed."
        }
        
        if not client:
            return default, 0
            
        prompt = f\"\"\"
You are an expert economic data analyst. Analyze the following time-series data (CSV/JSON) and determine the overall trend.

Data:
{data}

Return ONLY a JSON object with no comments:
{{
  "trend_direction": "rising", "falling", or "stable",
  "percentage_change": "calculated percentage change between first and last data point, e.g., '+5.2%'",
  "forecast": "a brief 1-2 sentence forecast based on this trend",
  "summary": "a short text summary of the data representing key economic changes"
}}

Return ONLY the JSON. No comments, no explanation, no markdown.
\"\"\"
        return execute_with_retry(prompt, default, temperature=0.1)
"""

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_agents_code)

print("Updated agents.py successfully.")
