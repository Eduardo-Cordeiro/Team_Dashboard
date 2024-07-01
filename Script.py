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

# Display the initial bar chart
st.plotly_chart(fig)

# Create buttons for each project
for project in qtd_jira['Projeto']:
    if st.button(f'Show details for {project}'):
        # Function to create a new bar chart based on selected project
        st.table(jira[jira["Chave do projeto"] == project])

        # Display the detailed chart for the selected project
       
