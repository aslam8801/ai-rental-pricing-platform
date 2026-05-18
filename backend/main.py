from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import pandas as pd
import joblib
import psycopg2
import os

from dotenv import load_dotenv

# =========================
# Load ENV
# =========================

load_dotenv()

# =========================
# Load ML Model
# =========================

model = joblib.load("xgboost_rent_model.pkl")

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
    school_score: float
    noise: float


class Feedback(BaseModel):
    property_id: int
    accepted: bool
    predicted_rent: float
    final_rent: float


# =========================
# Routes
# =========================

@app.get("/")
def home():

    return {
        "message": "AI Rental Intelligence Platform 🚀"
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
# REAL Comparable Retrieval
# =========================

@app.post("/similar-properties")
def similar_properties(property: Property):

    cursor.execute(
        """
        SELECT
            id,
            sqft,
            bedrooms,
            school_score,
            noise,
            rent,

            (
                ABS(sqft - %s) * 0.40 +

                ABS(bedrooms - %s) * 0.20 +

                ABS(school_score - %s) * 0.25 +

                ABS(noise - %s) * 0.15

            ) AS similarity_score

        FROM properties

        ORDER BY similarity_score ASC

        LIMIT 5
        """,
        (
            property.sqft,
            property.bedrooms,
            property.school_score,
            property.noise
        )
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
            "rent": row[5],
            "similarity_score": round(float(row[6]), 2)
        })

    return {
        "comparables": properties
    }