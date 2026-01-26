import streamlit as st
import pandas as pd
import os
from pymongo import MongoClient
from datetime import datetime
from Functions.databases import Mysql
from core.auth import require_login
from core.session import init_session
from core.db import generate_create_table
from core.commun import commun
from Functions.databases import MongoDB
from Functions.inputs import inputs
from pages.job import job



st.set_page_config(page_title="Import Excel vers MySQL")

init_session()
require_login()



class excelFile(job):
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


  def executer(self):
    
    if st.button("Envoyer vers MySQL"):
        try:
            conn = Mysql().connect_to_MySQL()
            cursor = conn.cursor()
            self.path=self.path+".xls"
            if self.path:
                if os.path.exists(self.path):  # check if the path exists
                    try:
                        self.df = pd.read_excel(self.path)  # read excel
                        st.success("Excel loaded successfully!")
                    except Exception as e:
                        st.error(f"Error reading Excel: {e}")
                else:
                    st.error("File does not exist. Check the path.")
            
            # 3. Afficher le dataframe
            st.subheader("Aperçu des données")
            st.dataframe(self.df)
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
        







ExcelFile = excelFile()
if st.button("Accueil"):
    st.switch_page("home.py")


st.title("Excel vers MySQL")
titre, path , dbName ,host , table , sql = inputs().render_inputs_file()
if st.button("Ajouter Job"):
    MongoDB().ajouter_job(job(titre,path,dbName,host,table,sql))
ExcelFile.executer()
commun().display_table()
commun().supprimer_lignes()




