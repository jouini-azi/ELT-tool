import streamlit as st
import pandas as pd
import os
from datetime import datetime
from core.auth import require_login
from core.session import init_session
from core.db import get_connection
from core.db import generate_create_table
from core.commun import commun
from pages.Mongo import MongoDB
########################* DONE ! *#################################

init_session()
require_login()


class csvFile(commun):
    def __init__(self):
        self.df = st.session_state.get("df", pd.DataFrame())
        self.selected = st.session_state.get("selected", pd.DataFrame())
        self.titre = st.session_state.get("titre", "")
        self.file = st.session_state.get("file", "")
        self.dbName = st.session_state.get("dbName", "")
        self.host = st.session_state.get("host", "")
        self.table = st.session_state.get("table", "")
        self.sql = st.session_state.get("sql", "")
        MongoDB().init_mongo()

    def render_inputs(self):
            """Affichage des inputs Streamlit"""
            col1, col2 = st.columns([3,1])
            with col1:
                self.titre = st.text_input("Titre")
                self.file = st.text_input("Path copmplet du ficher(.csv)")         
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
            st.session_state["titre"] = self.titre
            st.session_state["file"] = self.file
            st.session_state["dbName"] = self.dbName
            st.session_state["host"] = self.host
            st.session_state["table"] = self.table
            st.session_state["sql"] = self.sql


    def ajouter_job(self):
        """Ajouter un job dans MongoDB"""
        if st.button("Ajouter Job"):
            try:
                self.client.admin.command('ping')
            except Exception as e:
                st.error(f"Erreur MongoDB : {e}")
                return
            
            if self.titre and self.file and self.dbName and self.host and self.table:
                req = self.sql.split("-")[1:]  # On supprime le premier élément vide
                resultat = self.collection.insert_one({
                    "titre": self.titre,
                    "path": self.file,
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
        if st.button("Envoyer vers MySQL"):
            if not os.path.exists(self.file):  # check if the path exists
                st.error("File does not exist. Check the path.")
                return
            try:
                self.df = pd.read_csv(self.file)  # read CSV
                st.session_state['df']=self.df
                st.success("CSV loaded successfully!")

                conn = get_connection()
                cursor = conn.cursor()
                create_query = generate_create_table(self.df, self.table)
                cursor.execute(create_query)
                cols = [f"`{c.replace(' ', '_')}`" for c in self.df.columns]
                placeholders = ",".join(["%s"] * len(cols))

                insert_sql = f"""
                INSERT INTO `{self.table}` ({",".join(cols)})
                VALUES ({placeholders})
                """
                for _, row in self.df.iterrows():
                    cursor.execute(insert_sql, tuple(row))
                if self.sql:
                    req = self.sql.split("-")[1:]
                    for r in req:
                        r = r.strip()
                        if r:
                            try:
                                cursor.execute(r)
                                st.success(f"Requête exécutée : {r}")
                            except Exception as e:
                                st.error(f"Erreur lors de l'exécution de la requête '{r}': {e}")
                    conn.commit()
                    tab = pd.read_sql(f"SELECT * FROM {self.table}", conn)
                    tab["select"] = False
                    st.session_state.tab = tab


                    if self.client:
                        self.hist.insert_one({"Job": self.titre, "date execution": datetime.now(), "erreur": ""})
                        st.success("Données transférées vers MySQL avec succès !")

            except Exception as e:
                st.error(f"Error reading CSV: {e}")
                if self.client:
                    self.hist.insert_one({"Job": self.titre, "date execution": datetime.now(), "erreur": str(e)})
            finally:
                if 'conn' in locals():
                    cursor.close()
                    conn.close()
    def display_table(self):
        """Affichage du tableau éditable et sélection des lignes"""            
        if st.session_state.tab is not None:
            self.selected = st.session_state.get("selected", pd.DataFrame())

            edited_tab = st.data_editor(
																st.session_state.tab,
                key="table_editor",
                hide_index=False
            )

            if not edited_tab.equals(st.session_state.tab):
                st.session_state.tab = edited_tab
                st.session_state["selected"] = self.selected
                st.rerun()
            # Lignes sélectionnées
            self.selected = st.session_state.tab[st.session_state.tab["select"]]
            st.session_state.selected = self.selected
            st.write("Lignes sélectionnées")                
            st.write(self.selected)

                
    



obj = csvFile()
if st.button("Accueil"):
    st.switch_page("home.py")
st.set_page_config(page_title="Import CSV vers MySQL")

st.title("CSV vers MySQL")
obj.render_inputs()
obj.ajouter_job()
obj.executer()
obj.display_table()
obj.supprimer_lignes()




