import streamlit as st
from app.services.user_service import login_user, register_user
from app.data.users import get_user_by_username
from app.data.db import connect_database


st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")

# Connect to database
conn = connect_database()

#initialise session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""    

if "role" not in st.session_state:                              
    st.session_state.role = ""

st.title("🔐 Welcome")

#if already logged in, go straight to dashboard
if st.session_state.logged_in:
    st.write(f"Welcome, {st.session_state.username} ({st.session_state.role})")
    if st.button("Go to dashboard"):
        #use the official navigation api to switch pages
        st.switch_page("pages/1_Cyber_Security_Dashboard.py") 
    st.stop()

#tabs: login/register
tab_login, tab_register = st.tabs(["Login", "Register"])

#login tab
with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in", type="primary"):
        success, message = login_user(conn, login_username, login_password)
        if success:
            #fetch full user to get role
            user = get_user_by_username(conn, login_username)
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.session_state.role = user[3]
            #navigate to dashboard page
            st.success(message)
            st.switch_page("pages/1_Cyber_Security_Dashboard.py")
        else:
            st.error(message)


#register tab
with tab_register:
    st.subheader("Register")

    new_username = st.text_input("Enter a username", key="register_username")
    new_password = st.text_input("Enter a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")
    role = st.selectbox("Select Role", ["user", "admin"])

    if st.button("Create account"):
        if new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            success, message = register_user(conn, new_username, new_password, role)
            if success:
                st.success(message)
                st.info("Go to Login tab to sign in.")
            else:
                st.error(message)

if st.session_state.logged_in:
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.info("You have been logged out.")

    