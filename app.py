
import streamlit as st
import pandas as pd
import yaml
import os
import sys

import dashboard  # ✅ Fix dashboard reference

from dq_agent.core.rules_engine import apply_rules # ✅ Rule engine logic
from dq_agent.db_connector_ui import database_connector_ui  # ✅ Dynamic DB UI

st.set_page_config(page_title="Trudata: Autonomous DQ Agent", layout="wide")

page = st.sidebar.selectbox("📂 Select Page", ["Dashboard", "Data Quality Agent"])

if page == "Dashboard":
    dashboard.run(
        metrics_data=st.session_state.get("metrics"),
        rule_issues=st.session_state.get("rule_issues")
    )

else:
    st.image("Assets/trudata_logo.png", width=200)
    st.markdown("## Trudata: Autonomous Data Quality Agent")

    tab1, tab2 = st.tabs(["🧪 Rule Builder", "✅ Run Validator"])

    # ------------------- CSV Upload + Rule Builder -------------------
    with tab1:
        st.markdown("### 📥 Upload CSV for Rule Builder")
        uploaded_file = st.file_uploader("Choose your data file", type="csv")

        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.success("CSV uploaded successfully!")
            st.markdown("### 👀 Data Preview")
            st.dataframe(df.head())

            st.markdown("### 🧠 Define Rules")
            columns = df.columns.tolist()
            rule_configs = []

            for col in columns:
                with st.expander(f"Rules for **{col}**"):
                    rules = []
                    if st.checkbox("Not null", key=f"{col}_not_null"):
                        rules.append("not_null")
                    if st.checkbox("Unique", key=f"{col}_uniq"):
                        rules.append("unique")
                    if st.checkbox("Range", key=f"{col}_range"):
                        col1, col2 = st.columns(2)
                        min_val = col1.number_input("Min", key=f"{col}_min")
                        max_val = col2.number_input("Max", key=f"{col}_max")
                        rules.append({"range": {"min": min_val, "max": max_val}})
                    if st.checkbox("Regex", key=f"{col}_regex"):
                        pattern = st.text_input("Regex pattern", key=f"{col}_pattern")
                        rules.append({"pattern": pattern})
                    if rules:
                        rule_configs.append({"column": col, "rules": rules})

            if rule_configs:
                yaml_obj = {"rules": rule_configs}
                config = yaml_obj

                issues = apply_rules(df, config)
                st.session_state["rule_issues"] = issues

                total = len(df)
                failed = len(issues)
                quality_score = round((1 - failed / total) * 100, 2) if total > 0 else 0
                active_policies = len(config["rules"])
                compliance_score = "100%" if quality_score >= 95 else "85%"

                st.session_state["metrics"] = {
                    "Data Assets": str(total),
                    "Quality Score": f"{quality_score}%",
                    "Active Policies": str(active_policies),
                    "Compliance": compliance_score
                }

                st.warning(f"⚠️ {failed} rows failed validation")
                st.markdown("### ✅ Rules Applied")
                st.write(rule_configs)

    # ------------------- Database Source + Rule Validator -------------------
    with tab2:
        st.markdown("### 🧭 Connect to a Database and Run Validation")
        database_connector_ui()

        if 'dataframe' in st.session_state:
            df = st.session_state['dataframe']
            st.markdown("### 👀 Preview from Database")
            st.dataframe(df.head())

            if st.button("🚀 Run Rules on Database Table"):
                config = {
                    "rules": [
                        {"column": col, "rules": ["not_null"]}
                        for col in df.columns
                    ]
                }

                issues = apply_rules(df, config)
                st.session_state["rule_issues"] = issues

                total = len(df)
                failed = len(issues)
                quality_score = round((1 - failed / total) * 100, 2) if total > 0 else 0
                active_policies = len(config["rules"])
                compliance_score = "100%" if quality_score >= 95 else "85%"

                st.session_state["metrics"] = {
                    "Data Assets": str(total),
                    "Quality Score": f"{quality_score}%",
                    "Active Policies": str(active_policies),
                    "Compliance": compliance_score
                }

                st.warning(f"⚠️ {failed} rows failed validation")
                st.markdown("### ✅ Basic Rules Applied on DB Table")
                st.write(config["rules"])
