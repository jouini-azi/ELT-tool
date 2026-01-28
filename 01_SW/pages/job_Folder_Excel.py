import streamlit as st
from core.auth import require_login
from core.session import init_session
from core.commun import commun
from Functions.databases import MongoDB
from Functions.inputs import inputs
from models.job import job_Folder_Excel


init_session()
require_login()
st.set_page_config(page_title="Excel vers MySQL (dossier)")

if st.button("Accueil"):
    st.switch_page("Accueil.py")
st.title("Excel vers MySQL (dossier)")
st.markdown("---")


if st.session_state["role"]=="admin":
    titre, path , dbName ,host , table , sql  = inputs().render_inputs_folder()
    ExcelFolder = job_Folder_Excel(titre,path,dbName,host,table,sql)

    if st.button("Ajouter Job"):
        MongoDB().ajouter_job(ExcelFolder)
    
    if st.button("Executer"):
        ExcelFolder.executer()
    commun().display_table()
    commun().supprimer_lignes(table=ExcelFolder.table)
else:
    st.warning("Vous n'etes pas autorisé à acceder à cette page !")
