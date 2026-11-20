# AI security evidence

The [curated security screenshot](../evidence/ai-security-validation/auth-and-injection-statuses.png) is a redacted copy of a November 20 CloudWatch task log. It shows missing JWT `401`, invalid JWT `401`, selected sensitive input `400`, and one prompt-injection test request returning `200`. That status alone does not establish that the prompt was blocked or that prompt-injection controls are complete.

The HTTP 200 means the request reached the model and returned a response; it does not prove complete prompt-injection resistance. The response text is not a security guarantee. Local source tests additionally cover sensitive input rejection, mocked Bedrock failure handling, unsafe-output rejection, and a known false positive.

Historical November 17 cloud results recorded four checks: missing authentication 401, invalid JWT 401, sensitive input 400, authenticated AI request 200. These used a synthetic JWT inside a private Fargate test task, not public authenticated ALB traffic.

Raw AI screenshots remain in the ignored source intake because they may contain task IDs, account details, paths, or prompt content. See the [complete screenshot inventory](../README.md), [AI operations design](../../ai-operations.md), and [security design](../../security-design.md).
