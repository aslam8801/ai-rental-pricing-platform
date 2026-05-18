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
# DATABASE CONNECTION
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
# FASTAPI APP
# =========================

app = FastAPI()

# =========================
# ENABLE CORS
# =========================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# =========================
# REQUEST MODELS
# =========================

class Property(BaseModel):

    locality: str

    sqft: int

    bedrooms: int

    metro_distance_km: float

    hospital_distance_km: float

    flood_risk: float


class Feedback(BaseModel):

    property_id: int

    accepted: bool

    predicted_rent: float

    final_rent: float

# =========================
# HOME ROUTE
# =========================

@app.get("/")
def home():

    return {

        "message": "AI Rental Intelligence API Running"
    }

# =========================
# PREDICT RENT
# =========================

@app.post("/predict")
def predict(property: Property):

    # =========================
    # GET COMPARABLE PROPERTIES
    # =========================

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

                ABS(sqft - %s) * 0.20 +

                ABS(bedrooms - %s) * 0.20 +

                ABS(metro_distance_km - %s) * 0.30 +

                ABS(hospital_distance_km - %s) * 0.20 +

                RANDOM() * 0.10

            ) AS similarity_score

        FROM properties

        WHERE locality IS NOT NULL

        ORDER BY similarity_score ASC

        LIMIT 5
        """,
        (

            property.sqft,

            property.bedrooms,

            property.metro_distance_km,

            property.hospital_distance_km
        )
    )

    results = cursor.fetchall()

    # =========================
    # FORMAT RESPONSE
    # =========================

    comparables = []

    rents = []

    for row in results:

        rents.append(row[8])

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

            "similarity_score": round(row[9], 2)
        })

    # =========================
    # RENT ESTIMATION
    # =========================

    if len(rents) > 0:

        predicted_rent = round(

            sum(rents) / len(rents)
        )

    else:

        predicted_rent = 0

    # =========================
    # EXPLANATIONS
    # =========================

    explanation = [

        "Pricing derived from nearby comparable listings.",

        "Metro connectivity influenced accessibility scoring.",

        "Hospital distance influenced livability scoring.",

        "Property size and bedroom count affected similarity ranking."
    ]

    # =========================
    # RESPONSE
    # =========================

    return {

        "predicted_rent": predicted_rent,

        "comparables": comparables,

        "explanation": explanation
    }

# =========================
# SAVE FEEDBACK
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

        "message": "Feedback saved successfully"
    }