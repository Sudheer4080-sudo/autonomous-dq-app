
import streamlit as st
import pandas as pd
from dq_agent.db_connector import load_from_postgres, load_from_mysql

def run(metrics_data=None, rule_issues=None):
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
        }
        .metric {
            font-size: 20px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("## TruData Dashboard")

    # Metrics section
    default_metrics = {
        "Data Assets": "2,847",
        "Quality Score": "98.2%",
        "Active Policies": "156",
        "Compliance": "99.9%"
    }
    metrics = metrics_data or default_metrics
    cols = st.columns(4)
    for col, (label, value) in zip(cols, metrics.items()):
        col.metric(label, value)

    st.markdown("---")

    # Dashboard Modules
    st.subheader("Dashboard Modules")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Data Governance")
        st.markdown("Manage policies and stewards.")
        if st.button("Configure Governance"):
            st.session_state["show_config"] = True
            st.info("Governance configuration UI coming soon.")

    with col2:
        st.markdown("#### Data Quality")
        st.markdown("Monitor data health and rules.")
        if st.button("Monitor Quality"):
            st.session_state["go_to_quality"] = True
            st.success("Switching to Data Quality Agent...")

    with col3:
        st.markdown("#### Compliance")
        st.markdown("Track and review compliance.")
        if st.button("Review Compliance"):
            st.session_state["show_compliance"] = True
            st.info("Compliance summary loaded.")

    st.markdown("---")

    # Catalog Workflow
    st.subheader("Data Catalog Workflow")
    step = st.radio("Step", ["Discovery", "Classification", "Validation", "Publication"], horizontal=True)
    st.write(f"**Current Step**: {step}")

    wf_col1, wf_col2 = st.columns(2)
    with wf_col1:
        st.button("▶️ Run Workflow", on_click=lambda: st.success("Workflow executed"))
    with wf_col2:
        st.button("📅 Schedule Workflow", on_click=lambda: st.info("Scheduler opened"))

    st.markdown("---")

    # Data Source Configuration
    with st.expander("🔌 Connect a Data Source"):
        st.markdown("Configure your connection below.")
        db_type = st.selectbox("Data Source", ["PostgreSQL", "MySQL"])
        c1, c2 = st.columns(2)
        host = c1.text_input("Host", "localhost")
        database = c2.text_input("Database", "mydb")
        user = c1.text_input("User", "admin")
        password = c2.text_input("Password", type="password")
        table = st.text_input("Table name", "your_table")

        if st.button(f"Connect to {db_type}"):
            try:
                if db_type == "PostgreSQL":
                    df = load_from_postgres(host, database, user, password, table)
                else:
                    df = load_from_mysql(host, database, user, password, table)
                st.success(f"Connected to {db_type} ✅")
                st.dataframe(df.head())
            except Exception as e:
                st.error(f"Connection failed: {e}")

    st.markdown("---")

    # Bar chart for rule validation failures
    if rule_issues and isinstance(rule_issues, list) and len(rule_issues) > 0:
        st.subheader("🔍 Rule Validation Failures")
        df_issues = pd.DataFrame(rule_issues)
        if "rule" in df_issues.columns:
            chart_data = df_issues["rule"].value_counts().reset_index()
            chart_data.columns = ["Rule", "Failures"]
            st.bar_chart(chart_data.set_index("Rule"))

    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<center style='color:gray;'>© 2025 TruData</center>", unsafe_allow_html=True)
