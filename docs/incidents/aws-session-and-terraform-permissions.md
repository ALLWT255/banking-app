# AWS session and Terraform permission failures

**Classification:** Deployment/operator troubleshooting, not an observed customer outage. **Outcome:** The documented deployment subsequently completed; current AWS access was not checked.

## Incident overview

The deployment sequence includes invalid AWS session-token evidence, an MFA/role recovery sequence, and Terraform access-denied errors while creating infrastructure. These are related operational blockers but have different causes: credential validity is not the same as authorization.

## Symptoms and observed errors

The session screenshots record `InvalidClientTokenId` during role assumption and an `iam:ListMFADevices` access denial during MFA recovery. Terraform deployment screenshots record access-denied failures for `rds:CreateDBSubnetGroup` and `iam:PutRolePolicy`. Complete error text and effective principal are not available in a clean transcript here.

## Potential banking business impact

If an authorized operator cannot provision or repair the stack, a planned release or recovery can be delayed. No customer outage, real-customer impact, or financial loss is evidenced.

## Investigation process

Separate credential-chain failure from IAM authorization:

1. Confirm the selected AWS profile and region without printing credentials.
2. Verify caller identity after obtaining fresh approved temporary credentials.
3. For each `AccessDenied`, capture action, resource, principal, region, and request time.
4. Compare the required action with identity policy, permission boundary, trust policy, SCP, and resource/KMS policy.
5. Re-run a fresh plan and inspect the exact proposed resource set before apply.

## Root cause

The credential screenshot names indicate an invalid/expired or otherwise unusable temporary session; the later screenshot shows an assumed role/caller identity succeeding. Terraform also lacked one or more provisioning permissions for the actions denied in the deployment screenshots. The exact session expiry cause and full policy delta are not preserved, so no more specific root cause is asserted.

## Corrective action

The evidence sequence shows an MFA-backed role/session succeeding after the invalid-token state and deployment-role permissions being updated. A later infrastructure apply completed with nine resources added. The exact policy document and scope used for that recovery are not available; this report does not recommend broad administrator access.

## Why the correction worked

Fresh valid temporary credentials restore a usable AWS identity; adding only the missing authorized provisioning actions allows Terraform to perform those operations. These are distinct fixes and should be validated separately.

## Recovery validation

The screenshot sequence includes successful role/caller-identity output and a later Terraform apply summary with nine resources added and no reported errors. Stage 2 deployment records also report a completed deployment. This verifies historical recovery of the documented deployment flow, not current credentials or current infrastructure state.

## Preventive recommendations

- Use role federation/MFA and short-lived sessions; never copy session tokens into files or screenshots.
- Verify caller identity before Terraform operations.
- Maintain a documented, reviewed least-privilege deployment policy and inspect exact denied actions.
- Keep provisioning, image publishing, ECS execution, and application task roles separate.
- Use a fresh plan after policy or partial-apply recovery; protect state and plan artifacts.
- Avoid printing credentials or full resource ARNs in shared logs.

## Associated evidence

The original AWS session and Terraform permission screenshots remain in the ignored intake folder because they contain account, role, or MFA context. No public derivative is included. The report relies on the preserved deployment sequence and repository history; see the [screenshot inventory](../screenshots/README.md) for intake handling.

## Related documentation

- [Terraform IAM module](../../terraform/modules/iam/main.tf)
- [Architecture](../architecture.md)
- [Troubleshooting index](../troubleshooting.md)
