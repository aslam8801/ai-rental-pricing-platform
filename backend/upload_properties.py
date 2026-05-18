import pandas as pd
import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()

# =========================
# Load CSV
# =========================

df = pd.read_csv("properties.csv")

# Keep only first 5000 rows
df = df.head(5000)

print("CSV Loaded:", len(df))

# =========================
# Remove Missing Values
# =========================

df = df.dropna()

print("After cleaning:", len(df))

# =========================
# Database Connection
# =========================

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

# =========================
# Insert Data
# =========================

inserted = 0

for _, row in df.iterrows():

    try:

        cursor.execute(
            """
            INSERT INTO properties (

                property_type,

                locality,
                city,

                latitude,
                longitude,

                sqft,
                bedrooms,

                metro_distance_km,
                airport_distance_km,
                hospital_distance_km,

                rent

            )

            VALUES (
                %s,%s,%s,
                %s,%s,
                %s,%s,
                %s,%s,%s,
                %s
            )
            """,

            (
                str(row["property_type"]),

                str(row["locality"]),
                str(row["city"]),

                float(row["latitude"]),
                float(row["longitude"]),

                int(row["sqft"]),
                int(row["bedrooms"]),

                float(row["metro_distance_km"]),
                float(row["airport_distance_km"]),
                float(row["hospital_distance_km"]),

                float(row["rent"])
            )
        )

        inserted += 1

        # commit every 200 rows
        if inserted % 200 == 0:

            conn.commit()

            print(f"Inserted {inserted} rows")

    except Exception as e:

        print("FAILED ROW:", e)

# =========================
# Final Commit
# =========================

conn.commit()

print("DONE!")
print("Total inserted:", inserted)

cursor.close()
conn.close()