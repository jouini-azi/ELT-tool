import streamlit as st
from core.auth import require_login
from core.session import init_session
from core.login import Login

init_session()
require_login()

st.set_page_config(page_title="Accueil",layout="wide")
col4,col5=st.columns([1,8])
with col4:
  if st.button("Déconnexion"):
    Login().logout()
with col5:
  if st.button("Profile"):
    st.switch_page("pages/profil.py")

st.title("Bienvenue "+st.session_state["username"]+" !")
st.markdown("---")

col1, col2, col3,col4= st.columns(4)
with col1:
  if st.button("Consulter les Jobs"):
    st.switch_page("pages/listJobs.py")
with col2:
  if st.session_state["role"]=="admin":
    if st.button("Créer un Job"):
      st.switch_page('pages/JOB_new.py')
with col3:
  if st.session_state["role"]=="admin":
    if st.button("Gérer les utilisateurs"):
      st.switch_page('pages/users.py')
with col4:
  if st.button("Historique"):
    st.switch_page('pages/historique.py')