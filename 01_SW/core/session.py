import streamlit as st

def init_session():
    if "initialized" not in st.session_state:
        st.session_state["initialized"] = True
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.session_state["role"] = None