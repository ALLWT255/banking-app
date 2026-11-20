# Incident and break/fix reports

These reports distinguish observed deployment/runtime failures from controlled permission/security checks, and separate symptoms from likely explanations and unknowns. They do not infer customer impact, duration, or remediation where evidence does not establish it. All linked images are redacted publication copies; unredacted intake screenshots remain local and ignored by Git.

## Deployment and runtime incidents

| Report | Evidence/status |
| --- | --- |
| [AWS session and Terraform permissions](aws-session-and-terraform-permissions.md) | Invalid STS token, MFA permission denial, Terraform action denials, later role and apply evidence |
| [KMS key metadata permissions](kms-permission.md) | `DescribeKey` denial; operator note confirms scoped `kms:DescribeKey`; later key query reports Enabled |
| [ALB 503 and target draining](alb-503-recovery.md) | Operator note confirms deliberate scale-to-zero exercise; later health/readiness HTTP 200 |
| [ECS startup failure](ecs-startup.md) | Invalid ASGI import module recorded; later application startup logged, but exact corrective change and service readiness are unverified |
| [Database connectivity and migrations](database-connectivity-and-migrations.md) | Authentication failure; operator note identifies historical SQLAlchemy URL masking and corrected rendering/escaping; later migration evidence |
| [RDS security-group connectivity](rds-security-group-connectivity.md) | Operator note confirms missing backend SG caused a separate migration-task timeout; November 19 connection-close event remains unresolved |

## Controlled permission and security checks

| Report | Evidence/status |
| --- | --- |
| [Secrets Manager task startup](secrets-manager-access.md) | Test execution role denied `GetSecretValue`; Terraform source configures scoped execution-role reads; later startup is uncorrelated |
| [Bedrock task-role permission](bedrock-task-role-permission.md) | Isolated test role denied `InvokeModel`; Terraform configures invocation on the app task role; later analysis/API checks recorded |

## Evidence gaps (not promoted to verified incidents)

- **RDS backup retention restriction:** operator note says development-account constraints led to one-day retention. The current module corroborates the final value; no error screenshot or prior value is available, so this is not a fully evidenced incident.
- **SQLAlchemy URL/password masking:** operator note identifies `str(database_url)` masking as the migration issue and states the fix. Current `env.py` confirms explicit password rendering and percent escaping; the earlier local version is not in Git history, so historical detail remains operator-provided.
- **ECS startup correction:** the failing ASGI target is visible as `app.invalid`, but the exact change that led to later successful process startup is not recorded.
- **Secrets Manager recovery:** app startup in a later task does not show the permission update or establish that it was the same test role/task.
- **November 19 RDS connection close:** a different operator note explains a standalone migration timeout caused by a missing backend security group; it must not be used to assign a cause to the connection-close event.

## How these exercises map to engineering practice

The evidence demonstrates practical credential-chain diagnosis, least-privilege permission troubleshooting, infrastructure dependency reasoning, staged recovery validation, separation of application health from dependency readiness, and clear uncertainty management. These are relevant to Cloud Engineering, SRE, DevOps, AI Platform Engineering, and technical consulting; they are not evidence of production incident command or customer-impact management.
