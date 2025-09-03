from fastapi import APIRouter, Path, Query
from typing import Optional
from . import schemas
from .exception import ErrorCode
from .controllers import InvoiceController

router = APIRouter(prefix="/v1/invoice", tags=["invoice"])
controller = InvoiceController()


@router.post("/checkout/{user_id}", status_code=201, responses={
    201: {"model": schemas.InvoiceResponse, "description": "Create items success"},
})
async def checkout_invoice(user_id: str = Path(...)):
    result = await controller.checkout_cart(user_id)
    if not result:
        raise ErrorCode.InvoiceNotFound()
    return result


@router.get("/get/{invoice_id}", status_code=200, responses={
    200: {"model": schemas.InvoiceResponse, "description": "Get items success"},
})
async def get_invoice(invoice_id: str = Path(...)):
    result = await controller.get(invoice_id)
    if not result:
        raise ErrorCode.InvalidInvoiceId()
    return result


@router.put("/edit/{invoice_id}", status_code=200, responses={
    200: {"model": schemas.InvoiceResponse, "description": "Edit items success"},
})
async def update_invoice(invoice_id: str, data: schemas.InvoiceUpdate):
    result = await controller.update(invoice_id, data.model_dump(exclude_unset=True))
    return schemas.InvoiceResponse(**result)


@router.delete("/delete/{invoice_id}", status_code=200, responses={
    200: {"description": "Xóa invoice thành công"},
})
async def delete_invoice(invoice_id: str):
    result = await controller.delete(invoice_id)
    return result


@router.get("/search", status_code=200, responses={
    200: {"model": schemas.PaginatedInvoiceResponse, "description": "Get items success"},
})
async def list_invoices(
    page: int = Query(1, gt=0, description="Số trang"),
    limit: int = Query(10, le=100, description="Số item / mỗi trang"),
    user_id: Optional[str] = Query(None, description="Lọc theo user"),
    status: Optional[str] = Query(None, description="Lọc theo trạng thái"),
):
    query = {}
    if user_id: query["user_id"] = user_id
    if status: query["status"] = status

    result = await controller.search(query, page, limit)
    return result
