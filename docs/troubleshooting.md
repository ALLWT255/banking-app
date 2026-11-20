# Troubleshooting and incident index

This index separates recorded failures, controlled break/fix exercises, and unresolved hypotheses. All dates/times below come from visible screenshot dates only where explicitly stated. No outage duration, customer impact, or current AWS status is inferred.

## Evidence-backed incident reports

| Topic | Observed state | Recovery status | Detailed report |
| --- | --- | --- | --- |
| Invalid AWS session / Terraform IAM denies | Invalid-session and provisioning permission errors indicated in screenshot names and deployment sequence | Later role/session validation and Terraform apply are recorded | [AWS session and Terraform permissions](incidents/aws-session-and-terraform-permissions.md) |
| KMS metadata permission | KMS denial indicated by image names; later permission/key-state evidence | Partial; no correlated RDS result | [KMS permission](incidents/kms-permission.md) |
| ALB 503 / target drain | HTTP 503, two targets draining and none healthy | Health and DB readiness both HTTP 200 on Nov 18 | [ALB 503 recovery](incidents/alb-503-recovery.md) |
| ECS startup failure | CloudWatch log reports an ASGI import failure for `app.invalid`; later logs show startup complete | Later process startup is recorded; exact corrective change and service-wide readiness are unknown | [ECS startup failure](incidents/ecs-startup.md) |
| PostgreSQL/Alembic authentication | `FATAL: password authentication failed for user "bankadmin"` | Later migration/head evidence; exact fix not correlated | [Database connectivity and migrations](incidents/database-connectivity-and-migrations.md) |
| Migration connection timeout | `ConnectionTimeout` / `connection timeout expired` in task logs | Later migration succeeded; original cause unproven | [Database connectivity and migrations](incidents/database-connectivity-and-migrations.md) |
| RDS connection closed | Nov 19 log shows private DB connection closed unexpectedly | Follow-up screenshot label suggests SG change; no same-task readiness proof | [RDS security-group connectivity](incidents/rds-security-group-connectivity.md) |
| Secrets Manager denial | Access-denied screenshot by filename; later task startup screenshot | Indication only; role/task correlation incomplete | [Secrets Manager access](incidents/secrets-manager-access.md) |
| Bedrock `InvokeModel` denied | Empty test task role and denial sequence | Later analysis and AI API checks recorded | [Bedrock permission](incidents/bedrock-task-role-permission.md) |
| AI authentication/input/output checks | 401/400/200 cases in source tests and cloud screenshot | Expected security behavior, not an outage | [AI operations](ai-operations.md) |

## Triage sequence

1. **Identify scope:** process health (`/api/health`), DB readiness (`/api/ready`), ALB status/target reason, or AI provider response.
2. **Capture time and version:** UTC timestamp, ECS task definition/release digest, deployment events, and exact non-secret error. Do not expose JWTs, secret values, AWS session tokens, customer data, or full secret/resource ARNs.
3. **Check edge and target health:** ALB listener/rule, target type/IP port 8000, health path `/api/health`, registered target state/reason, ECS desired/running count, and service events.
4. **Check container startup:** task stop reason/exit code, image digest, Uvicorn bind to `0.0.0.0:8000`, required environment/secret injection, memory/CPU, and CloudWatch logs.
5. **Check DB separately:** RDS state/endpoint, private routes, task/RDS security-group relationship on TCP 5432, CA path/TLS mode, then credentials. A timeout, TLS failure, and password rejection are different diagnoses.
6. **Check AWS API permissions:** determine execution role vs application task role; capture exact action/resource/principal, region, and service. Check key/resource policies and organization controls.
7. **Recover cautiously:** use a reviewed Terraform plan or controlled service deployment; avoid granting broad permissions or changing infrastructure from model recommendations.
8. **Validate and close:** verify task health, target health, `/api/health`, `/api/ready`, and a scoped authorized workflow; record what was not verified.

## Incident response learning

The documented work demonstrates IAM and temporary-credential diagnosis, network and health-check reasoning, Terraform partial-deployment recovery, separation of startup and runtime roles, PostgreSQL migration troubleshooting, and human-supervised AI analysis. This is evidence of development practice—not a measured SRE service level, real customer outage, or production response exercise.

## Evidence not verified

- No primary evidence supports a specific RDS backup-retention failure or correction. The current module sets one-day retention and `skip_final_snapshot = true`.
- No evidence confirms SQLAlchemy URL password masking/escaping as the root cause of the PostgreSQL authentication error. The source uses `URL.create`; exact deployed credential handling remains unknown.
- The ECS startup log explicitly reports `Could not import module "app.invalid"`; a later log reports startup complete and Uvicorn listening on port 8000, but the exact change and ALB recovery are not shown.
- Secrets Manager follow-up evidence does not establish a same-role, same-task permission recovery.
- A screenshot labeled `11-rds-kms-key-not-accessible.png` is an exact byte-for-byte duplicate of `09-terraform-partial-deployment-recovery-plan.png`; it is not independent KMS evidence.

See the [incident report index](incidents/README.md), [architecture](architecture.md), [AI operations](ai-operations.md), and [screenshot index](screenshots/README.md).
