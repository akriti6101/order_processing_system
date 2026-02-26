"""
This file is for storing the dummy data in customers table and items table.
"""

from fastapi import APIRouter,Depends,HTTPException,Body
from models.pydantic_models import Customer,Item
from typing import List
from models.db_models import Customers,Items
from utils.helper import get_db_connection

data_ingestion_routes=APIRouter()

@data_ingestion_routes.post("/customers")
async def add_customers(customer:Customer=Body(...),db_con=Depends(get_db_connection)):
    try:
        print(customer['customer_id'])
        if db_con.query(Customers).filter(Customers.customer_id==customer['customer_id']).first() :
            raise HTTPException(status_code=400,detail="Customer already exists")
        else:
            customer_obj=Customers(**customer.dict())
            db_con.add(customer_obj)
            db_con.commit()
            return {'status_code':200,'message':'customer details added'}
    except Exception as e:
        raise HTTPException(status_code=400,detail="Could not save customer details")
    
@data_ingestion_routes.get("/customers")
async def get_customers(db_con=Depends(get_db_connection)):
    try:
        customers_list=[]
        customers=db_con.query(Customers).all()
        print('customers',customers)
        for customer in customers:
            customers_list.append(Customer(customer_id=customer.customer_id,name=customer.name,contact=customer.contact))
        print(customers_list)
        return {'status_code':200,'customers':customers_list}
    except Exception as e:
        raise HTTPException(status_code=400,detail="Could not fetch customers")

    
########## FOR ITEMS 


@data_ingestion_routes.post("/items")
async def add_item(item:Item=Body(...),db_con=Depends(get_db_connection)):
    try:
        item_obj=Items(**item.dict())
        db_con.add(item_obj)
        db_con.commit()
        return {'status_code':200,'message':'Item details added'}
    except Exception as e:
        raise HTTPException(status_code=400,detail="Could not save item details")
    
@data_ingestion_routes.get("/items")
async def get_items(db_con=Depends(get_db_connection)):
    try:
        items_list=[]
        items=db_con.query(Items).all()
        for item in items:
            items_list.append(Item(item_id=item.item_id,name=item.name,description=item.description,price=item.price))
        return {'status_code':200,'items':items_list}
    except Exception as e:
        raise HTTPException(status_code=400,detail="Could not fetch items")

    




