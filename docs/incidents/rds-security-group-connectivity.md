# RDS security-group connectivity follow-up

**Classification:** Development connectivity troubleshooting. **Outcome:** The intake includes a connection failure and a follow-up image labeled as a security-group recovery; an application-level post-change readiness result is not correlated to this event.

## 1. Incident overview

CloudWatch evidence dated November 19 shows the backend failing while opening a PostgreSQL connection. A later screenshot is named as RDS connectivity restored through a backend security-group change.

## 2. Symptoms and observed error

The visible log reports that the server at a private `10.0.12.x` address on port 5432 closed the connection unexpectedly. It also indicates an abnormal server termination or connection processing interruption. This is not the same symptom as `password authentication failed`.

## 3. Potential banking business impact

If active, database connection failures could block login, account reads, or transaction processing. No customer data, real transaction, outage duration, or financial impact is evidenced.

## 4. Investigation process

Check RDS health/events and endpoint, task-to-RDS route, security-group ingress/egress, task ENI/security group, TLS mode/CA bundle, and PostgreSQL logs. Confirm diagnosis from the same task and timestamp; do not conclude that a security group is responsible from a connection error alone.

## 5. Root cause

Not conclusively established. The follow-up filename suggests a security-group correction, but the available log does not prove that the SG was the cause of the server closing the connection.

## 6. Corrective action

The original is labeled as a backend security-group restoration. The precise rule delta and change record are not available, so no CIDR-wide rule or exact change is claimed. The intended source relationship in Terraform is backend SG to database SG on port 5432.

## 7. Why the correction may have worked

Allowing only the backend security group to reach the database on TCP 5432 is consistent with the Terraform segmentation and can resolve a blocked connection path. It would not by itself resolve a database process failure, bad credentials, or TLS trust error.

## 8. Recovery validation

The later screenshot is not an explicit `/api/ready` or successful SQL query tied to the same deployment/task. The event is therefore **not marked fully recovered** here. Earlier November 17 readiness evidence is not a post-November 19 validation.

## 9. Preventive recommendations

- Use the backend SG as the database SG ingress source; avoid public CIDRs.
- Test `/api/ready` from the ALB and a private task after changing rules.
- Correlate CloudWatch/RDS events and record the changed rule, principal, and validation.
- Use PostgreSQL TLS verification and distinguish network, TLS, authentication, and server faults.

## 10. Associated evidence

![RDS connection failure, with task identifier and private address masked](../screenshots/evidence/database-migrations/rds-connection-failed.png)

The screenshot named `44-rds-connectivity-restored-backend-security-group.png` remains in the ignored original set and requires review before publication; no derivative is linked because the screenshot itself did not establish application readiness.

## Related documentation

- [Security-group module](../../terraform/modules/security/main.tf)
- [RDS module](../../terraform/modules/database/main.tf)
- [Database TLS implementation](../../backend/app/db/database.py)
- [Troubleshooting index](../troubleshooting.md)
