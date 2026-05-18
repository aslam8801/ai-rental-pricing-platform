CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE properties (

    id BIGSERIAL PRIMARY KEY,

    property_type TEXT,

    locality TEXT,

    latitude FLOAT,
    longitude FLOAT,

    sqft INT,
    bedrooms INT,
    bathrooms INT,

    school_score FLOAT,
    amenities_score FLOAT,
    crime_score FLOAT,
    flood_risk FLOAT,
    noise_score FLOAT,

    metro_distance FLOAT,

    rent FLOAT,

    embedding VECTOR(384)
);