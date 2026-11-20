# Troubleshooting and incident index

This index separates recorded failures, controlled break/fix exercises, and unresolved hypotheses. All dates/times below come from visible screenshot dates only where explicitly stated. No outage duration, customer impact, or current AWS status is inferred.

## Evidence-backed incident reports

| Topic | Observed state | Recovery status | Detailed report |
| --- | --- | --- | --- |
| Invalid AWS session / Terraform IAM denies | `InvalidClientTokenId`, MFA `iam:ListMFADevices` denial, Terraform `rds:CreateDBSubnetGroup`/`iam:PutRolePolicy` denials | Later role identity and Terraform apply recorded; exact external policy delta unknown | [AWS session and Terraform permissions](incidents/aws-session-and-terraform-permissions.md) |
| KMS metadata permission | `DescribeKey` denial; operator note confirms scoped `kms:DescribeKey`; later key query reports Enabled | Partial; no correlated RDS result | [KMS permission](incidents/kms-permission.md) |
| ALB 503 / target drain | HTTP 503 and draining/zero-healthy target state; operator note says desired count was deliberately set to zero | Capacity restored per operator note; health and DB readiness both HTTP 200 on Nov 18 | [ALB 503 recovery](incidents/alb-503-recovery.md) |
| ECS startup failure | CloudWatch log reports an ASGI import failure for `app.invalid`; later logs show startup complete | Later process startup is recorded; exact corrective change and service-wide readiness are unknown | [ECS startup failure](incidents/ecs-startup.md) |
| PostgreSQL/Alembic authentication | `FATAL: password authentication failed`; operator note attributes migration URL issue to `str()` masking the password and documents the rendering/escaping fix | Later ECR push and migration revision evidence recorded | [Database connectivity and migrations](incidents/database-connectivity-and-migrations.md) |
| Migration connection timeout | `ConnectionTimeout`; operator note says standalone task lacked backend SG and was relaunched with it | Later migration succeeded; task SG itself is not visible in the screenshot | [RDS security-group connectivity](incidents/rds-security-group-connectivity.md) |
| RDS connection closed | Nov 19 log shows private DB connection closed unexpectedly | Cause and same-event recovery remain unverified; do not conflate with the migration timeout | [RDS security-group connectivity](incidents/rds-security-group-connectivity.md) |
| Secrets Manager denial | Test execution role denied `GetSecretValue` | Terraform source configures scoped execution-role read; later startup is not same-task proof | [Secrets Manager access](incidents/secrets-manager-access.md) |
| Bedrock `InvokeModel` denied | Test task role denied the invocation action | Terraform puts scoped permission on application task role; later analysis/API checks recorded | [Bedrock permission](incidents/bedrock-task-role-permission.md) |
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

- Operator note says a development-account restriction led to one-day RDS backup retention; current Terraform corroborates the final value, but no original error or prior retention value is preserved.
- Operator note supplies the historical SQLAlchemy URL masking cause; the current source confirms `render_as_string(hide_password=False)` and percent escaping, but the earlier local version is not in Git history.
- The ECS startup log explicitly reports `Could not import module "app.invalid"`; a later log reports startup complete and Uvicorn listening on port 8000, but the exact change and ALB recovery are not shown.
- Secrets Manager follow-up evidence does not establish a same-role, same-task permission recovery.
- The migration-task backend-SG note does not establish the root cause or recovery of the separate November 19 RDS connection-close log.
- A screenshot labeled `11-rds-kms-key-not-accessible.png` is an exact byte-for-byte duplicate of `09-terraform-partial-deployment-recovery-plan.png`; it is not independent KMS evidence.

See the [incident report index](incidents/README.md), [architecture](architecture.md), [AI operations](ai-operations.md), and [screenshot index](screenshots/README.md).
