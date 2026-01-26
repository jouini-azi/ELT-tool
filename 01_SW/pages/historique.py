import streamlit as st
from pymongo import MongoClient
from core.auth import require_login
from core.session import init_session
from Functions.databases import MongoDB
init_session()
require_login()

st.set_page_config(page_title="Historique")

class Gestion_hist:
    def __init__(self):
        self.uri , self.client , self.db , self.collection , self.historique = MongoDB().connect_to_mongodb()


    def effacer_historique(self):
        """Efface tout l'historique"""
        if st.button("Effacer historique"):
            self.historique.delete_many({})
            st.success("Historique effacé !")
            st.rerun()

    def afficher_historique(self):
        """Affiche tous les jobs dans l'historique"""
        hist = list(self.historique.find())
        if not hist:
            st.info("Aucun historique disponible !")
        for h in hist:
            with st.container(border=True):
                st.write(f"**Titre:** {h.get('Job', '')}")
                st.write(f"**Date execution:** {h.get('date execution', '')}")
                erreur = h.get('erreur', '')
                if erreur:
                    st.write(f"**Erreur:** {erreur}")


# ==================== MAIN ====================
if st.button("Accueil"):
    st.switch_page("home.py")

st.header("Historique des Jobs")

hist = Gestion_hist()
hist.effacer_historique()
hist.afficher_historique()


