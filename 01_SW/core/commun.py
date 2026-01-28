import streamlit as st
import pandas as pd
from Functions.databases import Mysql


class commun:
    st.session_state.tab=pd.DataFrame()
    st.session_state.tab["select"]=False
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

    

    def supprimer_lignes(self,table):
        """Supprimer les lignes sélectionnées"""
        if st.button("Supprimer lignes"):
            # Vérifier si le tableau existe et contient des lignes sélectionnées
            if "tab" not in st.session_state or st.session_state.tab.empty:
                st.warning("Aucune ligne à supprimer.")
                return

            # Extraire les lignes sélectionnées
            self.selected = st.session_state.tab[st.session_state.tab["select"] == True]
            if self.selected.empty:
                st.warning("Aucune ligne sélectionnée.")
                return

            try:
                # Connexion à MySQL
                conn = Mysql().connect_to_MySQL()  # Assurez-vous que connect_to_MySQL() prend self
                cursor = conn.cursor()

                # Supprimer les lignes une par une
                for _, row in self.selected.iterrows():
                    cursor.execute(f"DELETE FROM {table} WHERE id = %s", (row["id"],))
                
                conn.commit()

                # Mettre à jour le tableau pour l'affichage
                st.session_state.tab = st.session_state.tab[st.session_state.tab["select"] == False]

                st.success("Lignes supprimées avec succès !")
            except Exception as e:
                st.error(f"Erreur suppression : {e}")
            finally:
                if 'conn' in locals():
                    cursor.close()
                    conn.close()