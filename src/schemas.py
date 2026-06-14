from pydantic import BaseModel

class OrderCreate(BaseModel):
    customer_name: str
    lens_type: str
    power: str

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    lens_type: str
    status: str
    risk: str

    class Config:
        from_attributes = True

class InventoryUpdate(BaseModel):
    stock_count: int