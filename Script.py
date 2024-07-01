import pandas as pd
import requests
from io import StringIO
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px

url1 = 'https://raw.githubusercontent.com/Eduardo-Cordeiro/Team_Dashboard/main/Jira_Data.csv'
response1 = requests.get(url1)
response1.raise_for_status()  
csv_content1 = response1.text
jira = pd.read_csv(StringIO(csv_content1), delimiter=',')

jira = pd.read_csv('Jira_Data.csv')

st.title("Jira")

# Plotting the bar chart
qtd_jira = pd.DataFrame()
qtd_jira['Projeto'] = jira['Chave do projeto'].value_counts().index 
qtd_jira['Quantidade'] = jira['Chave do projeto'].value_counts().values

fig = px.bar(qtd_jira, x='Projeto', y='Quantidade', title='Distribuição dos Projetos')

# Display the bar chart
st.plotly_chart(fig)


