from init import db_con_obj, base
from sqlalchemy import Column, String, Float, ForeignKey,DateTime
from sqlalchemy.orm import relationship

class OrderItems(base):
    __tablename__ = "order_items"

    order_id = Column(String, ForeignKey("orders.order_id"), primary_key=True)
    item_id = Column(String, ForeignKey("items.item_id"), primary_key=True)

class Customers(base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True)
    name = Column(String)
    contact = Column(String)

    orders = relationship("Orders", back_populates="customer")


class Items(base):
    __tablename__ = "items"

    item_id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)

    orders = relationship("Orders", secondary="order_items", back_populates="items")


class Orders(base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"))
    status = Column(String)
    total_amount=Column(Float)

    customer = relationship("Customers", back_populates="orders")
    items = relationship("Items", secondary="order_items", back_populates="orders")


class Payment(base):
    __tablename__='payments'
    pid=Column(String,primary_key=True)
    order_id=Column(String,ForeignKey("orders.order_id"))
    customer_id=Column(String,ForeignKey("customers.customer_id"))
    amount=Column(Float)
    date=Column(String)

