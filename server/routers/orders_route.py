from fastapi import APIRouter,Depends,Body,Path,HTTPException,Query
from models.pydantic_models import OrderItem
from typing import Optional
from models.db_models import Orders,Items
from utils.helper import get_db_connection,get_next_order_id

orders_router=APIRouter(prefix='/orders')

@orders_router.post("",status_code=200)
async def place_order(order:OrderItem=Body(...),db_con=Depends(get_db_connection)):
    try:
        order_id='ODR000'+str(get_next_order_id())
        items_obj = db_con.query(Items).filter(Items.item_id.in_([item.item_id for item in order.items])).all()
        orders=Orders(order_id=order_id,customer_id=order.customer_id,status='PENDING',items=items_obj)
        db_con.add(orders)
        db_con.commit()
        return {'status_code':200,'message':'All orders placed.'}
    except Exception as e:
        raise HTTPException(status_code=400,detail="Oops :) could not place order.")

@orders_router.get("/customer/{customer_id}")
async def retrive_customer_orders(customer_id:str,db_con=Depends(get_db_connection)):
    try:
        orders=db_con.query(Orders).filter(Orders.customer_id==customer_id).all()
        orders_list=[]
        for order in orders:
            items_list=','.join([item.name  for item in order.items])
            total_price=sum([item.price for item in order.items])
            orders_list.append({'order_id':order.order_id,'customer_name':order.customer.name,'items':items_list,'total_bill':total_price,'status':order.status})
        return {'status_code':200,'orders':orders_list}
    except Exception as e:
        raise HTTPException(status_code=400,detail="Could not fetch customer's order")


@orders_router.get("/{order_id}")
async def retrive_order_details(order_id=Path(...),db_con=Depends(get_db_connection)):
    try:
        order_obj=db_con.query(Orders).filter(Orders.order_id==order_id).first()
        order={'order_id':order_obj.order_id,'customer':order_obj.customer,'status':order_obj.status,'items':order_obj.items}
        return {'status_code':200,'order':order}
    except Exception as e:
        raise HTTPException(status_code=400,detail="Could not fetch order details.")

@orders_router.get("")
async def retrive_all_order_details(status:Optional[str]=Query(None),db_con=Depends(get_db_connection)):
    try:
        if not status:
            orders=db_con.query(Orders).all()
        else:
            orders=db_con.query(Orders).filter(Orders.status==status).all()
        orders_list=[]
        for order in orders:
            orders_list.append({'order_id':order.order_id,'customer_name':order.customer.name,'customer_contact':order.customer.contact,'status':order.status})
        return {'status_code':200,'orders':orders_list}
    except Exception as e:
        raise HTTPException(status_code=400,detail="Could not fetch all orders")

@orders_router.delete("/{customer_id}/{order_id}")
async def cancel_order(order_id:str,customer_id:str,db_con=Depends(get_db_connection)):
    try:
        order=db_con.query(Orders).filter((Orders.order_id==order_id)&(Orders.customer_id==customer_id)).first()
        if order.status!='PENDING':
            return {'status_code':200,'message':"The order is in progress,Can't be cancelled !"}
        else:
            db_con.delete(order)
            db_con.commit()
            return {'status_code':200,'message':"Your order is cancelled !"}
    except Exception as e:
        raise HTTPException(status_code=400,detail="Could not delete order")