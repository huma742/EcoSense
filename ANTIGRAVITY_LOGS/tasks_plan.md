## Workplan — Antigravity Reasoning & Planning
### Problem Analysis
- Organizations flooded with Pakistan economic news but no system to act on it
- Existing tools only summarize — no action taken autonomously
- Need: system that ingests → understands → decides → acts → shows outcome
### Architecture Decision
- Flutter mobile app for cross-platform UI
- FastAPI Python backend for agent orchestration
- Groq LLM for fast inference
- 8 specialized agents each handling one responsibility
### Agent Design Reasoning
- IngestionAgent: clean raw input before processing
- InsightAgent: extract meaningful Pakistan-specific economic signals
- ActionAgent: generate realistic domain-relevant recommendations
- ChainAgent: chain top action into 3-5 autonomous steps
- ConstraintAgent: validate feasibility against budget/time limits
- ContradictionAgent: detect conflicts across multiple sources
- TemporalAgent: analyze trends over time from CSV data
- SimulationAgent: simulate before/after state change
### Tool Selection Reasoning
- Groq chosen for speed and reliability
- Flutter chosen for cross-platform mobile + desktop
- FastAPI chosen for async Python performance
- Firebase for real-time sync
### Execution Plan
- Phase 1: Core agents + basic UI
- Phase 2: Advanced features — contradiction, temporal, constraints
- Phase 3: Polish — autonomy score, trace terminal, JSON logs

# EconoSense PK — Antigravity Tasks Plan

## Advanced Features Implementation
- [x] Add execute_with_retry helper to agents.py
- [x] Update all agents with retry logic and return retry counts
- [x] Add TemporalAgent to agents.py
- [x] Update main.py to handle retry counts in agent_timeline
- [x] Add /analyze-csv endpoint to main.py
- [x] Update Flutter UI to 6 tabs (Text, URL, PDF, Multi-Source, CSV/JSON, Real-time Feed)
- [x] Implement CSV tab and _analyzeCsv function
- [x] Implement Real-time Feed tab with simulation logic
- [x] Update ResultsScreen with Temporal Analysis trend chart
- [x] Add ChainAgent for autonomous action chaining
- [x] Add ContradictionAgent for multi-source conflict detection
- [x] Add ConstraintAgent for budget/time feasibility checking
- [x] Add Antigravity Trace Terminal in Flutter UI
- [x] Add System Autonomy Score badge
- [x] Add Retry Warning cards
- [x] Update README with full documentation
