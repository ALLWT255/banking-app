# ECS Secrets Manager access denial

**Classification:** Candidate controlled break/fix. **Outcome:** A later task-startup screenshot is consistent with recovery but does not prove the denied secret access was corrected on the same role/task.

## 1. Incident overview

The screenshot intake contains an ECS Secrets Manager access-denied image followed by a screenshot labeled as access restored. The later CloudWatch view shows Uvicorn startup complete.

## 2. Symptoms and observed error

The screenshot records `secretsmanager:GetSecretValue` denied while ECS attempted startup-time secret retrieval under the execution role. The secret ARN and complete error context are omitted from this public report.

## 3. Potential banking business impact

If ECS cannot retrieve required database/JWT secrets, tasks may fail initialization or the application may be unable to authenticate/connect to its database. No user impact is evidenced.

## 4. Investigation process

Identify whether ECS secret injection failed under the **execution role** (not the application task role); verify the exact secret ARN, execution-role trust, `GetSecretValue`, optional customer-managed KMS decrypt/key policy, region, and secret JSON key names. Review stopped-task reason and startup logs without exposing secret values.

## 5. Root cause

Not confirmed from a readable error transcript. The source name suggests a Secrets Manager permission issue; the role/policy delta and any KMS dependency are not shown.

## 6. Corrective action

The later image is labeled as access restored. The repository's Terraform execution-role policy grants `secretsmanager:GetSecretValue` on the supplied DB and JWT secret ARNs. The exact change performed during the screenshot sequence is not evidenced.

## 7. Why the correction may have worked

ECS uses the execution role to retrieve task-definition secrets before the container starts. Granting the narrowly required secret read to that role can allow initialization; a task role policy is not a substitute.

## 8. Recovery validation

A later screenshot shows the application startup complete at 08:59 on November 20. It does not show the role update, secret retrieval event, same task identity, or a successful `/api/ready` response. Recovery is **indicated but not confirmed**.

## 9. Preventive recommendations

- Document role ownership: execution role for startup injection; task role for runtime AWS API calls.
- Scope secret reads to the exact secret ARN and review KMS key policy when applicable.
- Validate secret JSON keys and rotation/version behavior without printing values.
- Capture ECS stopped reason and confirm readiness from the same release after repair.
- Never publish screenshots with secret ARNs/account IDs unless redacted.

## 10. Associated evidence

Original screenshots are named `46-ecs-secrets-manager-access-denied` and `47-ecs-secrets-manager-access-restored`. They contain resource identifiers and remain in the ignored unredacted intake folder; because the denial and recovery could not be correlated reliably, no screenshot derivative is published.

## Related documentation

- [IAM module](../../terraform/modules/iam/main.tf)
- [ECS task definition](../../terraform/modules/compute/main.tf)
- [Architecture](../architecture.md)
- [Incident index](README.md)
