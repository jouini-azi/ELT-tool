import streamlit as st
class inputs:
  def render_inputs_file(self):
          """Affichage des inputs Streamlit"""
          col1, col2 = st.columns([3,1])
          with col1:
              self.titre = st.text_input("**Titre**")
              self.path = st.text_input("**Path copmplet du ficher**")
              self.dbName = st.text_input("**Nom de la base**","elt_tool")
              self.host = st.text_input("**Host**","localhost")
              self.table = st.text_input("**Nom de la table**")
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
          return self.titre, self.path , self.dbName ,self.host , self.table,self.sql
  
  def render_inputs_folder(self):
        """Affichage des inputs Streamlit"""
        col1, col2 = st.columns([3,1])
        with col1:
            self.titre = st.text_input("**Titre**")
            self.path = st.text_input("**Path copmplet du dossier**")
            self.dbName = st.text_input("**Nom de la base**","elt_tool")
            self.host = st.text_input("**Host**","localhost")
            self.table = st.text_input("**Nom de la table**")
        with col2:
            st.title("Requetes SQL")
            self.sql = st.text_area(
                '**Entrez vos requetes SQL (precedées par " - " ) **',
                height=260
            )
        st.session_state["titre"] = self.titre
        st.session_state["file"] = self.path
        st.session_state["dbName"] = self.dbName
        st.session_state["host"] = self.host
        st.session_state["table"] = self.table
        st.session_state["sql"] = self.sql
        return self.titre, self.path , self.dbName ,self.host , self.table,self.sql
  
