import psycopg2
import pandas as pd


special = pd.read_csv(
    r"C:\Users\samet\Documents\January_2021\CSI4142\Project_Git\Data\Special_Measures\Special_Measures_Dimension.csv")

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
            surrogate_key              INT NOT NULL,
            begin_date                DATE NOT NULL,
            end_date                  DATE NOT NULL, 
            city                 VARCHAR(10) NOT NULL,
            zone_measures        VARCHAR(10) NOT NULL,
            description          VARCHAR(150) NOT NULL,
            key_word             VARCHAR(100) NOT NULL,
            lockdown             INT NOT NULL,
            mandatory_masks      INT NOT NULL,
            indoor_dining        INT NOT NULL,
            gyms_open            INT NOT NULL,
            stay_at_home_order   INT NOT NULL,
            max_indoor_capacity  INT NOT NULL,
            max_outdoor_capacity  INT NOT NULL,

            PRIMARY KEY (surrogate_key)
            );""")


sqlInsert = """ INSERT INTO d_special_measures (surrogate_key, begin_date, end_date, city, zone_measures, description, key_word, lockdown, mandatory_masks, 
indoor_dining, gyms_open,stay_at_home_order, max_indoor_capacity, max_outdoor_capacity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """

for idx, row in special.iterrows():
    record = (row["Special_Measures_Surrogate_Key"], row["Start_Date"], row["End_Date"], row["City"], row["Zone_Measures"],
              row["Description"], row["Key_Word"], row["Lockdown"], row["Mandatory Masks"], row["Indoor Dining"], row["Gyms Open"],
              row["Stay-at-home Order"], row["Max Indoor Capacity"], row["Max Outdoor Capacity"] )
    curr.execute(sqlInsert, record)

conn.commit()

# Close connections
curr.close()
conn.close()
