import streamlit as st
import io
import pandas as pd
import mysql.connector
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from core.auth import require_login
from core.session import init_session

init_session()
require_login()

# -------------------------------
# STREAMLIT UI
# -------------------------------
st.set_page_config(page_title="SharePoint to MySQL")
st.title("SharePoint File to MySQL")

site_url = st.text_input(
    "SharePoint site URL",
    "https://mohetn.sharepoint.com/sites/test8195"
)

username = st.text_input(
    "SharePoint username",
    "hiba.dhouib@djerba.r-iset.tn"
)

password = st.text_input(
    "SharePoint password",
    type="password"
)

file_path = st.text_input(
    "File path in SharePoint",
    "/sites/test8195/Shared Documents/Classeur2.xlsx"
)

st.markdown("---")

# -------------------------------
# MYSQL CONFIG (EDIT IF NEEDED)
# -------------------------------
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"
MYSQL_DATABASE = "essai_app"
MYSQL_TABLE = "excel_data"

# -------------------------------
# IMPORT BUTTON
# -------------------------------
if st.button("Import File"):

    try:
        # -------------------------------
        # 1️⃣ CONNECT TO SHAREPOINT
        # -------------------------------
        ctx = ClientContext(site_url).with_credentials(
            UserCredential(username, password)
        )

        # -------------------------------
        # 2️⃣ DOWNLOAD FILE INTO MEMORY
        # -------------------------------
        sp_file = ctx.web.get_file_by_server_relative_url(file_path)
        buffer = io.BytesIO()
        sp_file.download(buffer)
        ctx.execute_query()

        buffer.seek(0)

        # -------------------------------
        # 3️⃣ READ FILE WITH PANDAS
        # -------------------------------
        if file_path.endswith(".csv"):
            df = pd.read_csv(buffer)
        else:
            df = pd.read_excel(buffer)

        st.success("File read successfully from SharePoint")
        st.dataframe(df)

        # -------------------------------
        # 4️⃣ CONNECT TO MYSQL
        # -------------------------------
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )

        cursor = conn.cursor()

        # -------------------------------
        # 5️⃣ CREATE TABLE IF NOT EXISTS
        # -------------------------------
        columns_sql = ", ".join(
            [f"`{col}` TEXT" for col in df.columns]
        )

        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {MYSQL_TABLE} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            {columns_sql}
        )
        """

        cursor.execute(create_table_sql)

        # -------------------------------
        # 6️⃣ INSERT DATA INTO MYSQL
        # -------------------------------
        placeholders = ", ".join(["%s"] * len(df.columns))
        columns = ", ".join([f"`{c}`" for c in df.columns])

        insert_sql = f"""
        INSERT INTO {MYSQL_TABLE} ({columns})
        VALUES ({placeholders})
        """

        for _, row in df.iterrows():
            cursor.execute(insert_sql, tuple(row))

        conn.commit()

        cursor.close()
        conn.close()

        st.success("Data inserted into MySQL successfully!")

    except Exception as e:
        st.error(f"Failed: {e}")
