import streamlit as st
from core.auth import require_login
from core.session import init_session
from Functions.databases import MongoDB
from core.historique_manager import Gestion_hist
init_session()
require_login()

st.set_page_config(page_title="Historique",layout="wide")

if st.button("Accueil"):
    st.switch_page("Accueil.py")

st.title("Historique des Jobs")
st.markdown("---")


Gestion_hist().effacer_historique()
Gestion_hist().afficher_historique()


