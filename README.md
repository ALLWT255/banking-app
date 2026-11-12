# Cloud-Native Banking Application | Terraform, FastAPI & Amazon Bedrock

A cloud-engineering portfolio project combining modular Terraform infrastructure, a containerized FastAPI backend, and a source-level AI operations troubleshooting assistant. It demonstrates infrastructure design, AWS service integration, DevOps workflows, and layered AI security controls.

**Status: Stage 1 was deployed and verified on October 30, 2026, then torn down; ECR was preserved.** The owner confirmed empty Terraform state after cleanup and the ECR repository with its `dev` image as ACTIVE. This is historical HTTP development evidence, not a currently running API or a production-ready service. RDS was disabled. The Stage 1 application exposed only the health API and Swagger UI, not a complete banking platform.

The current backend source also contains a JWT-protected Amazon Bedrock operations endpoint and automated security tests. This later source and test evidence does not establish that the assistant or the current backend has been deployed to AWS. This documentation review did not query AWS.

## Project overview

- **Cloud-native application:** FastAPI backend packaged as a container and designed to run on ECS Fargate.
- **Infrastructure as Code:** Terraform modules define the VPC, networking, security groups, IAM roles, compute, logging, image repository, and optional database.
- **AI platform integration:** The backend source calls Amazon Bedrock using Boto3 and Claude Haiku 4.5 to provide read-only operational troubleshooting suggestions.
- **DevOps and security:** The repository includes Terraform deployment guidance, backend tests, JWT-protected API access, input/output checks, and prompt-injection evaluations.

The project is a portfolio implementation, not a complete or production-ready banking platform. The deployed Stage 1 and current source-code capabilities are described separately below.

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

The historical Stage 1 application exposed only the health API and Swagger UI. Its deployment did not include account or transaction operations, authentication, database integration, or an AI assistant. The current source tree has since added the JWT-protected operations endpoint and related tests; those changes do not alter the historical deployment evidence or prove current AWS deployment.

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
| [backend](backend) | FastAPI source, Dockerfile, and automated tests |
| [Terraform root](terraform) | Provider, variables, module wiring, outputs |
| [modules](terraform/modules) | `vpc`, `security`, `iam`, `compute`, optional `database` |
| [docs](docs) | Architecture, troubleshooting, evidence guidance |

All application documentation and screenshot guidance live inside this project. Paths and commands below are relative to `terraform/banking-app/`, the Banking App project root.

## AWS infrastructure

### Terraform implementation

The Terraform source defines:

- **Amazon ECS Fargate** for the containerized backend, with private task networking.
- **Application Load Balancer** across public subnets, forwarding to backend tasks in private subnets.
- **Amazon VPC** with public and private subnets across two Availability Zones, an Internet Gateway, and a shared NAT Gateway.
- **Amazon ECR** for the backend image, configured for image scanning on push.
- **Amazon CloudWatch Logs** for container logs with seven-day retention.
- **IAM roles and security groups** separating ECS task execution from application role identity and restricting backend/database traffic.
- **Amazon RDS for PostgreSQL** as an optional Terraform module; the project default disables database creation.

These are resources defined in Terraform, not a statement that they currently exist in AWS. The documented Stage 1 deployment was historically applied and verified, then torn down. ECR was preserved; no current ECS service, load balancer, VPC, or RDS deployment is claimed. See the [architecture and Terraform reference](docs/architecture.md) for the module inventory and historical deployment details.

The Bedrock operations integration is not wired into the current Terraform task definition: the application task role has no Bedrock permissions attached by the IAM module, and the task definition does not configure the AI runtime. Treat the assistant as implemented and locally tested source code, not as an AWS-hosted feature.

## AI operations assistant

The FastAPI backend implements `POST /api/ops/analyze`, an authenticated endpoint intended to provide read-only operational troubleshooting:

- **Model and SDK:** Amazon Bedrock Runtime Converse API through Boto3, using the Claude Haiku 4.5 model identifier configured in the service.
- **Authentication:** JWT-authenticated HTTP access. The route rejects unauthenticated or invalid-token requests.
- **Input and output:** The request accepts an operational description; the response contains an `analysis` string. The service has no infrastructure execution tools and is designed to return explanations and safe troubleshooting suggestions, not to change AWS resources.
- **Untrusted input handling:** The backend checks selected sensitive-data patterns before calling Bedrock and JSON-serializes the operational description before placing it in the user message.
- **Failure handling:** Sensitive input is rejected with a client error; Bedrock invocation failures and rejected model output return controlled gateway errors rather than the raw exception or unsafe response.

The configured AWS region is `us-east-1`. Live Bedrock invocation also depends on a locally configured AWS identity with appropriate model access; passing the automated tests does not establish live AWS access.

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

