
import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from botocore.exceptions import BotoCoreError, ClientError

from app.core.security import get_current_user_id
from app.core.ai_security import check_sensitive_data, validate_ai_output
from app.services.bedrock_service import analyze_operations


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ops", tags=["AI Operations"])


class OpsRequest(BaseModel):
    description: str = Field(min_length=10, max_length=1000)


class OpsResponse(BaseModel):
    analysis: str


@router.post("/analyze", response_model=OpsResponse)
def analyze_ops(
    request: OpsRequest,
    current_user_id: int = Depends(get_current_user_id),
):
    try:
        # Step 1: Validate user input before calling Bedrock.
        check_sensitive_data(request.description)

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Operational description contains prohibited sensitive data.",
        )

    try:
        # Step 2: Generate operational analysis using Claude.
        analysis = analyze_operations(request.description)

    except (BotoCoreError, ClientError):
        logger.exception("Bedrock invocation failed")

        raise HTTPException(
            status_code=502,
            detail="AI operations service is temporarily unavailable.",
        )

    # Step 3: Validate the AI-generated response.
    try:
        validate_ai_output(analysis)

    except ValueError:
        logger.warning("AI output failed security validation")

        raise HTTPException(
            status_code=502,
            detail="AI response failed security validation.",
        )

    # Step 4: Return only validated AI output.
    return OpsResponse(analysis=analysis)
