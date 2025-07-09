
import streamlit as st

def run(metrics_data=None):
    st.markdown("""
        <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
        }
        .metric {
            font-size: 20px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("## TruData Dashboard")

    # Metrics
    default_metrics = {
        "Data Assets": "2,847",
        "Quality Score": "98.2%",
        "Active Policies": "156",
        "Compliance": "99.9%"
    }
    metric_data = metrics_data or default_metrics
    cols = st.columns(4)
    for i, (label, value) in enumerate(metric_data.items()):
        cols[i].metric(label, value)

    st.markdown("---")

    # Dashboard modules with button actions
    st.subheader("Dashboard Modules")
    mod_cols = st.columns(3)

    with mod_cols[0]:
        st.markdown("#### Data Governance")
        st.markdown("Manage data policies, stewardship, and governance workflows across your organization.")
        if st.button("Configure Governance"):
            st.info("Governance configuration will appear here.")

    with mod_cols[1]:
        st.markdown("#### Data Quality")
        st.markdown("Monitor data quality metrics, set up validation rules, and track data health across sources.")
        if st.button("Monitor Quality"):
            st.session_state["go_to_quality"] = True
            st.success("Switch to the 'Data Quality Agent' tab to manage quality.")

    with mod_cols[2]:
        st.markdown("#### Compliance")
        st.markdown("Ensure regulatory compliance with automated checks and audit trails.")
        if st.button("Review Compliance"):
            st.info("Compliance checks are up to date. No new issues found.")

    st.markdown("---")

    # Data Catalog Workflow
    st.subheader("Data Catalog Workflow")
    step = st.radio("Select a step", ["Discovery", "Classification", "Validation", "Publication"], horizontal=True)
    st.write(f"You are viewing: **{step}** step of the workflow.")
    st.button("Run Workflow", on_click=lambda: st.success("✅ Workflow executed successfully."))
    st.button("Schedule Workflow", on_click=lambda: st.info("🕒 Scheduler launched."))

    st.markdown("---")

    # New: Data Source Configuration
    with st.expander("🔌 Connect a Data Source"):
        st.markdown("Select a data source type and provide credentials.")

        db_type = st.selectbox("Data Source", ["PostgreSQL", "MySQL", "BigQuery (coming soon)", "Snowflake (coming soon)"])

        if db_type in ["PostgreSQL", "MySQL"]:
            col1, col2 = st.columns(2)
            host = col1.text_input("Host", "localhost")
            db = col2.text_input("Database", "my_db")
            user = col1.text_input("User", "user")
            password = col2.text_input("Password", type="password")
            table = st.text_input("Table name", "table_name")

            if st.button(f"Connect to {db_type}"):
                st.success(f"✅ Connected to {db_type} and fetched data from `{table}` (placeholder)")

    st.markdown("---")

    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<center style='color:gray;'>© 2025 TruData</center>", unsafe_allow_html=True)
