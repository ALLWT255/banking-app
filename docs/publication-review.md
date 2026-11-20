# GitHub publication and sensitive-data review

**Review date:** November 20, 2026
**Scope:** Current repository source/docs, local Git state/history, ignored artifact candidates, and screenshot intake filenames/content that could be visually inspected. This is a practical review, not a guarantee that every secret format or image region was detected.

## Repository and history

- Current branch at review start: `main`, tracking `origin/main`.
- Git history available locally: four commits through the November 17 Stage 2 deployment commit.
- Tracked worktree was clean before documentation edits. The screenshot intake directory was untracked.
- No commit or push was made for this update.
- The new `.gitignore` rule keeps the original unredacted screenshot intake local; curated redacted copies are stored separately under `docs/screenshots/evidence/`.

## Sensitive material and publication handling

The original screenshots are not safe to publish as a set. They remain unmodified in `docs/screenshots/banking-appdocsscreenshots/` and are excluded from Git. Notable items observed or indicated by filenames include:

- `18-fastapi-startup-resolved.png` visibly prints a generated `JWT_SECRET_KEY` value in a terminal session. Treat it as sensitive; do not publish it. The screenshot does not establish whether the value remains active or was reused. If it was used beyond disposable local testing, rotate/revoke it through the approved owner workflow.
- AWS account IDs, role/secret/task ARNs, resource identifiers, private IPs, and an MFA device ARN appear in several AWS Console/CLI screenshots.
- Windows terminal screenshots expose the local profile name and project path.
- `25-corrected-alembic-docker-image-pushed.png` exposes an AWS account identifier and image digest.
- Browser screenshots may expose URL/resource details, browser chrome/bookmarks, and operational context.
- No credential/token/password in the displayed AI test screenshot was observed, but prompt text and model output are operational content and should be minimized.

Only reviewed derivatives are intended for publication. Redaction uses opaque masks/cropping; the originals are not altered. Curated copies linked from the README and incident reports were visually checked after processing. Uncurated screenshots remain outside the publishable set; do not add the raw intake folder.

No clearly healthcare-specific infrastructure screenshot was identified from the reviewed filenames/previews. Two generic historical-development images (`test installaization ...` and `website GET operation success ...`) remain excluded pending owner confirmation; do not use them as banking evidence. No screenshot known to show backend port 5000 is included in curated evidence.

## Tracked files and exclusions

`.gitignore` excludes Terraform `.tfstate`/backups, `.tfplan`/plans, `.tfvars`, `.env`, provider cache, Python virtual environments, local databases, credentials, private keys, and logs. Local copies of state, plans, ignored development variables, `.venv`, and test databases exist and must remain untracked.

The public CA bundle `backend/certs/global-bundle.pem` is intentionally allowed by a specific exception after the `*.pem` rule. Preserve it; it is a public AWS RDS CA bundle, not a private key.

Do not force-add ignored files. Before commit, review both staged paths and content, not only `.gitignore`:

```powershell
git status --short --ignored
git diff --check
git diff --cached --name-only
git diff --cached --check
```

## Claims and limitations

- Stage 1 and Stage 2 deployment statements are historical, dated evidence; this review did not query AWS and does not claim that services are currently running.
- Staging and production are not deployed or configured in tracked files.
- Public development HTTP, Single-AZ RDS, one NAT Gateway, mutable ECR tag, local state, master-user DB credential use, short backup retention, and missing production observability/CI remain limitations.
- No backup-retention incident or SQLAlchemy password-masking root cause is substantiated by reviewed evidence.
- Prompt-based defenses/regex are not complete prompt-injection or data-loss-prevention controls.
- No production-readiness, availability SLA, regulatory compliance, or full banking transaction claim is made.

## Validation and remaining publication work

- The local backend suite passed during this documentation update: **19 passed**, with one Starlette test-client deprecation warning.
- All 149 local Markdown file references, including 19 image references, resolved to existing files or directories; links to unredacted/non-publishable AWS session and KMS screenshots were removed rather than left broken.
- No AWS commands, deployment, destroy, or infrastructure changes were performed for this update.

1. Owner review remains necessary for raw originals and the JWT secret visible in `18-fastapi-startup-resolved.png`; if it was used beyond disposable local testing, rotate/revoke it.
2. Keep the unredacted intake directory ignored and do not stage it.
3. Before any commit, inspect the complete staged diff and rerun secret/path checks.

## Related documentation

- [Screenshot inventory and evidence](screenshots/README.md)
- [Security design](security-design.md)
- [Troubleshooting](troubleshooting.md)
- [Architecture](architecture.md)
