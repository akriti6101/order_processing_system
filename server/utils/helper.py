from init import session
from fastapi import HTTPException
from models.db_models import Orders,Payment
def get_db_connection():
    try:
        db=session()
        return db
    except Exception as e:
        raise HTTPException(status_code=503,detail='Could not establish database connection')
    
def get_next_order_id(prefix='ODR000'):
    db_con=get_db_connection()
    last_order_id = db_con.query(Orders).order_by(Orders.order_id.desc()).first()
    if last_order_id:
        last_order_id = int(last_order_id.order_id.replace(prefix, ""))
        next_order_id = last_order_id+ 1
    else:
        next_order_id = 1
    return next_order_id

def get_next_payment_id(prefix='PAY000'):
    db_con=get_db_connection()
    last_payment_id = db_con.query(Payment).order_by(Payment.pid.desc()).first()
    if last_payment_id:
        last_payment_id = int(last_payment_id.pid.replace(prefix, ""))
        next_payment_id = last_payment_id+ 1
    else:
        next_payment_id = 1
    return next_payment_id

def update_order_status():
    """This method is executed every 5 mins to update the order's status to PROCESSING."""
    try:
        db_con=get_db_connection()
        # orders=db_con.query(Orders).filter(Orders.status=='PENDING').all()
        # for order in orders:
        #     order.status='PROCESSING'
        #     db_con.add(order)
        #     db_con.commit()
        # print('All orders updated')
        orders=db_con.query(Orders).filter(Orders.status=='PENDING').all()
        for order in orders:
            total_amount=order.total_amount
            payments=db_con.query(Payment).filter(Payment.order_id==order.order_id).all()
            paid_amount=0
            for payment in payments :
                paid_amount=paid_amount+payment.amount
            if paid_amount>=total_amount:
                order.status='COMPLETED'
                db_con.add(order)
                db_con.commit()  
        print('All orders updated')         
    except Exception as e:
        print(f'Could not update order status : {e}')
