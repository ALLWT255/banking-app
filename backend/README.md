# Banking API backend

FastAPI backend for the Cloud-Native Banking Application. The API demonstrates user registration/login, account operations, withdrawal recording, PostgreSQL persistence, JWT authentication, health/readiness checks, and read-only AI operations analysis. It is not a complete payment/ledger system or production banking service.

## Routes and behavior

Routes are registered under `/api` in `app/main.py`.

| Route | Authentication | Behavior |
| --- | --- | --- |
| `GET /api/health` | Public | Process health only |
| `GET /api/ready` | Public | Runs a PostgreSQL `SELECT 1`; returns 503 when unavailable |
| `POST /api/users/register` | Public | Register user; store password hash |
| `POST /api/users/login` | Public | Verify credentials and return bearer JWT |
| `GET, POST /api/accounts` | JWT | List current user's accounts / create a zero-balance account |
| `POST /api/transactions` | JWT | Record a withdrawal for an owned account; deposits are rejected until a trusted payment source exists |
| `POST /api/ops/analyze` | JWT | Request read-only Bedrock troubleshooting analysis |

There is no verified real-money payment rail, double-entry ledger, deposit funding source, or full transaction history API.

## Prerequisites

- Python 3.12 or newer supported by the selected dependencies
- PostgreSQL for application/migration work (local or authorized remote)
- Docker Desktop for image builds
- Terraform/AWS CLI and approved AWS identity only for separate deployment work

## Local setup

Run from `backend/` in PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Configure `.env` with local-only values. Example placeholders:

```dotenv
DATABASE_URL=postgresql+psycopg://<DB_USER>:<URL_ENCODED_DB_PASSWORD>@localhost:5432/banking_db
JWT_SECRET_KEY=<generate-a-unique-local-random-secret>
```

Do not paste AWS or deployed RDS credentials into `.env`. For a password with URL-reserved characters, percent-encode it in a direct `DATABASE_URL`; alternatively provide `DB_HOST`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` separately. The application uses SQLAlchemy `URL.create` for separate fields. Never print or log a password-bearing URL.

To use discrete local PostgreSQL settings instead of `DATABASE_URL`:

```powershell
$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"
$env:DB_NAME = "banking_db"
$env:DB_USER = "<local-db-user>"
$env:DB_PASSWORD = "<local-only-password>"
$env:JWT_SECRET_KEY = "<local-only-random-secret>"
```

The application reads environment variables at import/startup. For RDS TLS, set `DB_SSL_ROOT_CERT` to the certificate bundle path. ECS uses `/app/certs/global-bundle.pem`; the file at `certs/global-bundle.pem` is a public AWS CA bundle and must remain in the repository. Without a CA path, source falls back to `sslmode=require`, which does not verify the server identity.

## Migrations and run

Create a local PostgreSQL database, set the environment above, then:

```powershell
alembic upgrade head
alembic current
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The API listens on port **8000**. Migrations should be run as an explicit deployment task, not automatically on every application container start. The recorded cloud schema revision is `d368608d12af`.

## Authentication and database

JWT access tokens use HS256 with a 30-minute expiration. Passwords are hashed with `pwdlib.PasswordHash.recommended()`. Local tests use synthetic secrets and SQLite fixtures; do not reuse their values outside tests.

The SQLAlchemy URL builder accepts `DATABASE_URL` or discrete `DB_*` fields. The RDS task config uses TLS certificate verification through the bundled AWS CA certificate. The development Terraform module currently injects the RDS master-user secret into the app; a production system should use a separate least-privilege application DB role.

## Amazon Bedrock

`app/services/bedrock_service.py` calls Bedrock Runtime's Boto3 Converse API with the Claude Haiku 4.5 US inference profile:

```text
us.anthropic.claude-haiku-4-5-20251001-v1:0
```

Deployed ECS inference uses the application task role; no static AWS keys are required in the task. Local inference needs explicitly configured, approved AWS credentials and Bedrock access. Selected input/output checks and prompt instructions do not fully prevent prompt injection or data leakage. Do not submit customer data, balances, tokens, or credentials.

## Docker

From the repository root:

```powershell
docker build -t banking-api:dev .\backend
docker run --rm -p 8000:8000 `
  -e DATABASE_URL="postgresql+psycopg://<DB_USER>:<URL_ENCODED_PASSWORD>@host.docker.internal:5432/banking_db" `
  -e JWT_SECRET_KEY="<local-only-random-secret>" `
  banking-api:dev
```

The image runs as non-root UID 10001 and includes the RDS CA bundle.

## Tests

From `backend/`:

```powershell
python -m pytest -q
python -m pytest -q tests/test_ops.py tests/test_security.py
```

Tests use local SQLite and synthetic secrets configured by `tests/conftest.py`. They do not prove cloud IAM, public HTTPS, or real banking workflow behavior. Check the current test output rather than relying on a historical screenshot count.

## Related documentation

- [Architecture](../docs/architecture.md)
- [Security design](../docs/security-design.md)
- [AI operations](../docs/ai-operations.md)
- [Troubleshooting and incidents](../docs/troubleshooting.md)
- [Screenshot evidence](../docs/screenshots/README.md)
- [Engineering tradeoffs](../docs/engineering-tradeoffs.md)
