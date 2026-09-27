# Tectonic starter

Open [COMMAND.md](COMMAND.md) for the team plan and [PREPARATION.md](PREPARATION.md) for sources and brainstorming. This starter proves that a frontend can render structured assistant output from a mock API. It is a preparation exercise, not a claim about KBC's actual systems or the event challenge.

## Run

Backend (Python 3.10+):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python backend/app.py
```

Frontend (Node 20+), in another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Vite proxies `/api` to `http://localhost:5000`. Smoke check: `curl -s http://localhost:5000/api/health` and `curl -s -X POST http://localhost:5000/api/ask -H 'Content-Type: application/json' -d '{"message":"Show my spending","user_id":"demo"}'`.

Copy `.env.example` to `.env` only when a provider is actually selected. No key is needed for the mock. The API contract and role split live in `COMMAND.md`.

## Git remote

The shared repository is `git@github.com:541l0r/tectonic2026.git`. Clone it with `git clone git@github.com:541l0r/tectonic2026.git`. Work on a branch and use the local merge workflow in `COMMAND.md`; no pull request is needed. The original `.bundle` is a backup of the starter, not the shared remote.
