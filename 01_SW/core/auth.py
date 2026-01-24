import streamlit as st
from core.db import get_connection

def check_user(username, password):
    conn = get_connection()
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
        st.switch_page("pages/login.py")
