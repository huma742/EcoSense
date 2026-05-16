# EconoSense PK 🇵🇰
### AI-Powered Pakistan Economy News Analysis System

## Problem Statement
Organizations in Pakistan are flooded with economic news but don't know what actions to take. Most AI systems only summarize — EconoSense PK goes further by generating actions and simulating outcomes.

## Solution
A 4-agent autonomous system that transforms unstructured economic news into actionable decisions.

## How It Works
1. User pastes news text / uploads PDF / enters URL
2. IngestionAgent cleans and preprocesses the text
3. InsightAgent extracts event, affected sectors, risk score (1-10)
4. ActionAgent generates 3 prioritized actions (HIGH/MED/LOW)
5. SimulationAgent simulates the top action with before/after state

## Tech Stack
- Frontend: Flutter (Mobile + Desktop)
- Backend: FastAPI (Python)
- AI: Google Gemini API (gemini-2.0-flash)
- IDE: Antigravity (AI-powered development)
- Libraries: google-genai, uvicorn, pydantic, httpx

## How Antigravity Was Used
- Generated all 4 agent classes in agents.py
- Built complete FastAPI backend in main.py
- Designed entire Flutter UI with all screens
- Fixed bugs and errors throughout development

## Project Structure
EconoSense-pk/
├── backend/
│   ├── agents.py        # 4 AI agents
│   ├── main.py          # FastAPI server
│   ├── requirements.txt
│   └── .env
├── econosense_app/      # Flutter app
└── README.md

## How To Run

### Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

### Flutter App
cd econosense_app
flutter run

## Screens
- Splash Screen
- Login / Signup
- Dashboard
- Analyze (Text / PDF / URL)
- Results (Insights, Actions, Simulation, Agent Timeline)
- Profile

## Team
EconoSense PK — Built for Google AI Hackathon 2026
