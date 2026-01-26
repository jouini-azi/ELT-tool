import streamlit as st
from Functions.databases import Mysql

from core.auth import require_login
from core.session import init_session
import pandas as pd
from core.commun import commun

init_session()
require_login()

class UserManager(commun):
    def add_user(self, username, password, role="user"):
      conn = Mysql().connect_to_MySQL()

      cursor = conn.cursor()
      query = f"""
                INSERT INTO `users`(`username`, `password`, `role`)
                VALUES (`{username}`,`{password}`, `{role}`)
                """
      cursor.execute(query)


    def delete_user(self, username):
      conn = Mysql().connect_to_MySQL()
      cursor = conn.cursor()
      query = f"""
                DELETE FROM `users` WHERE username={username}
                """
      cursor.execute(query)

    def update_user(self, username, new_password):
      conn = Mysql().connect_to_MySQL()
      cursor = conn.cursor()
      query = f"""
                UPDATE `users` SET `password`='{new_password}' WHERE username={username}
                """
      cursor.execute(query)

    def get_users(self):
      conn = Mysql().connect_to_MySQL()
      query = f"""SELECT * FROM users"""
      st.session_state.tab = pd.read_sql(query,conn)
      self.display_table()

u=UserManager()
u.get_users()


