import pandas as pd
import requests
from io import StringIO
import streamlit as st
import plotly.express as px

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

# Inject custom CSS to style the buttons
st.markdown("""
    <style>
    .stButton button {
        font-size: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for each project's table visibility
for project in qtd_jira['Projeto']:
    if f'show_{project}' not in st.session_state:
        st.session_state[f'show_{project}'] = False

# Function to toggle table visibility
def toggle_table(project):
    st.session_state[f'show_{project}'] = not st.session_state[f'show_{project}']

# Create columns for buttons
columns = st.columns(len(qtd_jira['Projeto']))

# Create buttons for each project and place them in columns
for i, project in enumerate(qtd_jira['Projeto']):
    with columns[i]:
        if st.button(f'Tabela {project}', key=f'button_{project}', on_click=toggle_table, args=(project,)):
            pass

    # Display the table based on the visibility state
    if st.session_state[f'show_{project}']:
        st.table(jira[jira["Chave do projeto"] == project][["Chave do item","Prioridade","Solicitante","Criado"]].head(20))
