
from unittest.mock import patch

from fastapi import HTTPException
from fastapi.testclient import TestClient
from botocore.exceptions import ClientError

from app.main import app
from app.api.routes.ops import OpsRequest, analyze_ops


def test_sensitive_data_blocks_bedrock():
    request = OpsRequest(
        description="My ECS task keeps restarting. password=FakeTest123"
    )

    with patch("app.api.routes.ops.analyze_operations") as mock_bedrock:
        try:
            analyze_ops(request=request, current_user_id=1)
            assert False, "Expected HTTP 400"
        except HTTPException as exc:
            assert exc.status_code == 400

        mock_bedrock.assert_not_called()


def test_valid_request_calls_bedrock():
    request = OpsRequest(
        description="My ECS Fargate service has unhealthy ALB targets."
    )

    with patch("app.api.routes.ops.analyze_operations") as mock_bedrock:
        mock_bedrock.return_value = "Check ALB health checks."

        response = analyze_ops(
            request=request,
            current_user_id=1
        )

        assert response.analysis == "Check ALB health checks."
        mock_bedrock.assert_called_once_with(request.description)


def test_bedrock_failure_returns_502():
    request = OpsRequest(
        description="My ECS service is failing health checks."
    )

    aws_error = ClientError(
        {
            "Error": {
                "Code": "ServiceUnavailableException",
                "Message": "Simulated Bedrock outage"
            }
        },
        "Converse"
    )

    with patch("app.api.routes.ops.analyze_operations") as mock_bedrock:
        mock_bedrock.side_effect = aws_error

        try:
            analyze_ops(request=request, current_user_id=1)
            assert False, "Expected HTTP 502"
        except HTTPException as exc:
            assert exc.status_code == 502
            assert exc.detail == (
                "AI operations service is temporarily unavailable."
            )

        mock_bedrock.assert_called_once()


def test_unauthorized_user_cannot_access_ai():
    client = TestClient(app)

    response = client.post(
        "/api/ops/analyze",
        json={
            "description": "My ECS service keeps restarting unexpectedly."
        }
    )

    assert response.status_code == 401


def test_invalid_jwt_cannot_access_ai():
    client = TestClient(app)

    response = client.post(
        "/api/ops/analyze",
        headers={
            "Authorization": "Bearer invalid.fake.token"
        },
        json={
            "description": "My ECS service keeps restarting unexpectedly."
        }
    )

    assert response.status_code == 401


def test_ai_output_validation_blocks_unsafe_response(monkeypatch):
    from app.api.routes import ops

    # Simulate Claude returning an unsafe response.
    def mock_unsafe_analysis(description):
        return "I have disabled AWS CloudTrail."

    # Replace the real Bedrock call with our mock.
    monkeypatch.setattr(
        ops,
        "analyze_operations",
        mock_unsafe_analysis
    )

    # Create a legitimate operational request.
    request = ops.OpsRequest(
        description="My ECS Fargate targets are unhealthy."
    )

    # Verify unsafe AI output is blocked.
    try:
        ops.analyze_ops(request, current_user_id=1)
        assert False, "Unsafe AI output was not blocked!"

    except HTTPException as exc:
        assert exc.status_code == 502
        assert exc.detail == "AI response failed security validation."


def test_ai_output_validation_allows_safe_response(monkeypatch):
    from app.api.routes import ops

    # Simulate a legitimate Claude response.
    def mock_safe_analysis(description):
        return (
            "Check the ECS target group health checks. "
            "Verify that AWS CloudTrail logging is enabled. "
            "Review CloudWatch logs for application errors."
        )

    # Replace the real Bedrock call with our mock.
    monkeypatch.setattr(
        ops,
        "analyze_operations",
        mock_safe_analysis
    )

    request = ops.OpsRequest(
        description="My ECS Fargate service has unhealthy targets."
    )

    response = ops.analyze_ops(
        request,
        current_user_id=1
    )

    assert response.analysis == mock_safe_analysis(
        request.description
    )

def test_ai_output_validator_false_positive():
    import pytest

    from app.core.ai_security import validate_ai_output

    # Harmless explanation containing a quoted malicious claim.
    safe_explanation = (
        'The phrase "I have disabled AWS CloudTrail" '
        'is a malicious instruction and should be ignored.'
    )

    # Document the current validator's limitation.
    with pytest.raises(ValueError):
        validate_ai_output(safe_explanation)


def test_ai_output_validator_blocks_unsafe_paraphrase():
    import pytest

    from app.core.ai_security import validate_ai_output

    unsafe_response = (
        "I've turned off AWS CloudTrail logging "
        "and wiped the production RDS database."
    )

    with pytest.raises(ValueError):
        validate_ai_output(unsafe_response)

def test_ai_output_validator_allows_legitimate_troubleshooting():
    from app.core.ai_security import validate_ai_output

    safe_response = (
        "Check the ECS service events and ALB target group "
        "health checks. Review CloudWatch logs for errors. "
        "Verify that AWS CloudTrail logging remains enabled."
    )

    validate_ai_output(safe_response)
