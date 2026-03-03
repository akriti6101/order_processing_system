import streamlit as st
import requests
from router.routes import CUSTOMERS_ROUTE,ITEMS_ROUTE
from utils.helper import get_customers_id,get_items,place_order,get_orders_id,\
    get_order_details,get_all_details,get_my_orders,delete_order,make_payment

st.title("Welcome to the shopping cart :shopping_cart:")

with st.sidebar:
    sel_option=st.selectbox(label='Actions',options=('Order Item','All Orders','Order Details','My Orders','Payment'),
                         placeholder="Select an option",index=None)
if sel_option=='Payment':
    try:
        customers_id=get_customers_id()
        customer_id=st.selectbox(label='Customer ID',options=customers_id,index=None,placeholder='Select your customer id')
        order_ids=get_orders_id()
        order_id=st.selectbox(label='Order ID',options=order_ids,index=None,placeholder='Select order id')
        amount=st.text_input('Enter amount in rupees')
        payment=st.button('Pay',type='primary')
        if payment and customer_id and order_id and amount :
            response=make_payment(customer_id,order_id,amount)
            st.success(response['message'])
    except Exception as e:
        st.error(f'Could not make payment !,{e}')



if sel_option=='Order Item':
    try:
        customers_id=get_customers_id()
        id=st.selectbox(label='Customer ID',options=customers_id,index=None,placeholder='Select your customer id')
        if id :
            items=get_items()
            selected_items=st.multiselect(label='Items',options=items)
            if st.button('Place Order',type='primary'):
                if(place_order(id,selected_items)):
                    st.success("Congrats!! Order placed successfully ")
                else:
                    st.error('Oops :( Could not place order')
    except Exception as e:
        st.error(e)
if sel_option=='Order Details':
    try:
        order_ids=get_orders_id()
        id=st.selectbox(label='Order ID',options=order_ids,index=None,placeholder='Select order id')
        if id :
            details=get_order_details(id)
            if st.button('Get Order Details',type='primary'):
                st.write(f"**Order ID : {details['order_id']}**")
                st.write(f"Order Status : **{details['status']}**")
                st.write(f"**Customer Name :** {details['customer']['name']}")
                st.write(f"Customer Phone No : {details['customer']['contact']}")
                st.markdown('<span style="color:green">**********************Items Ordered by the customer ***************************</span>',unsafe_allow_html=True)
                for item in details['items']:
                    st.markdown(f"**{item['name']}** ,MRP : {item['price']}")
    except Exception as e:
        st.error(e)
if sel_option=='All Orders':
    try:
        status=st.selectbox(label='Order Status',options=["PENDING","PROCESSING","SHIPPED","DELIVERED"],index=None,placeholder='Select order status')
        if st.button('Fetch All Orders',type='primary'):
            orders=get_all_details(status)
            if len(orders)==0:
                st.write('<span style="color:red">No records found !</span>',unsafe_allow_html=True)
            else:
                st.write('<span style="color:blue">List of Orders</span>',unsafe_allow_html=True)
                st.table(orders)
    except Exception as e:
        st.error(e)
if sel_option=='My Orders':
    try:
        customer_id=st.text_input('Enter your customer_id')
        fetch_orders=st.button('Fetch Order')
        if customer_id:
            details=get_my_orders(customer_id)
            if len(details)>0:
                order_id=st.selectbox('Order ID',options=details['order_id'],index=None,placeholder='Order to Cancel')
                if order_id and st.button('Cancel Order',type='primary'):
                    response=delete_order(customer_id,order_id)
                    st.markdown(f'<span>**{response["message"]}**</span>',unsafe_allow_html=True)
            else:
                st.markdown('<span style="color:red">**No records found !**</span>',unsafe_allow_html=True)
    except Exception as e:
        st.error(e)