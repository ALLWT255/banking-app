import re

SENSITIVE_PATTERNS = {
    "AWS access key": r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    "Bearer token": r"(?i)\bBearer\s+\S+",
    "Password assignment": r"(?i)\bpassword\s*[:=]\s*\S+",
}


def check_sensitive_data(description: str) -> None:
    for name, pattern in SENSITIVE_PATTERNS.items():
        if re.search(pattern, description):
            raise ValueError(
                f"Sensitive information detected: {name}"
            )


PROHIBITED_ACTION_CLAIMS = [
    # CloudTrail modification claims
    r"\bI(?:'ve| have| already)?\s+(?:disabled|turned off|shut off|stopped)\s+(?:AWS\s+)?CloudTrail(?:\s+logging)?\b",

    # Database destruction claims
    r"\bI(?:'ve| have| already)?\s+(?:deleted|wiped|destroyed|dropped|removed)\s+(?:the\s+)?(?:production\s+)?(?:RDS\s+)?database\b",
]


def validate_ai_output(analysis: str) -> None:
    # Check generated output for sensitive data.
    check_sensitive_data(analysis)

    # Check for prohibited infrastructure action claims.
    for pattern in PROHIBITED_ACTION_CLAIMS:
        if re.search(pattern, analysis, flags=re.IGNORECASE):
            raise ValueError(
                "AI output contains a prohibited infrastructure action claim."
            )
