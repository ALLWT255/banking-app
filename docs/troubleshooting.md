# Deployment troubleshooting

The owner confirmed the following troubleshooting work for the October 30, 2026 deployment:

- IAM/ECR permissions were addressed for the deployment and image-publishing workflow.
- Temporary MFA session credentials were used.
- Docker ECR login from Windows PowerShell used `cmd /c` to execute the AWS CLI-to-Docker pipeline.

The exact error transcripts, policy changes, and publisher profile were not supplied, so this guide does not invent them. Diagnostic advice below is distinct from that confirmed history. No AWS commands were run during documentation preparation.

The verified outcome was 34 resources added, 0 changed, 0 destroyed; ECR tag `dev`; two healthy targets across `us-east-1a` and `us-east-1b`; successful health JSON and Swagger UI. The verified ECR digest is `sha256:3fe7c32bc744e6749cda39018f645680921555191b1ae3babc7dfd35cad8f57d`. See the [deployment record](../README.md#verified-deployment).

## MFA and temporary credentials

Expired or incomplete sessions can prevent CLI/Terraform requests. Temporary credentials require an access key, secret key, and session token; an MFA code is not a session token. Renew using the approved local MFA/role workflow and keep returned values out of source, screenshots, and shared terminal output. See [AWS temporary credentials](https://docs.aws.amazon.com/cli/latest/reference/sts/get-session-token.html).

Terraform selects profile `banking-terraform-role`; CLI commands using another profile may use another identity. Confirm intended profile and local environment overrides without printing secrets. A profile name does not prove its effective role. Credential renewal and role trust configuration are different operations; this guide does not change either.

## ECR permissions

Repository creation, workstation publishing, and ECS pulling need different permissions. Publishing normally requires `ecr:GetAuthorizationToken` on `*`, and `ecr:BatchCheckLayerAvailability`, `ecr:InitiateLayerUpload`, `ecr:UploadLayerPart`, `ecr:CompleteLayerUpload`, `ecr:PutImage`, and `ecr:BatchGetImage` on `arn:aws:ecr:us-east-1:<AWS_ACCOUNT_ID>:repository/banking-app-dev-backend`. Read-back checks need their own read permissions. See [AWS image publishing](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-push-iam.html).

Match access-denied errors to the exact action, principal, region, and repository. Do not assume repository-management permissions include image publishing. The ECS execution role is for pulls/logging, not workstation publishing. Review effective policies, boundaries, and organization restrictions with the account owner rather than adding administrator access. The identity and exact permission changes used for the successful push still need to be recorded.

## Docker login on Windows PowerShell

Use Docker Desktop's Linux engine. PowerShell variables and continuation syntax differ from Bash. Authenticate to the registry host without the repository path/tag, using `--password-stdin`. The [project workflow](../README.md#deployment-workflow) documents the confirmed `cmd /c` workaround. An illustrative command, using a locally configured profile named `approved-publisher`, is:

```powershell
cmd /c "aws ecr get-login-password --region us-east-1 --profile approved-publisher | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com"
```

Replace `<AWS_ACCOUNT_ID>` with your account ID and `approved-publisher` with the actual authorized local profile before running the example. Angle-bracket placeholders are documentation only; cmd.exe interprets them as redirection if left unchanged. This is a reusable example, not the recorded literal command or profile from the deployment. `cmd /c` executes the pipeline in cmd.exe from PowerShell and passes the password over stdin. Its pipeline exit status reflects Docker, so also inspect AWS CLI failures. No token is printed or placed directly in command arguments. The confirmed use of this workaround does not establish the original failure's exact root cause.

Stop when token retrieval fails. A downstream non-interactive-login error can result from an empty password. Check profile, session expiration, region, and Docker availability. Never echo the ECR password or pass it as a visible command-line password. See the [AWS CLI publishing workflow](https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html).

## Build and image push

Use `backend/` from the Banking App project root as the Docker build context; the Dockerfile copies `requirements.txt` and `app/`. Tag with the full registry/repository/tag and confirm the repository exists. Successful login does not prove layer-upload or manifest-write permission.

For image-pull failures, check that `dev` exists, review ECS stopped-task reasons, execution-role permissions, and NAT routing. Check image compatibility with the task runtime when building on a different CPU architecture; the task definition does not explicitly set architecture. Overwriting a mutable tag does not replace running tasks. A rollout is a separate, explicitly authorized deployment operation.

## ECS health verification

In an authorized Console session, inspect:

1. Cluster `banking-app-dev-cluster` and service `banking-app-dev-backend-service`: desired/running counts, deployment status, events, stopped-task reasons.
2. ECR `banking-app-dev-backend`: `dev` tag/digest; compare with running tasks when investigating an older image.
3. Target group `banking-app-dev-tg`: health/reason codes, private target IPs on 8000, and AZ placement.
4. CloudWatch `/ecs/banking-app-dev-backend`: startup/request errors within seven-day retention.

For timeouts, check security groups and Uvicorn binding to `0.0.0.0:8000`. For HTTP failures, verify `/api/health` and status 200. The 60-second ECS grace period suppresses early health reactions; it does not make an unhealthy target healthy. See [AWS load-balancer health checks](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/load-balancer-healthcheck.html).

An operator can substitute the actual ALB DNS name:

```powershell
$AlbDnsName = '<actual-alb-dns-name>'
Invoke-RestMethod -Uri "http://${AlbDnsName}/api/health"
# Open http://<actual-alb-dns-name>/docs in a browser.
```

Expected JSON: `{"status":"healthy","service":"banking-api"}`. Swagger should show health. Accounts/transactions returning 404 is consistent with current startup registering only health. Port 443 allowed in a security group does not establish HTTPS: no certificate is passed and no HTTPS listener is active.

## State and remaining evidence

Saved plan artifacts may reflect older database-enabled configuration. Do not treat them as current deployment evidence or reapply them without review. RDS is disabled in the inspected dev file and owner's report; this review did not inventory AWS. Preserve state privately and create fresh reviewed plans for future changes.

Still to record: sanitized original errors, the approved publisher identity, exact IAM/policy changes, and real screenshots. The date, ECR digest, temporary MFA credential use, and `cmd /c` workaround are confirmed. HTTPS, RDS, and banking operations remain outside the verified development functionality. No screenshot or claim of a running task digest was inferred from the ECR digest alone.

## Teardown and preserved ECR

The owner confirmed this teardown incident and outcome:

1. The deployment role lacked `ec2:DisassociateAddress`, blocking completion of the EIP cleanup.
2. That permission was added to the deployment role.
3. The final EIP was destroyed and Terraform state became empty.
4. The ECR repository `banking-app-dev-backend`, containing image tag `dev`, was verified as ACTIVE after teardown.

These are owner-confirmed results, not AWS operations performed during this publication review. The exact permission statement/scope and teardown timestamp have not been supplied. No policy was changed by this review.

The ECR repository was removed from Terraform state to preserve it during destroy. Removing an object from state does not remove its resource block or import it automatically later. `terraform/modules/compute/main.tf` still declares `aws_ecr_repository.backend`; the task definition still references its repository URL with `:dev`. Before a future normal apply, an authorized operator must re-import the preserved repository into the correct workspace/state. From the project's `terraform/` directory, after initialization and restoration of the local dev variable file:

```powershell
terraform import -var-file=environments/dev/terraform.tfvars module.compute.aws_ecr_repository.backend banking-app-dev-backend
```

This is documentation only; it was not executed. Verify account, region, workspace, and existing state membership first. Then generate and review a fresh plan, confirming ECR is retained without replacement or deletion. Do not apply an old saved plan. Import brings the repository back under Terraform management, so future destruction requires another deliberate retention decision. Repository/image storage costs can continue despite empty Terraform state.

The import identifier is the repository name, as documented by the [AWS provider ECR resource reference](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecr_repository). Empty Terraform state alone does not establish that every AWS resource in the account was removed. The health endpoint and Swagger results above are historical Stage 1 evidence, not current availability claims.
