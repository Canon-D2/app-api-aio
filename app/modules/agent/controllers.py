from .services import gemini_services, openai_services
from .exception import ErrorCode


class GeminiController:
    def __init__(self):
        self.service = gemini_services

    async def generate(self, content: str, model: str, prompt: None):
        try:
            return await self.service.generate(content, model, prompt)
        except Exception as e:
            raise ErrorCode.GeminiError(str(e))


class OpenAIController:
    def __init__(self):
        self.service = openai_services

    async def generate(self, content: str, model: str, prompt: None):
        try:
            return await self.service.generate(content, model, prompt)
        except Exception as e:
            raise ErrorCode.OpenAIError(str(e))
