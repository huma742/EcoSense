# Add Advanced Features to EconoSense PK

This plan outlines the addition of several advanced features including a TemporalAgent, retry logic across all API-calling agents, new CSV/JSON and Real-time Feed tabs, and an updated backend to support these workflows.

## Proposed Changes

### Backend: `backend/agents.py`
We will introduce an API retry mechanism and a new `TemporalAgent` to analyze trends over time.

#### [MODIFY] agents.py
- **Retry Logic**: Update the methods to implement retry logic internally. The logic will catch exceptions from the Groq API, log the failure, wait 2 seconds, and retry up to 3 times. If all retries fail, it falls back to the default response. We will implement this directly in the methods `analyze`, `get_actions`, `create_chain`, `detect_contradictions`, and `check_feasibility`. Note: decorators might make returning specific fallbacks tricky without passing the fallback into the decorator, so we will use a helper function or inline the retry loop.
- **TemporalAgent**: Add a new class `TemporalAgent` with an `analyze_trend(self, data: str) -> Dict[str, Any]` method. It will prompt the LLM to detect trends (rising/falling/stable), calculate percentage change (if applicable), and provide a forecast based on the CSV/JSON data.

### Backend: `backend/main.py`
We need to update the pipeline to pass retry attempts to the client and add a new endpoint for CSV data.

#### [MODIFY] main.py
- **Agent Initialization**: Import and instantiate `TemporalAgent`.
- **`/analyze-csv` Endpoint**: Add a POST endpoint that takes `{"csv_data": "..."}`.
  1. Runs `TemporalAgent` on the CSV data.
  2. Runs the standard 6 agents on the CSV data.
  3. Returns the results along with a new `temporal_analysis` field.
- **Agent Timeline update**: Because the retries are internal to the agents, we will track retries inside the agents and update them to return `retries` as part of their response payload or we can just track the overall time. Actually, the prompt says: "Update agent_timeline in all responses to include retry attempts if any occurred". This means the agents need to return `retries_used` along with their standard output, or we wrap the agent calls in `main.py` to handle the retry logic there!
Wait, if `main.py` handles the retries, it's easier to track `agent_timeline`. But the prompt says "Add retry logic to ALL agents...". I will modify the agents to return a tuple `(result, retries)` or update an internal variable. I'll use a `call_with_retry` helper inside `agents.py` that returns `(result, retries)`.

### Frontend: `econosense_app/lib/main.dart`
The Flutter UI will be expanded with new tabs and a new visual component for temporal analysis.

#### [MODIFY] main.dart
- **Tabs Update**: Change the Analyze Screen to have 6 tabs: `Text`, `URL`, `PDF`, `Multi-Source`, `CSV/JSON`, `Real-time Feed`.
- **CSV/JSON Tab**: A text area to paste CSV/JSON data with a "Load Sample CSV" button (filling `date,sector,value\n2024-01,Banking,8.5\n...`). An "Analyze Data" button will hit `/analyze-csv`.
- **Real-time Feed Tab**: Simulate a live feed using a `Timer.periodic` every 30 seconds that adds new Pakistan economy news headlines. An "Analyze Feed" button will join these headlines and send them to `/analyze-multi`.
- **Temporal Analysis Section**: In `ResultsScreen`, if `temporal_analysis` exists, display a trend chart (a simple `Row` of colored vertical bars or icons) showing risk/trend direction, along with the percentage change and forecast returned by the `TemporalAgent`.

## Verification Plan

### Automated Tests
- No formal automated tests exist, but we will manually verify the Python script syntax and backend startup via `uvicorn`.

### Manual Verification
- Test all API endpoints (`/analyze`, `/analyze-multi`, `/analyze-csv`) with valid and invalid data to ensure the retry logic acts as expected and falls back securely.
- Ensure the Flutter app loads all tabs and the "Sample CSV" fills correctly.
- Verify the `ResultsScreen` displays the Temporal Analysis section with colored trend indicators without throwing layout errors.
