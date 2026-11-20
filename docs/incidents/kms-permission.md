# KMS key metadata permission failure

**Classification:** Deployment/operator permission troubleshooting. **Outcome:** Key-state evidence follows the permission update; end-to-end RDS recovery is not established by this evidence alone.

## Incident overview

The intake includes screenshots named for RDS KMS key access and `kms:DescribeKey` denial, followed by a deployment-role permission update and a key-state check. One screenshot labeled `11-rds-kms-key-not-accessible.png` is an exact duplicate of a Terraform plan screenshot, so it is not treated as independent KMS evidence.

## Symptoms and observed errors

The source filenames indicate a KMS key access/metadata permission failure and a `DescribeKey` access-denied check for an AWS-managed RDS key alias. The unredacted terminal evidence is retained locally; the image content is not sufficiently reliable to quote an exact error string in this publication copy.

## Potential banking business impact

Missing KMS permissions can block an authorized infrastructure operator from inspecting or configuring encrypted resources and can delay database provisioning/recovery. No database outage, lost data, or customer impact is established.

## Investigation process

Identify whether the failing principal needs key metadata visibility or cryptographic use; inspect the exact denied action, target key, region, caller identity, and key policy. Confirm that the key exists and is enabled, and distinguish AWS-managed key behavior from customer-managed key policy requirements. Do not grant decrypt or key-administration permissions without a demonstrated need.

## Root cause

The sequence is consistent with the deployment identity lacking a required KMS metadata permission. The precise effective policy, service request, and whether the initial failure blocked RDS creation are not established by the available screenshot text.

## Corrective action

A later image is labeled as an updated deployment-role KMS permission set, and another shows a successful key-state query. Exact action/resource scope cannot be safely reconstructed from the visible evidence and is not stated as a policy recipe.

## Why the correction worked

Allowing the exact required metadata operation for the relevant key can let Terraform/operator diagnostics inspect key state. That does not automatically grant encryption/decryption access, override a key policy, or prove RDS connectivity.

## Recovery validation

The follow-up key check reports the key as enabled, according to the screenshot context. No correlated RDS apply/connection test is included in this incident evidence, so the incident is only partially validated.

## Preventive recommendations

- Capture exact denial details with secrets and account identifiers redacted.
- Validate the minimum KMS action/resource through policy simulation and an authorized operation.
- Review key policies, IAM policies, boundaries, and organization controls together.
- Keep development and production key policies distinct; avoid wildcard KMS grants.
- Verify database provisioning/connectivity separately from key metadata checks.

## Associated evidence

KMS-related originals remain in the ignored intake folder because the visible account/resource context is not suitable for publication. One screenshot labeled for KMS is an exact duplicate of a Terraform plan and is not independent KMS evidence. No public before/after image is included; the partial outcome above is based on the remaining screenshot sequence.

## Related documentation

- [Terraform IAM module](../../terraform/modules/iam/main.tf)
- [Security design](../security-design.md)
- [Incident index](README.md)
