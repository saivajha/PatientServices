# AGENTS.md

## Cursor Cloud specific instructions

### Overview
NaturoSage is a homeopathy assistant with two parallel frontends:
1. **Streamlit app** (primary, port 8501) — full-featured with Constitution Detector, Symptom Checker, Diagnosis, Prescription, AI Chat, Materia Medica
2. **Express.js server** (secondary, port 3000) — REST API + HTML frontend with AI chat

Both work in **demo mode** without any API keys. Set `OPENAI_API_KEY` env var for real GPT-4 responses.

### Running services

**Streamlit (primary):**
```
export PATH="$HOME/.local/bin:$PATH"
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
```

**Express (secondary):**
```
node server.js
```
Requires a `.env` file — copy from `env.example` and set `JWT_SECRET` to any value.

### Gotchas
- `streamlit` binary installs to `~/.local/bin` which may not be on PATH — always `export PATH="$HOME/.local/bin:$PATH"` before running.
- Express route handlers use class methods. Routes in `routes/*.js` use arrow-function wrappers to preserve `this` context — do not revert to bare `aiController.generateResponse` style.
- The app has no database, no Docker, no external service dependencies. All data is in-memory demo data.
- No lint or test frameworks are configured in this repository.

### Standard commands
See `README.md` for full setup and usage instructions. Key scripts from `package.json`:
- `npm start` / `npm run dev` — run Express server
- `pip install -r requirements.txt` — install Python deps
- `npm install` — install Node deps
