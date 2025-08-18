from fastapi import status
from fastapi.exceptions import HTTPException


class StandardException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=kwargs.get("status", 400), detail=kwargs)


class ErrorCode:
    @staticmethod
    def GeminiError(message: str = ""):
        return StandardException(
            type="ai/error/gemini-failed",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="Gemini Service Error",
            detail=message or "An unexpected error occurred while calling Gemini."
        )

    @staticmethod
    def OpenAIError(message: str = ""):
        return StandardException(
            type="ai/error/openai-failed",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="OpenAI Service Error",
            detail=message or "An unexpected error occurred while calling OpenAI."
        )
