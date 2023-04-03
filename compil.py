import requests
import pandas as pd
from datetime import datetime
from utils import get_nord_weather
import os
from dotenv import load_dotenv
import sqlite3


load_dotenv()
api_key = os.environ.get("API_KEY")



def get_wind_direction(deg):
    if (deg >= 337.5) or (deg < 22.5):
        return "Nord"
    elif (deg >= 22.5) and (deg < 67.5):
        return "Nord-Est"
    elif (deg >= 67.5) and (deg < 112.5):
        return "Est"
    elif (deg >= 112.5) and (deg < 157.5):
        return "Sud-Est"
    elif (deg >= 157.5) and (deg < 202.5):
        return "Sud"
    elif (deg >= 202.5) and (deg < 247.5):
        return "Sud-Ouest"
    elif (deg >= 247.5) and (deg < 292.5):
        return "Ouest"
    elif (deg >= 292.5) and (deg < 337.5):
        return "Nord-Ouest"


# Charger les variables d'environnement à partir du fichier .env
load_dotenv()
# Récupérer la clé API
api_key = os.environ.get("API_KEY")


def get_nord_weather():
    df = pd.read_csv("cities.csv")
    weather_data = []   
    for index, row in df.iterrows():
        # Récupération des coordonnées de la ville
        lat = row["Latitude"]
        lon = row["Longitude"]
        
        # Requête API OpenWeather pour récupérer les informations météorologiques de la ville
        params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
        response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
        
        # Récupération des informations météorologiques pour chaque ville et stockage dans la liste 'weather_data'
        city_name = row["City"]
        temperature = response.json()["main"]["temp"]
        temp_feels_like = response.json()["main"]["feels_like"]
        temp_min = response.json()["main"]["temp_min"]
        temp_max = response.json()["main"]["temp_max"]
        pressure = response.json()["main"]["pressure"]
        humidity = response.json()["main"]["humidity"]
        W_speed = response.json()["wind"]["speed"]
        W_direction = response.json()["wind"]["deg"]
        Sun_Rise = response.json()["sys"]["sunrise"]
        Sun_Set = response.json()["sys"]["sunset"]
        weather_description = response.json()["weather"][0]["description"]
        
        
        
        # Conversion des valeurs de lever et coucher de soleil en heure lisible par l'humain
        sunrise_time = datetime.fromtimestamp(Sun_Rise).strftime('%H:%M:%S')
        sunset_time = datetime.fromtimestamp(Sun_Set).strftime('%H:%M:%S')
        
        # Conversion des valeurs de la direction du vent
        
        
        wind_direction = get_wind_direction(W_direction)
        
        
        # Ajout des informations météorologiques de la ville dans la liste 'weather_data'
        city_weather_data = {"City": city_name, 
                            "Temperature en C°": temperature,
                            "Feels like":temp_feels_like,
                            "Temp_min en C°":temp_min,
                            "Temp_max en C°":temp_max,
                            "Pression" : pressure,
                            "Humidité" : humidity,
                            "Vitesse_Vent en M":W_speed,
                            "Direction Vent" : wind_direction,
                            "Weather Description": weather_description,
                            "Lever du soleil" : sunrise_time,
                            "Coucher du soleil" : sunset_time
                            }
        weather_data.append(city_weather_data)

# Création du DataFrame à partir de la liste de dictionnaires
        weather_df = pd.DataFrame(weather_data)

        weather_df.to_csv("weather_20.csv", index=False)
        
    
    df = pd.read_csv('weather_20.csv')

    # Se connecter à la base de données SQLite
    conn = sqlite3.connect('weather_db.db')

    # Écrire les données dans la base de données SQLite
    df.to_sql('ma_table', conn, if_exists='replace', index=False)

    # Fermer la connexion à la base de données
    conn.close()
    get_nord_weather()