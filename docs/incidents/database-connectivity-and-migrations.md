# PostgreSQL connectivity and Alembic migration failures

This report distinguishes a credential-rendering failure from a later network timeout. A successful migration does not prove that every earlier database error shared one cause.

## Incident A: PostgreSQL authentication rejected the migration connection

### Incident overview

An Alembic migration task received a PostgreSQL authentication error during the development deployment sequence.

### Symptoms and observed error

The log reports `FATAL: password authentication failed for user "bankadmin"` while connecting to a private address on port 5432. The credential itself is not included in the publication copy.

### Potential banking business impact

A blocked migration can delay a release or leave an application incompatible with the intended schema. No customer impact, data loss, or real transaction impact is evidenced.

### Investigation process

Check the migration task's DB host/name, secret version and field mapping, execution-role secret retrieval, password rendering, CA path/TLS mode, and task network. Avoid printing a password-bearing URL or secret value. Test reserved characters using synthetic credentials.

### Root cause

**Operator note:** an earlier Alembic version converted a SQLAlchemy URL object with `str(database_url)`. SQLAlchemy's string representation masked the password, causing the migration to receive an unusable URL. Git history first tracks the corrected migration environment; it does not contain the earlier local version, so the historical `str()` implementation is supported by the operator note rather than a committed diff.

### Corrective action

The migration configuration was corrected to call `render_as_string(hide_password=False)` for SQLAlchemy URL objects and then replace `%` with `%%` before setting Alembic's config option. The current [Alembic environment](../../backend/migrations/env.py) contains this logic. **Operator note:** the Docker image was rebuilt and pushed after the correction.

### Why the correction worked

SQLAlchemy hides passwords in ordinary string conversion. Alembic requires the password-bearing URL to connect, while its configuration parser treats `%` as interpolation syntax. Explicit rendering plus percent escaping preserves the intended URL through both steps.

### Recovery validation

The [ECR push screenshot](../screenshots/evidence/ecr/dev-image-pushed.png) records uploaded image layers with repository and digest masked. A later [migration log](../screenshots/evidence/database-migrations/alembic-revision-applied.png) records the Alembic revision upgrade. These support the later image/migration sequence; no credential values are published.

### Preventive recommendations

- Use structured SQLAlchemy URL creation and explicit rendering where Alembic config interpolation is involved.
- Never print/log a password-bearing URL.
- Test reserved characters using synthetic values.
- Pin the image digest/task-definition revision used for the migration.
- Verify the Alembic head and application readiness before routing traffic.

## Incident B: standalone migration task timed out

### Incident overview

A later standalone migration task timed out while connecting to PostgreSQL. This is a network symptom, distinct from an authentication rejection.

### Symptoms and observed error

The task log reports a SQLAlchemy/Psycopg `ConnectionTimeout` and `connection timeout expired`.

### Potential banking business impact

A timeout can block a schema release or delay service recovery. No real user, transaction, or data impact is evidenced.

### Investigation process

Check the task ENI, VPC, selected private subnets and security groups; confirm backend-SG egress and RDS-SG ingress on TCP 5432; then check DNS, routes, RDS status, and logs. A timeout alone does not identify a security-group cause.

### Root cause

**Operator note:** the task was launched without the intended backend security group. The timeout's root cause is therefore recorded from the operator account; the available network screenshot shows private subnet selection but does not show the chosen group.

### Corrective action

**Operator note:** the migration task was relaunched with the correct backend security group and the migration succeeded. The [RDS security-group report](rds-security-group-connectivity.md) keeps this separate from a different November 19 connection-closed log.

### Why the correction worked

RDS permits PostgreSQL traffic from the backend security group on TCP 5432. Attaching the intended group restores the allowed task-to-database path without opening the database to public CIDRs.

### Recovery validation

The later [Alembic task log](../screenshots/evidence/database-migrations/alembic-revision-applied.png) records a revision upgrade. The screenshot does not display the SG selection, so the task relaunch details remain operator-provided.

### Preventive recommendations

- Make migration task network settings explicit and review subnet/SG selection before launch.
- Use only backend-SG-to-database-SG ingress on TCP 5432.
- Correlate task and RDS events by timestamp and task identity.
- Validate database readiness from the same release after a network change.

## Related implementation and configuration notes

- [SQLAlchemy URL/TLS setup](../../backend/app/db/database.py)
- [Alembic environment](../../backend/migrations/env.py)
- [Initial schema revision](../../backend/migrations/versions/d368608d12af_create_initial_banking_tables.py)
- [RDS and security groups](../../terraform/modules/database/main.tf)
- [RDS security-group incident](rds-security-group-connectivity.md)
- [Incident index](README.md)

**RDS backup retention:** **Operator note:** retention was reduced to one day following a development-account restriction. The current Terraform value corroborates one-day retention, but the restriction/error screenshot and previous value are not available. This is a development constraint, not a verified production backup incident.
