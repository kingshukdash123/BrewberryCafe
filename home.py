import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import item
import json
import os


if "page" not in st.session_state:
    st.session_state.page = "home"

if "current_user" not in st.session_state:
    st.session_state.current_user = ""


def go_home():
    st.session_state.page = "home"

def go_signup():
    st.session_state.page = "signup"

def go_signin():
    st.session_state.page = "signin"

def go_table():
    st.session_state.current_user = username
    st.session_state.page = "table"

def go_accounts():
    st.session_state.page = "accounts"

def go_order():
    st.session_state.page = "order"


#  Page rendering
if st.session_state.page == "home":
    st.title("Welcome to BrewBerry Cafe...")
    st.write("⚠️ Please do not use the browser's back button. Use the 'Back to Home' button to navigate.")
    st.caption("- At first you have to sign up and then you can order.")

    st.write("")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col2:
        st.subheader("Dashboard")
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sign Up to proceed...")
        st.button("Sign Up", on_click=go_signup)
        st.write("Or if you have an account, then Sign in...")
        st.button("Sign In", on_click=go_signin)
    with col2:
        st.subheader("User Details")
        st.button("Show Me", on_click=go_accounts)

    st.divider()
    col1, col2, col3 = st.columns(3)
    with col2:
        st.title("User Guide")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 👤 How to Sign Up")
        st.write("- Go to **Sign Up** page from Home.")
        st.write("- Enter basic details.")
        st.write("- Click **Submit** to register your account.")

        st.markdown("### 🔑 How to Sign In")
        st.write("- Go to **Sign In** page from Home.")
        st.write("- Enter your registered Username and Password.")
        st.write("- Click **Login** to access your account.")
    with col2:
        st.markdown("### 🍔 How to Place an Order")
        st.write("- After Sign-in or Sign up, click **Go to order Table**.")
        st.write("- Select the item and quantity.")
        st.write("- Click **Order** to place your order.")

        st.markdown("### 🧾 How to View Bill")
        st.write("- After placing order, bill will be generated automatically.")
        st.write("- You can see ordered item name, quantity, and total cost.")
        


elif st.session_state.page == "signup":

    st.title("Sign Up")
    st.write("⚠️ Please do not use the browser's back button. Use the 'Back to Home' button to navigate.")
    st.divider()
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    contact = st.text_input("Contact Number")
    email = st.text_input("Email")
    
    if st.button("Submit"):
        # validate
        if not (username and password and contact and email):
            st.warning("Please fill in all fields.")
        else:
            new_user_data = pd.DataFrame(
                [
                    {
                        "username": username, 
                        "password": password,
                        "contact": contact,
                        "email": email,
                    }
                ]
            )

            conn = st.connection("gsheets", type=GSheetsConnection)
            df = conn.read(worksheet="user_details", ttl=0)

            if username in df["username"].values:
                st.warning("This username is already taken. Please choose another one.")
            else:
                updated_df = pd.concat([df, new_user_data], ignore_index=True)
                conn.update(worksheet="user_details", data=updated_df)
                st.success("Sign‑up successful ! Now you can order from bellow button.")
                st.write("")

                if st.button("Go to Order Table", on_click=go_table):
                    pass

    st.write("")
    st.button("Back to Home", on_click=go_home)

elif st.session_state.page == "signin":
    st.title("Sign In")
    st.write("⚠️ Please do not use the browser's back button. Use the 'Back to Home' button to navigate.")
    st.divider()
    username = st.text_input("Username", key="login_name")
    password = st.text_input("Password", type="password", key="login_pw")
    
    if st.button("Submit"):
        if not (username and password):
            st.warning("Please fill in all fields.")
        else:
            conn = st.connection("gsheets", type=GSheetsConnection)
            df = conn.read(worksheet="user_details")

            if username not in df["username"].values:
                st.warning("This account doesn't exist.")

            else:
                user_row = df[df["username"] == username]
                stored_password = user_row["password"].values[0]

                if password == str(stored_password):
                    st.success("Sign in completed successfully.")
                    st.write("")

                    if st.button("Go to Order Table", on_click=go_table):
                        pass
                        
                else:
                    st.warning("Invalid username or password !")

    st.write("")
    st.button("Back to Home", on_click=go_home)

elif st.session_state.page == "accounts":
    st.title("Registered Accounts")
    st.write("⚠️ Please do not use the browser's back button. Use the 'Back to Home' button to navigate.")
    st.divider()

    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="user_details")

    username = st.text_input("Admin's Username")
    password = st.text_input("Admin's Password", type="password")

    if st.button("Show me"):
        if username and password:
            if username == "Admin123" and password == "123":
                if len(df) == 0:
                    st.warning("You have no account! First go for sign up.")
                else:
                    st.dataframe(df)
            else:
                st.warning("You are not an admin. This is for admin's only.")
        else:
            st.warning("Fill all the field.")


    

    st.divider()
    st.write("")
    st.button("Back to Home", on_click=go_home)

elif st.session_state.page == "table":
    st.title("Order Table")

    if st.session_state.current_user:
        st.subheader(f"Welcome {st.session_state.current_user}")
        st.write("⚠️ Please do not use the browser's back button. Use the 'Back to Home' button to navigate.")
        st.caption("You're on the order page. Browse the menu, choose your items, and place your order!")
        st.divider()

    col1, col2 = st.columns(2)
    with col2:
        with st.expander("View Snacks Menu", expanded=False) :
            for i in item.orderItem:
                st.write(f"{i} : Rs {item.orderItem[i]}/-")

        with st.expander("View Drinks Menu", expanded=False) :
            for i in item.coldDrinks:
                st.write(f"{i} : Rs {item.coldDrinks[i]}/-")

    with col1:
        food = []
        cold_drinks = []

        for i in item.orderItem:
            food.append(i)

        for i in item.coldDrinks:
            cold_drinks.append(i)

        def orderFromUser():
            selected_items = st.selectbox(
                "Select your items",
                ["Choose one"] + food
            )
            quantity_selected_items = st.slider("Select quantity", 1, 10, 1, key="food_quantity")
            
            selected_coldDrink = st.selectbox(
                "Select cold drink", 
                ["Choose One"] + cold_drinks
            )
            quantity_cold_drinks = st.slider("Select quantity", 1, 10, 1, key="drink_quantity")
            if st.button("Order"):
                if selected_items == "Choose one" or selected_coldDrink == "Choose One":
                    st.warning("Select both of them before placed")
                else:
                    st.divider()

                    st.success(f"Your order {quantity_selected_items} plates of {selected_items} and {quantity_cold_drinks} bottles of {selected_coldDrink} successfully placed.")

                    st.divider()
                    st.subheader("Your Bill")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(selected_items)
                        st.write(selected_coldDrink)
                    with col2:
                        food_total = item.orderItem[selected_items] * quantity_selected_items
                        drink_total = item.coldDrinks[selected_coldDrink] * quantity_cold_drinks
                        total = food_total + drink_total
                        st.write(f"{item.orderItem[selected_items]} * {quantity_selected_items}")
                        st.write(f"{item.coldDrinks[selected_coldDrink]} * {quantity_cold_drinks}")

                    st.subheader(f"Total : {(item.orderItem[selected_items]*quantity_selected_items) + (item.coldDrinks[selected_coldDrink]*quantity_cold_drinks)}")

            st.divider()
            st.button("Back to Home", on_click=go_home)

        orderFromUser()