import pandas as pd
import requests
from io import StringIO
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Load data from URL
url1 = 'https://raw.githubusercontent.com/Eduardo-Cordeiro/Team_Dashboard/main/Jira_Data.csv'
response1 = requests.get(url1)
response1.raise_for_status()
csv_content1 = response1.text
jira = pd.read_csv(StringIO(csv_content1), delimiter=',')

st.title("Jira Dashboard")

# Create the initial bar chart
qtd_jira = pd.DataFrame()
qtd_jira['Projeto'] = jira['Chave do projeto'].value_counts().index
qtd_jira['Quantidade'] = jira['Chave do projeto'].value_counts().values

fig = px.bar(qtd_jira, x='Projeto', y='Quantidade', title='Distribuição dos Projetos')
fig.update_traces(marker_color='lightskyblue', selector=dict(type='bar'))

# Function to create a new bar chart based on selected project
def create_detailed_bar_chart(selected_project):
    filtered_data = jira[jira['Chave do projeto'] == selected_project]
    issue_counts = filtered_data['Tipo de issue'].value_counts()
    detailed_fig = px.bar(issue_counts, x=issue_counts.index, y=issue_counts.values, title=f'Detalhes do Projeto: {selected_project}')
    detailed_fig.update_traces(marker_color='lightcoral', selector=dict(type='bar'))
    return detailed_fig

# Function to handle click event and update the chart
def on_bar_click(trace, points, state):
    selected_project = points.point_inds[0]
    detailed_fig = create_detailed_bar_chart(qtd_jira['Projeto'][selected_project])
    st.plotly_chart(detailed_fig)

# Attach click event handler
fig.data[0].on_click(on_bar_click)

# Display the initial bar chart
st.plotly_chart(fig)
