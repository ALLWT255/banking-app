# Screenshot inventory and evidence guide

## Intake, retention, and chronology

The source intake is `docs/screenshots/banking-appdocsscreenshots/`. It contains **114 original PNG files, 79 unique SHA-256 contents, and 35 extra byte-for-byte duplicate copies**. Originals remain unmodified at that path and are ignored by Git; do not add them. There are currently **32 reviewed publication derivatives** under `docs/screenshots/evidence/`.

Chronology was assessed using the numbered filenames and visible console/log timestamps where available, not filesystem modification times. The numbered 36–51 series is the newest incident/security-validation batch; visible timestamps include November 18 target recovery and November 20 role/AI validation. Earlier numbered screenshots cover development, initial deployment, migration, and AI integration. Some duplicate filenames have different phase labels, so a filename alone is not proof of an independent event or chronology.

## Curated publication images

| Category | Curated image | What it shows |
| --- | --- | --- |
| Architecture | `evidence/architecture/banking-platform-overview.png` | Cropped project architecture illustration; not an AWS state screenshot or compliance evidence |
| ECS and load balancing | `evidence/ecs-load-balancing/healthy-targets-two-az.png` | Two healthy ALB targets across two AZs |
| Database/migrations | `evidence/database-migrations/health-and-database-readiness-200.png` | `/api/health` and `/api/ready` HTTP 200; local command lines are masked |
| Database/migrations | `evidence/database-migrations/postgres-authentication-failed.png` | PostgreSQL password authentication failure; private address is masked |
| Database/migrations | `evidence/database-migrations/migration-connection-timeout.png` | Alembic task connection timeout |
| Database/migrations | `evidence/database-migrations/alembic-revision-applied.png` | Alembic revision task log |
| Database/migrations | `evidence/database-migrations/rds-connection-failed.png` | PostgreSQL connection closed unexpectedly; task identifier and private address are masked |
| AI integration | `evidence/ai-integration/authenticated-ai-operations-response.png` | HTTP 200 response body from an AI operations request; generated advice is not verified infrastructure state |
| AI security validation | `evidence/ai-security-validation/auth-and-injection-statuses.png` | Missing/invalid JWT, selected sensitive input, and one prompt-injection request status; HTTP 200 is not proof of blocking |
| Incident response | `evidence/incident-response/alb-503-response.png` | Development ALB HTTP 503 |
| Incident response | `evidence/incident-response/alb-targets-draining.png` | Two registered targets draining and zero healthy |
| Incident response | `evidence/incident-response/alb-health-readiness-restored.png` | Later health and database readiness HTTP 200; local command lines are masked |
| Incident response | `evidence/incident-response/ecs-startup-failure.png` | ECS log reports an invalid ASGI module import |
| Incident response | `evidence/incident-response/ecs-startup-recovered.png` | Later log records application startup complete and Uvicorn on port 8000 |
| Bedrock/IAM | `evidence/ai-integration/bedrock-analysis-after-iam.png` | Later operational-analysis log output; account/task identifiers removed |
| IAM/security | `evidence/iam-security/task-role-without-policy.png` | Isolated test role with no attached policy; not the production app task role |
| IAM/security | `evidence/iam-security/bedrock-task-role-policy-attached.png` | Application task role shows an inline policy attachment; statements are not visible in the capture |
| AWS authentication | `evidence/aws-authentication/sts-invalid-token.png` | `InvalidClientTokenId` error excerpt; local path and command context excluded |
| AWS authentication | `evidence/aws-authentication/mfa-role-identity-verified.png` | Assumed-role identity fragment; account and session identifiers are masked |
| Terraform/IAM | `evidence/terraform/iam-permission-denied.png` | Cropped RDS subnet-group operation failure; account/request details excluded |
| Terraform/IAM | `evidence/terraform/deployment-policy-updated.png` | Deployment-role policy attachment success; account context masked |
| Terraform/IAM | `evidence/terraform/infrastructure-apply-nine-resources.png` | Apply summary reports nine resources added; outputs and paths excluded |
| KMS | `evidence/kms/describe-key-access-denied.png` | Redacted `DescribeKey` access-denied excerpt |
| KMS | `evidence/kms/deployment-policy-kms-read.png` | IAM policy summary showing limited KMS read; exact statement is not visible |
| KMS | `evidence/kms/rds-key-enabled.png` | KMS query reports key state `Enabled`; local path removed |
| Database | `evidence/database-migrations/rds-instance-available.png` | RDS PostgreSQL summary shows Available; no customer data |
| Networking | `evidence/networking/migration-task-private-network.png` | VPC/private-subnet selection; VPC/subnet IDs masked and selected SG not visible |
| ECR | `evidence/ecr/dev-image-pushed.png` | Docker push layer output; local path, registry URI, and digest masked |
| ECS | `evidence/ecs-load-balancing/ecs-service-running.png` | ECS cluster snapshot shows an active service, two running tasks, and no pending tasks; cluster ARN masked |
| Secrets Manager | `evidence/secrets-manager/getsecretvalue-denied.png` | ECS startup secret-retrieval failure; account, secret, task, and request identifiers masked |
| Secrets Manager | `evidence/secrets-manager/later-task-startup.png` | Later Uvicorn startup log; not correlated to the denied test role/task |
| Bedrock/IAM | `evidence/ai-integration/bedrock-invokemodel-denied.png` | `InvokeModel` denial log excerpt; principal/account/task identifiers masked |

