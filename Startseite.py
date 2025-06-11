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

# Alle Ligen laden
leagues_df = pd.read_sql("SELECT league_id, name FROM leagues", conn)
league_names = leagues_df['name'].tolist()

# Session-State für aktive Liga
# Initialisiere den Liga-State
if "selected_league" not in st.session_state:
    st.session_state.selected_league = leagues_df["name"].tolist()[0]  # z. B. "Serie A"

cols = st.columns(len(league_names))

# Temporärer Speicher für Klick
clicked_league = None

for i, col in enumerate(cols):
    with col:
        if st.button(league_names[i], use_container_width=True):
            clicked_league = league_names[i]

# Nach der Schleife den Zustand aktualisieren (nur wenn geklickt)
if clicked_league:
    st.session_state.selected_league = clicked_league

# Dann verwendest du diesen Wert:
selected_league = st.session_state.selected_league

for i, col in enumerate(cols):
    with col:
        if league_names[i] == st.session_state.selected_league:
            st.markdown(
                f"""
                <div style='
                    position: relative;
                    top: -3.65rem;
                    padding: 0.6rem 0.5rem;
                    background-color: #0066cc;
                    color: white;
                    border-radius: 10px;
                    font-weight: bold;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                    text-align: center;
                    z-index: 999;
                    margin-bottom: -10.8rem;
                '>{league_names[i]}</div>
                """,
                unsafe_allow_html=True
            ) 



# Lookup: ID zur gewählten Liga finden
selected_league_id = leagues_df.loc[leagues_df["name"] == selected_league, "league_id"].values[0]

# Tabelle laden 
standings_df = pd.read_sql(f"""
    SELECT *
    FROM standings
    WHERE league_id = {selected_league_id}
    ORDER BY points DESC
""", conn)

# Teamnamen hinzufügen
teams_df = pd.read_sql("SELECT team_id, name FROM teams", conn)
df = (
    standings_df
    .rename(columns={
        "position": "Platz",
        "played_games": "Spiele",
        "won": "Siege",
        "draw": "Unentschieden",
        "lost": "Niederlagen","points": "Punkte"
        })
    .merge(teams_df, on="team_id", how="left")
    .drop(columns=["team_id"])
    .rename(columns={"name": "Team"})
)

# Spaltenreihenfolge definieren
df = df[["Platz", "Team", "Spiele", "Siege", "Unentschieden", "Niederlagen", "Punkte"]]
df = df.set_index("Platz")

# Daten anzeigen
st.table(df)