import streamlit as st
import pandas as pd
import os
from pymongo import MongoClient
from datetime import datetime
from core.db import get_connection
from core.auth import require_login
from core.session import init_session
from core.db import generate_create_table
from core.commun import commun
from pages.Mongo import MongoDB

st.set_page_config(page_title="Import Excel vers MySQL")

init_session()
require_login()

class excelFile(commun):
  def __init__(self):
    self.df = pd.DataFrame()
    self.selected = pd.DataFrame()
    MongoDB().init_mongo()
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
            self.file = st.text_input("Path complet du fichier(.xls)")   
            self.dbName = st.text_input("Nom de la base")
            self.host = st.text_input("host")
            self.table = st.text_input("Nom de la table")
            self.files = pd.DataFrame()
        with col2:
            st.title("Requetes SQL")
            self.sql = st.text_area(
                'Entrez vos requetes SQL (precedées par " - " ) ', height=260
            )

  def ajouter_job(self):
        if st.button("Ajouter Job"):
            if not all([self.titre, self.file, self.dbName, self.host, self.table]):
                st.warning("Veuillez remplir tous les champs")
                return

            req = self.sql.split("-")[1:] if self.sql else []

            try:
                self.collection.insert_one({
                    "titre": self.titre,
                    "path": self.file,
                    "db": self.dbName,
                    "host": self.host,
                    "table": self.table,
                    "requete": req
                })
                st.success("Job ajouté")
            except Exception as e:
                st.error(f"MongoDB erreur : {e}")

        

  
  def executer(self):
    
    if st.button("Envoyer vers MySQL"):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            self.file=self.file+".xls"
            if self.file:
                if os.path.exists(self.file):  # check if the path exists
                    try:
                        self.df = pd.read_excel(self.file)  # read excel
                        st.success("Excel loaded successfully!")
                    except Exception as e:
                        st.error(f"Error reading Excel: {e}")
                else:
                    st.error("File does not exist. Check the path.")
            
            # 3. Afficher le dataframe
            st.subheader("Aperçu des données")
            st.dataframe(self.df)
            print(self.df)
            
            # Créer la table automatiquement
            create_query = generate_create_table(self.df, self.table)
            cursor.execute(create_query)

            # Insertion des données excel
            cols = [f"`{c.replace(' ', '_')}`" for c in self.df.columns]
            placeholders = ",".join(["%s"] * len(cols))

            insert_sql = f"""
            INSERT INTO `{self.table}` ({",".join(cols)})
            VALUES ({placeholders})
            """
            for _, row in self.df.iterrows():
                cursor.execute(insert_sql, tuple(row))
            req = self.sql.split("-")[1:]
            for r in req:
                if r.strip():
                    cursor.execute(r)

            conn.commit()
            st.success("Données transférées vers MySQL avec succès !")
            tab = pd.read_sql(f"SELECT * FROM {self.table}", conn)
            tab["select"] = False
            st.session_state.tab = tab

            self.hist.insert_one({"Job": self.titre, "date execution": datetime.now(), "erreur": ""})
        except Exception as e:
            st.error(f"Erreur : {e}")
            self.hist.insert_one({"Job": self.titre, "date execution": datetime.now(), "erreur": str(e)})
        finally:
            if 'conn' in locals():
                cursor.close()
                conn.close()
        







obj = excelFile()
if st.button("Accueil"):
    st.switch_page("home.py")


st.title("Excel vers MySQL")
obj.render_inputs()
obj.ajouter_job()
obj.executer()
obj.display_table()
obj.supprimer_lignes()




