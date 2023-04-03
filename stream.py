import streamlit as st
import pandas as pd
from utils import get_nord_weather
import sqlite3

st.title("Données météo pour les villes du Nord de la France")

# Créer un bouton pour mettre à jour les données
if st.button("Mettre à jour les données"):
    get_nord_weather()

# Charger les données depuis la base de données SQLite
conn = sqlite3.connect('weather_db.db')
df = pd.read_sql_query("SELECT * from ma_table", conn)
conn.close()

# Afficher les données dans un tableau
st.write(df)
