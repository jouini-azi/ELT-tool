import streamlit as st
from Functions.databases import Mysql


def check_user(username, password):
    conn = Mysql().connect_to_MySQL()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


def require_login():
    if not st.session_state.get("logged_in"):
        st.switch_page("pages/Login.py")
