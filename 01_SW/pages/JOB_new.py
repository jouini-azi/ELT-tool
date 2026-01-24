import streamlit as st
from core.auth import require_login
from core.session import init_session

init_session()
require_login()

st.set_page_config(page_title="Créer Job", layout="wide")


if st.button("Accueil"):
    st.switch_page("home.py")
    
col1, col2= st.columns([1,1])
with col1:
  if st.button("SharePoint"):
    st.switch_page('pages/sharepoint.py')
with col2:
  if st.button("Localhost"):
    st.switch_page('pages/localhost.py')



