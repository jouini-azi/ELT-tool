import streamlit as st
from core.auth import require_login
from core.session import init_session
from core.job_manager import JobManager

init_session()
require_login()

st.set_page_config(page_title="Jobs")
if st.button("Accueil"):
    st.switch_page("home.py")
    
st.title("Jobs")
st.markdown("---")


job_manager = JobManager()
job_manager.display_jobs()