import streamlit as st
from core.auth import require_login
from core.session import init_session

init_session()
require_login()

st.set_page_config(page_title="Nouveau job")
if st.button("Accueil"):
    st.switch_page("Accueil.py")
st.title("Nouveau job")
st.markdown("---")


if st.session_state["role"]=="admin":
  col1, col2, col3, col4= st.columns([1,1,1,1])
  with col1:
    if st.button("CSV to MySQL"):
      st.switch_page("pages/Job_CSV.py")
  with col2:
    if st.button("Excel to MySQL"):
      st.switch_page('pages/Job_Excel.py')
  with col3:
    if st.button("Folder Excel to MySQL"):
      st.switch_page('pages/job_Folder_Excel.py')
  with col4:
    if st.button("Folder CSV to MySQL"):
      st.switch_page('pages/job_Folder_CSV.py')
else:
    st.warning("Vous n'estes pas autorisé à acceder à cette page !")