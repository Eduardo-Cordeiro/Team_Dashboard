import pandas as pd
import requests
from io import StringIO
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

# Load data from URL
# %%
url1 = 'https://raw.githubusercontent.com/Eduardo-Cordeiro/Team_Dashboard/main/Zendesk_Data.csv'
response1 = requests.get(url1)
response1.raise_for_status()
csv_content1 = response1.text
zendesk = pd.read_csv(StringIO(csv_content1), delimiter=',')

zendesk["Creation Date"] = pd.to_datetime(zendesk["Creation Date"])
zendesk['Last Update Date'] = pd.to_datetime(zendesk['Last Update Date'])
zendesk["Unidade"] = 1
num1 = np.random.uniform(-0.2, 0.2)
num2 = np.random.uniform(-0.2, 0.2)        
num3 = -(num1 + num2)

team = []
size = len(zendesk["Agent"])
for i in range(0,size,1):
    if i < ((size/3) + (size/3)*num1):
        team.append('A')
    elif (i>((size/3) + (size/3)*num1)) and i < (2*(size/3) + 2*(size/3)*num2):
        team.append('B')
    else:
        team.append('C')

zendesk["Team"] = team

good = zendesk[zendesk["Satisfação"] == 'Good'].groupby("Team")['Unidade'].sum()
print(good)

bad = zendesk[zendesk["Satisfação"] == 'Bad'].groupby("Team")['Unidade'].sum()
print(bad)

times = zendesk.groupby('Team')["Agent"].value_counts()
members_per_team = [len(times.xs("A", level="Team")),len(times.xs("B", level="Team")),len(times.xs("C", level="Team"))]

zendesk_teams = pd.DataFrame()
zendesk_teams["Team"] = zendesk["Team"].value_counts().index
zendesk_teams["Quantidade"] = zendesk["Team"].value_counts().values
zendesk_teams["Membros"] = members_per_team
zendesk_teams["Tickets por agente"] = zendesk_teams["Quantidade"] / zendesk_teams["Membros"]
zendesk_teams["Bom"] = good.values
zendesk_teams["Ruim"] = bad.values
zendesk_teams["Unoffered"] = zendesk_teams["Quantidade"] - (zendesk_teams["Bom"] + zendesk_teams["Ruim"])

print(zendesk_teams.head(20))

st.title("Zendesk Dashboard")
days_to_subtract = timedelta(days=31)

col1, col2, col3, col4 = st.columns([1,1,1,1])

with col1:
    st.multiselect('Projeto', zendesk_teams['Team'])
with col2:
    st.multiselect('Satisfação', ['Good','Bad','Unoffered','All'])
with col3:
    st.date_input('Data Inicial')
with col4:
    st.date_input('Data Final')


fig = px.bar(zendesk_teams,x='Team',y=['Unoffered','Bom','Ruim'],barmode='stack')
st.plotly_chart(fig)

print(len(zendesk))
