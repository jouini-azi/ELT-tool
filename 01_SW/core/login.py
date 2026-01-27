# pages/login_page.py
import streamlit as st
from core.auth import check_user
from core.session import init_session

st.set_page_config(page_title="Login")  

class Login:
    def __init__(self):
        # Initialisation de la session
        init_session()

        # Attributs pour le formulaire
        self.username = ""
        self.password = ""
    
    def render(self):
        """Affiche le formulaire de login"""
        st.set_page_config(page_title="Login")

        # Inputs
        self.username = st.text_input("Login")
        self.password = st.text_input("Mot de passe", type="password")

        # Bouton de connexion
        if st.button("Se connecter"):
            self.authenticate()

    def authenticate(self):
        """Vérifie les identifiants et redirige vers HomePage"""
        user = check_user(self.username, self.password)
        if user:
            # Stocker les informations de session
            st.session_state["logged_in"] = True
            st.session_state["username"] = user["username"]
            st.session_state["password"] = user["password"]
            st.session_state["role"] = user["role"]

            # Redirection vers la page d'accueil
            st.switch_page("home.py")
        else:
            st.error("Login ou mot de passe incorrect !")
    
    def logout(self):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("pages/login_page.py")
