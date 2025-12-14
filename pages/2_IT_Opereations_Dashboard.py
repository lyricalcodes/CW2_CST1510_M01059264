import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from app.data.db import connect_database
from app.data.tickets import (get_all_tickets, insert_ticket, update_ticket_status, delete_ticket)

st.set_page_config(page_title="IT Operations Dashboard", page_icon="💻", layout="wide")

#if logged in show dashboard content
if not st.session_state.get("logged_in", False):
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()

conn = connect_database()

st.title("💻 IT Operations Dashboard")

#display all tickets
tickets = get_all_tickets(conn)
st.subheader("All Tickets")
if not tickets.empty:
    st.dataframe(tickets, use_container_width=True)
else:
    st.info("No tickets found.")

#add new ticket
st.subheader("Add New Ticket")
with st.form("add_ticket_form"):
    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    description = st.text_area("Description")
    status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
    assigned_to = st.text_input("Assigned To")
    resolution_time = st.number_input("Resolution Time (hours)", min_value=0, step=1)
    submitted = st.form_submit_button("Add Ticket")

if submitted:
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insert_ticket(conn, priority, description, status, assigned_to, created_at, resolution_time)
    st.success("Ticket added successfully!")
    st.rerun()

#update ticket
st.subheader("Update Ticket Status")
if not tickets.empty:
    selected_id = st.selectbox("Select ticket to update", tickets['ticket_id'])
    ticket = tickets[tickets['ticket_id'] == selected_id].iloc[0]

    with st.form("update_ticket_form"):
        new_status = st.selectbox(
            "Status",
            ["Open", "In Progress", "Resolved"],
            index=["Open", "In Progress", "Resolved"].index(ticket['status'])
        )
        if st.form_submit_button("Update Status"):
            update_ticket_status(conn, selected_id, new_status)
            st.success("Ticket status updated!")
            st.rerun()

#delete ticket
st.subheader("Delete Ticket")
if not tickets.empty:
    delete_id = st.selectbox("Select ticket to delete", tickets['ticket_id'], key="delete_ticket_id")
    ticket = tickets[tickets['ticket_id'] == delete_id].iloc[0]

    col1, col2 = st.columns([3, 1])
    with col1:
        st.warning("Are you sure you want to delete this ticket?")
    with col2:
        if st.button("Delete Ticket", key="confirm_delete_ticket"):
            delete_ticket(conn, delete_id)
            st.success("Ticket deleted!")
            st.rerun()

#metrics
st.subheader("Ticket Metrics")
if not tickets.empty:
    total_tickets = len(tickets)
    open_tickets = tickets['status'].value_counts().get("Open", 0)
    high_priority = tickets['priority'].value_counts().get("High", 0) + tickets['priority'].value_counts().get("Critical", 0)
    st.metric("Total Tickets", total_tickets)
    st.metric("Open Tickets", open_tickets)
    st.metric("High Priority Tickets", high_priority)

#visual Analytics
st.subheader("Visual Analytics")
if not tickets.empty:
    #bar chart showing tickets per priority
    priority_counts = tickets.groupby("priority").size().reset_index(name="Count")
    fig_priority = px.bar(
        priority_counts,
        x="priority",
        y="Count",
        title="Tickets by Priority",
        color="Count",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_priority, use_container_width=True)

    #pie chart tickets by status
    status_counts = tickets.groupby("status").size().reset_index(name="Count")
    fig_status = px.pie(
        status_counts,
        names="status",
        values="Count",
        title="Tickets by Status",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig_status, use_container_width=True)

    #scatter comparing resolution time and priority to detect anomalies
    fig_scatter = px.scatter(
        tickets,
        x='priority',
        y='resolution_time_hours',
        size='resolution_time_hours',
        hover_data=['description', 'assigned_to'],
        title="Resolution Time by Priority"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

#IT Operations Insights
st.subheader("Operational Insights")
if not tickets.empty:
    #tickets taking long to resolve
    long_tickets = tickets[tickets['resolution_time_hours'] > 48]
    if not long_tickets.empty:
        st.warning(f"{len(long_tickets)} tickets have resolution time > 48 hours. Consider reviewing these.")
        st.dataframe(long_tickets[['ticket_id', 'priority', 'status', 'assigned_to', 'resolution_time_hours']], use_container_width=True)
    else:
        st.success("All tickets are being resolved in reasonable time.")

    #staff with most open tickets
    open_by_staff = tickets[tickets['status'] == "Open"].groupby("assigned_to").size().reset_index(name="Open Tickets")
    open_by_staff = open_by_staff.sort_values("Open Tickets", ascending=False)
    if not open_by_staff.empty:
        st.markdown("**Staff with most open tickets:**")
        st.dataframe(open_by_staff, use_container_width=True)
