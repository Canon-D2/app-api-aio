from pydantic import BaseModel

class ReportRequest(BaseModel):
    invoice: str
    customer: str
    total: str
    time: str
    method: str
    address: str
    note: str