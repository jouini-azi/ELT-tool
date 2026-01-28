import streamlit as st
from core.auth import require_login
from core.session import init_session
from core.user_manager import UserManager


init_session()
require_login()

st.set_page_config(page_title="Profil")
if st.button("Accueil"):
    st.switch_page("Accueil.py")
st.header("Votre profil")
st.markdown("---")


name=st.text_input("Username",st.session_state["username"])
if st.button("Modifier le username"):
    UserManager().update_username(st.session_state["username"],name)

    

mp=st.text_input("Mot de passe",st.session_state["password"],type="password")
if st.button("Modifier le mot de passe"):
    UserManager().update_password(st.session_state["password"],mp)



if st.session_state['role']=="admin":
    role=st.selectbox("Role",options=['admin','user'],index=0)
    if st.button("Modifier le role"):
        print("role new:",role)
        print("role old:",st.session_state["role"])

        UserManager().update_role(st.session_state["username"],st.session_state["role"],role)
        
if st.session_state['role']=="user":
    role=st.selectbox("Role",options=['Admin','User'],index=1,disabled=True)
        

st.markdown("---")

if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = False

if st.button("Supprimer compte"):
    st.session_state.confirm_delete = True

if st.session_state.confirm_delete:
    st.warning("Êtes-vous sûr de vouloir supprimer votre compte ?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Oui, supprimer"):
            UserManager().delete_user(st.session_state["username"])
            st.session_state.confirm_delete = False

    with col2:
        if st.button("Annuler"):
            st.session_state.confirm_delete = False
            st.rerun()


