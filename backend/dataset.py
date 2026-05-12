import pandas as pd
import random

data = []

for _ in range(100):
    sqft = random.randint(500, 3000)
    bedrooms = random.randint(1, 5)
    school_score = random.randint(1, 10)
    noise = random.randint(1, 10)

    rent = (
        sqft * 2
        + bedrooms * 500
        + school_score * 300
        - noise * 200
    )

    data.append([
        sqft,
        bedrooms,
        school_score,
        noise,
        rent
    ])

df = pd.DataFrame(data, columns=[
    "sqft",
    "bedrooms",
    "school_score",
    "noise",
    "rent"
])

df.to_csv("properties.csv", index=False)

print(df.head())