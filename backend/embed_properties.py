import pandas as pd
import psycopg2
import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

df = pd.read_csv("properties.csv")

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

for _, row in df.iterrows():

    text = f"""
    Property with {row['sqft']} sqft,
    {row['bedrooms']} bedrooms,
    school score {row['school_score']},
    noise level {row['noise']}
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

cursor.close()
conn.close()

print("Embeddings stored successfully!")