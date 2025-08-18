from openai import OpenAI
from .config import OPENAI_API_KEY, GEMINI_API_KEY, GEMINI_BASE_URL


openai_client = OpenAI(api_key=OPENAI_API_KEY)
gemini_client = OpenAI(api_key=GEMINI_API_KEY, base_url=GEMINI_BASE_URL)


class GeminiServices:
    def __init__(self, client: OpenAI):
        self.client = client

    async def generate(self, content: str, model: str, prompt: None):
        messages = []
        if prompt:
            messages.append({"role": "system", "content": prompt})
        messages.append({"role": "user", "content": content})

        resp = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return resp.choices[0].message.content



class OpenAIServices:
    def __init__(self, client: OpenAI):
        self.client = client

    async def generate(self, content: str, model: str, prompt: None):
        messages = []
        if prompt:
            messages.append({"role": "system", "content": prompt})
        messages.append({"role": "user", "content": content})

        resp = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return resp.choices[0].message.content


gemini_services = GeminiServices(gemini_client)
openai_services = OpenAIServices(openai_client)
