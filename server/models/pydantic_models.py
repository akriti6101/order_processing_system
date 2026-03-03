from pydantic import BaseModel
from datetime import datetime

class Customer(BaseModel):
    customer_id:str
    name:str
    contact:str

class Item(BaseModel):
    item_id:str
    name:str
    description:str|None
    price:float

class OrderItem(BaseModel):
    customer_id:str
    items:list[Item]
    total_amount:float

class OrderPayment(BaseModel):
    order_id:str
    customer_id:str
    amount:float
    date:str