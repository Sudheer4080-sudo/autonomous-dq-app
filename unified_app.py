
import streamlit as st
import pandas as pd
import yaml

from dq_agent.core.rules_engine import apply_rules
from dq_agent.db_connector_ui import database_connector_ui
import dashboard

st.set_page_config(page_title="Trudata – Autonomous Data Quality Agent", layout="wide")

# ----------------- Branding Header -----------------
with st.container():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image("Assets/trudata_logo.png", width=160)
        st.markdown("### Autonomous Data Quality Agent")
        st.caption("Minimal. Intelligent. Enterprise-ready.")

# ----------------- Data Source Selector -----------------
st.markdown("## 📥 Select Your Data Source")

source_type = st.selectbox("Choose Input Type", ["Upload CSV", "Connect to Database"], index=0)

df = None
if source_type == "Upload CSV":
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("✅ CSV loaded successfully!")
else:
    st.info("Enter connection details to preview a database table:")
    database_connector_ui()
    df = st.session_state.get("dataframe")

# ----------------- Data Preview & Rule Builder -----------------
if df is not None:
    st.markdown("### 👁️ Data Preview")
    st.dataframe(df.head(), use_container_width=True)
    st.divider()

    st.markdown("### 🧠 Rule Builder")
    columns = df.columns.tolist()
    rule_configs = []

    for col in columns:
        with st.expander(f"Rules for **{col}**", expanded=False):
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
        st.divider()
        st.markdown("### ✅ Apply Rules")
        if st.button("🚀 Run Validation"):
            config = {"rules": rule_configs}
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

            st.success("✅ Validation complete.")
            st.toast(f"⚙️ {failed} rows failed validation", icon="⚠️")

            with st.container():
                st.markdown("### 📊 Results Summary")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("📦 Data Assets", total)
                col2.metric("🎯 Quality Score", f"{quality_score}%")
                col3.metric("🔒 Compliance", compliance_score)
                col4.metric("📋 Policies", active_policies)

# ----------------- Footer -----------------
st.markdown("---")
st.caption("⚙️ Trudata · Built with AI · 2025")
