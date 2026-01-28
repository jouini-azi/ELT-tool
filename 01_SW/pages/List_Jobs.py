import streamlit as st
from core.auth import require_login
from core.session import init_session
from core.job_manager import JobManager

init_session()
require_login()

st.set_page_config(page_title="Jobs")
if st.button("Accueil"):
    st.switch_page("Accueil.py")
    
st.title("Jobs")
st.markdown("---")


JobManager().display_jobs()