The historical Stage 1 deployment was an HTTP demo. Its ALB security group allowed port 443, but no HTTPS listener was active because the root passed no ACM certificate. Health checks return static JSON and do not verify database readiness. The database security group remains even with RDS disabled. The current backend source includes JWT authentication for the AI operations endpoint, but this was not part of the deployed Stage 1 service. WAF, autoscaling, alarms, a deployment CI/CD workflow, and durable banking data remain unconfigured. Two-AZ targets do not remove the shared single-NAT egress dependency.

## AI security controls and testing

The implementation uses multiple defense-in-depth measures:

1. **JWT authentication** protects the operations route.
2. **Sensitive-data validation** checks selected patterns such as AWS access keys, bearer tokens, and password assignments before sending input to Bedrock. This regex-based check is not comprehensive sensitive-data detection.
3. **System-level security instructions** define the assistant as read-only, direct it to treat user descriptions as untrusted data, and tell it to ignore embedded instructions and authority claims.
4. **JSON serialization** separates user-provided operational text into a JSON value, with instructions that the value is untrusted. JSON serialization is a data-formatting measure, not a security boundary or a prompt-injection prevention guarantee.
5. **Output validation** checks for selected sensitive patterns and prohibited infrastructure-action claims before returning the response.
6. **Controlled API errors** reject sensitive input with HTTP 400 and return HTTP 502 for Bedrock invocation failures or output rejected by validation, without returning raw provider details or the rejected output.

These controls reduce risk but cannot guarantee that a language model will resist prompt injection. In particular, regex-based output validation can reject safe explanatory text that quotes a prohibited phrase. The original validator also missed some unsafe paraphrases; additional patterns were implemented, and a regression test now covers an unsafe paraphrase. These limitations are covered by [the operations tests](backend/tests/test_ops.py).

### Security evaluation results

- **Live prompt-injection evaluations:** The project owner reports five live scenarios. The reported coverage included direct instruction overrides, authority spoofing, and XML/JSON boundary manipulation. Per-scenario prompts, transcripts, and results were not present in the repository, so this README records the reported test coverage but does not claim independently reproducible pass results.
- **Automated tests:** The full backend suite passed with **14 tests** in this documentation review: 10 operations-assistant tests, three security tests, and one health test. The operations tests exercise authentication, input checks, Bedrock error handling with a mocked call, and output-validation behavior. They do not make a live Bedrock request. Pytest also emitted three dependency/test-key warnings; the test key is not a production credential.
- **Known validator behavior:** A test documents a false positive for harmless text quoting a prohibited claim; another verifies that the added patterns catch a previously missed unsafe paraphrase.

No AI security screenshot images were found in the repository, so no image links are included. The [AI security screenshot folder](docs/screenshots/ai-security/README.md) contains publication guidance for future sanitized evidence.

## Local development and testing

The following PowerShell commands are for local development from the Banking App project root. Use your own local-only values; do not commit secrets, credentials, JWTs, or populated environment files. Activate a Python environment containing the backend dependencies first.

```powershell
Set-Location backend
$env:DATABASE_URL = "sqlite:///./local-dev.db"
$env:JWT_SECRET_KEY = "<local-only-random-secret>"
# Set this only when making a live Bedrock request with an authorized local AWS profile.
$env:AWS_PROFILE = "<authorized-local-aws-profile>"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

In another terminal, run the automated tests from `backend/`:

```powershell
python -m pytest -q
```

For just the operations-assistant tests:

```powershell
python -m pytest -q tests/test_ops.py
```

The full test command above was run successfully in the project's configured local Python environment. Note that `backend/requirements.txt` currently does not declare all packages imported by the AI/authentication code, including Boto3, PyJWT, and `pwdlib`; a fresh environment may need those dependencies installed before the application can start. No dependency or environment files were changed as part of this documentation update.

Provisioning and image publishing require separately reviewed operator permissions. Application execution/task roles do not grant the workstation image-push permission. Local policy artifacts alone do not prove effective AWS authorization. Ignore rules do not remove secrets already tracked in Git/history; check the actual publishing repository before committing.

## Future improvements and AWS cost awareness

Next steps include structured AI responses, additional prompt-injection evaluations, AI request monitoring, rate limiting, and expanded security regression coverage. Cloud platform improvements include HTTPS/certificate wiring, immutable image digests, short-lived CI/CD role credentials, encrypted remote state with locking, and operational monitoring. Database integration requires application work: enabling the existing RDS module alone does not connect the container to it. Review its single-AZ setting and skipped final snapshot before storing valuable data.

Costs include Fargate compute, ALB hours/capacity, NAT hours/data processing, public IPv4 addresses, ECR storage, CloudWatch ingestion/storage, and data transfer. Shared NAT egress can also incur cross-AZ transfer costs. Enabling RDS adds database costs. Use budgets, cost tags, and current regional pricing; no free-tier or fixed-price claim is made. Plan authorized cleanup of unused resources and review data retention before destruction.

## Publication review

See the [publication audit and complete first-commit file list](docs/publication-review.md). Screenshots remain outstanding; no placeholder evidence is included.
