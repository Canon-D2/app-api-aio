from fastapi import APIRouter, Path
from . import schemas
from .controllers import TaxController

router = APIRouter(prefix="/v1/tax", tags=["tax"])
controller = TaxController()


@router.post("/fetch/{tax_code}", status_code=201, responses={
                201: {"model": schemas.TaxResponse, "description": "Fetch items success"}})
async def get_tax(tax_code: str = Path(..., title="Tax Code Company", description="No space in tax code")):
    result = await controller.get_tax(tax_code)
    return result
