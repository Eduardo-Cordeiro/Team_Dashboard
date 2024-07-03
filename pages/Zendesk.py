import pandas as pd
import requests
from io import StringIO
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta

# Load data from URL
url1 = 'https://raw.githubusercontent.com/Eduardo-Cordeiro/Team_Dashboard/main/Zendesk_Data.csv'
response1 = requests.get(url1)
response1.raise_for_status()
csv_content1 = response1.text
zendesk = pd.read_csv(StringIO(csv_content1), delimiter=',')

zendesk["Creation Date"] = pd.to_datetime(zendesk["Creation Date"])
zendesk['Last Update Date'] = pd.to_datetime(zendesk['Last Update Date'])

st.title("Zendesk Dashboard")
days_to_subtract = timedelta(days=31)

st.markdown(f'Tickets nos últimos 30 dias: {len(zendesk[zendesk["Creation Date"] > (zendesk["Creation Date"].max() - days_to_subtract)])}')

days_to_subtract2 = timedelta(days=7)

st.markdown(f'Tickets nos últimos 7 dias: {len(zendesk[zendesk["Creation Date"] > (zendesk["Creation Date"].max() - days_to_subtract2)])}')

zen_categoria = pd.DataFrame()
zen_categoria["Categoria"] = zendesk["Categoria"].value_counts().index
zen_categoria["Quantidade"] = zendesk["Categoria"].value_counts().values


# Display the selected option
fig3 = px.bar(zen_categoria.head(20),x="Categoria",y="Quantidade",title="20 pricipais categorias dos atendimentos realizados")
st.plotly_chart(fig3)
