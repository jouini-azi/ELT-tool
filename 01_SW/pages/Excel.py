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
from Functions.databases import MongoDB

st.set_page_config(page_title="Import Excel vers MySQL")

init_session()
require_login()

class excelFile(commun):
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
            self.path = st.text_input("Path copmplet du ficher")
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
        
        return self.titre , self.path , self.dbName , self.host , self.table , self.sql,self.collection


        

  
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

            self.historique.insert_one({"Job": self.titre, "date execution": datetime.now(), "erreur": ""})
        except Exception as e:
            st.error(f"Erreur : {e}")
            self.historique.insert_one({"Job": self.titre, "date execution": datetime.now(), "erreur": str(e)})
        finally:
            if 'conn' in locals():
                cursor.close()
                conn.close()
        







obj = excelFile()
if st.button("Accueil"):
    st.switch_page("home.py")


st.title("Excel vers MySQL")
titre, path , dbName ,host , table , requette_sql,collection  = obj.render_inputs()
MongoDB().ajouter_job(titre, path , dbName ,host , table , requette_sql,collection)
obj.executer()
obj.display_table()
obj.supprimer_lignes()




