# KBC Future

A personal financial digital twin that forecasts cash flow and validates personalised spending and savings proposals.

- [Project description](KBC_FUTURE_PROJECT_DESCRIPTION.md)
- [Algorithm in one page](KBC_FUTURE_ALGORITHM.md)
- [Two-minute video script](KBC_FUTURE_VIDEO_SCRIPT.md)
- [Backend integration guide](docs/DAMIENS_START_HERE.md) and [team next tasks](docs/TEAM_NEXT_TASKS.md)

Earlier preparation documents are kept in [docs/](docs/).

## What deployment includes

The Dockerfile builds React/Vite, then serves the frontend and Flask API together through Gunicorn on **port 8080**. MySQL runs separately: Docker Compose locally, Cloud SQL on Google Cloud.

**Current limitation:** the tested algorithm is in `backend/future_engine.py`, but `/api/ask` still returns a static mock. Deployment does not connect `future()` to the UI, add an LLM, or implement customer authentication. Follow the integration guide for that work. Use synthetic data only.

## 1. Run locally with Docker

Install and start Docker with Compose. Run from the repository root:

```bash
docker compose up -d --build
docker compose ps
curl --fail http://localhost:8080/api/health
curl --fail http://localhost:8080/db-test
```

Open **http://localhost:8080**. Expect `status: "ok"` and `database: "ok"`. Health alone does not verify database access.

On a **new, empty MySQL volume**, Compose loads `sql/schema.sql`: three synthetic customers and 389 transactions. Local database: `app_dev`; development-only credentials: `app` / `app`. Do not expose this Compose setup or its MySQL port to the internet.

For an **existing database**, back it up, then run the repeatable migration:

```bash
docker compose exec -T -e MYSQL_PWD=app mysql mysql -uapp app_dev < sql/migrations/001_customer_product_ownership.sql
```

This preserves records, renames the legacy ownership table if needed, and rejects mismatched customer/product records. Do not rerun the full seed against populated tables, use `mysql --force`, or run `docker compose down -v`: deleting the volume deletes the database.

Check one customer's real forecast independently of the mock API (requires host Python 3.9+):

```bash
python3 scripts/future_demo_data.py --database --customer-id 1001
```

Choose `1001` for Alex, `1002` for Sam or `1003` for Robin. Each call requires an ID and returns one customer only.

Logs: `docker compose logs --tail=100 flask mysql`. Stop without deleting data: `docker compose stop`.

## 2. Deploy to Google Cloud Run

These commands deploy a **private demo**, not a production-ready banking system. Cloud resources can incur charges. Use Bash/zsh or Google Cloud Shell from the repository root.

### Prepare the project

Install the Google Cloud CLI and select a billing-enabled project. Replace every `YOUR_...` placeholder:

```bash
gcloud auth login
KBC_PROJECT_ID="YOUR_PROJECT_ID"
KBC_REGION="europe-west1"
KBC_SERVICE="kbc-future-demo"
KBC_SQL_INSTANCE="YOUR_CLOUD_SQL_INSTANCE"
KBC_DB_NAME="YOUR_DATABASE_NAME"
KBC_DB_USER="YOUR_DATABASE_USER"
KBC_RUNTIME_SA="kbc-future-runtime@${KBC_PROJECT_ID}.iam.gserviceaccount.com"
KBC_BUILD_SA="kbc-future-build@${KBC_PROJECT_ID}.iam.gserviceaccount.com"
KBC_DB_SECRET="kbc-future-db-password"
KBC_SECRET_VERSION="1"

gcloud config set project "$KBC_PROJECT_ID"
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com sqladmin.googleapis.com secretmanager.googleapis.com
```

Before deployment, ask the project administrator to prepare:

