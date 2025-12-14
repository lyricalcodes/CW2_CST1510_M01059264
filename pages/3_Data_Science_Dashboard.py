import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from app.data.db import connect_database
from app.data.datasets import (get_all_datasets, insert_dataset, update_dataset, delete_dataset)

st.set_page_config(page_title="Data Science Dashboard", page_icon="📊", layout="wide")

#if logged in show dashboard content
if not st.session_state.get("logged_in", False):
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()

#connecting to week8 database
conn = connect_database()

st.title("📊 Data Science Dashboard")

#read: display datasets as a table
datasets = get_all_datasets(conn)
st.subheader("All Datasets")
if not datasets.empty:
    st.dataframe(datasets, use_container_width=True)
else:
    st.info("No datasets found.")

#creating new dataset
st.subheader("Add New Dataset")
with st.form("add_dataset_form"):
    name = st.text_input("Dataset Name")
    rows = st.number_input("Number of Rows", min_value=0, step=1)
    columns_count = st.number_input("Number of Columns", min_value=0, step=1)
    uploaded_by = st.text_input("Uploaded By")
    upload_date = st.date_input("Upload Date")
    submitted = st.form_submit_button("Add Dataset")

if submitted:
    insert_dataset(conn, name, rows, columns_count, uploaded_by, upload_date.strftime("%Y-%m-%d"))
    st.success("Dataset added successfully!")
    st.rerun()

# Update dataset
st.subheader("Update Dataset")
if not datasets.empty:
    selected_id = st.selectbox("Select dataset to update", datasets['dataset_id'])
    dataset = datasets[datasets['dataset_id'] == selected_id].iloc[0]

    with st.form("update_dataset_form"):
        new_name = st.text_input("Dataset Name", value=dataset['name'])
        new_rows = st.number_input("Number of Rows", value=dataset['rows'], step=1)
        new_columns = st.number_input("Number of Columns", value=dataset['columns'], step=1)
        new_uploaded_by = st.text_input("Uploaded By", value=dataset['uploaded_by'])
        if st.form_submit_button("Update Dataset"):
            update_dataset(
                conn,
                selected_id,
                name=new_name,
                rows=new_rows,
                columns=new_columns,
                uploaded_by=new_uploaded_by
            )
            st.success("Dataset updated!")
            st.rerun()

#delete dataset
st.subheader("Delete Dataset")
if not datasets.empty:
    delete_id = st.selectbox("Select dataset to delete", datasets['dataset_id'], key="delete_dataset_id")
    dataset = datasets[datasets['dataset_id'] == delete_id].iloc[0]

    col1, col2 = st.columns([3, 1])
    with col1:
        st.warning("Are you sure you want to delete this dataset?")
    with col2:
        if st.button("Delete Dataset", key="confirm_delete_dataset"):
            delete_dataset(conn, delete_id)
            st.success("Dataset deleted!")
            st.rerun()

#metrics
st.subheader("Dataset Metrics")
if not datasets.empty:
    total_datasets = len(datasets)
    total_rows = datasets['rows'].sum()
    st.metric("Total Datasets", total_datasets)
    st.metric("Total Rows Across All Datasets", total_rows)

#visual Analytics
st.subheader("Visual Analytics")
if not datasets.empty:
    #bar chart showing number of rows per dataset
    fig_rows = px.bar(
        datasets,
        x='name',
        y='rows',
        title="Number of Rows per Dataset",
        color='rows',
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_rows, use_container_width=True)

    #pie chart showing distribution of datasets by uploader
    uploader_counts = datasets.groupby("uploaded_by").size().reset_index(name="Count")
    fig_pie = px.pie(
        uploader_counts,
        names='uploaded_by',
        values='Count',
        title="Datasets per Uploader",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    #scatter chart comparing rows and columns 
    fig_scatter = px.scatter(
        datasets,
        x='columns',
        y='rows',
        size='rows',
        hover_data=['name', 'uploaded_by'],
        title="Rows vs Columns per Dataset"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

#data governance insights
st.subheader("Data Governance Insights")
if not datasets.empty:
    #identifying largest datasets
    largest_datasets = datasets.nlargest(5, 'rows')[['name', 'rows', 'columns']]
    st.markdown("**Top 5 Largest Datasets (by rows):**")
    st.dataframe(largest_datasets, use_container_width=True)

    #identifing datasets with fewest rows
    smallest_datasets = datasets.nsmallest(5, 'rows')[['name', 'rows', 'columns']]
    st.markdown("**Top 5 Smallest Datasets (possible archive candidates):**")
    st.dataframe(smallest_datasets, use_container_width=True)

    #counting datasets per uploader
    uploader_counts = datasets.groupby('uploaded_by').size().reset_index(name='Dataset Count')
    st.markdown("**Dataset Count by Uploader:**")
    st.dataframe(uploader_counts, use_container_width=True)



