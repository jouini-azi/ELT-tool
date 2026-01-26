import streamlit as st
import pandas as pd
import os
from datetime import datetime
from core.auth import require_login
from core.session import init_session
from core.db import generate_create_table
from core.commun import commun
from Functions.databases import MongoDB
from Functions.inputs import inputs


class job():
    def __init__(self,titre,path,dbName,host,table,sql):
        self.df = st.session_state.get("df", pd.DataFrame())
        self.selected = st.session_state.get("selected", pd.DataFrame())
        self.titre = titre
        self.path = path
        self.dbName = dbName
        self.host = host
        self.table = table
        self.sql = sql
        self.uri , self.client , self.db , self.collection , self.historique = MongoDB().connect_to_mongodb()
    
    def supprimer(self):
        self.collection.delete_one({"_id": self['_id']})
        st.success(f"{self.titre} supprimé avec succès !")
        st.rerun()