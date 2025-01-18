from pydantic import BaseModel
from typing import Optional, List


class ProductCreate(BaseModel):
    title: str
    price: float
    description: str
    quantity: int
    owner_id: int


class ProductUpdate(BaseModel):
    title: Optional[str]
    price: Optional[float]
    description: Optional[str]
    quantity: Optional[int]
    owner_id: Optional[int]


class ProductOut(BaseModel):
    id: int
    title: str
    price: float
    description: str
    quantity: int
    owner_id: int
    buyers: List[int] = []

    class Config:
        orm_mode = True

class BuyProductRequest(BaseModel):
    user_id: int
