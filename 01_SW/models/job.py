import streamlit as st
import pandas as pd
import os
from datetime import datetime
from core.auth import require_login
from core.session import init_session
from Functions.databases import generate_create_table
from core.commun import commun
from Functions.databases import MongoDB
from Functions.databases import Mysql
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


############################################################################

class csvFile(job):
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



  
    def executer(self):        
        if st.button("Envoyer vers MySQL"):
            try:
                conn = Mysql().connect_to_MySQL()
                cursor = conn.cursor()
                self.path=self.path+".csv"
                if self.path:
                    if os.path.exists(self.path):  # check if the path exists
                        try:
                            self.df = pd.read_csv(self.path)  # read excel
                            st.success("Csv loaded successfully!")
                        except Exception as e:
                            st.error(f"Error reading Csv: {e}")
                    else:
                        st.error("File does not exist. Check the path.")

                st.subheader("Aperçu des données")
                st.dataframe(self.df)      
               
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

###########################################################################################################

class excelFile(job):
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

######################################################################################################

class job_Folder_CSV(job):
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
    
    def executer(self):
        """Exécuter le job"""
        if st.button("Executer"):
            if not (self.titre and self.path and self.dbName and self.host and self.table):
                st.warning("Veuillez remplir tous les champs correctement !")
                st.switch_page("pages/transform.py")
                return

            try:
                conn = Mysql().connect_to_MySQL()
                cursor = conn.cursor()
                
                # Lecture des fichiers CSV
                for f in os.listdir(self.path):
                    if f.endswith(".csv"):
                        self.df = pd.concat([self.df, pd.read_csv(os.path.join(self.path, f))], ignore_index=True)

                # Création de la table si nécessaire
                cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS {self.table} "
                    "(id INT AUTO_INCREMENT PRIMARY KEY, nom VARCHAR(50), prenom VARCHAR(50))"
                )

                # Insertion des données CSV
                for _, row in self.df.iterrows():
                    cursor.execute(f"INSERT INTO {self.table} (nom, prenom) VALUES (%s, %s)", (row["nom"], row["prenom"]))

                # Exécution des requêtes SQL
                req = self.sql.split("-")[1:]
                for r in req:
                    if r.strip():
                        cursor.execute(r)
                
                conn.commit()

                # Chargement des données pour affichage
                tab = pd.read_sql(f"SELECT * FROM {self.table}", conn)
                tab["select"] = False
                st.session_state.tab = tab

                st.success(f"Job '{self.titre}' exécuté avec succès !")
                self.historique.insert_one({"Job": self.titre, "date execution": datetime.now(), "erreur": ""})
            except Exception as e:
                st.error(f"Erreur : {e}")
                self.historique.insert_one({"Job": self.titre, "date execution": datetime.now(), "erreur": str(e)})
            finally:
                if 'conn' in locals():
                    cursor.close()
                    conn.close()
##################################################################################################

class job_Folder_Excel(job):
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



    
    def executer(self):
      """Exécuter le job (Excel folder only)"""
      if st.button("Executer"):
          if not (self.titre and self.path and self.dbName and self.host and self.table):
              st.warning("Veuillez remplir tous les champs correctement !")
              return

          try:
            conn = Mysql().connect_to_MySQL()
            cursor = conn.cursor()
              
              # Lecture des fichiers Excel uniquement
            all_dfs = []
            for f in os.listdir(self.path):
                  if f.lower().endswith((".xls", ".xlsx", ".xlsm")):
                      file_path = os.path.join(self.path, f)
                      try:
                          # Choix du moteur selon le type
                          if f.lower().endswith(".xls"):
                              df_tmp = pd.read_excel(file_path, engine="xlrd")
                          else:
                              df_tmp = pd.read_excel(file_path, engine="openpyxl")

                          # Cas Excel avec une seule colonne (CSV à l'intérieur)
                          if df_tmp.shape[1] == 1:
                              df_tmp = df_tmp[df_tmp.columns[0]].astype(str).str.split(",", expand=True)
                              df_tmp.columns = ["nom", "prenom"]

                          all_dfs.append(df_tmp)
                      except Exception as e:
                          st.warning(f"Fichier ignoré : {f} → {e}")

            if all_dfs:
                  self.df = pd.concat(all_dfs, ignore_index=True)
            else:
                  st.warning("Aucun fichier Excel valide trouvé")
                  return

              # Création de la table si nécessaire
            cursor.execute(
                  f"CREATE TABLE IF NOT EXISTS {self.table} "
                  "(id INT AUTO_INCREMENT PRIMARY KEY, nom VARCHAR(50), prenom VARCHAR(50))"
              )

              # Insertion des données Excel (rapide)
            sql = f"INSERT INTO {self.table} (nom, prenom) VALUES (%s, %s)"
            cursor.executemany(sql, self.df[["nom", "prenom"]].values.tolist())

              # Exécution des requêtes SQL additionnelles
            req = self.sql.split("-")[1:]
            for r in req:
                  if r.strip():
                      cursor.execute(r)
              
            conn.commit()

              # Chargement des données pour affichage
            tab = pd.read_sql(f"SELECT * FROM {self.table}", conn)
            tab["select"] = False
            st.session_state.tab = tab

            st.success(f"Job '{self.titre}' exécuté avec succès !")
            self.historique.insert_one({"Job": self.titre, "date execution": datetime.now(), "erreur": ""})

          except Exception as e:
              st.error(f"Erreur : {e}")
              self.historique.insert_one({"Job": self.titre, "date execution": datetime.now(), "erreur": str(e)})
          finally:
              if 'conn' in locals():
                  cursor.close()
                  conn.close()
          