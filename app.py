
import streamlit as st
import pandas as pd
import yaml
from dq_agent.core import apply_rules

st.set_page_config(page_title="Autonomous DQ", layout="wide")
st.title("Autonomous Data Quality App")

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
