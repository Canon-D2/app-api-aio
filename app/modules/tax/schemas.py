from pydantic import BaseModel
from typing import Optional

class TaxResponse(BaseModel):
    status: str
    tax_code: str
    name: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    province: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    registrant: Optional[str] = None
    phone: Optional[str] = None
    business_sectors: Optional[str] = None
