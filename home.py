import streamlit as st
import item

# —————————————————————————————
#  Model
# —————————————————————————————
class User:
    def __init__(self, name, password, contact, email):
        self.name = name
        self.password = password
        self.contact = contact
        self.email = email

    def __str__(self):
        return f"Name: {self.name} | Contact: {self.contact} | Email: {self.email}"

# —————————————————————————————
#  Session‐state setup
# —————————————————————————————
if "page" not in st.session_state:
    st.session_state.page = "home"

if "users" not in st.session_state:
    st.session_state.users = []  # persists across reruns

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "orders" not in st.session_state:
    st.session_state.orders = {}

# —————————————————————————————
#  Navigation callbacks
# —————————————————————————————
def go_home():
    st.session_state.page = "home"

def go_signup():
    st.session_state.page = "signup"

def go_signin():
    st.session_state.page = "signin"

def go_table():
    st.session_state.page = "table"

def go_accounts():
    st.session_state.page = "accounts"

def go_order():
    st.session_state.page = "order"

# —————————————————————————————
#  Page rendering
# —————————————————————————————
if st.session_state.page == "home":
    st.title("Welcome to BrewBerry Cafe...")
    st.write("- At first you have to sign up then sign in and then you can order.")
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
        st.subheader("My Accounts")
        st.button("Show Me", on_click=go_accounts)

    st.divider()
    col1, col2, col3 = st.columns(3)
    with col2:
        st.title("User Guide")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 👤 How to Sign Up")
        st.write("- Go to **Sign Up** page from Home.")
        st.write("- Enter Username, Password, Contact, and Email.")
        st.write("- Click **Submit** to register your account.")

        st.write("")
        st.markdown("### 🔑 How to Sign In")
        st.write("- Go to **Sign In** page from Home.")
        st.write("- Enter your registered Username and Password.")
        st.write("- Click **Login** to access your account.")
    with col2:
        st.markdown("### 🍔 How to Place an Order")
        st.write("- After sign-in, click **Go to order Table**.")
        st.write("- Click **Add to Cart** to go to order page.")
        st.write("- Select the item and quantity.")
        st.write("- Click **Order** to place your order.")

        st.markdown("### 🧾 How to View Bill")
        st.write("- After placing order, bill will be generated automatically.")
        st.write("- You can see ordered item name, quantity, and total cost.")
        


elif st.session_state.page == "signup":

    st.title("Sign Up")
    st.divider()
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    contact  = st.text_input("Contact Number", placeholder="9876543210")
    email    = st.text_input("Email")
    
    if st.button("Submit"):
        # validate
        if not (username and password and contact and email):
            st.error("Please fill in all fields.")
        else:
            new_user = User(username, password, contact, email)
            st.session_state.users.append(new_user)
            st.success("Sign‑up successful ! You can now sign in.")
    st.write("")
    st.button("Back to Home", on_click=go_home)

elif st.session_state.page == "signin":
    st.title("Sign In")
    st.divider()
    username = st.text_input("Username", key="login_name")
    password = st.text_input("Password", type="password", key="login_pw")
    
    if st.button("Submit"):
        # simple lookup
        if not (username and password):
            st.error("Please fill in all fields.")
        else:

            userMatch = False
            if not st.session_state.users:
                st.error("You have no account ! first go for sign up.")
                userMatch = True

            for u in st.session_state.users:
                if u.name == username and u.password == password:
                    userMatch = True
                    st.success(f"Sign up completed successfully.")
                    st.session_state.current_user = u
                    st.write("")
                    st.button("Go to Order Table", on_click=go_table)
                    break
                
            if userMatch == False:
                st.error("Invalid username or password !")
    st.write("")
    st.button("Back to Home", on_click=go_home)

elif st.session_state.page == "accounts":
    st.title("My Accounts")
    st.divider()
    st.write("")

    if not st.session_state.users:
        st.write("You have no account ! first go for sign up.")
    for u in st.session_state.users:
        st.write(u)

    st.write("")
    st.button("Back to Home", on_click=go_home)

elif st.session_state.page == "table":

    if st.session_state.current_user:
        st.title(f"Welcome {st.session_state.current_user.name}")
        st.divider()

    st.subheader("Order Something")
    with st.expander("View today's menu") :
        for i in item.orderItem:
            st.write(f"{i} : Rs {item.orderItem[i]}/-")

    st.button("Add to Cart", on_click=go_order)
    st.divider()
    st.write("")
    st.button("Back to Home", on_click=go_home)

elif st.session_state.page == "order":

    st.title("Order here")
    st.divider()
    food = []

    for i in item.orderItem:
        food.append(i)

    def orderFromUser():
        selected_items = st.selectbox(
            "Select your items:",
            ["Choose one"] + food
        )
        quantity = st.slider("Select quantity", 1, 10, 1)

        st.session_state.orders[selected_items] = quantity
        if st.button("Order"):
            if not st.session_state.orders:
                st.error("Select something before placed")
            else:
                st.divider()
                st.subheader("Your Bill")
                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    st.write(selected_items)
                with col2:
                    st.write(f"{item.orderItem[i]} * {quantity} = {item.orderItem[i]*quantity}")
                st.write("")
                st.success(f"Your order {quantity} plates of {selected_items} successfully placed.")

    orderFromUser()

    st.divider()
    st.write("")
    st.button("Go to Table", on_click=go_table)

    