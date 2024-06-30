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

# Dropdown to select city
projec = st.selectbox("Select a project", options=[jira['Chave do projeto'].unique()])

# Filter DataFrame based on city
filtered_df = jira[jira['Chave do projetoy'] == projec]

# Plotting the bar chart
fig = px.bar(filtered_df, x='Fruit', y='Amount', color='Fruit', barmode='group')

# Display the bar chart
st.plotly_chart(fig)


