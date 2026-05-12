from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import pandas as pd
import joblib
import psycopg2
import os

from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer

# =========================
# Load ENV
# =========================

load_dotenv()

# =========================
# Load ML Models
# =========================

model = joblib.load("xgboost_rent_model.pkl")

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

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
# FastAPI App
# =========================

app = FastAPI()

# =========================
# Enable CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Request Models
# =========================

class Property(BaseModel):
    sqft: int
    bedrooms: int
    school_score: int
    noise: int


class Feedback(BaseModel):
    property_id: int
    accepted: bool
    predicted_rent: float
    final_rent: float


class ComparableRequest(BaseModel):
    sqft: int
    bedrooms: int
    school_score: int
    noise: int

# =========================
# Routes
# =========================

@app.get("/")
def home():
    return {
        "message": "AI Rental Prediction API 🚀"
    }

# =========================
# Predict Rent
# =========================

@app.post("/predict")
def predict(property: Property):

    data = pd.DataFrame([{
        "sqft": property.sqft,
        "bedrooms": property.bedrooms,
        "school_score": property.school_score,
        "noise": property.noise
    }])

    prediction = model.predict(data)[0]

    return {
        "predicted_rent": round(float(prediction), 2)
    }

# =========================
# Save Feedback
# =========================

@app.post("/feedback")
def save_feedback(feedback: Feedback):

    cursor.execute(
        """
        INSERT INTO feedback (
            property_id,
            accepted,
            predicted_rent,
            final_rent
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            feedback.property_id,
            feedback.accepted,
            feedback.predicted_rent,
            feedback.final_rent
        )
    )

    conn.commit()

    return {
        "message": "Feedback saved successfully!"
    }

# =========================
# Similar Properties
# =========================

@app.post("/similar-properties")
def similar_properties(property: ComparableRequest):

    text = f"""
    Property with
    {property.sqft} sqft,
    {property.bedrooms} bedrooms,
    school score {property.school_score},
    noise level {property.noise}
    """

    embedding = embedding_model.encode(text).tolist()

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
        (embedding,)
    )

    results = cursor.fetchall()

    properties = []

    for row in results:

        properties.append({
            "id": row[0],
            "sqft": row[1],
            "bedrooms": row[2],
            "school_score": row[3],
            "noise": row[4],
            "rent": row[5]
        })

    return {
        "comparables": properties
    }