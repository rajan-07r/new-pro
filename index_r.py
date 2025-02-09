import streamlit as st
import mysql.connector as mysql
import pandas as pd

class restaurants():
    def __init__(self):
        pass

def get_connection():
    return mysql.connect(
        host="localhost",
        user="root",
        password="admin",
        database="rest_db"
    )

def myMenu():
    # get menu function
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu")
    menu = cursor.fetchall()
    conn.close()
    return menu

def add_to_cart(item_id, quantity):
    # add to cart function
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Cart(item_id, quantity) VALUES(%s, %s)", (item_id, quantity))
    conn.commit()
    conn.close()

def fetch_cart():
    # fetch cart function
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """SELECT menu.dish_name, menu.price, Cart.quantity 
        FROM Cart 
        JOIN menu ON Cart.item_id = menu.dID"""
    )
    cart = cursor.fetchall()
    conn.close()
    return cart

def clear_cart():
    # clear cart function
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Cart")
    conn.commit()
    conn.close()

st.sidebar.title("Narmada The Chain Of Restaurant")
page = st.sidebar.radio("Go To", ["Menu", "Cart"])

if page == "Menu":
    menu = myMenu()

    st.title("Restaurant Menu")
    menu_df = pd.read_csv("menu3.csv")
    st.subheader("Menu")
    st.dataframe(menu_df)

    # Input fields for adding items to the cart
    st.write("### Add to Cart")
    sno = st.number_input("Enter Serial Number (Sno)", min_value=0, step=1, key="sno_input")
    quantity = st.number_input("Enter Quantity", min_value=0, step=1, key="quantity_input")

    # Add button
    if st.button("Add to Cart"):
        # Find the item in the menu by serial number
        selected_item = next((item for item in menu if item['dID'] == sno), None)
        if selected_item:
            add_to_cart(selected_item['dID'], quantity)
            st.success(f"{selected_item['dish_name']} (Qty: {quantity}) added to cart! Add next item or go to cart for checkout")
        else:
            st.error("Invalid Serial Number. Please enter a valid number.")

elif page == "Cart":
    st.title("Your Cart")
    cart_items = fetch_cart()

    if not cart_items:
        st.write("Your cart is empty.")
    else:
        total = 0
        total_w_gst = 0
        for item in cart_items:
            st.write(f"{item['dish_name']} - ₹{item['price']} x {item['quantity']} = ₹{item['price'] * item['quantity']}")
            total += item['price'] * item['quantity']

        st.write(f"**Total: ₹{total}**")
        gst = total * 0.18
        total_w_gst = total + gst
        st.write(f"**Subtotal: ₹{total}**")
        st.write(f"**GST (18%): ₹{gst:.2f}**")
        st.write(f"**Total with GST: ₹{total_w_gst:.2f}**")
        if st.button("Clear Cart"):
            clear_cart()
            st.success("Cart cleared!")
        elif st.button("Place Order"):
            clear_cart()
            st.success("Order Placed!")