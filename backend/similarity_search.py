import psycopg2
import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

query = "3 bedroom apartment with good schools and low noise"

query_embedding = model.encode(query).tolist()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

cursor.execute(
    """
    SELECT
        id,
        sqft,
        bedrooms,
        school_score,
        noise,
        rent
    FROM properties
    ORDER BY embedding <=> %s::vector
    LIMIT 5
    """,
    (query_embedding,)
)

results = cursor.fetchall()

for row in results:
    print(row)

cursor.close()
conn.close()