import streamlit as st
from core.auth import require_login
from core.session import init_session

init_session()
require_login()

st.set_page_config(page_title="Local")
if st.button("Accueil"):
    st.switch_page("home.py")
st.header("Votre profil")

name=st.text_input("Username",st.session_state["username"])
if st.button("Modifier username"):
    pass
    ##   TODO  fonction modifier username

name=st.text_input("Mot de passe",st.session_state["password"],type="password")
if st.button("Modifier mot de passe"):
    pass
     ##   TODO  fonction modifier mot de passe
