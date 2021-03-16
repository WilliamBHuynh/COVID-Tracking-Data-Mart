import psycopg2
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
import pandas as pd
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

# Load fact table data
factTableData = pd.read_csv(
    "/mnt/c/Users/William's Zenbook/Desktop/Data Science (4142)/COVID-Tracking-Data-Mart/Data/Fact_Table/Fact_Table_Final.csv")

# Connect to database
conn = psycopg2.connect(
    "host=www.eecs.uottawa.ca port=15432 dbname=group_20 user=whuyn056 password=")

# Open a cursor to perform database operations
cur = conn.cursor()

# Create Fact table
cur.execute("""DROP TABLE if exists fact_table;
            CREATE TABLE fact_table
            (
            onset_date_key              INT NOT NULL,
            reported_date_key           INT NOT NULL,
            test_date_key               INT NOT NULL,
            specimen_date_key           INT NOT NULL,
            patient_key                 INT NOT NULL,
            phu_key                     INT NOT NULL,
            mobility_key                INT NOT NULL,
            special_measures_key        INT NOT NULL,
            weather_key                 INT NOT NULL,
            resolved                    INT NOT NULL,
            unresolved                  INT NOT NULL,
            fatal                       INT NOT NULL,
            FOREIGN KEY (onset_date_key) REFERENCES d_onset_date(onset_date_surrogate_key),
            FOREIGN KEY (reported_date_key) REFERENCES d_reported_date(reported_date_surrogate_key),
            FOREIGN KEY (test_date_key) REFERENCES d_test_date(test_date_surrogate_key),
            FOREIGN KEY (specimen_date_key) REFERENCES d_specimen_date(specimen_date_surrogate_key),
            FOREIGN KEY (patient_key) REFERENCES d_patient(patient_surrogate_key),
            FOREIGN KEY (phu_key) REFERENCES d_phu(phu_surrogate_key),
            FOREIGN KEY (mobility_key) REFERENCES d_mobility(mobility_key),
            FOREIGN KEY (special_measures_key) REFERENCES d_special_measures(surrogate_key),
            FOREIGN KEY (weather_key) REFERENCES d_weather(weather_key)
            );""")

# Insert values from the fact table data to database
sqlInsert = """ INSERT INTO fact_table (onset_date_key, reported_date_key, test_date_key, specimen_date_key, patient_key,
    phu_key, mobility_key, special_measures_key, weather_key, resolved, unresolved, fatal) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
for idx, row in factTableData.iterrows():
    record = (row["Onset_Date_Surrogate_Key"], row["Reported_Date_Surrogate_Key"], row["Test_Date_Surrogate_Key"], row["Specimen_Date_Surrogate_Key"], row["Patient_Surrogate_Key"],
              row["PHU_Surrogate_Key"], row["Mobility_Surrogate_Key"], row["Special_Measures_Surrogate_Key"], row["Weather_Surrogate_Key"], row["Resolved"], row["Unresolved"], row["Fatal"])
    cur.execute(sqlInsert, record)

# Make the changes to the database persistent
conn.commit()

# Close connections
cur.close()
conn.close()
