
import streamlit as st
import pandas as pd
from core import db_connectors

def database_connector_ui():
    st.header("🔗 Connect to a Data Source")

    db_type = st.selectbox("Select Database Type", [
        "postgresql", "mysql", "sqlite", "snowflake", 
        "sqlserver", "oracle", "redshift", "athena", "bigquery"
    ])

    credentials = {}
    if db_type in ["postgresql", "mysql", "redshift", "sqlserver", "oracle"]:
        credentials['host'] = st.text_input("Host")
        credentials['port'] = st.text_input("Port")
        credentials['database'] = st.text_input("Database Name")
        credentials['user'] = st.text_input("Username")
        credentials['password'] = st.text_input("Password", type="password")
        if db_type == "oracle":
            credentials['sid'] = st.text_input("Oracle SID")
    elif db_type == "snowflake":
        credentials['user'] = st.text_input("User")
        credentials['password'] = st.text_input("Password", type="password")
        credentials['account'] = st.text_input("Account")
        credentials['warehouse'] = st.text_input("Warehouse")
        credentials['database'] = st.text_input("Database")
        credentials['schema'] = st.text_input("Schema")
    elif db_type == "athena":
        credentials['s3_staging_dir'] = st.text_input("S3 Staging Directory")
        credentials['region'] = st.text_input("AWS Region")
    elif db_type == "sqlite":
        credentials['filepath'] = st.text_input("SQLite File Path")
    elif db_type == "bigquery":
        st.info("BigQuery uses service account credentials from environment.")

    if st.button("🔌 Connect and Preview"):
        try:
            engine = db_connectors.get_sqlalchemy_engine(db_type, **credentials)
            table_name = st.text_input("Enter table name to preview")
            if table_name:
                df = db_connectors.preview_table(engine, table_name)
                st.success("✅ Connection successful. Preview below:")
                st.dataframe(df.head())
                st.session_state['dataframe'] = df
        except Exception as e:
            st.error(f"❌ Connection failed: {e}")