1. A Cloud SQL **MySQL** instance, database and database user. The current backend uses `IPTypes.PUBLIC`, so the instance must have a public IP; private-IP-only deployment needs backend/network changes. The Python connector authenticates and encrypts the connection; do not open MySQL to all IPs. See [Cloud SQL connection setup](https://docs.cloud.google.com/sql/docs/mysql/connect-run).
2. Schema and fixtures through an authorized MySQL connection or Cloud SQL Studio. Load `sql/schema.sql` only into a new empty demo database. For an existing schema, back up and apply `sql/migrations/001_customer_product_ownership.sql` instead. **Cloud Run does not initialize or migrate the database.** Verify `customers`, `customer_product` and `transactions`: respectively 3, 3 and 389 rows for the unchanged demo seed.
3. A Secret Manager secret named `kbc-future-db-password` containing the database user's password. Add it through the Google Cloud console, not a command containing the password. Set `KBC_SECRET_VERSION` to the actual numeric version. Runtime access is granted below. See [Cloud Run secrets](https://docs.cloud.google.com/run/docs/configuring/services/secrets).

**Rotate the exposed password:** a database credential was previously committed in this README. Replace it in Cloud SQL and store the replacement in Secret Manager. Removing the text does not erase Git history. This documentation update does not rotate credentials.

### Configure service accounts

An administrator may need to run these setup commands. Create the accounts only if they do not already exist:

```bash
gcloud iam service-accounts create kbc-future-runtime --display-name="KBC Future runtime"
gcloud iam service-accounts create kbc-future-build --display-name="KBC Future build"

gcloud projects add-iam-policy-binding "$KBC_PROJECT_ID" \
  --member="serviceAccount:${KBC_RUNTIME_SA}" --role="roles/cloudsql.client"

gcloud secrets add-iam-policy-binding "$KBC_DB_SECRET" \
  --member="serviceAccount:${KBC_RUNTIME_SA}" --role="roles/secretmanager.secretAccessor"

gcloud projects add-iam-policy-binding "$KBC_PROJECT_ID" \
  --member="serviceAccount:${KBC_BUILD_SA}" --role="roles/run.builder"
```

The deployer needs Cloud Run Source Developer and Service Usage Consumer on the project, plus permission to act as both selected service accounts (`roles/iam.serviceAccountUser`). Enabling APIs, creating accounts and changing IAM require additional administrator permissions. See [deployment roles](https://docs.cloud.google.com/run/docs/reference/iam/roles) and [custom build accounts](https://docs.cloud.google.com/run/docs/configuring/services/build-service-account).

### Build and deploy

Check upload candidates with `gcloud meta list-files-for-upload`. Exclude credentials, backups and `.env` files; keep secrets outside the source directory.

```bash
gcloud run deploy "$KBC_SERVICE" \
  --source . \
  --project "$KBC_PROJECT_ID" \
  --region "$KBC_REGION" \
  --service-account "$KBC_RUNTIME_SA" \
  --build-service-account "projects/${KBC_PROJECT_ID}/serviceAccounts/${KBC_BUILD_SA}" \
  --port 8080 \
  --no-allow-unauthenticated \
  --max-instances 2 \
  --update-env-vars "APP_ENV=production,INSTANCE_CONNECTION_NAME=${KBC_PROJECT_ID}:${KBC_REGION}:${KBC_SQL_INSTANCE},DB_USER=${KBC_DB_USER},DB_NAME=${KBC_DB_NAME}" \
  --update-secrets "DB_PASS=${KBC_DB_SECRET}:${KBC_SECRET_VERSION}"
```

Use the instance's actual `project:region:instance` connection name if it differs from the variables above. This backend's Python connector uses that name directly, not a mounted Unix socket. The instance cap is a demo setting, not a scalability guarantee.

Cloud Build uses the repository Dockerfile for `--source .`; no separate frontend hosting is needed. Repeat the deployment command after pulling reviewed changes to create a new revision. See [source deployment](https://docs.cloud.google.com/run/docs/deploying-source-code).

### Verify the cloud deployment

An authorized tester needs Cloud Run Invoker on the service. Start Google's authenticated local proxy:

```bash
gcloud run services proxy "$KBC_SERVICE" --project "$KBC_PROJECT_ID" --region "$KBC_REGION" --port 8081
```

Keep this terminal open and browse to **http://localhost:8081**. In another terminal:

```bash
curl --fail http://localhost:8081/api/health
curl --fail http://localhost:8081/db-test
curl --fail -X POST http://localhost:8081/api/ask \
  -H 'Content-Type: application/json' \
  -d '{"message":"Show my spending","user_id":"demo"}'
```

Expect production health, a successful database check and `source: "mock"` for the current chat route. These smoke checks do not prove `future()` or LLM integration. The [authenticated proxy](https://docs.cloud.google.com/sdk/gcloud/reference/run/services/proxy) supports browser testing without making the service public.

Cloud logs:

```bash
gcloud run services logs read "$KBC_SERVICE" --project "$KBC_PROJECT_ID" --region "$KBC_REGION" --limit 50
```

Do not enable anonymous access to real customer data. Before public release, implement authentication and customer authorization, review CORS, remove detailed database errors from `/db-test`, and complete the required security audit. The engine's single-customer check is not authentication.

## 3. Develop without building the app container

Start MySQL with `docker compose up -d mysql`. Use Python 3.12 and Node 22 to match the Dockerfile.

macOS/Linux backend:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
APP_ENV=development PORT=5000 DEV_DATABASE_URL="mysql+pymysql://app:app@127.0.0.1:3306/app_dev" python backend/app.py
```

PowerShell backend:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r backend/requirements.txt
$env:APP_ENV = "development"
$env:PORT = "5000"
$env:DEV_DATABASE_URL = "mysql+pymysql://app:app@127.0.0.1:3306/app_dev"
.\.venv\Scripts\python backend/app.py
```

Frontend in another terminal:

```bash
cd frontend
npm ci
npm run dev
```

Open **http://localhost:5173**. Vite proxies `/api` to **port 5000**, so set the backend port explicitly as above. Check database connectivity directly at `http://localhost:5000/db-test`. `.env.example` contains optional LLM placeholders, not a working integration. Never use a `VITE_` prefix for secrets.

## 4. Run checks

From the repository root:

```bash
python3 -m unittest discover -s backend -p 'test_future_engine.py'
python3 -m unittest discover -s scripts -p 'test_future_demo_data.py'
KBC_TEST_MYSQL=1 python3 -m unittest discover -s scripts -p 'test_future_database.py'
```

The last command requires local Compose MySQL and creates/deletes isolated test databases, not `app_dev`. The current suite contains 43 tests. In PowerShell, set `$env:KBC_TEST_MYSQL = "1"` before running the third Python command without its shell prefix.

## Shared repository

Clone with `git clone git@github.com:541l0r/tectonic2026.git`. Pull reviewed updates using `git pull --ff-only origin main` from a clean working tree. Never commit passwords, API keys or database backups.
