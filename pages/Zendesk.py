import pandas as pd
import requests
from io import StringIO
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

# Load data from URL and adjust Frame

url1 = 'https://raw.githubusercontent.com/Eduardo-Cordeiro/Team_Dashboard/main/Zendesk_Data.csv'
response1 = requests.get(url1)
response1.raise_for_status()
csv_content1 = response1.text
zendesk = pd.read_csv(StringIO(csv_content1), delimiter=',')
zendesk["Creation Date"] = pd.to_datetime(zendesk["Creation Date"])
zendesk['Last Update Date'] = pd.to_datetime(zendesk['Last Update Date'])
zendesk["Unidade"] = 1
zendesk["NoUpdate"] = zendesk["Last Update Date"] - zendesk["Creation Date"]

#Randomizing teams
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

# Construindo Widgets iniciais
min_date = zendesk["Creation Date"].min().date()
max_date = zendesk["Creation Date"].max().date()


st.title("Zendesk Dashboard")

col1, col2 = st.columns([1,1])
with col1:
    time_selected = st.multiselect('Time', ["A",'B','C'],default=["A", "B", "C"])
    start = st.date_input('Data Inicial',min_value=min_date, max_value=max_date, value=min_date)
with col2:
    satis = st.multiselect('Satisfação', ['Good','Bad','Unoffered'],default=['Unoffered','Good','Bad'])
    end = st.date_input('Data Final',min_value=min_date, max_value=max_date, value=max_date)

# Creating the teams DataFrame 
zendesk = zendesk[(zendesk["Creation Date"] >= pd.Timestamp(start)) & (zendesk["Creation Date"] <= pd.Timestamp(end))]
good = zendesk[zendesk["Satisfação"] == 'Good'].groupby("Team")['Unidade'].sum()
bad = zendesk[zendesk["Satisfação"] == 'Bad'].groupby("Team")['Unidade'].sum()
times = zendesk.groupby('Team')["Agent"].value_counts()
members_per_team = [len(times.xs("A", level="Team")),len(times.xs("B", level="Team")),len(times.xs("C", level="Team"))]

zendesk_teams = pd.DataFrame()
zendesk_teams["Team"] = zendesk["Team"].value_counts().index
zendesk_teams["Quantidade"] = zendesk["Team"].value_counts().values
zendesk_teams["Membros"] = members_per_team
zendesk_teams["Tickets por agente"] = zendesk_teams["Quantidade"] / zendesk_teams["Membros"]
zendesk_teams["Good"] = good.values
zendesk_teams["Bad"] = bad.values
zendesk_teams["Unoffered"] = zendesk_teams["Quantidade"] - (zendesk_teams["Good"] + zendesk_teams["Bad"])
a = zendesk_teams[zendesk_teams["Team"].isin(time_selected)]

# Displaying Teams Chart
st.markdown("")
st.markdown("#### Quantidade de Atendimentos por Time e Satisfação") 
fig = px.bar(a,x='Team',y=satis,barmode='stack')
st.plotly_chart(fig)

b = zendesk[(zendesk["Team"].isin(time_selected)) & (zendesk["Satisfação"].isin(satis))]
category = b["Categoria"].value_counts()
category = category.reset_index()
print(category.head())

st.markdown("#### 15 Principais Categorias") 
fig2 = px.bar(category.head(15), x='count',y="Categoria",barmode='stack')
st.plotly_chart(fig2)

st.markdown("#### Tickets DataFrame") 
st.dataframe(b[["Ticket ID",'Client ID','Ticket Status','Agent','Categoria','Creation Date']], hide_index=True)
