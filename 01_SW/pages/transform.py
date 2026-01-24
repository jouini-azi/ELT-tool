import streamlit as st
import mysql.connector
import pandas as pd
from pages.JOB_new import JobManager
from core.auth import require_login
from core.session import init_session

init_session()
require_login()

st.set_page_config(page_title="Transformations",layout="wide")

col1, col2, col3, col4, col5= st.columns([1,1,1,1,1])
with col1:
  st.button("test1")
with col2:
  st.button("test2")
with col3:
  st.button("test3")
with col4:
  st.button("test4")
with col5:
  st.button("test5")
  
job=JobManager()
job.executer()

#if st.session_state.get("df") is not None:
 # st.dataframe(st.session_state["df"])
  #print(st.session_state["df"])
#else: 
 # st.warning("aucune donnée disponible")


params=st.query_params
if params.get("run")==["executer"] or params.get("run")=="executer":
  if "df" in st.session_state:
    df_result =st.session_state["df"]
    st.dataframe(df_result)
  else: 
    st.warning("aucune donnée disponible")
else:
  print(st.session_state["df"])
  st.warning("acces directe non autorisé")
