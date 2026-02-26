from pydantic import BaseModel

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