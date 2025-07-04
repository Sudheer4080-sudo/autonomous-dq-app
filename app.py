
import streamlit as st
import pandas as pd
import yaml
from dq_agent.core import apply_rules

st.image("Assets/trudata_logo.png", width=200)
st.markdown("<h1 style='color:#007ACC;'>Trudata: Autonomous Data Quality Agent</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs([" Rule Builder", " Run Validator"])

with tab1:
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        columns = df.columns.tolist()
        rule_configs = []
        for col in columns:
            with st.expander(f"Rules for {col}"):
                rules = []
                if st.checkbox("Not null", key=f"{col}_null"):
                    rules.append("not_null")
                if st.checkbox("Unique", key=f"{col}_uniq"):
                    rules.append("unique")
                if st.checkbox("Range", key=f"{col}_range"):
                    min_val = st.number_input("Min", key=f"{col}_min")
                    max_val = st.number_input("Max", key=f"{col}_max")
                    rules.append({"range": {"min": min_val, "max": max_val}})
                if st.checkbox("Regex", key=f"{col}_regex"):
                    pattern = st.text_input("Regex pattern", key=f"{col}_pattern")
                    rules.append({"pattern": pattern})
                if rules:
                    rule_configs.append({"column": col, "rules": rules})
        if rule_configs:
            yaml_obj = {"rules": rule_configs}
            yaml_str = yaml.dump(yaml_obj, sort_keys=False)
            st.code(yaml_str, language="yaml")
            st.download_button("Download YAML", data=yaml_str, file_name="rules.yaml")

with tab2:
    csv = st.file_uploader("Upload CSV", type="csv", key="dq_csv")
    yml = st.file_uploader("Upload YAML", type="yaml")
    if csv and yml:
        df = pd.read_csv(csv)
        config = yaml.safe_load(yml)
        issues = apply_rules(df, config)
        if issues:
            for issue in issues:
                st.warning(f"{issue['rule']}: {len(issue['rows'])} rows")
        else:
            st.success(" No issues found!")

    st.markdown("AI-Powered Rule Suggestions")
    
    ai_csv = st.file_uploader("Upload CSV for AI suggestion", type="csv", key="ai_csv")
    if ai_csv:
        df_ai = pd.read_csv(ai_csv)
        if st.button("Suggest Rules (AI)"):
            with st.spinner("Analyzing..."):
                from dq_agent.suggest_rules import suggest_rules
                rules_yaml = suggest_rules(df_ai)
                yaml_str = yaml.dump(rules_yaml, sort_keys=False)
                st.code(yaml_str, language="yaml")
                st.download_button("Download Suggested YAML", data=yaml_str, file_name="suggested_rules.yaml")

    st.markdown("---")
    st.markdown("<center><small>Powered by <strong>Trudata</strong> • An AutonomousDQ Innovation</small></center>", unsafe_allow_html=True)

           
