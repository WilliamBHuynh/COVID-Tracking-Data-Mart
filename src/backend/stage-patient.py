import psycopg2
import pandas as pd

# Load data
data = pd.read_csv(
    "/mnt/c/Users/William's Zenbook/Desktop/Data Science (4142)/COVID-Tracking-Data-Mart/Data/PHU & Patient dimensions/Patient_dimension.csv")

# Connect to database
conn = psycopg2.connect(
    "host=www.eecs.uottawa.ca port=15432 dbname=group_20 user=whuyn056 password=")

# Open a cursor to perform database operations
cur = conn.cursor()

# Create table
cur.execute("""DROP TABLE if exists d_patient;
            CREATE TABLE d_patient
            (
            patient_surrogate_key       INT NOT NULL,
            patient_key                 INT NOT NULL,
            age                         VARCHAR(7) NOT NULL,
            gender                      VARCHAR(6) NOT NULL,
            acquisition_group           VARCHAR(20) NOT NULL,
            outbreak_related            BOOLEAN NOT NULL,
            PRIMARY KEY (patient_surrogate_key)
            );""")

# Insert values from data to table
sqlInsert = """ INSERT INTO d_patient (patient_surrogate_key, patient_key, age, gender, acquisition_group,
     outbreak_related) VALUES (%s,%s,%s,%s,%s,%s) """
for idx, row in data.iterrows():
    record = (row["Patient_Surrogate_Key"], row["Patient_Key"], row["Age"], row["Gender"],
              row["Acquisition_Group"], row["Outbreak_Related"])
    cur.execute(sqlInsert, record)

# Make the changes to the database persistent
conn.commit()

# Close connections
cur.close()
conn.close()
