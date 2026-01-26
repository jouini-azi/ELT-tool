from core.user_manager import UserManager
import streamlit as st
from core.auth import require_login
from core.session import init_session

init_session()
require_login()

st.set_page_config(page_title="Utilisateurs")
if st.button("Accueil"):
    st.switch_page("home.py")
st.header("Utilisateurs")

if st.session_state["role"]=="admin":
  u=UserManager()
  u.get_users()
else:
    st.warning("Vous n'etes pas autorisé à acceder à cette page !")