from .services import TaxServices

class TaxController:
    def __init__(self):
        self.service = TaxServices()

    async def get_tax(self, tax_code):
        result = await self.service.get_tax(tax_code)
        return result

tax_controller = TaxController()
