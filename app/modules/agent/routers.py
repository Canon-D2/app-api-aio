from fastapi import APIRouter
from . import schemas
from .controllers import GeminiController, OpenAIController

router = APIRouter(prefix="/v1/ai", tags=["AI"])

gemini_controller = GeminiController()
openai_controller = OpenAIController()


@router.post("/gemini", status_code=200, responses={
                200: {"model": schemas.Response, "description": "Generate via Gemini"}})
async def generate_gemini(data: schemas.GeminiRequest):
    result = await gemini_controller.generate(data.content, data.model, data.prompt)
    return schemas.Response(generate=result)


@router.post("/openai", status_code=200, responses={
                200: {"model": schemas.Response, "description": "Generate via OpenAI"}})
async def generate_openai(data: schemas.OpenAIRequest):
    result = await openai_controller.generate(data.content, data.model, data.prompt)
    return schemas.Response(generate=result)
