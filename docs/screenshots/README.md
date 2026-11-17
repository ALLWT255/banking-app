# Screenshot evidence index

No screenshot files currently exist in this directory or in [docs/screenshots/ai-security/](ai-security/). This index links only to files that are actually present.

## Existing evidence

No deployment screenshots are present.

## Evidence still required

| Evidence category | Suggested capture | Current status |
| --- | --- | --- |
| Modular Terraform deployment | Applied resource summary or reviewed plan summary | Missing |
| ECS and ALB infrastructure | ECS service desired/running tasks and ALB target status | Missing |
| IAM troubleshooting | Sanitized role/policy or access-denied diagnosis | Missing |
| RDS and migration | RDS private configuration and Alembic current/head evidence | Missing |
| Database tables | Query output for `users`, `accounts`, `transactions`, and `alembic_version` | Missing |
| Health validation | `/api/health` HTTP 200 | Missing |
| Readiness validation | `/api/ready` HTTP 200 and database connected | Missing |
| Bedrock integration | Task execution or application log showing live Claude Haiku inference exit 0 | Missing |
| Bedrock IAM | Task role policy showing scoped inference-profile resources | Missing |
| AI security testing | Sanitized four-result TestClient evidence | Missing in AI subdirectory |

Before publication, verify each image is genuine, record the capture date, crop credentials and session data, redact AWS account/resource identifiers, and review EXIF metadata.

Do not copy Terraform state, saved plans, environment files, terminal secret values, or raw JWTs into screenshots.

## Historical Stage 1

Stage 1 evidence from October 30, 2026 remains historical: 34 Terraform resources, ECS/ALB health, and preserved ECR. It was torn down and must not imply current availability.

Stage 2 evidence is from November 17, 2026 and should be labeled separately.
