# AWS Banking API — Terraform and ECS Fargate

A containerized FastAPI service deployed to AWS with modular Terraform. This portfolio project demonstrates private container networking, load balancing, IAM role separation, image publishing, and deployment verification.

**Status: Stage 1 was deployed and verified on October 30, 2026, then torn down; ECR was preserved.** The owner confirmed empty Terraform state after cleanup and the ECR repository with its `dev` image as ACTIVE. This is historical HTTP development evidence, not a currently running API or a production-ready service. RDS was disabled. The Stage 1 application exposed only the health API and Swagger UI, not a complete banking platform.

## Verified deployment

These results were verified by the project owner for the **October 30, 2026** deployment. This documentation review did not query AWS:

| Check | Result |
| --- | --- |
| Terraform apply | 34 resources added, 0 changed, 0 destroyed |
| ECR | `banking-app-dev-backend:dev` |
| ECR image digest | `sha256:3fe7c32bc744e6749cda39018f645680921555191b1ae3babc7dfd35cad8f57d` |
| ECS service | `banking-app-dev-backend-service` |
| ALB | `banking-app-dev-alb` |
| Target health | Two healthy targets across `us-east-1a` and `us-east-1b`, port 8000 |
| `GET /api/health` | `{"status":"healthy","service":"banking-api"}` |
| `/docs` | Swagger UI accessible; documents the health route |

[Application startup](backend/app/main.py) registers only the health router. Account and transaction route files exist but are empty and are not registered. No deployed account, transaction, authentication, database integration, or AI agent functionality is claimed. Those files are empty scaffolds for planned features; a populated health test exists, but test scaffolds do not prove deployed features.

## Stage 1 infrastructure (deployed, then torn down)

- A DNS-enabled VPC contains two public and two private subnets across two AZs.
- A public ALB forwards development HTTP on port 80 to private Fargate task IPs on port 8000.
- ECS runs two desired tasks, each with 0.25 vCPU and 512 MiB memory, without public IPs.
- One NAT Gateway in `us-east-1a` provides egress for both private subnets.
- ECR stores a mutable `dev` tag with scan-on-push enabled.
- Separate execution and application task roles distinguish image-pull/logging permissions from application permissions.
- CloudWatch retains container logs in `/ecs/banking-app-dev-backend` for seven days.

See the [architecture and module reference](docs/architecture.md), [troubleshooting runbook](docs/troubleshooting.md), and [screenshot guide](docs/screenshots/README.md). No screenshot images were present during documentation preparation.

## Project map

| Path | Purpose |
| --- | --- |
| [backend](backend) | FastAPI source, Dockerfile, test scaffolding |
| [Terraform root](terraform) | Provider, variables, module wiring, outputs |
| [modules](terraform/modules) | `vpc`, `security`, `iam`, `compute`, optional `database` |
| [docs](docs) | Architecture, troubleshooting, evidence guidance |

All application documentation and screenshot guidance live inside this project. Paths and commands below are relative to `terraform/banking-app/`, the Banking App project root.

## Deployment workflow

Prerequisites: Terraform >= 1.6.0, AWS CLI, Docker Desktop using Linux containers, and authorized local AWS credentials. Terraform requires AWS provider `~> 6.0` and explicitly selects region `us-east-1` and profile `banking-terraform-role`. Profile configuration and MFA/session renewal are local prerequisites; never store credentials in the repository.

These commands are operator instructions, not commands executed during this documentation review. From the Banking App project root:

```powershell
Set-Location terraform
terraform init
terraform fmt -check -recursive
terraform validate
# Existing preserved ECR repository: import before planning a normal redeployment.
terraform import -var-file=environments/dev/terraform.tfvars module.compute.aws_ecr_repository.backend banking-app-dev-backend
terraform plan -var-file=environments/dev/terraform.tfvars -out=banking-dev.tfplan
```

