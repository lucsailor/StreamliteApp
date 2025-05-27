import streamlit as st
import sqlite3
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Datenbanken Hausarbeit",
    page_icon="📊",  # Optional: Emoji oder Icon-URL
    layout="wide",
)

st.title("Kamkinis der Piç!")
st.write("Das ist meine erste Streamlit-A.")

conn = sqlite3.connect('sports_league.sqlite')

tables = pd.read_sql("SELECT * FROM leagues", conn)
st.dataframe(tables, hide_index=True)

fig = px.pie(
    pd.read_sql("SELECT name, cl_spot FROM leagues", conn),
    names='name',
    values='cl_spot',
    title='Champions League Plätze pro Liga',
)
fig.update_traces(textinfo='label+value')

st.plotly_chart(fig, use_container_width=True)