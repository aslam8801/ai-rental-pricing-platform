DROP TABLE IF EXISTS properties;

CREATE TABLE properties (

    id BIGSERIAL PRIMARY KEY,

    property_type TEXT,

    locality TEXT,
    city TEXT,

    latitude FLOAT,
    longitude FLOAT,

    sqft INT,
    bedrooms INT,

    metro_distance_km FLOAT,
    airport_distance_km FLOAT,
    hospital_distance_km FLOAT,

    rent FLOAT
);