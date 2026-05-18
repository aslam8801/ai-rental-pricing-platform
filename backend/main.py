from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import psycopg2
import os
from dotenv import load_dotenv

# =========================
# LOAD ENV
# =========================

load_dotenv()

# =========================
# FASTAPI APP
# =========================

app = FastAPI()

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DATABASE CONNECTION
# =========================

def get_db_connection():

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

# =========================
# REQUEST MODELS
# =========================

class Property(BaseModel):

    locality: str
    latitude: float
    longitude: float

    sqft: int
    bedrooms: int

    metro_distance_km: float


class Feedback(BaseModel):

    property_id: int
    accepted: bool
    predicted_rent: float
    final_rent: float

# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "message": "AI Rental Pricing API Running 🚀"
    }

# =========================
# PREDICT
# =========================

@app.post("/predict")
def predict(property: Property):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            locality,
            latitude,
            longitude,
            sqft,
            bedrooms,
            metro_distance_km,
            hospital_distance_km,
            rent,

            (
                (
                    ABS(latitude - %s) +
                    ABS(longitude - %s)
                ) * 100 * 0.40

                +

                ABS(sqft - %s) * 0.25

                +

                ABS(bedrooms - %s) * 5 * 0.20

                +

                ABS(metro_distance_km - %s) * 10 * 0.15

            ) AS similarity_score

        FROM properties

        WHERE locality = %s

        ORDER BY similarity_score ASC

        LIMIT 5
        """,
        (
            property.latitude,
            property.longitude,

            property.sqft,

            property.bedrooms,

            property.metro_distance_km,

            property.locality
        )
    )

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    # =========================
    # NO RESULTS SAFETY
    # =========================

    if len(results) == 0:

        return {
            "message": "No comparable properties found"
        }

    comparables = []

    rents = []

    for row in results:

        geo_distance = round(
            (
                abs(row[2] - property.latitude) +
                abs(row[3] - property.longitude)
            ) * 111,
            2
        )

        comparables.append({

            "id": row[0],
            "locality": row[1],

            "latitude": row[2],
            "longitude": row[3],

            "sqft": row[4],
            "bedrooms": row[5],

            "metro_distance_km": round(row[6], 2),

            "hospital_distance_km": round(row[7], 2),

            "rent": round(row[8]),

            "geo_distance_km": geo_distance,

            "similarity_score": round(row[9], 2)
        })

        rents.append(row[8])

    # =========================
    # RENT ESTIMATION
    # =========================

    predicted_rent = round(sum(rents) / len(rents))

    return {

        "predicted_rent": predicted_rent,

        "comparables": comparables,

        "explanation": [

            "Rent estimated using nearby comparable listings.",

            "Geographic proximity heavily influenced ranking.",

            "Property size and metro access affected pricing."
        ]
    }

# =========================
# FEEDBACK
# =========================

@app.post("/feedback")
def save_feedback(feedback: Feedback):

    conn = get_db_connection()
    cursor = conn.cursor()

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

    cursor.close()
    conn.close()

    return {
        "message": "Feedback saved successfully"
    }