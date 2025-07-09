
import streamlit as st
import pandas as pd
import yaml

import dashboard
from da_agent.core import apply_rules
from da_agent.db_connector import load_from_postgres, load_from_mysql

st.set_page_config(page_title="Trudata: Autonomous DQ Agent", layout="wide")

page = st.sidebar.selectbox("📂 Select Page", ["Dashboard", "Data Quality Agent"])

if page == "Dashboard":
    dashboard.run(st.session_state.get("metrics"))
else:
    st.image("Assets/trudata_logo.png", width=200)
    st.markdown("## Trudata: Autonomous Data Quality Agent")

    tab1, tab2 = st.tabs(["🧪 Rule Builder", "✅ Run Validator"])

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

    with tab2:
        st.markdown("### Coming soon: Run Validator for other sources")
