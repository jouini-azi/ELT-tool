import streamlit as st
from Functions.databases import Mysql
from core.login import Login
from core.auth import require_login
from core.session import init_session
import pandas as pd
from core.commun import commun
import re
pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{10,}$'
init_session()
require_login()

class UserManager(commun):
    def add_user(self, username, password, role):
      try:
        
        conn=Mysql().connect_to_MySQL()
        cursor = conn.cursor()
        query=f"INSERT INTO `users`(`username`, `password`, `role`) VALUES ('{username}','{password}', '{role}')"
        if not re.match(pattern,password):
          st.warning("Mot de passe invalide: Mot de passe doit avoir 10 caractères (Majuscule, miniscule, chiffre, caractère special)")
          return
        cursor.execute(query)
        st.success("utilisateur "+username+" ajouté avec succes !")
        conn.commit()
      except Exception as e:
          st.error(e.args)
      finally:
          cursor.close()
          conn.close()


    def delete_user(self, username):
      try:
        conn = Mysql().connect_to_MySQL()
        cursor = conn.cursor()
        query = "DELETE FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        if cursor.rowcount == 0:
            st.warning("Utilisateur introuvable.")
            return

        conn.commit()
        st.success(f"Utilisateur '{username}' supprimé avec succès.")
        if st.session_state.get("username") == username:
            Login().logout()
      except Exception as e:
          st.error(str(e))
      finally:
          cursor.close()
          conn.close()

    def update_username(self,old_username,new_username):
      try:
        conn=Mysql().connect_to_MySQL()
        query=f"UPDATE `users` SET `username`='{new_username}' WHERE username='{old_username}'"
        cursor = conn.cursor()
        cursor.execute(query)
        st.success("Username changé avec succes !")
        conn.commit()
      except Exception as e:
          st.error(e.args)

    def update_password(self,username,old_pass, new_pass):
      try:
        conn=Mysql().connect_to_MySQL()
        query=f"UPDATE `users` SET `password`='{new_pass}' WHERE username='{username}' AND password='{old_pass}'"
        cursor = conn.cursor()
        if not re.match(pattern,new_pass):
          st.warning("Mot de passe invalide: Mot de passe doit avoir 10 caractères (Majuscule, miniscule, chiffre, caractère special)")
          return
        cursor.execute(query)
        st.success("Mot de passe changé avec succes !")
        conn.commit()
      except Exception as e:
        st.error(e.args)

    def update_role(self, username,old_role, new_role):
      try:
        conn=Mysql().connect_to_MySQL()
        query=f"UPDATE `users` SET `role`='{new_role}' WHERE username='{username}' AND role='{old_role}'"
        cursor = conn.cursor()
        cursor.execute(query)
        st.success("Role changé avec succes !")
        
        conn.commit()
        if st.session_state.get("username") == username:
            Login().logout()

      except Exception as e:
        st.error(e.args)

    def get_users(self):
      conn = Mysql().connect_to_MySQL()
      query = f"""SELECT * FROM users"""
      cursor=conn.cursor(dictionary=True)
      cursor.execute(query)
      users = cursor.fetchall()
      st.session_state.users = users
      for u in users:
         with st.expander(u['username']):
            name=st.text_input("Username",u["username"])
            password=st.text_input("Mot de passe",u["password"],type="password")
            if u["role"]=="admin":
              role=st.selectbox("Role",options=['admin','user'],index=0,key=u['id'])
            elif u["role"]=="user":
              role=st.selectbox("Role",options=['admin','user'],index=1,key=u['id'])
            col1,col2=st.columns(2)   
            with col1:              
              if st.button("Supprimer utilisateur",key=str(u["id"])+"s"):
                self.delete_user(u["username"])
                st.rerun()
            with col2:
              save=st.button("Enregistrer les modifications",key=str(u["id"])+"e")
            if save:              
              if u["username"]!=name:
                  UserManager().update_username(u["username"],name)
              if u["password"]!= password:
                UserManager().update_password(u["username"],u["password"], password)
              if u["role"]!=role:
                UserManager().update_role(u["username"],u["role"],role)


