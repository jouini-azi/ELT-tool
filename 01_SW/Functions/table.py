
from pymongo import MongoClient
import mysql.connector
import streamlit as st

class table:
  def generate_create_table(self,df, table_name):
      columns_sql = []
      for col, dtype in df.dtypes.items():
          col = col.replace(" ", "_")  # sécurité
          mysql_type = self.pandas_to_mysql(dtype)
          columns_sql.append(f"`{col}` {mysql_type}")

      columns_str = ",\n".join(columns_sql)

      query = f"""
      CREATE TABLE IF NOT EXISTS `{table_name}` (
          id INT AUTO_INCREMENT PRIMARY KEY,
          {columns_str}
      )
      """
      return query


  def pandas_to_mysql(self,dtype):
      if "int" in str(dtype):
          return "INT"
      elif "float" in str(dtype):
          return "FLOAT"
      elif "bool" in str(dtype):
          return "BOOLEAN"
      elif "datetime" in str(dtype):
          return "DATETIME"
      else:
          return "VARCHAR(255)"