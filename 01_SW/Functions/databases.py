
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
            "requete": req,
            "type":job.type
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

# def pandas_to_mysql(dtype):
#     if "int" in str(dtype):
#         return "INT"
#     elif "float" in str(dtype):
#         return "FLOAT"
#     elif "bool" in str(dtype):
#         return "BOOLEAN"
#     elif "datetime" in str(dtype):
#         return "DATETIME"
#     else:
#         return "VARCHAR(255)"

# def generate_create_table(df, table_name):
#     columns_sql = []
#     for col, dtype in df.dtypes.items():
#         col = col.replace(" ", "_")  # sécurité
#         mysql_type = pandas_to_mysql(dtype)
#         columns_sql.append(f"`{col}` {mysql_type}")

#     columns_str = ",\n".join(columns_sql)

#     query = f"""
#     CREATE TABLE IF NOT EXISTS `{table_name}` (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         {columns_str}
#     )
#     """
#     return query