These are actual source screenshots cropped or masked to remove identifiers/local details where needed. Curated copies have been visually reviewed after processing. Generated model advice is shown as evidence of a response only, not as verified operational guidance. The architecture illustration includes development HTTP and security-control labels; it is illustrative, not evidence of compliance or a guarantee that controls are complete.

## Source evidence categories

The source originals were classified by filename and, where available, visual content:

| Category | Original evidence families |
| --- | --- |
| Architecture | `Cloud-Native AI Banking Architecture*.png`, `Cloud-Native Banking AI Operations Architecture.png` |
| Terraform/infrastructure | `01`–`15` Terraform/IAM/KMS screenshots, `terraform apply banking.png` |
| AWS deployment | `15`–`19`, `29`, `ecs cluster running .png`, `events tasks started.png` |
| Networking | `21-ecs-migration-private-network-configuration*`, target group and DB connectivity screenshots |
| ECS/load balancing | `16`, `17`, `29`, `36`–`42`, `banking-app tg .png` |
| Database/migrations | `08`–`09` local config, `17`–`19`, `21`–`22`, `24`–`28`, `31`–`32`, `43`–`44` |
| IAM/security | `01`, `03`–`04`, `07`–`08`, `11`–`14`, `33`, `45`–`50` |
| AI integration | `02`–`03`, `06`, `19`, `33`–`35`, `ai ops*`, `200 ok ai ops project .png` |
| AI security validation | `04`–`05`, `23`–`32`, `51` |
| Troubleshooting/incident response | Newest `36`–`51` incident sequence and earlier Terraform/KMS/migration failures |
| Historical development/manual review | `api health check success broswer.png`, `website GET operation success broswer.png`, `test installaization ...`; excluded from the main README pending context confirmation |

No clear healthcare-app screenshot was identified. Generic older images remain excluded until the owner confirms project context. No port-5000 screenshot is used as banking evidence.

## Exact duplicate inventory

Each pair below has identical SHA-256 content. Keep one copy for evidence; the source originals are all retained in the ignored intake folder. Pairs with misleading titles must not be used as evidence for both claims.

