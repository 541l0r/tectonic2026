"""Flask API with development and production MySQL connections."""

import os

import sqlalchemy
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import text


load_dotenv()


# ---------------------------------------------------------------------------
# Database configuration
# ---------------------------------------------------------------------------

APP_ENV = os.getenv("APP_ENV", "development").lower()


def create_development_engine():
    """
    Development:
    Connect to the MySQL container from docker-compose.

    Default connection:
        host: mysql
        port: 3306
        database: app_dev
        user: app
        password: app
    """

    database_url = os.getenv(
        "DEV_DATABASE_URL",
        "mysql+pymysql://app:app@mysql:3306/app_dev",
    )

    print(f"Using development database: {database_url}")

    return sqlalchemy.create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800,
    )


def create_production_engine():
    """
    Production:
    Connect to Google Cloud SQL using the Cloud SQL Python Connector.
    """

    from google.cloud.sql.connector import Connector, IPTypes

    required_env_vars = [
        "INSTANCE_CONNECTION_NAME",
        "DB_USER",
        "DB_PASS",
        "DB_NAME",
    ]

    missing = [
        name
        for name in required_env_vars
        if not os.getenv(name)
    ]

    if missing:
        raise RuntimeError(
            "Missing required production environment variables: "
            + ", ".join(missing)
        )

    connector = Connector(
        ip_type=IPTypes.PUBLIC,
        refresh_strategy="LAZY",
    )

    def getconn():
        return connector.connect(
            os.environ["INSTANCE_CONNECTION_NAME"],
            "pymysql",
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            db=os.environ["DB_NAME"],
        )

    print(
        "Using production Google Cloud SQL database: "
        f"{os.environ['INSTANCE_CONNECTION_NAME']}"
    )

    return sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800,
    )


def create_database_engine():
    if APP_ENV == "development":
        return create_development_engine()

    if APP_ENV == "production":
        return create_production_engine()

    raise RuntimeError(
        f"Invalid APP_ENV: {APP_ENV}. "
        "Expected 'development' or 'production'."
    )


engine = create_database_engine()


# ---------------------------------------------------------------------------
# Flask
# ---------------------------------------------------------------------------

app = Flask(
    __name__,
    static_folder="../frontend/dist",
    static_url_path="",
)

CORS(app)


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health():
    return jsonify(
        status="ok",
        environment=APP_ENV,
    )


@app.post("/api/ask")
def ask():
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify(error="Expected a JSON object"), 400

    message = payload.get("message")

    if (
        not isinstance(message, str)
        or not message.strip()
        or len(message) > 2000
    ):
        return jsonify(
            error="message must be 1–2000 characters"
        ), 400

    if payload.get("user_id", "demo") != "demo":
        return jsonify(
            error="Only the demo user is available"
        ), 400

    return jsonify(
        answer="Your spending is up in groceries this month.",
        blocks=[
            {
                "type": "metric",
                "label": "Groceries",
                "value": "€420",
                "detail": "+€60 vs previous month",
            },
            {
                "type": "list",
                "title": "Possible next steps",
                "items": [
                    "Review recent grocery purchases",
                    "Set a monthly alert",
                ],
            },
        ],
        source="mock",
    )


@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT 1")
            ).scalar()

        return jsonify(
            database="ok",
            environment=APP_ENV,
            result=result,
        )

    except Exception as exc:
        app.logger.exception(
            "Database connection failed"
        )

        return jsonify(
            database="error",
            environment=APP_ENV,
            error=str(exc),
        ), 500


# ---------------------------------------------------------------------------
# React / Vite frontend
# ---------------------------------------------------------------------------

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def frontend(path):
    if path and os.path.exists(
        os.path.join(app.static_folder, path)
    ):
        return app.send_static_file(path)

    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        debug=APP_ENV == "development",
    )
