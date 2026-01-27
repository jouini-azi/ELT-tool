import streamlit as st
from core.session import init_session
from core.login import Login
st.set_page_config(page_title="Login")
init_session()


if not st.session_state["role"]:
  st.title("Login")
  st.markdown("---")

  page = Login()
  page.render()  
else:
  if st.button("Accueil"):
    st.switch_page("home.py")
  st.title("Login")
  st.markdown("---")

  
  st.info("Vous etes déja connecté !")
  if st.button("Déconnexion"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.switch_page("pages/Login.py")