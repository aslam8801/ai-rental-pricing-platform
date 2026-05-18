import pandas as pd

# Load original CSV
df = pd.read_csv("properties.csv")

# Keep only first 5000 rows
df_5000 = df.head(5000)

# Save new CSV
df_5000.to_csv("properties_5000.csv", index=False)

print("Created properties_5000.csv with 5000 rows")