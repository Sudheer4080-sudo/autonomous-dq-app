
import streamlit as st

def run(metrics_data=None):
    st.set_page_config(page_title="TruData Dashboard", layout="wide")

    # TruData Logo and Header
    st.markdown("""
    <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 20px;'>
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    width: 40px; height: 40px; border-radius: 8px; 
                    display: flex; align-items: center; justify-content: center; 
                    font-weight: bold; color: white;'>TD</div>
        <h1 style='margin: 0;'>TruData Dashboard</h1>
    </div>
    """, unsafe_allow_html=True)

    # Metrics Overview
    st.subheader("📊 Data Governance Overview")

    default_metrics = {
        "Data Assets": "2,847",
        "Quality Score": "98.2%",
        "Active Policies": "156",
        "Compliance": "99.9%"
    }

    metric_data = metrics_data or default_metrics
    metric_cols = st.columns(4)

    for col, (label, value) in zip(metric_cols, metric_data.items()):
        col.metric(label, value)

    st.markdown("---")

    # Dashboard Cards
    st.subheader("🗂️ Dashboard Modules")
    card_cols = st.columns(3)

    with card_cols[0]:
        st.markdown("#### 🏛️ Data Governance")
        st.markdown("Manage data policies, stewardship, and governance workflows across your organization.")
        st.button("Configure Governance")

    with card_cols[1]:
        st.markdown("#### ✨ Data Quality")
        st.markdown("Monitor data quality metrics, set up validation rules, and track data health across sources.")
        st.button("Monitor Quality")

    with card_cols[2]:
        st.markdown("#### 📋 Compliance")
        st.markdown("Ensure regulatory compliance with automated checks and audit trails.")
        st.button("Review Compliance")

    st.markdown("---")

    # Data Catalog Workflow
    st.subheader("🔄 Data Catalog Workflow")
    workflow_steps = ["Discovery", "Classification", "Validation", "Publication"]
    selected_step = st.radio("Select a step", workflow_steps, horizontal=True)

    if selected_step:
        st.info(f"### 🛠️ Step: {selected_step}\nUse this step to configure your data catalog workflow.")

    st.markdown("#### Actions")
    col1, col2 = st.columns(2)
    with col1:
        st.button("🚀 Run Workflow")
    with col2:
        st.button("⏰ Schedule Workflow")

    st.markdown("---")

    # Data Integrations
    st.subheader("🔌 Integrations")

    left, right = st.columns(2)

    with left:
        st.markdown("#### Data Sources")
        st.success("✅ Snowflake (Active)")
        st.success("✅ Databricks (Active)")
        st.warning("⏳ BigQuery (Pending)")
        st.error("❌ Redshift (Inactive)")

    with right:
        st.markdown("#### Output Tools")
        st.success("✅ Tableau (Active)")
        st.success("✅ Power BI (Active)")
        st.success("✅ Looker (Active)")
        st.warning("⏳ Jupyter (Pending)")

    st.markdown("---")

    # Bottom Navigation Cards
    st.subheader("🧭 Navigation")

    nav_cols = st.columns(3)
    with nav_cols[0]:
        st.markdown("#### 🔗 Data Lineage")
        st.caption("Track data flow across systems")

    with nav_cols[1]:
        st.markdown("#### 🔒 Security")
        st.caption("Manage access controls")

    with nav_cols[2]:
        st.markdown("#### 📊 Reports")
        st.caption("View analytics and insights")