The import shown above is a future operator action, not an action performed in this review. First confirm the selected account/workspace and that the repository is not already managed in that state. Import writes state; never import the same object into multiple resource addresses. See the [preserved ECR runbook](docs/troubleshooting.md#teardown-and-preserved-ecr).

The development tfvars file is intentionally ignored. Recreate it using the non-secret values in the [variable reference](docs/architecture.md#root-variables). Review a fresh plan before an authorized apply; do not reuse historical saved plans. An operator can apply the reviewed plan with `terraform apply banking-dev.tfplan`. This changes infrastructure and incurs cost. No remote backend is configured; protect local state and plans.

Terraform creates ECR but does not build or publish images. For a fresh environment, ECS can attempt to start before `dev` exists and initially fail image pulls. Publish after the repository exists and verify convergence. For this project, the existing ECR repository was removed from Terraform state to preserve it during destroy. Its resource block remains in the compute module; import it before a future normal apply to avoid trying to create an already existing repository. No live ECS/ALB deployment is claimed after teardown.

From the Banking App project root, build and push using an approved publisher profile with image-push permissions. Replace `<AWS_ACCOUNT_ID>` with your account ID before running these examples:

```powershell
$Region = 'us-east-1'
$Registry = '<AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com'
$Image = "${Registry}/banking-app-dev-backend:dev"
$PublisherProfile = '<authorized-image-publisher-profile>'
docker build -t $Image ./backend
if ($LASTEXITCODE -ne 0) { throw 'Docker build failed' }
# Use a locally configured, approved publisher profile (replace the value above).
# cmd /c runs the pipe in cmd.exe, the confirmed login workaround for this deployment.
cmd /c "aws ecr get-login-password --region $Region --profile $PublisherProfile | docker login --username AWS --password-stdin $Registry"
if ($LASTEXITCODE -ne 0) { throw 'Docker login failed; inspect both AWS CLI and Docker errors' }
docker push $Image
if ($LASTEXITCODE -ne 0) { throw 'Docker push failed' }
```

The `cmd /c` pipeline reports the Docker exit status; inspect AWS CLI errors too, since it does not separately enforce the left-hand command's exit code. The profile placeholder is a local prerequisite, not a claim about the identity used on October 30.

The digest above records the verified ECR image, while Terraform still references the mutable `dev` tag. Overwriting `dev` does not automatically replace running tasks. Coordinate an explicitly authorized rollout with Terraform. See [troubleshooting](docs/troubleshooting.md) for publishing and health checks. Obtain the ALB DNS name from the Console; current Terraform outputs do not expose it. After a future authorized redeployment, visit `http://<alb-dns-name>/api/health` and `http://<alb-dns-name>/docs`; the old deployment is no longer represented as live.

## Security design and limitations

Tasks have no public IPs. Their port 8000 accepts inbound traffic only from the ALB security group; ALB egress is limited to that backend port. Backend egress permits HTTPS to the internet and PostgreSQL to the database security group. The final Docker build stage runs as a non-root user. The application task role has no permissions attached by these modules.

This is an HTTP demo. The ALB security group allows port 443, but no HTTPS listener is active because the root passes no ACM certificate. Health checks return static JSON and do not verify database readiness. The database security group remains even with RDS disabled. Authentication, WAF, autoscaling, alarms, a deployment CI/CD workflow, and durable banking data are not configured. Two-AZ targets do not remove the shared single-NAT egress dependency.

Provisioning and image publishing require separately reviewed operator permissions. Application execution/task roles do not grant the workstation image-push permission. Local policy artifacts alone do not prove effective AWS authorization. Ignore rules do not remove secrets already tracked in Git/history; check the actual publishing repository before committing.

## Future improvements and AWS cost awareness

Next steps include HTTPS/certificate wiring, immutable image digests, short-lived CI/CD role credentials, encrypted remote state with locking, application tests/authentication, and monitoring. Database integration requires application work: enabling the existing RDS module alone does not connect the container to it. Review its single-AZ setting and skipped final snapshot before storing valuable data.

Costs include Fargate compute, ALB hours/capacity, NAT hours/data processing, public IPv4 addresses, ECR storage, CloudWatch ingestion/storage, and data transfer. Shared NAT egress can also incur cross-AZ transfer costs. Enabling RDS adds database costs. Use budgets, cost tags, and current regional pricing; no free-tier or fixed-price claim is made. Plan authorized cleanup of unused resources and review data retention before destruction.

## Publication review

See the [publication audit and complete first-commit file list](docs/publication-review.md). Screenshots remain outstanding; no placeholder evidence is included.
