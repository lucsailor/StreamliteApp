import streamlit as st
import sqlite3
import plotly.express as px
import pandas as pd

# Seiten Einstellungen
st.set_page_config(
    page_title="Datenbanken Hausarbeit",
    page_icon="https://crests.football-data.org/BL1.png",
    layout="wide",
)

# Bild mit Text
image = "https://ethianum-klinik-heidelberg.de/wp-content/uploads/2024/01/header-sportorthopaedie_fussball_2400x824px.webp",
st.markdown(f"""
<div style="position: relative; text-align: center;">
    <img src="https://ethianum-klinik-heidelberg.de/wp-content/uploads/2024/01/header-sportorthopaedie_fussball_2400x824px.webp" style="width: 100%; border-radius: 10px;" />
    <div style="
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: rgba(0,0,0,0.6);
        color: white;
        padding: 1.2rem 2rem;
        border-radius: 8px;
        font-size: 2.2rem;
        font-weight: bold;
        z-index: 2;">
        Willkommen zur Fußball-Datenanalyse
    </div>
</div>
""", unsafe_allow_html=True)

# Abstand und Text darunter
st.markdown("---")
st.subheader("Willkommen auf unserer Datenanalyse-Plattform")
st.write("Hier analysieren wir die Top-5 Fußballligen Europas anhand echter Daten.")

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