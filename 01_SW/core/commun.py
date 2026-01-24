import streamlit as st
import pandas as pd
from core.db import get_connection

class commun:     
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

  def supprimer_lignes(self):
    """Supprimer les lignes sélectionnées"""
    if st.button("Supprimer lignes") and not self.selected.empty:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            for _, s in self.selected.iterrows():
                cursor.execute(f"DELETE FROM {self.table} WHERE id = %s", (s["id"],))
            conn.commit()
            st.success("Lignes supprimées avec succès")
        except Exception as e:
            st.error(f"Erreur suppression : {e}")
        finally:
            if 'conn' in locals():
                cursor.close()
                conn.close()