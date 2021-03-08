import psycopg2
import pandas as pd

# Load mobility data
mobilityData = pd.read_csv(
    "/mnt/c/Users/William's Zenbook/Desktop/Data Science (4142)/COVID-Tracking-Data-Mart/Data/Mobility/mobility_dimension.csv")

# Connect to database
conn = psycopg2.connect(
    "host=www.eecs.uottawa.ca port=15432 dbname=group_20 user=whuyn056 password=")

# Open a cursor to perform database operations
cur = conn.cursor()

# Create Mobility table
cur.execute("""DROP TABLE if exists d_mobility;
            CREATE TABLE d_mobility
            (
            mobility_key              INT NOT NULL,
            date                      DATE NOT NULL,
            subregion                 VARCHAR(16) NOT NULL,
            province                  VARCHAR(7) NOT NULL,
            retail_and_recreation     FLOAT(2) NOT NULL,
            grocery_and_pharmacy      FLOAT(2) NOT NULL,
            parks                     FLOAT(2) NOT NULL,
            transit_stations          FLOAT(2) NOT NULL,
            workplaces                FLOAT(2) NOT NULL,
            residential               FLOAT(2) NOT NULL,
            PRIMARY KEY (mobility_key)
            );""")


# Insert values from mobility data to table
sqlInsert = """ INSERT INTO d_mobility (mobility_key, date, subregion, province, retail_and_recreation, grocery_and_pharmacy,
    parks, transit_stations, workplaces, residential) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
for idx, row in mobilityData.iterrows():
    record = (row["Mobility_key"], row["Date"], row["Subregion"], row["Province"], row["Retail_and_recreation"],
              row["Grocery_and_phramacy"], row["Parks"], row["Transit_stations"], row["Workplaces"], row["Residential"])
    cur.execute(sqlInsert, record)

# Make the changes to the database persistent
conn.commit()

# Close connections
cur.close()
conn.close()
