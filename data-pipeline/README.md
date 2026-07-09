# ASAK Data Pipeline

This folder owns data collection, processing, and phase pipeline outputs.

## Scope

- `phase1/`: first-phase crawling and processing pipeline
- `phase1/output/`: generated phase 1 JSON outputs
- `phase1/db/`: database schema/reference SQL for the phase 1 data work

## Repository Boundary

- Keep pipeline code and generated phase outputs here.
- Keep canonical seed JSON in `../asak-data/seed/`.
- Keep canonical menu images in `../asak-data/images/menu/`.
- Do not copy pipeline data into `../frontend/` or `../backend/`; those projects read from root-level data folders when needed.

## Run

```powershell
cd data-pipeline\phase1
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_phase1.py
```
