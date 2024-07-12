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
jira["Criado"] = pd.to_datetime(jira["Criado"])


st.title("Jira Dashboard")

# Construindo Widgets iniciais
min_date = jira["Criado"].min().date()
max_date = jira["Criado"].max().date()

col1, col2, col3, col4 = st.columns([1,1,1,1])
col1, col2 = st.columns([1,1])
with col1:
    proj_selected = st.multiselect('Projeto', ["PLAT",'ROUT','SITE',"NET",'BASE','CONN','DATA','PHON'],default=["PLAT",'ROUT','SITE',"NET",'BASE','CONN','DATA','PHON'])
    start = st.date_input('Data Inicial',min_value=min_date, max_value=max_date, value=min_date)
with col2:
    satis = st.multiselect('Prioridade', ['Lowest','Low','Medium','High','Highest'],default=['Lowest','Low','Medium','High','Highest'])
    end = st.date_input('Data Final',min_value=min_date, max_value=max_date, value=max_date)
jira["Index"] = jira["Unnamed: 0"].astype(str)
jira = jira.drop(columns=['Unnamed: 0'])
jira["ID do item"] = jira["ID do item"].astype(str)
jira["Campo personalizado (Client ID)"] = jira["Campo personalizado (Client ID)"].astype(str)
jira = jira[(jira["Chave do projeto"].isin(proj_selected)) & (jira["Prioridade"].isin(satis)) & (jira["Criado"] > pd.Timestamp(start)) & (jira["Criado"] < pd.Timestamp(end)) ]

# Create the initial bar chart
qtd_jira = pd.DataFrame()
qtd_jira['Projeto'] = jira['Chave do projeto'].value_counts().index
qtd_jira['Quantidade'] = jira['Chave do projeto'].value_counts().values

fig = px.bar(qtd_jira, x='Projeto', y='Quantidade')
fig.update_traces(marker_color='lightskyblue', selector=dict(type='bar'))

st.markdown("### Quantidade de chamados por Projeto")
st.plotly_chart(fig)

st.markdown("### Dataframes por Projeto")
st.markdown("Selecione o Projeto e visualize as pricipais informações sobre as issues.")
st.dataframe(jira,hide_index=True)
category = pd.DataFrame()
category["Categoria"] = jira["Campo personalizado (Categoria)"].value_counts().index
category["Quantidade"] = jira["Campo personalizado (Categoria)"].value_counts().values
fig2 = px.bar(category.head(15), x='Categoria', y='Quantidade')

fig2.update_traces(marker_color='lightskyblue', selector=dict(type='bar'))
st.markdown("### Categorias por Projeto")
st.markdown("Selecione o Projeto e visualize as pricipais categorias das issues.")
st.plotly_chart(fig2)
