import psycopg2
import numpy as np
#from psycopg2.extensions import register_adapter, AsIs
#psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)
import pandas as pd

#f = open(r"C:\Users\samet\Documents\passwordpy.txt", "r")
#password = f.readline()

"""
conn = psycopg2.connect(
    host = "www.eecs.uottawa.ca",
    port = 15432,
    user = "syilm068",
    database = "group_20",
    password = password
)
conn.close()
#cursor = conn.cursor()

"""

df =  pd.read_csv(r'C:\Users\samet\Documents\January_2021\CSI4142\Project_Git\Data\weather_dimension.csv')
print(df.head())

output_file = open(r'C:\Users\samet\Documents\January_2021\CSI4142\Project\weather_sql.txt', "w")


for ind in df.index: 
    str = """INSERT INTO d_weather (weather_key, daily_high_temp, daily_low_temp, daily_mean, station_name, total_precipitation, weather_date) 
    VALUES (%s, %s, %s, %s, \'%s\', %s, \'%s\') ;\n""" % (df['surrogate_key'][ind], df['Max Temp (°C)'][ind], df['Min Temp (°C)'][ind], df['Mean Temp (°C)'][ind], 
    df['Station Name'][ind], df['Total Precip (mm)'][ind], df['Date/Time'][ind])

    output_file.write(str)

output_file.close()