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
from Functions.inputs import inputs


init_session()
require_login()

class JobManager(commun):
    def __init__(self):
        self.df = st.session_state.get("df", pd.DataFrame())
        self.selected = st.session_state.get("selected", pd.DataFrame())
        self.titre = st.session_state.get("titre", "")
        self.path = st.session_state.get("file", "")
        self.dbName = st.session_state.get("dbName", "")
        self.host = st.session_state.get("host", "")
        self.table = st.session_state.get("table", "")
        self.sql = st.session_state.get("sql", "")
        self.uri , self.client , self.db , self.collection , self.historique = MongoDB().connect_to_mongodb()
    #def init_session(self):
        #"""Initialisation des states"""
        #if "tab" not in st.session_state:
        #    st.session_state.tab = None
        #if "df" not in st.session_state:
        #    st.session_state.df = pd.DataFrame()


    
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
titre, path , dbName ,host , table , sql= inputs().render_inputs_folder()
MongoDB().ajouter_job(titre, path , dbName ,host , table , sql, job_manager.collection)
job_manager.executer()
job_manager.display_table()
job_manager.supprimer_lignes()
