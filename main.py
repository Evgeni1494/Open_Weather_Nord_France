import requests
import pandas as pd
from datetime import datetime
from utils import get_nord_weather
import os
from dotenv import load_dotenv
import sqlite3


load_dotenv()
api_key = os.environ.get("API_KEY")


get_nord_weather()