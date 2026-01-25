import streamlit as st
import pandas as pd
import os
from pymongo import MongoClient
from datetime import datetime
from core.db import get_connection
from core.auth import require_login
from core.session import init_session
from core.commun import commun
from Functions.databases import MongoDB

init_session()
require_login()

class JobManager(commun):
    def __init__(self):
        self.df = pd.DataFrame()
        self.selected = pd.DataFrame()
        self.uri , self.client , self.db , self.collection , self.historique = MongoDB().connect_to_mongodb()
        self.init_session()

    def init_session(self):
        """Initialisation des states"""
        if "tab" not in st.session_state:
            st.session_state.tab = None
        if "df" not in st.session_state:
            st.session_state.df = pd.DataFrame()

    def render_inputs(self):
        """Affichage des inputs Streamlit"""
        col1, col2 = st.columns([3,1])
        with col1:
            self.titre = st.text_input("Titre")
            self.path = st.text_input("Chemin complet du dossier")
            self.dbName = st.text_input("Nom de la base")
            self.host = st.text_input("host")
            self.table = st.text_input("Nom de la table")
        with col2:
            st.title("Requetes SQL")
            self.sql = st.text_area(
                'Entrez vos requetes SQL (precedées par " - " ) ',
                height=260
            )

        st.session_state["titre"] = self.titre
        st.session_state["file"] = self.path
        st.session_state["dbName"] = self.dbName
        st.session_state["host"] = self.host
        st.session_state["table"] = self.table
        st.session_state["sql"] = self.sql

        return self.titre , self.path , self.dbName , self.host , self.table , self.sql, self.collection
    
    def executer(self):
        """Exécuter le job"""
        if st.button("Executer"):
            if not (self.titre and self.path and self.dbName and self.host and self.table):
                st.warning("Veuillez remplir tous les champs correctement !")
                st.switch_page("pages/transform.py")
                return

            try:
                conn = get_connection()
                cursor = conn.cursor()
                
                # Lecture des fichiers CSV
                for f in os.listdir(self.path):
                    if f.endswith(".csv"):
                        self.df = pd.concat([self.df, pd.read_csv(os.path.join(self.path, f))], ignore_index=True)

                # Création de la table si nécessaire
                cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS {self.table} "
                    "(id INT AUTO_INCREMENT PRIMARY KEY, nom VARCHAR(50), prenom VARCHAR(50))"
                )

                # Insertion des données CSV
                for _, row in self.df.iterrows():
                    cursor.execute(f"INSERT INTO {self.table} (nom, prenom) VALUES (%s, %s)", (row["nom"], row["prenom"]))

                # Exécution des requêtes SQL
                req = self.sql.split("-")[1:]
                for r in req:
                    if r.strip():
                        cursor.execute(r)
                
                conn.commit()

                # Chargement des données pour affichage
                tab = pd.read_sql(f"SELECT * FROM {self.table}", conn)
                tab["select"] = False
                st.session_state.tab = tab

                st.success(f"Job '{self.titre}' exécuté avec succès !")
                self.historique.insert_one({"Job": self.titre, "date execution": datetime.now(), "erreur": ""})
            except Exception as e:
                st.error(f"Erreur : {e}")
                self.historique.insert_one({"Job": self.titre, "date execution": datetime.now(), "erreur": str(e)})
            finally:
                if 'conn' in locals():
                    cursor.close()
                    conn.close()


# ================== MAIN ==================
job_manager = JobManager()
if st.button("Accueil"):
    st.switch_page("home.py")
st.header("CSV vers MySQL (dossier)")
titre, path , dbName ,host , table , requette_sql ,collection= job_manager.render_inputs()
MongoDB().ajouter_job(titre, path , dbName ,host , table , requette_sql, collection)
job_manager.executer()
job_manager.display_table()
job_manager.supprimer_lignes()
