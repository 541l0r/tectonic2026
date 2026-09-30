# Tectonic starter

Open [COMMAND.md](COMMAND.md) for the team working method; [IDEATION_METHOD.md](docs/IDEATION_METHOD.md) for the opening idea-to-concept process; [IDEAS.md](docs/IDEAS.md) for research leads, innovation lenses, and rehearsal ideas; [PREPARATION.md](PREPARATION.md) for before-event tasks and the working Trusted AI checklist; and [WORKFLOW_TEMPLATE.md](WORKFLOW_TEMPLATE.md) for the fillable day-of guide. This starter proves that a frontend can render structured assistant output from a mock API. It is a preparation exercise, not a claim about KBC's actual systems or the event challenge.

## Run

Backend (Python 3.10+), PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r backend/requirements.txt
.\.venv\Scripts\python backend/app.py
```

On macOS/Linux:

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

Copy `.env.example` to `.env` only when a provider is actually selected. No key is needed for the current connectivity check. The team roles and method for agreeing on an MVP interface live in `COMMAND.md`.


## Docker

### Production

```bash
gcloud auth login

gcloud config set project YOUR_PROJECT_ID

gcloud services enable run.googleapis.com cloudbuild.googleapis.com

gcloud run deploy my-app \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated

gcloud run services update my-app   --region=europe-west1   --add-cloudsql-instances=hackaton-tectonic:europe-west1:hackaton-db   --update-env-vars DB_USER="hackaton-user",DB_PASS="TcEi@1983.pw",DB_NAME="hackaton",INSTANCE_CONNECTION_NAME="hackaton-tectonic:europe-west1:hackaton-db",APP_ENV="production"
```

```bash
docker compose up -d
```

## Git remote

The shared repository is `git@github.com:541l0r/tectonic2026.git`. Clone it with `git clone git@github.com:541l0r/tectonic2026.git`. Work on a branch and use the local merge workflow in `COMMAND.md`; no pull request is needed. The original `.bundle` is a backup of the starter, not the shared remote.
