# EconoSense PK Advanced Features Task List

- [x] Modify `backend/agents.py` to add `execute_with_retry` helper.
- [x] Update all agents in `backend/agents.py` to use retry logic and return retry counts.
- [x] Add `TemporalAgent` to `backend/agents.py`.
- [x] Update `backend/main.py` to handle retry counts in `agent_timeline`.
- [x] Add `/analyze-csv` endpoint to `backend/main.py`.
- [x] Create Python script to update `econosense_app/lib/main.dart`.
- [x] Update Tabs in Flutter UI to 6 tabs (Text, URL, PDF, Multi-Source, CSV/JSON, Real-time Feed).
- [x] Implement `_buildCsvTab` and `_analyzeCsv` in Flutter UI.
- [x] Implement `_buildFeedTab` and real-time feed simulation logic in Flutter UI.
- [x] Update `ResultsScreen` in Flutter UI to display Temporal Analysis trend chart.
- [x] Verify functionality.
