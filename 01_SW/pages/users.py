from core.user_manager import UserManager
import streamlit as st
from core.auth import require_login
from core.session import init_session

init_session()
require_login()

st.set_page_config(page_title="Gestion utilisateurs")
if st.button("Accueil"):
    st.switch_page("home.py")
st.header("Gestion utilisateurs")
st.markdown("---")

if st.session_state["role"]=="admin":  
  with st.expander("Ajouter un utilisateur"):
    name=st.text_input("Username")
    password=st.text_input("Mot de passe")
    role=st.selectbox("Role",options=['admin','user'],index=1)
    if st.button("Ajouter"):
       UserManager().add_user(name,password,role)

  st.markdown("Liste utilisateurs")
  UserManager().get_users()
else:
    st.warning("Vous n'etes pas autorisé à acceder à cette page !")