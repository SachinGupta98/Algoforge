# AlgoForge

AlgoForge is an AI-powered DSA learning platform focused on **Understand → Practice → Master**.

## What was missing and fixed
The repository had only a vision document and no runnable product. This scaffold now provides:
- A working **FastAPI backend** for roadmap, starter problems, AI coach, and Judge0 execution.
- A working **React frontend** with an amber/orange default UI.
- A practical **Phase 1 vs Phase 2** roadmap exposed by API and shown in UI.
- Secure environment templates (`.env.example`) without hardcoding secrets.

## Implemented MVP (Phase 1)
- Smart dashboard message + progress-ready shell.
- Starter Problem Bank endpoint and problem workspace.
- Code execution API proxy for Judge0.
- Logic AI Socratic coach endpoint (Groq if configured, fallback mentor mode otherwise).

## Phase 2 (explicitly included)
- Voice input coach mode.
- Hindi/regional language mode.
- Interview simulation mode.
- Pattern recognition engine.

## Tech Stack
- Frontend: React + TypeScript + Vite
- Backend: FastAPI + HTTPX + Pydantic Settings

## Project Structure
- `/frontend` → UI app
- `/backend` → API server

## Setup
### 1) Backend
```bash
cd /home/runner/work/Algoforge/Algoforge/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### 2) Frontend
```bash
cd /home/runner/work/Algoforge/Algoforge/frontend
npm install
cp .env.example .env
npm run dev
```

## Configuration
Use local `.env` files and fill keys there.

### Backend `.env`
- `GROQ_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `JUDGE0_RAPIDAPI_KEY`

> Security: API secrets are intentionally **not** hardcoded in source control.
