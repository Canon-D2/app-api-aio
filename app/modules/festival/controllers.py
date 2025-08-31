from .services import event_crud, ticket_crud, EventServices, TicketServices

class EventController:
    def __init__(self):
        self.service = EventServices(event_crud)

    async def create(self, data):
        result = await self.service.create(data)
        return result

    async def get(self, _id):
        result = await self.service.get(_id)
        return result
    
    async def update(self, _id, data):
        result = await self.service.update(_id, data)
        return result

    async def delete(self, _id):
        result = await self.service.delete(_id)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.service.search(query, page, limit)
        return result


class TicketController:
    def __init__(self):
        self.service = TicketServices(ticket_crud)

    async def checkout(self, data):
        result = await self.service.checkout(data)
        return result

    async def checkin(self, data):
        result = await self.service.checkin(data)
        return result
    
    async def cofirm_pay(self, ticket, status):
        result = await self.service.confirm_pay(ticket, status)
        return result
    
    async def search(self, query: dict, page: int, limit: int):
        result = await self.service.search(query, page, limit)
        return result