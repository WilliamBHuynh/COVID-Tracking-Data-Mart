import psycopg2
import pandas as pd

# Load fact table data
factTableData = pd.read_csv(
    "/mnt/c/Users/William's Zenbook/Desktop/Data Science (4142)/COVID-Tracking-Data-Mart/Data/Fact_table/fact_table.csv")

# Connect to database
conn = psycopg2.connect(
    "host=www.eecs.uottawa.ca port=15432 dbname=group_20 user=whuyn056 password=")

# Open a cursor to perform database operations
cur = conn.cursor()

# Create Fact table
cur.execute("""DROP TABLE if exists fact_table;
            CREATE TABLE fact_table
            (
            Onset_date_key              INT NOT NULL,
            Reported_date_key           INT NOT NULL,
            Test_date_key               INT NOT NULL,
            Specimen_date_key           INT NOT NULL,
            Patient_key                 INT NOT NULL,
            PHU_key                     INT NOT NULL,
            Mobility_key                INT NOT NULL,
            Special_measures_key        INT NOT NULL,
            Weather_key                 INT NOT NULL,
            Resolved                    BIT NOT NULL,
            UnResolved                  BIT NOT NULL,
            Fatal                       BIT NOT NULL,
            FOREIGN KEY (Onset_date_key) REFERENCES d_onset_date(Onset_date_key),
            FOREIGN KEY (Reported_date_key) REFERENCES d_reported_date(Reported_date_key),
            FOREIGN KEY (Test_date_key) REFERENCES d_test_date(Test_date_key),
            FOREIGN KEY (Specimen_date_key) REFERENCES d_specimen_date(Specimen_date_key),
            FOREIGN KEY (Patient_key) REFERENCES d_patient(Patient_key),
            FOREIGN KEY (PHU_key) REFERENCES d_phu(PHU_key),
            FOREIGN KEY (Mobility_key) REFERENCES d_mobility(Mobility_key),
            FOREIGN KEY (Special_measures_key) REFERENCES d_special_measures(Special_measures_key),
            FOREIGN KEY (Weather_key) REFERENCES d_weather(Weather_key)
            );""")


# Insert values from the fact table data to database
sqlInsert = """ INSERT INTO fact_table (Onset_date_key, Reported_date_key, Test_date_key, Specimen_date_key, Patient_key,
    PHU_key, Mobility_key, Special_measures_key, Weather_key, Resolved, UnResolved, Fatal) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
for idx, row in factTableData.iterrows():
    record = (row["Mobility_key"], row["Date"], row["Subregion"], row["Province"], row["Retail_and_recreation"],
              row["Grocery_and_phramacy"], row["Parks"], row["Transit_stations"], row["Workplaces"], row["Residential"])
    cur.execute(sqlInsert, record)

# Make the changes to the database persistent
conn.commit()

# Close connections
cur.close()
conn.close()
