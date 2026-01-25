
from pymongo import MongoClient
import streamlit as st
class MongoDB:
  def connect_to_mongodb(self):
    """Connexion à MongoDB"""
    try:
        self.uri = "mongodb://localhost:27017/"
        self.client = MongoClient(self.uri)
        self.db = self.client.app
        self.collection = self.db.test_job
        self.historique = self.db.historique
        return self.uri , self.client , self.db , self.collection , self.historique
    except Exception:
        self.client=None

  def ajouter_job(self,titre, path , dbName ,host , table , requette_sql):
    """Ajouter un job dans MongoDB"""
    if st.button("Ajouter Job"):
        if titre and path and dbName and host and table:
            req = requette_sql.split("-")[1:]
            resultat = self.collection.insert_one({
                "titre": titre,
                "path": path,
                "db": dbName,
                "host": host,
                "table": table,
                "requete": req
            })
            if resultat.inserted_id:
                st.success(f"Job '{titre}' ajouté")
        else:
            st.warning("Veuillez remplir tous les champs correctement !")


class Mysql:
  pass