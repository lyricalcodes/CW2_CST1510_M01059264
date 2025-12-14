import streamlit as st

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

#if logged in show dashboard content
if not st.session_state.get("logged_in", False):
    st.error("You must be logged in to access settings.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()
