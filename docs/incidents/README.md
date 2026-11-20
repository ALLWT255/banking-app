# Incident and break/fix reports

These reports distinguish observed deployment/runtime failures from controlled permission/security checks, and separate symptoms from likely explanations and unknowns. They do not infer customer impact, duration, or remediation where evidence does not establish it. All linked images are redacted publication copies; unredacted intake screenshots remain local and ignored by Git.

## Deployment and runtime incidents

| Report | Evidence/status |
| --- | --- |
| [AWS session and Terraform permissions](aws-session-and-terraform-permissions.md) | MFA-backed session recovery and permission failures; later deployment success recorded |
| [KMS key metadata permissions](kms-permission.md) | Permission-denial evidence and later key-state evidence; exact policy statement/end-to-end RDS effect not established |
| [ALB 503 and target draining](alb-503-recovery.md) | 503 and two draining targets followed by health/readiness HTTP 200; initiating change/root cause unknown |
| [ECS startup failure](ecs-startup.md) | Invalid ASGI import module recorded; later application startup logged, but exact corrective change and service readiness are unverified |
| [Database connectivity and migrations](database-connectivity-and-migrations.md) | PostgreSQL authentication/timeout errors and later migration/schema evidence; causes are not over-attributed |
| [RDS security-group connectivity](rds-security-group-connectivity.md) | Database connection errors and a follow-up screenshot labeled as restored; application-level recovery is not proven |

## Controlled permission and security checks

| Report | Evidence/status |
| --- | --- |
| [Secrets Manager task startup](secrets-manager-access.md) | `GetSecretValue` denied under the execution role; later app-startup screenshot is not enough correlation to confirm recovery |
| [Bedrock task-role permission](bedrock-task-role-permission.md) | Deliberately isolated empty test role / invocation denial followed by later analysis and API checks |

## Evidence gaps (not promoted to verified incidents)

- **RDS backup retention restriction:** Terraform config sets one-day retention, but the reviewed material has no verifiable retention error/correction sequence. The prior README's general claim is not treated as an incident.
- **SQLAlchemy URL/password masking:** a PostgreSQL authentication failure is visible, but evidence does not establish URL masking/escaping as its root cause. The source currently uses `sqlalchemy.engine.URL.create`, which avoids manual URL interpolation. Do not infer the deployed correction from a later image push alone.
- **ECS startup correction:** the failing ASGI target is visible as `app.invalid`, but the exact change that led to later successful process startup is not recorded.
- **Secrets Manager recovery:** app startup in a later task is consistent with recovery but does not show the permission update or establish that it was the same task/configuration.

## How these exercises map to engineering practice

The evidence demonstrates practical credential-chain diagnosis, least-privilege permission troubleshooting, infrastructure dependency reasoning, staged recovery validation, separation of application health from dependency readiness, and clear uncertainty management. These are relevant to Cloud Engineering, SRE, DevOps, AI Platform Engineering, and technical consulting; they are not evidence of production incident command or customer-impact management.
