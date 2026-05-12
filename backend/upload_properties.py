import pandas as pd
import psycopg2
import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# =========================
# Load ENV
# =========================

load_dotenv()

# =========================
# Embedding Model
# =========================

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# =========================
# DB Connection
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
# Load Dataset
# =========================

df = pd.read_csv("properties.csv")

# =========================
# Upload Properties
# =========================

for _, row in df.iterrows():

    text = f"""
    Property with
    {row['sqft']} sqft,
    {row['bedrooms']} bedrooms,
    school score {row['school_score']},
    noise level {row['noise']},
    rent {row['rent']}
    """

    embedding = model.encode(text).tolist()

    cursor.execute(
        """
        INSERT INTO properties (
            sqft,
            bedrooms,
            school_score,
            noise,
            rent,
            embedding
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            int(row["sqft"]),
            int(row["bedrooms"]),
            int(row["school_score"]),
            int(row["noise"]),
            float(row["rent"]),
            embedding
        )
    )

conn.commit()

print("Properties uploaded successfully!")

cursor.close()
conn.close()