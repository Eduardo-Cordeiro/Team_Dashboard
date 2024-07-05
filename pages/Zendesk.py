import pandas as pd
import requests
from io import StringIO
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

# Load data from URL
url1 = 'https://raw.githubusercontent.com/Eduardo-Cordeiro/Team_Dashboard/main/Zendesk_Data.csv'
response1 = requests.get(url1)
response1.raise_for_status()
csv_content1 = response1.text
zendesk = pd.read_csv(StringIO(csv_content1), delimiter=',')

zendesk["Creation Date"] = pd.to_datetime(zendesk["Creation Date"])
zendesk['Last Update Date'] = pd.to_datetime(zendesk['Last Update Date'])

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

print(zendesk["Team"])
print(zendesk["Team"].value_counts())
times = zendesk.groupby('Team')["Agent"].value_counts()
members_per_team = [len(times.xs("A", level="Team")),len(times.xs("B", level="Team")),len(times.xs("C", level="Team"))]

zendesk_teams = pd.DataFrame()
zendesk_teams["Team"] = zendesk["Team"].value_counts().index
zendesk_teams["Quantidade"] = zendesk["Team"].value_counts().values
zendesk_teams["Membros"] = members_per_team
zendesk_teams["Tickets por agente"] = zendesk_teams["Quantidade"] / zendesk_teams["Membros"]
print(zendesk_teams)

st.title("Zendesk Dashboard")
days_to_subtract = timedelta(days=31)

st.markdown(f'Tickets nos últimos 30 dias: {len(zendesk[zendesk["Creation Date"] > (zendesk["Creation Date"].max() - days_to_subtract)])}')

days_to_subtract2 = timedelta(days=7)

st.markdown(f'Tickets nos últimos 7 dias: {len(zendesk[zendesk["Creation Date"] > (zendesk["Creation Date"].max() - days_to_subtract2)])}')

zen_categoria = pd.DataFrame()
zen_categoria["Categoria"] = zendesk["Categoria"].value_counts().index
zen_categoria["Quantidade"] = zendesk["Categoria"].value_counts().values

st.markdown('### 20 Principais categorias dos atendimentos.')
# Display the selected option
fig3 = px.bar(zen_categoria.head(20),x="Categoria",y="Quantidade")
st.plotly_chart(fig3)

# Title of the Streamlit app
st.markdown('### Tickets atendidos por time')

# Plotting the pie chart
fig4, ax = plt.subplots()
ax.pie(zendesk_teams["Tickets por agente"], labels=zendesk_teams["Team"], autopct='%1.1f%%', startangle=90, textprops={'color': 'white'})
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Display the pie chart in Streamlit
fig4.savefig('transparent_pie_chart.png', transparent=True)

# Load and display the transparent pie chart in Streamlit
st.image('transparent_pie_chart.png')

fig5 = px.bar(zendesk_teams,x = 'Team', y = "Tickets por agente")
fig5.update_traces(marker_color='lightskyblue', selector=dict(type='bar'))
st.plotly_chart(fig5)
