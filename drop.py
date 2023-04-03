import sqlite3

conn = sqlite3.connect('weather_db.db')
c = conn.cursor()

c.execute("DROP TABLE weather_20.csv")

conn.commit()
conn.close()
