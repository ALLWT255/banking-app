# Deployment screenshots

Place sanitized evidence here. No screenshots were present during documentation preparation, so the Banking App README embeds no images and links to no nonexistent image files.

| Suggested filename | Capture |
| --- | --- |
| `terraform-apply.png` | Completed summary: 34 added, 0 changed, 0 destroyed |
| `ecr-image.png` | Repository, `dev` tag, digest and push time |
| `ecs-service.png` | Service name, desired/running counts and deployment status |
| `healthy-targets.png` | Two healthy port-8000 targets across both AZs |
| `api-health.png` | HTTP health response with status and service name |
| `swagger-ui.png` | Swagger showing the deployed health route |

Capture actual evidence, not mockups. Record capture dates and what each image proves. Crop credentials, passwords, MFA/session tokens, private terminal history, and unrelated account details. Review Console URLs/account identifiers before publication. Never capture full state, plan payloads, or environment files.

Once a file exists and is reviewed, embed it in the Banking App README using `docs/screenshots/<actual-filename>` and descriptive alt text. Match case exactly. Health evidence does not prove banking operations or database integration.

The verified deployment date is October 30, 2026. Compare ECR evidence with digest `sha256:3fe7c32bc744e6749cda39018f645680921555191b1ae3babc7dfd35cad8f57d`. Record the actual screenshot capture date separately if captured later. Store real images only in this directory; no placeholder images have been created.

Stage 1 was torn down after deployment verification. Label historical screenshots as historical; do not imply the API is still running. Optional real cleanup evidence may show the final EIP deletion, an empty Terraform resource list, and the preserved ECR repository/image status. Never capture state payloads or credentials. These evidence files have not been supplied and no images were generated.
