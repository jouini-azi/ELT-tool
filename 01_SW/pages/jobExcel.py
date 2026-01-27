import streamlit as st
from core.auth import require_login
from core.session import init_session
from core.commun import commun
from Functions.databases import MongoDB
from Functions.inputs import inputs
from models.job import excelFile




st.set_page_config(page_title="Import Excel vers MySQL")

init_session()
require_login()


if st.button("Accueil"):
    st.switch_page("home.py")
st.title("Excel vers MySQL")
st.markdown("---")

if st.session_state["role"]=="admin":
    
    titre, path , dbName ,host , table , sql = inputs().render_inputs_file()
    ExcelFile = excelFile(titre,path,dbName,host,table,sql)

    if st.button("Ajouter Job"):
        MongoDB().ajouter_job(ExcelFile)
    ExcelFile.executer()
    commun().display_table()
    commun().supprimer_lignes(table=ExcelFile.table)
else:
    st.warning("Vous n'etes pas autorisé à acceder à cette page !")



