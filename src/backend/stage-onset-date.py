import psycopg2
import pandas as pd

# Load data
data = pd.read_csv(
    "/mnt/c/Users/William's Zenbook/Desktop/Data Science (4142)/COVID-Tracking-Data-Mart/Data/Dates/Onset_Date_dimension.csv")

# Connect to database
conn = psycopg2.connect(
    "host=www.eecs.uottawa.ca port=15432 dbname=group_20 user=whuyn056 password=")

# Open a cursor to perform database operations
cur = conn.cursor()

# Create table
cur.execute("""DROP TABLE if exists d_onset_date2;
            CREATE TABLE d_onset_date2
            (
            onset_date_key              INT NOT NULL,
            day                         INT NOT NULL,
            month                       INT NOT NULL,
            day_of_week                 VARCHAR(10),
            week_in_year                INT,
            holiday                     BOOLEAN,
            season                      VARCHAR(10),
            weekend                     BOOLEAN,
            year                        INT NOT NULL,
            date_full_format            DATE,
            PRIMARY KEY (onset_date_key)
            );""")

# Insert values from data to table
sqlInsert = """ INSERT INTO d_onset_date2 (onset_date_key, day, month, day_of_week, week_in_year, holiday,
    season, weekend, year, date_full_format) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
for idx, row in data.iterrows():
    record = (row["Onset_Date_Surrogate_Key"], row["Day"], row["Month"], row["Day_of_Week"], row["Week_of_Year"],
              row["Holiday"], row["Season"], row["Weekend"], row["Year"], row["Date_Full_Format"])
    cur.execute(sqlInsert, record)

# Make the changes to the database persistent
conn.commit()

# Close connections
cur.close()
conn.close()
