import psycopg2
import pandas as pd


special = pd.read_csv(
    r"C:\Users\samet\Documents\January_2021\CSI4142\Project_Git\Data\Special_Measures\Restrictions.csv")

f = open(r"C:\Users\samet\Documents\passwordpy.txt", "r")
password = f.readline()


conn = psycopg2.connect(
    host = "www.eecs.uottawa.ca",
    port = 15432,
    user = "syilm068",
    database = "group_20",
    password = password
)

curr = conn.cursor()


curr.execute("""DROP TABLE if exists d_special_measures;
            CREATE TABLE d_special_measures
            (
            measures_key              INT NOT NULL,
            begin_date                DATE NOT NULL,
            end_date                  DATE NOT NULL, 
            city                 VARCHAR(10) NOT NULL,
            zone_measures        VARCHAR(10) NOT NULL,
            description          VARCHAR(150) NOT NULL,
            PRIMARY KEY (measures_key)
            );""")


sqlInsert = """ INSERT INTO d_special_measures (measures_key, begin_date, end_date, city, zone_measures, description) VALUES (%s,%s,%s,%s,%s,%s) """

for idx, row in special.iterrows():
    record = (row["surrogate_key"], row["start_date"], row["end_date"], row["city"], row["zone_measures"],
              row["description"])
    curr.execute(sqlInsert, record)

conn.commit()

# Close connections
curr.close()
conn.close()
