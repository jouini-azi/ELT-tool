import streamlit as st
import pandas as pd
import os
from pymongo import MongoClient
from datetime import datetime
from core.db import get_connection
from core.auth import require_login
from core.session import init_session
from core.commun import commun


init_session()
require_login()

class JobManager(commun):
    def __init__(self):
        self.df = pd.DataFrame()
        self.selected = pd.DataFrame()
        self.init_mongo()
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
            self.path_doss = st.text_input("Chemin complet du dossier")
            self.dbName = st.text_input("Nom de la base")
            self.host = st.text_input("host")
            self.table = st.text_input("Nom de la table")
            self.files = pd.DataFrame()
        with col2:
            st.title("Requetes SQL")
            self.sql = st.text_area(
                'Entrez vos requetes SQL (precedées par " - " ) ',
                height=260
            )
    
    def ajouter_job(self):
        """Ajouter un job dans MongoDB"""
        if st.button("Ajouter Job"):
            try:
                self.client.admin.command('ping')
            except Exception as e:
                st.error(f"Erreur MongoDB : {e}")
                return
            
            if self.titre and self.path_doss and self.dbName and self.host and self.table:
                req = self.sql.split("-")[1:]  # On supprime le premier élément vide
                resultat = self.collection.insert_one({
                    "titre": self.titre,
                    "path": self.path_doss,
                    "db": self.dbName,
                    "host": self.host,
                    "table": self.table,
                    "requete": req
                })
                if resultat.inserted_id:
                    st.success(f"Job '{self.titre}' ajouté")
            else:
                st.warning("Veuillez remplir tous les champs correctement !")
    
    def executer(self):
      """Exécuter le job (Excel folder only)"""
      if st.button("Executer"):
          if not (self.titre and self.path_doss and self.dbName and self.host and self.table):
              st.warning("Veuillez remplir tous les champs correctement !")
              return

          try:
            conn = get_connection()
            cursor = conn.cursor()
              
              # Lecture des fichiers Excel uniquement
            all_dfs = []
            for f in os.listdir(self.path_doss):
                  if f.lower().endswith((".xls", ".xlsx", ".xlsm")):
                      file_path = os.path.join(self.path_doss, f)
                      try:
                          # Choix du moteur selon le type
                          if f.lower().endswith(".xls"):
                              df_tmp = pd.read_excel(file_path, engine="xlrd")
                          else:
                              df_tmp = pd.read_excel(file_path, engine="openpyxl")

                          # Cas Excel avec une seule colonne (CSV à l'intérieur)
                          if df_tmp.shape[1] == 1:
                              df_tmp = df_tmp[df_tmp.columns[0]].astype(str).str.split(",", expand=True)
                              df_tmp.columns = ["nom", "prenom"]

                          all_dfs.append(df_tmp)
                      except Exception as e:
                          st.warning(f"Fichier ignoré : {f} → {e}")

            if all_dfs:
                  self.df = pd.concat(all_dfs, ignore_index=True)
            else:
                  st.warning("Aucun fichier Excel valide trouvé")
                  return

              # Création de la table si nécessaire
            cursor.execute(
                  f"CREATE TABLE IF NOT EXISTS {self.table} "
                  "(id INT AUTO_INCREMENT PRIMARY KEY, nom VARCHAR(50), prenom VARCHAR(50))"
              )

              # Insertion des données Excel (rapide)
            sql = f"INSERT INTO {self.table} (nom, prenom) VALUES (%s, %s)"
            cursor.executemany(sql, self.df[["nom", "prenom"]].values.tolist())

              # Exécution des requêtes SQL additionnelles
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
            self.hist.insert_one({"Job": self.titre, "date execution": datetime.now(), "erreur": ""})

          except Exception as e:
              st.error(f"Erreur : {e}")
              self.hist.insert_one({"Job": self.titre, "date execution": datetime.now(), "erreur": str(e)})
          finally:
              if 'conn' in locals():
                  cursor.close()
                  conn.close()
          


# ================== MAIN ==================
job_manager = JobManager()
if st.button("Accueil"):
    st.switch_page("home.py")
st.header("Excel vers MySQL (dossier)")
job_manager.render_inputs()
job_manager.ajouter_job()
job_manager.executer()
job_manager.display_table()
job_manager.supprimer_lignes()
