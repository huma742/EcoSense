# EconoSense PK 🇵🇰
Autonomous Content-to-Action Agent System
Built for Google Antigravity Hackathon 2026

## One Line Pitch
EconoSense PK transforms Pakistan economy news into autonomous multi-step actions using 8 AI agents — organizations don't just read the news, they respond to it intelligently.

## Architecture Overview
**INPUT SOURCES (6 types)**
Text → URL → PDF → Multi-Source → CSV/JSON → Real-time Feed
                        ↓
                ANTIGRAVITY ORCHESTRATOR
                        ↓
        ┌───────────────────────────────┐
        │         8 AGENT PIPELINE      │
        │  1. IngestionAgent            │
        │  2. InsightAgent              │
        │  3. ActionAgent               │
        │  4. ChainAgent                │
        │  5. ConstraintAgent           │
        │  6. ContradictionAgent        │
        │  7. SimulationAgent           │
        │  8. TemporalAgent             │
        └───────────────────────────────┘
                        ↓
             AUTONOMOUS OUTPUT
        Insights → Chained Actions → Simulation → Dashboard

## Problem Statement
Organizations in Pakistan are flooded with economic news but don't know what actions to take. Most AI systems only summarize. EconoSense PK goes further — it autonomously ingests content, extracts insights, generates chained actions, checks constraints, detects contradictions, and simulates outcomes.

## How Antigravity Was Used (CENTRAL ROLE)
Antigravity was not just a coding tool — it was the CENTRAL ORCHESTRATOR of this entire system:
* Designed and built all 8 agent classes autonomously
* Created the entire FastAPI backend with multi-endpoint routing
* Built the complete Flutter mobile app with 6 input tabs
* Debugged Android build issues autonomously
* Planned and executed the full agentic pipeline architecture
* Generated reasoning traces for each agent decision
* All agent workplans, task plans and decision flows were created by Antigravity

## 8 Agents Explained
| Agent | Role | Input | Output |
| :--- | :--- | :--- | :--- |
| **IngestionAgent** | Cleans and preprocesses raw input | Raw text | Clean text |
| **InsightAgent** | Extracts event, sectors, risk score | Clean text | Structured insights |
| **ActionAgent** | Generates 3 prioritized actions | Insights | HIGH/MED/LOW actions |
| **ChainAgent** | Chains top action into 3-5 steps | Top action | Connected action chain |
| **ConstraintAgent** | Checks budget/time feasibility | Actions | FEASIBLE/INFEASIBLE |
| **ContradictionAgent** | Detects conflicts across sources | Multiple texts | Contradiction report |
| **TemporalAgent** | Analyzes trends over time | CSV/time data | Trend + forecast |
| **SimulationAgent** | Simulates before/after state | Actions | Simulation results |

## 6 Input Types
* **Text** — paste any news article or report
* **URL** — fetch content from any webpage
* **PDF** — upload PDF documents
* **Multi-Source** — analyze 2-3 sources simultaneously with contradiction detection
* **CSV/JSON** — upload structured data for temporal analysis
* **Real-time Feed** — simulated live Pakistan economy news feed

## Tech Stack
| Component | Technology |
| :--- | :--- |
| **Mobile App** | Flutter (Android) |
| **Backend** | FastAPI (Python) |
| **AI Model** | Groq API (llama-3.1-8b-instant) |
| **Orchestrator** | Google Antigravity |
| **PDF Parsing** | Syncfusion Flutter PDF |
| **Storage** | SharedPreferences |
| **HTTP** | httpx, BeautifulSoup4 |

## Agentic Workflow
User Input
    ↓
IngestionAgent → cleans text
    ↓
InsightAgent → extracts insights (autonomous reasoning)
    ↓
ActionAgent → generates actions (constraint-aware)
    ↓
ChainAgent → chains top action into steps (autonomous)
    ↓
ConstraintAgent → validates feasibility (budget/time)
    ↓
SimulationAgent → simulates outcome (before/after)
    ↓
Dashboard Updated → action saved → notification sent

## Evaluation Criteria Mapping
| Criteria | Weight | How We Meet It |
| :--- | :--- | :--- |
| **Antigravity Integration** | 25% | Antigravity built all 8 agents, entire backend, full Flutter UI, debugged all issues |
| **Agentic Reasoning** | 20% | 8-agent autonomous pipeline with reasoning traces and decision logs |
| **Insight Quality** | 20% | Real AI insights with Why It Matters, Affected Population, Risk Score |
| **Action Simulation** | 15% | ChainAgent + SimulationAgent with before/after state |
| **Robustness** | 15% | Retry logic, fallback data, contradiction detection, constraint checking |
| **Innovation & UX** | 10% | Professional mobile UI, 6 input types, autonomy score, temporal analysis |

## Key Features
✅ Autonomous 8-agent pipeline  
✅ Contradiction detection across multiple sources  
✅ Constraint-based decision making (budget/time/urgency)  
✅ Temporal trend analysis with forecasting  
✅ Chained action execution (3-5 connected steps)  
✅ Failure recovery with 3x retry logic  
✅ System autonomy score (0-100%)  
✅ Antigravity reasoning trace display  
✅ Real-time feed simulation  
✅ Before/After state visualization  

## How To Run

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Flutter App
```bash
cd econosense_app
flutter pub get
flutter run
```

## Assumptions & Limitations
* Backend requires active internet for Groq API calls
* URL scraping works for sites that allow public access
* Simulation uses statistical modeling (not real government data)
* Real-time feed uses simulated Pakistan economy headlines

## Team
**EconoSense PK** — Built for Google Antigravity Hackathon 2026
*Developed entirely using Google Antigravity as the central AI orchestrator*
