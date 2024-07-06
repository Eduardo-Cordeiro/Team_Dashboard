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
jira["Chave do projeto"] = jira["Chave do projeto"].apply(lambda x: "PHON" if x == "PHONE" else x) 

# Create the initial bar chart
qtd_jira = pd.DataFrame()
qtd_jira['Projeto'] = jira['Chave do projeto'].value_counts().index
qtd_jira['Quantidade'] = jira['Chave do projeto'].value_counts().values
fig = px.bar(qtd_jira, x='Projeto', y='Quantidade')
fig.update_traces(marker_color='lightskyblue', selector=dict(type='bar'))

col1, col2, col3, col4 = st.columns([1,1,1,1])

with col1:
    st.multiselect('Projeto', [1,2,3])
with col2:
    st.multiselect('Satisfaçao', ['Good','Bad'])
with col3:
    st.date_input('Data Inicial')
with col4:
    st.date_input('Data Final')


# Initialize session state for each project's table visibility
for project in qtd_jira['Projeto']:
    if f'show_{project}' not in st.session_state:
        st.session_state[f'show_{project}'] = False
        st.session_state[f'show_{"PLAT"}'] = True

# Create a list of options for the dropdown
options = qtd_jira['Projeto']

# Main categories per project

# Create a list of options for the dropdown
options2 = qtd_jira["Projeto"]

st.title("Jira Dashboard")
st.markdown("### Quantidade de chamados por Projeto")
st.plotly_chart(fig)
st.markdown("### Dataframes por Projeto")
st.markdown("Selecione o Projeto e visualize as pricipais informações sobre as issues.")
selected_option = st.selectbox('Projetos:', options)
st.dataframe(jira[jira["Chave do projeto"] == selected_option][["Chave do item","Solicitante","Prioridade","Criado"]],hide_index=True,use_container_width=True)

selected_option2 = st.selectbox('Projetos', options2)
category = pd.DataFrame()
category["Categoria"] = jira[jira["Chave do projeto"] == selected_option2]["Campo personalizado (Categoria)"].value_counts().index
category["Quantidade"] = jira[jira["Chave do projeto"] == selected_option2]["Campo personalizado (Categoria)"].value_counts().values
fig2 = px.bar(category.head(15), x='Categoria', y='Quantidade')

fig2.update_traces(marker_color='lightskyblue', selector=dict(type='bar'))
st.markdown("### Categorias por Projeto")
st.markdown("Selecione o Projeto e visualize as pricipais categorias das issues.")
st.plotly_chart(fig2)
