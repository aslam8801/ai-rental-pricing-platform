import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

query = "remove noisy properties"

prompt = f"""
You are an AI real estate assistant.

Convert the user query into JSON filters.

Available fields:
- min_sqft
- max_noise
- min_school_score
- bedrooms

Return ONLY valid JSON.

User Query:
{query}
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

result = response.choices[0].message.content

print(result)