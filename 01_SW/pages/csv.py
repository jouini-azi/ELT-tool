import streamlit as st
import pandas as pd
import os
from datetime import datetime
from core.auth import require_login
from core.session import init_session
from core.db import get_connection
from core.db import generate_create_table
from core.commun import commun
from Functions.databases import MongoDB


init_session()
require_login()


class csvFile(commun):
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

    def render_inputs(self):
        """Affichage des inputs Streamlit"""
        col1, col2 = st.columns([3,1])
        with col1:
            self.titre = st.text_input("Titre")
            self.path = st.text_input("Path copmplet du ficher(.csv)")
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
        
        return self.titre , self.path , self.dbName , self.host , self.table , self.sql

  
    def executer(self):        
        if st.button("Envoyer vers MySQL"):
            if not os.path.exists(self.path):  # check if the path exists
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
                        self.historique.insert_one({"Job": self.titre, "date execution": datetime.now(), "erreur": ""})
                        st.success("Données transférées vers MySQL avec succès !")

            except Exception as e:
                st.error(f"Error reading CSV: {e}")
                if self.client:
                    self.historique.insert_one({"Job": self.titre, "date execution": datetime.now(), "erreur": str(e)})
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

titre, path , dbName ,host , table , requette_sql =obj.render_inputs()
MongoDB().ajouter_job(titre, path , dbName ,host , table , requette_sql)
obj.executer()
obj.display_table()
obj.supprimer_lignes()




