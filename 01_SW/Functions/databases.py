
from pymongo import MongoClient
import mysql.connector
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

  def ajouter_job(self,job):
    """Ajouter un job dans MongoDB"""
    
    if job.titre and job.path and job.dbName and job.host and job.table:
        req = job.sql.split("-")[1:]
        resultat = job.collection.insert_one({
            "titre": job.titre,
            "path": job.path,
            "db": job.dbName,
            "host": job.host,
            "table": job.table,
            "requete": req
        })
        if resultat.inserted_id:
            st.success(f"Job '{job.titre}' ajouté")
    else:
        st.warning("Veuillez remplir tous les champs correctement !")


class Mysql:
  def connect_to_MySQL(self):
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="essai_app"
    )
