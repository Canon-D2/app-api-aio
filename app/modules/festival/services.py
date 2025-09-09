from app.mongo.base import BaseCRUD
from app.mongo.engine import engine_aio
from app.utils.helper import Helper
from .exception import ErrorCode

event_crud = BaseCRUD("fes-events", engine_aio)
ticket_crud = BaseCRUD("fes-tickets", engine_aio)
user_crud = BaseCRUD("users", engine_aio)


class EventServices:
    def __init__(self, crud: BaseCRUD):
        self.crud = crud

    async def create(self, data: dict):
        result = await self.crud.create(data)
        return result

    async def get(self, _id: str):  
        result = await self.crud.get_by_id(_id)
        if not result:
            raise ErrorCode.EventNotFound()
        return result

    async def update(self, _id: str, data: dict):
        result = await self.crud.update_by_id(_id, data)
        if not result:
            raise ErrorCode.EventNotFound()
        return result

    async def delete(self, _id: str):
        result = await self.crud.delete_by_id(_id)
        if not result:
            raise ErrorCode.EventNotFound()
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.crud.search(query, page, limit)
        return result


class TicketServices:
    def __init__(self, crud: BaseCRUD):
        self.crud = crud

    async def checkout(self, data: dict):
        event = await event_crud.get_by_id(data["event_id"])
        user = await user_crud.get_by_id(data["user_id"])
        if not (event and user):
            raise ErrorCode.EventNotFound()

        result = []

        for t in data["tickets"]:
            type_info = next((x for x in event["types"] if x["type"] == t["type"]), None)
            if not type_info or type_info["sold"] + t["quantity"] > type_info["quantity"]:
                raise ErrorCode.InvalidTicket(t["type"])

            for _ in range(t["quantity"]):
                ticket_data = {
                    "event_id": data["event_id"],
                    "user_id": data["user_id"],
                    "type": t["type"],
                    "price": type_info["price"],
                    "status": "pending",
                    "qr_token": Helper.generate_ticket_code(),
                    "check_in": None,
                    "check_by": None
                }
                result.append(await self.crud.create(ticket_data))

            # Update quantity sold
            type_info["sold"] += t["quantity"]

        await event_crud.update_by_id(data["event_id"], {"types": event["types"]})
        return result


    async def checkin(self, data):
        ticket = await self.crud.get_one_query({"qr_token": data.qr_token})
        user = await user_crud.get_by_id(data.check_by)
        if not ticket:
            raise ErrorCode.QrTokenNotFound()
        if not user:
            raise ErrorCode.StaffNotFound()
    
        if ticket.get("status") != "paid" or ticket.get("check_by"):
            raise ErrorCode.InvalidTicket()

        checkin_data = {
            "check_in": Helper.get_timestamp(),
            "check_by": data.check_by
        }
        result = await self.crud.update_by_id(ticket["_id"], checkin_data)
        return {"status": "success", "result": result}

    async def confirm_pay(self, ticket_id, status):
        ticket = await self.crud.get_by_id(ticket_id)
        if not ticket: return ErrorCode.InvalidTicket()

        result = await self.crud.update_by_id(ticket_id, {"status": status})
        return {"status": "success", "result": result}
    
    async def search(self, query: dict, page: int, limit: int):
        result = await self.crud.search(query, page, limit)
        return result
    
    async def qr_code(self, ticket_id: str, format: str):
        ticket = await self.crud.get_by_id(ticket_id)
        if not ticket:
            raise ErrorCode.InvalidTicket("ticket")
        
        result = Helper.generate_qr_code(data=ticket.get("qr_token"), format=format)
        return result