import requests
import pandas as pd
from datetime import datetime
from router.routes import CUSTOMERS_ROUTE,ITEMS_ROUTE,PLACE_ORDER_ROUTE,\
    ALL_ORDERS_ROUTE,ORDER_DETAIL_ROUTE,CUSTOMER_ORDER_ROUTE,CANCEL_ORDER_ROUTE,ORDER_PAYMENT_ROUTE

def get_customers_id():
    try:
        response=requests.get(CUSTOMERS_ROUTE)
        response=response.json()
        customers=response['customers']
        ids=[customer['customer_id'] for customer in customers]
        return ids
    except Exception as e:
        raise e
    
def get_items():
    try:
        response=requests.get(ITEMS_ROUTE)
        response=response.json()
        items=response['items']
        return items
    except Exception as e:
        raise e

def place_order(customer_id,items):
    try:
        print(items[0]['price'])
        total_amount=sum([item['price'] for item in items])
        data={'customer_id':customer_id,'items':items,'total_amount':total_amount}
        print(data)
        response=requests.post(PLACE_ORDER_ROUTE,json=data)
        response=response.json()
        print(response)
        if response['status_code']==200:
            return True
        else:
            return False
    except Exception as e:
        raise e

def get_orders_id():
    try:
        response=requests.get(ALL_ORDERS_ROUTE)
        response=response.json()
        orders=response['orders']
        ids=[order['order_id'] for order in orders]
        return ids
    except Exception as e:
        raise e

def get_order_details(order_id):
    try:
        url=ORDER_DETAIL_ROUTE.format(order_id=order_id)
        response=requests.get(url)
        response=response.json()
        order=response['order']
        details={'order_id':order['order_id'],
                 'customer':order['customer'],
                 'status':order['status'],
                 'items':order['items']}
        return details
    except Exception as e:
        raise e

def get_all_details(status):
    try:
        if status:
            url=f"{ALL_ORDERS_ROUTE}?status={status}"
        else:
            url=ALL_ORDERS_ROUTE
        print(url)
        response=requests.get(url)
        response=response.json()
        orders=response['orders']
        details=pd.DataFrame(orders)
        return details
    except Exception as e:
        raise e
def get_my_orders(customer_id):
    try:
        url=CUSTOMER_ORDER_ROUTE.format(customer_id=customer_id)
        response=requests.get(url)
        response=response.json()
        orders=response['orders']
        details=pd.DataFrame(orders)
        return details
    except Exception as e:
        raise e
def delete_order(customer_id,order_id):
    try:
        url=CANCEL_ORDER_ROUTE.format(customer_id=customer_id,order_id=order_id)
        print(url)
        response=requests.delete(url)
        response=response.json()
        return response
    except Exception as e:
        raise e
    
def make_payment(customer_id,order_id,amount):
    try:
        url=ORDER_PAYMENT_ROUTE
        print(url)
        data={'order_id':order_id,'customer_id':customer_id,'amount':amount,'date':datetime.now().strftime('%H:%M:%S-%d/%m/%y')}
        print(data)
        response=requests.post(url,json=data)
        response=response.json()
        return response
    except Exception as e:
        raise e