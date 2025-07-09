import streamlit as st
import pandas as pd
import yaml
import dashboard
from dq_agent.core import apply_rules
from dq_agent.db_connector import load_from_postgres, load_from_mysql

st.set_page_config(page_title="Trudata: Autonomous DQ Agent", layout="wide")

# --- Trudata Logo ---
st.image("Assets/trudata_logo.png", width=200)
st.markdown("## Trudata: Autonomous Data Quality Agent")

page = st.sidebar.selectbox("📂 Select Page", ["Dashboard", "Data Quality Agent"])

if page == "Dashboard":
    dashboard.run()
else:
    # Your existing DQ workflow code stays here


# ------------------- Tab 1: Rule Builder -------------------
with tab1:
    st.markdown("### 📤 Upload CSV for Rule Builder")
    uploaded_file = st.file_uploader("Choose your data file", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("CSV uploaded successfully!")
        st.markdown("#### 🔍 Data Preview")
        st.dataframe(df.head())

        st.markdown("### 🛠️ Define Rules")
        columns = df.columns.tolist()
        rule_configs = []
        for col in columns:
            with st.expander(f"Rules for **{col}**"):
                rules = []
                if st.checkbox("Not null", key=f"{col}_null"):
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

        import yaml

yaml_obj = {"rules": rule_configs}
config = yaml_obj  # mimic loaded YAML structure

# Apply rules
issues = apply_rules(df, config)

# Calculate live metrics
total = len(df)
failed = len(issues)
quality_score = round((1 - failed / total) * 100, 2) if total > 0 else 0
active_policies = len(config["rules"])
compliance_score = "100%" if quality_score >= 95 else "85%"

# Save for dashboard
st.session_state["metrics"] = {
    "Data Assets": str(total),
    "Quality Score": f"{quality_score}%",
    "Active Policies": str(active_policies),
    "Compliance": compliance_score
}

st.warning(f"⚠️ {failed} rows failed validation")

        if rule_configs:
            yaml_obj = {"rules": rule_configs}
            yaml_str = yaml.dump(yaml_obj, sort_keys=False)
            st.markdown("### 🧾 Generated YAML")
            st.code(yaml_str, language="yaml")
            st.download_button("⬇️ Download Rules YAML", data=yaml_str, file_name="rules.yaml")


# ------------------- Tab 2: Run Validator -------------------
with tab2:
    st.markdown("### 🧪 Run Data Validator")
    st.markdown("### 🔌 Data Source")
    source_type = st.selectbox("Choose data source", ["Upload CSV", "PostgreSQL", "MySQL"])

    df = None

    if source_type == "Upload CSV":
        csv = st.file_uploader("Upload CSV to validate", type="csv", key="dq_csv")
        if csv:
            df = pd.read_csv(csv)

    elif source_type == "PostgreSQL":
        st.markdown("#### 🔐 PostgreSQL Connection")
        col1, col2 = st.columns(2)
        pg_host = col1.text_input("Host")
        pg_db = col2.text_input("Database")
        pg_user = col1.text_input("User")
        pg_pass = col2.text_input("Password", type="password")
        pg_table = st.text_input("Table name")

        if st.button("🔄 Load from PostgreSQL"):
            try:
                df = load_from_postgres(pg_host, pg_db, pg_user, pg_pass, pg_table)
                st.success("Data loaded successfully!")
                st.dataframe(df.head())
            except Exception as e:
                st.error(f"Failed to connect: {e}")

    elif source_type == "MySQL":
        st.markdown("#### 🔐 MySQL Connection")
        col1, col2 = st.columns(2)
        my_host = col1.text_input("Host")
        my_db = col2.text_input("Database")
        my_user = col1.text_input("User")
        my_pass = col2.text_input("Password", type="password")
        my_table = st.text_input("Table name")

        if st.button("🔄 Load from MySQL"):
            try:
                df = load_from_mysql(my_host, my_db, my_user, my_pass, my_table)
                st.success("Data loaded successfully!")
                st.dataframe(df.head())
            except Exception as e:
                st.error(f"Failed to connect: {e}")

    # --- YAML Config Upload ---
    yml = st.file_uploader("Upload YAML config", type=["yaml", "yml"])
    if df is not None and yml:
        config = yaml.safe_load(yml)
        st.markdown("#### 🔍 Data Preview")
        st.dataframe(df.head())
        issues = apply_rules(df, config)
        if issues:
            for issue in issues:
                st.warning(f"⚠️ {issue['rule']}: {len(issue['rows'])} rows affected")
        else:
            st.success("✅ No issues found!")

    # --- AI Rule Suggestion from any loaded df (CSV or DB) ---
    if df is not None:
        st.markdown("---")
        st.markdown("### 🤖 AI-Powered Rule Suggestions")
        if st.button("Suggest Rules (AI)", key="ai_suggest"):
            with st.spinner("Analyzing with AI..."):
                from dq_agent.suggest_rules import suggest_rules
                rules_yaml = suggest_rules(df)
                yaml_str = yaml.dump(rules_yaml, sort_keys=False)
                st.markdown("#### 🧾 Suggested Rules")
                st.code(yaml_str, language="yaml")
                st.download_button("⬇️ Download Suggested YAML", data=yaml_str, file_name="suggested_rules.yaml")


# --- Footer ---
st.markdown("---")
st.markdown(
    "<center><small>🚀 Built with ❤️ by Trudata | Contact: hello@trudata.ai</small></center>",
    unsafe_allow_html=True,
)
