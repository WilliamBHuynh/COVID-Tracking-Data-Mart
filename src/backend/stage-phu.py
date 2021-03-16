import psycopg2
import pandas as pd

# Load data
data = pd.read_csv(
    "/mnt/c/Users/William's Zenbook/Desktop/Data Science (4142)/COVID-Tracking-Data-Mart/Data/PHU & Patient dimensions/PHU_dimension.csv")

# Connect to database
conn = psycopg2.connect(
    "host=www.eecs.uottawa.ca port=15432 dbname=group_20 user=whuyn056 password=")

# Open a cursor to perform database operations
cur = conn.cursor()

# Create table
cur.execute("""DROP TABLE if exists d_phu;
            CREATE TABLE d_phu
            (
            phu_surrogate_key           INT NOT NULL,
            phu_key                     INT NOT NULL,
            phu_name                    VARCHAR(21) NOT NULL,
            address                     VARCHAR(30) NOT NULL,
            city                        VARCHAR(7) NOT NULL,
            province                    VARCHAR(7) NOT NULL,
            postal_code                 VARCHAR(7) NOT NULL,
            url                         VARCHAR(100) NOT NULL,
            latitude                    REAL NOT NULL,
            longitude                   REAL NOT NULL,
            PRIMARY KEY (phu_surrogate_key)
            );""")

# Insert values from data to table
sqlInsert = """ INSERT INTO d_phu (phu_surrogate_key, phu_key, phu_name, address, city,
     province, postal_code, url, latitude, longitude) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
for idx, row in data.iterrows():
    record = (row["PHU_Surrogate_Key"], row["PHU_Key"], row["PHU_Name"], row["Address"],
              row["City"], row["Province"], row["Postal_Code"], row["URL"], row["Latitude"], row["Longitude"])
    cur.execute(sqlInsert, record)

# Make the changes to the database persistent
conn.commit()

# Close connections
cur.close()
conn.close()
