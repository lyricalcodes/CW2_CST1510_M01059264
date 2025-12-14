import streamlit as st
import pandas as pd
import plotly.express as px
from app.data.db import connect_database
from app.data.incidents import (get_all_incidents, insert_incident, update_incident_status, delete_incident)

st.set_page_config(page_title="Cyber Incidents Dashboard", page_icon="📊", layout="wide")

#if logged in show dashboard content
if not st.session_state.get("logged_in", False):
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page."):
        st.switch_page("Home.py")
    st.stop()
    
#connecting to week8 database
conn = connect_database()

#page title
st.title("📊 Cyber Incidents Dashboard")

#read: display incidents as a table
incidents = get_all_incidents(conn)

st.subheader("All Incidents")
if not incidents.empty:
    st.dataframe(incidents, use_container_width=True)
else:
    st.info("No incidents found.")

#create: insert new incident with a form
st.subheader("Add New Incident")
with st.form("add_incident_form"):
    severity = st.selectbox("Severity",["Low", "Medium", "High", "Critical"])
    category = st.selectbox("Category",["DDoS", "Malware", "Phishing", "Misconfiguration", "Unauthorized Access"])
    status = st.selectbox("Status",["Open", "In Progress", "Resolved"])
    description = st.text_area("Description")
    #form submit button
    submitted = st.form_submit_button("Add Incident")

#when form is submitted
if submitted:
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #call week8 function to insert into database
    insert_incident(conn, timestamp, severity, category, status, description)
    st.success("Incident added successfully!")
    st.rerun()

#updating incidents
st.subheader("Update Incident")
if not incidents.empty:
    selected_id = st.selectbox("Select incident to update", incidents['incident_id'])
    incident = incidents[incidents['incident_id'] == selected_id].iloc[0]

    with st.form("update_incident_form"):
        new_status = st.selectbox(
            "Status",
            ["Open", "In Progress", "Resolved"],
            index=["Open", "In Progress", "Resolved"].index(incident['status'])
        )
        if st.form_submit_button("Update Incident"):
            update_incident_status(conn, selected_id, new_status)
            st.success("Incident updated!")
            st.rerun()

#deleting incident
st.subheader("Delete Incident")
if not incidents.empty:
    selected_id = st.selectbox("Select incident to delete", incidents['incident_id'], key="delete_id")
    incident = incidents[incidents['incident_id'] == selected_id].iloc[0]
    
    #confirming deletion
    col1, col2 = st.columns([3, 1])
    with col1:
        st.warning("Are you sure you want to delete incident?")
    with col2:
        if st.button("Delete Incident", key="confirm_delete"):
            delete_incident(conn, selected_id)
            st.success("Incident deleted!")
            st.rerun()

st.subheader("Security Metrics")
if not incidents.empty:
    total_incidents = len(incidents)
    high_severity = incidents['severity'].value_counts().get("High", 0)
    st.metric("Total Incidents", total_incidents)
    st.metric("High Severity Incidents", high_severity)

st.subheader("Visual Analytics")

if not incidents.empty:
    #ensuring that created_at is datetime
    incidents['timestamp'] = pd.to_datetime(incidents['timestamp'], format='ISO8601')
    #bar chart to count incidents by type
    threat_counts = incidents.groupby("category").size().reset_index(name="Count")
    fig_bar = px.bar(
        threat_counts,
        x="category",
        y="Count",
        title="Incident Type Distribution",
        color="Count",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    #pie chart showing severity distribution
    severity_counts = incidents.groupby("severity").size().reset_index(name="Count")
    fig_pie = px.pie(
        severity_counts,
        names="severity",
        values="Count",
        title="Incident Severity Distribution",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    #time series chart to show incidents over times
    time_series = incidents.groupby(incidents['timestamp'].dt.date).size().reset_index(name='Count')
    fig_time = px.line(
        time_series,
        x='timestamp',
        y='Count',
        title='Incidents Over Time',
        markers=True
    )
    st.plotly_chart(fig_time, use_container_width=True)

    # High-Level Insights
st.subheader("High-Level Insights")
if not incidents.empty:
    #incident category with longest average resolution time
    if 'resolution_time_hours' in incidents.columns:
        avg_resolution = incidents.groupby('category')['resolution_time_hours'].mean().reset_index()
        slowest_category = avg_resolution.sort_values('resolution_time_hours', ascending=False).iloc[0]
        st.markdown(f"**Threat Category with Longest Avg Resolution Time:** {slowest_category['category']} ({slowest_category['resolution_time_hours']:.2f} hrs)")

    #spike detection for phishing incidents
    phishing_incidents = incidents[incidents['category'] == "Phishing"]
    if not phishing_incidents.empty:
        recent_count = phishing_incidents[phishing_incidents['timestamp'] > (pd.Timestamp.now() - pd.Timedelta(days=7))].shape[0]
        avg_count = phishing_incidents.shape[0] / max(1, ((pd.Timestamp.now() - phishing_incidents['timestamp'].min()).days))
        if recent_count > 1.5 * avg_count:
            st.warning(f"⚠️ Spike detected: {recent_count} Phishing incidents in the past week (avg: {avg_count:.1f}/week)")
        else:
            st.success("No recent Phishing spike detected.")

    #analyst/team causing bottlenecks
    if 'assigned_to' in incidents.columns:
        open_incidents = incidents[incidents['status'] != "Resolved"]
        if not open_incidents.empty:
            open_by_analyst = open_incidents.groupby('assigned_to').size().reset_index(name="Open Incidents")
            top_blocker = open_by_analyst.sort_values('Open Incidents', ascending=False).iloc[0]
            st.markdown(f"**Analyst/Team with most unresolved incidents:** {top_blocker['assigned_to']} ({top_blocker['Open Incidents']} incidents)")

