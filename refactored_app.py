
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

# ----------------- Sidebar Navigation -----------------
page = st.sidebar.radio("📂 Navigate", ["Data Quality Studio", "Validation Dashboard"])

# ----------------- Data Quality Studio -----------------
if page == "Data Quality Studio":
    st.markdown("## 🧪 Data Quality Studio")
    source_type = st.selectbox("Select Data Source", ["Upload CSV", "Connect to Database"])

    df = None

    if source_type == "Upload CSV":
        uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.success("CSV loaded successfully!")
    else:
        st.info("Fill in credentials below to preview a table from your database:")
        database_connector_ui()
        df = st.session_state.get("dataframe")

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

                st.warning(f"⚠️ {failed} rows failed validation")
                st.success("Validation complete. Switch to the dashboard to explore results.")

# ----------------- Results Dashboard -----------------
else:
    st.markdown("## 📊 Validation Dashboard")
    dashboard.run(
        metrics_data=st.session_state.get("metrics"),
        rule_issues=st.session_state.get("rule_issues")
    )

# ----------------- Footer -----------------
st.markdown("---")
st.caption("⚙️ Trudata · Built with AI · 2025")
