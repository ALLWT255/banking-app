# Banking API backend

FastAPI backend for the Cloud-Native Banking Application. Stage 2 includes PostgreSQL/Alembic persistence, JWT authentication, Argon2 password hashing, health/readiness checks, and a Bedrock operations assistant.

## Application routes

The API is registered under `/api` in [app/main.py](app/main.py).

| Route | Authentication | Purpose |
| --- | --- | --- |
| `/api/health` | No | Application process health |
| `/api/ready` | No | PostgreSQL connectivity readiness |
| `/api/users` and auth routes | Mixed | Registration and JWT login |
| `/api/accounts` | JWT | Account operations |
| `/api/transactions` | JWT | Transaction operations |
| `/api/ops/analyze` | JWT | Claude Bedrock operations analysis |

## Local prerequisites

- Windows PowerShell
- Python 3.12
- PostgreSQL 15 or later, local or remote
- Docker Desktop for container builds
- AWS CLI and approved credentials only for ECS/Bedrock validation

## Local setup

From `backend/`:

```powershell
py -3.12 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` with placeholders or local-only values. `.env` is ignored by Git:

```dotenv
DATABASE_URL=postgresql+psycopg://<DB_USER>:<DB_PASSWORD>@localhost:5432/banking_db
JWT_SECRET_KEY=<generate-a-unique-random-secret-locally>
```

PowerShell environment loading is application-specific; export the variables in the current shell or use a local process manager before starting Uvicorn:

```powershell
$env:DATABASE_URL = "postgresql+psycopg://<DB_USER>:<DB_PASSWORD>@localhost:5432/banking_db"
$env:JWT_SECRET_KEY = "<generate-a-unique-random-secret-locally>"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Do not use deployed secret values or real credentials in this example.

## PostgreSQL and Alembic

The SQLAlchemy URL builder prefers `DATABASE_URL`. Otherwise it uses `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, and optional `DB_SSL_ROOT_CERT`.

For local PostgreSQL, TLS is optional unless the deployment environment supplies the RDS CA bundle. ECS uses full certificate verification:

```dotenv
DB_SSL_ROOT_CERT=/app/certs/global-bundle.pem
```

Run migrations from `backend/`:

```powershell
alembic upgrade head
alembic current
```

The verified Stage 2 revision was `d368608d12af`. The migration creates the banking tables and `alembic_version`.

The RDS certificate bundle is retained at `certs/global-bundle.pem`. It is a public AWS CA bundle, not a private key, and must not be removed.

## Authentication

JWT access tokens use `HS256` and expire after 30 minutes. Password hashes use the Argon2-capable `pwdlib.PasswordHash.recommended()` configuration.

Local test secrets are synthetic and should never be reused as a deployed signing key.

## Bedrock

`app/services/bedrock_service.py` creates a Boto3 `bedrock-runtime` client using ECS task credentials. The configured inference profile is:

```text
us.anthropic.claude-haiku-4-5-20251001-v1:0
```

Local Bedrock testing requires approved temporary AWS credentials and Bedrock access. The application never requires static AWS access keys inside a normal ECS deployment.

The route validates input before inference and validates model output before responding. These controls are not complete prompt-injection protection or DLP.

## Docker

Build from the repository or backend context:

```powershell
docker build -t banking-app-backend:dev ./backend
docker run --rm -p 8000:8000 `
  -e DATABASE_URL="postgresql+psycopg://<DB_USER>:<DB_PASSWORD>@host.docker.internal:5432/banking_db" `
  -e JWT_SECRET_KEY="<local-placeholder-only>" `
  banking-app-backend:dev
```

The Docker image runs as UID 10001 and includes the RDS CA bundle.

## Tests

Run the complete local suite:

```powershell
python -m pytest -q
```

Run focused AI tests:

```powershell
python -m pytest -q tests/test_ops.py tests/test_security.py
```

The Stage 2 local suite passed 19 tests. Tests use a local SQLite database and synthetic JWT secret unless otherwise configured.

## ECS operations

Database migrations must run in ECS in the private network. Do not start an application migration automatically on every container boot without an explicit deployment design.

For AWS log, migration, health, and image troubleshooting, preserve [the troubleshooting runbook](../docs/troubleshooting.md).

For implementation details, see:

- [AI operations](../docs/ai-operations.md)
- [Architecture](../docs/architecture.md)
- [Security design](../docs/security-design.md)
- [Publication review](../docs/publication-review.md)
