from typing import Optional
from fastapi import APIRouter, Query, Path
from . import schemas
from .controllers import EventController, TicketController

router = APIRouter(prefix="/v1/fes", tags=["festival"])

event_controller = EventController()
ticket_controller = TicketController()


@router.post("/event/create", status_code=201, responses={
                201: {"model": schemas.EventResponse, "description": "Create items success"}})
async def create_event(data: schemas.EventCreate):
    result = await event_controller.create(data.model_dump())
    return result


@router.get("/event/get/{event_id}", status_code=200, responses={
                200: {"model": schemas.EventResponse, "description": "Get items success"}})
async def get_event(event_id: str = Path(...)):
    result = await event_controller.get(event_id)
    return result


@router.put("/event/edit/{event_id}", status_code=200, responses={
                200: {"model": schemas.EventResponse, "description": "Edit items success"}})
async def update_event(event_id: str, data: schemas.EventUpdate):
    result = await event_controller.update(event_id, data.model_dump(exclude_unset=True))
    return result


@router.delete("/event/delete/{event_id}", status_code=200, responses={
                200: {"description": "Delete items success"}})
async def delete_event(event_id: str):
    result = await event_controller.delete(event_id)
    return result


@router.get("/event/search", status_code=200, responses={
                200: {"model": schemas.PaginatedEventResponse, "description": "Get items success"}})
async def list_event(
    page: int = Query(1, gt=0),
    limit: int = Query(10, le=100),
    name: Optional[str] = None
):
    query = {}
    if name: query["name"] = {"$regex": name, "$options": "i"}

    result = await event_controller.search(query, page, limit)
    return result


@router.post("/ticket/check-out", status_code=201, responses={
                201: {"model": schemas.TicketResponse, "description": "Create items success"}})
async def checkout_tickets(data: schemas.CheckoutRequest):
    result = await ticket_controller.checkout(data.model_dump())
    return result


@router.post("/ticket/check-in", status_code=200, responses={
                201: {"model": schemas.TicketResponse, "description": "Edit items success"}})
async def checkin_ticket(data: schemas.CheckinRequest):
    result = await ticket_controller.checkin(data)
    return result


@router.post("/ticket/change-status", status_code=200, responses={
                201: { "description": "Edit items success"}})
async def cofirm_pay(ticket_id: str, status: str):
    result = await ticket_controller.cofirm_pay(ticket_id, status)
    return result


@router.get("/ticket/search", status_code=200, responses={
                200: {"model": schemas.PaginatedTicketResponse, "description": "Get items success"}})
async def list_ticket(
    page: int = Query(1, gt=0),
    limit: int = Query(10, le=100),
    event_id: Optional[str] = None,
    user_id: Optional[str] = None,
    type: Optional[str] = None,
    status: Optional[str] = None

):
    query = {}
    if event_id: query["event_id"] = {"$regex": event_id, "$options": "i"}
    if user_id: query["user_id"] = {"$regex": user_id, "$options": "i"}
    if type: query["type"] = {"$regex": type, "$options": "i"}
    if status: query["status"] = {"$regex": status, "$options": "i"}

    result = await ticket_controller.search(query, page, limit)
    return result

@router.get("/ticket/qr/{ticket_id}", status_code=200, responses={
                200: {"description": "Get items success"}})
async def get_ticket_qr(ticket_id: str, format: str = Query(enum=["base64", "image"])):
    result = await ticket_controller.qr_code(ticket_id, format)
    return result