| Original A | Original B |
| --- | --- |
| `08-pytest-database-config-failure.png` | `09-pytest-database-configuration-resolved.png` |
| `09-terraform-partial-deployment-recovery-plan.png` | `11-rds-kms-key-not-accessible.png` |
| `16-ecs-fargate-service-running.png - Copy.png` | `16-ecs-fargate-service-running.png.png` |
| `17-alb-target-group-healthy.png - Copy.png` | `17-alb-target-group-healthy.png.png` |
| `18-rds-postgresql-database-available - Copy.png` | `18-rds-postgresql-database-available.png` |
| `19-banking-api-health-and-database-readiness - Copy.png` | `19-banking-api-health-and-database-readiness.png` |
| `21-ecs-migration-private-network-configuration.png - Copy.png` | `21-ecs-migration-private-network-configuration.png.png` |
| `22-ecs-standalone-migration-task-launched - Copy.png` | `22-ecs-standalone-migration-task-launched.png` |
| `24-alembic-postgresql-authentication-failure - Copy.png` | `24-alembic-postgresql-authentication-failure.png` |
| `25-corrected-alembic-docker-image-pushed - Copy.png` | `25-corrected-alembic-docker-image-pushed.png` |
| `26-alembic-migration-database-connection-timeout - Copy.png` | `26-alembic-migration-database-connection-timeout.png` |
| `28-alembic-database-migration-success - Copy.png` | `28-alembic-database-migration-success.png` |
| `29-ecs-rolling-deployment-success.png - Copy.png` | `29-ecs-rolling-deployment-success.png.png` |
| `31-ai-output-validation-hardening.png` | `32-ai-security-ten-tests-passed.png` |
| `31-alembic-database-schema-revision-verified.png - Copy.png` | `31-alembic-database-schema-revision-verified.png.png` |
| `32-rds-banking-database-tables-verified.png - Copy.png` | `32-rds-banking-database-tables-verified.png.png` |
| `33-ecs-task-role-bedrock-invocation-policy.png - Copy.png` | `33-ecs-task-role-bedrock-invocation-policy.png.png` |
| `34-ecs-private-bedrock-inference-success - Copy.png` | `34-ecs-private-bedrock-inference-success.png` |
| `35-ecs-authenticated-ai-api-security-validation - Copy.png` | `35-ecs-authenticated-ai-api-security-validation.png` |
| `36-pre-incident-healthy-baseline - Copy.png` | `36-pre-incident-healthy-baseline.png` |
| `37-alb-http-503-service-unavailable - Copy.png` | `37-alb-http-503-service-unavailable.png` |
| `38-alb-target-group-no-registered-targets.png - Copy.png` | `38-alb-target-group-no-registered-targets.png.png` |
| `39-alb-503-incident-successful-recovery - Copy.png` | `39-alb-503-incident-successful-recovery.png` |
| `40-ecs-container-startup-failure - Copy.png` | `40-ecs-container-startup-failure.png` |
| `42-ecs-container-startup-recovery - Copy.png` | `42-ecs-container-startup-recovery.png` |
| `43-rds-database-connection-failure - Copy.png` | `43-rds-database-connection-failure.png` |
| `44-rds-connectivity-restored-backend-security-group - Copy.png` | `44-rds-connectivity-restored-backend-security-group.png` |
| `45-isolated-execution-role-permissions.png - Copy.png` | `45-isolated-execution-role-permissions.png.png` |
| `46-ecs-secrets-manager-access-denied - Copy.png` | `46-ecs-secrets-manager-access-denied.png` |
| `47-ecs-secrets-manager-access-restored - Copy.png` | `47-ecs-secrets-manager-access-restored.png` |
| `48-isolated-task-role-without-bedrock-permissions.png - Copy.png` | `48-isolated-task-role-without-bedrock-permissions.png.png` |
| `49-bedrock-runtime-iam-access-denied - Copy.png` | `49-bedrock-runtime-iam-access-denied.png` |
| `50-bedrock-runtime-permissions-restored - Copy.png` | `50-bedrock-runtime-permissions-restored.png` |
| `51-ai-authentication-and-prompt-injection-validation - Copy.png` | `51-ai-authentication-and-prompt-injection-validation.png` |
| `Cloud-Native AI Banking Architecture - Copy.png` | `Cloud-Native AI Banking Architecture.png` |

Notable mismatch: the `08` failure and `09` resolved screenshots are byte-identical; likewise the KMS-labeled `11` image duplicates a Terraform plan. The `31` AI output validation image duplicates the `32` file whose name says ten tests; the displayed test summary reports **9 passed**, so the filename is not accepted as a ten-test result.

## Sensitive or uncertain originals

Do not link or stage the raw originals. In particular:

- `18-fastapi-startup-resolved.png` shows a generated JWT signing secret in terminal output.
- MFA/session, Terraform, IAM, RDS, ECR, CloudWatch, and ECS originals contain account/resource identifiers or local paths; only the separately reviewed derivatives are publishable.
- `19-bedrock-direct-inference-success.png.png` shows MFA/device/account context.
- `25-corrected-alembic-docker-image-pushed.png` exposes account/repository details; its publication derivative masks the URI and digest.
- `33`–`51` contain role/task/secret/model/resource identifiers and operational prompts/logs.
- `test installaization ...` and `website GET operation success ...` need owner confirmation before classification as banking evidence.

See [publication review](../publication-review.md), [AI security evidence](ai-security/README.md), and the [incident reports](../incidents/README.md).
