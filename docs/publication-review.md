# GitHub publication review

Review date: November 17, 2026. Scope: tracked files, staged changes, ignored sensitive candidates, source implementation, and accessible Git history.

## Historical Stage 1 evidence

October 30, 2026 initial deployment evidence remains relevant:

- 34 Terraform resources provisioned.
- ECS Fargate backend and public ALB deployed.
- Two healthy targets across both public-subnet availability zones.
- `/api/health` and Swagger UI returned successful responses.
- Infrastructure was torn down while the ECR repository and image were preserved.

Stage 1 did not include RDS or live Bedrock integration. Historical results must not be presented as current availability.

## Stage 2 deployment status

November 17, 2026 Stage 2 verification succeeded:

- Modular Terraform infrastructure deployed.
- ECS Fargate backend ran in private subnets behind the ALB.
- RDS PostgreSQL was private and storage-encrypted.
- RDS used one-day backup retention and Single-AZ deployment.
- Database credentials and the JWT signing secret were managed through Secrets Manager.
- Alembic migrated to `d368608d12af`.
- Verified tables: `users`, `accounts`, `transactions`, and `alembic_version`.
- Health and readiness endpoints returned HTTP 200.
- 19 local Pytest tests passed.
- Scoped Bedrock permissions were added to the ECS application task role by Terraform.
- Live Claude Haiku 4.5 inference completed from private Fargate with exit code 0.
- Full Terraform plan returned no changes after the Bedrock IAM deployment.

## Verified AI API security tests

The endpoint was tested in a standalone ECS Fargate task with FastAPI `TestClient` and live Bedrock inference:

| Check | Result |
| --- | --- |
| Missing authentication | 401 |
| Invalid JWT | 401 |
| Prohibited sensitive input | 400 |
| Valid authenticated AI request | 200 |

All four checks passed. A synthetic JWT was generated inside the container. Public login and authenticated public-ALB traffic were not tested because HTTPS is not configured.

## Security review findings

PASS:

- No confirmed AWS access-key literals or private-key payloads were found in tracked publication candidates.
- RDS master passwords are AWS-managed rather than literals in Terraform.
- The JWT signing secret is not committed as a source value.
- Local state, saved plans, tfvars, environment files, virtual environments, provider caches, credentials, and databases are ignored.
- The public RDS CA certificate remains available at `backend/certs/global-bundle.pem`.

WARN:

- `terraform/environments/dev/terraform.tfvars` exists locally and must remain ignored.
- Terraform state and plan artifacts exist locally and must remain ignored.
- Screenshots are outstanding and could expose AWS identifiers or credentials if not sanitized.
- The ignore rules protect normal additions but not deliberately force-added files.
- Secret review cannot guarantee detection of every possible credential format.

## Remaining risks and architecture limitations

- Public development HTTP; HTTPS is not configured.
- RDS is Single-AZ with one-day backup retention.
- One shared NAT Gateway is an availability and egress-cost dependency.
- Terraform state is local and no remote locking backend is configured.
- Container tags are mutable.
- RDS master-user credentials are in use.
- Production monitoring, alerting, WAF, autoscaling, and automated CI/CD are absent.
- Prompt-injection controls are defense-in-depth, not complete prevention.
- No claim of production readiness or banking regulatory compliance is made.

## Publication readiness

Documentation can be published in source form after screenshots are copied and reviewed or explicitly recorded as missing. Before commit:

- Do not add `.tfstate`, `.tfplan`, `.tfvars`, `.env`, private keys, credentials, databases, virtual environments, or provider caches.
- Preserve and allow `backend/certs/global-bundle.pem`.
- Recheck the staged diff and repeat secret scanning after screenshots are added.
- Keep screenshots out of Git until AWS identifiers, JWTs, session tokens, passwords, MFA values, and unrelated account details are redacted.

## Current repository structure

```text
banking-app/
├── backend/
│   ├── app/
│   ├── certs/global-bundle.pem
│   ├── migrations/
│   ├── tests/
│   ├── Dockerfile
│   └── README.md
├── terraform/
│   ├── modules/{compute,database,iam,security,vpc}/
│   └── main.tf
└── docs/
    ├── architecture.md
    ├── security-design.md
    ├── ai-operations.md
    ├── troubleshooting.md
    ├── publication-review.md
    └── screenshots/
```

Related documents: [architecture](architecture.md), [security design](security-design.md), [AI operations](ai-operations.md), [troubleshooting](troubleshooting.md), and [screenshots](screenshots/README.md).
