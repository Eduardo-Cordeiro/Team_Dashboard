import pandas as pd
import requests
from io import StringIO
import streamlit as st
import plotly.express as px
import os

st.markdown("# Team Dashboard")
st.markdown("Apresentando dados do Jira e Zendesk de uma equipe de Suporte")
st.markdown("👈 À esquerda temos as páginas disponíveis para seleção.")
