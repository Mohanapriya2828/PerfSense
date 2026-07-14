import os
import json

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

scenarios = [
    {
        "name": "High Response Time",
        "metrics": {
            "Average(ms)": 3000,
            "Requests": 500,
            "ErrorRate": 1
        },
        "expected": "BOT001"
    },
    {
        "name": "High Error Rate",
        "metrics": {
            "Average(ms)": 200,
            "Requests": 500,
            "ErrorRate": 40
        },
        "expected": "BOT002"
    },
    {
        "name": "Low Throughput",
        "metrics": {
            "Average(ms)": 150,
            "Requests": 50,
            "ErrorRate": 0
        },
        "expected": "BOT003"
    }
]

for scenario in scenarios:

    prompt = f"""
You are a Performance Engineering Expert.

Classify the bottleneck.

Possible IDs:

BOT001 = High Response Time
BOT002 = High Error Rate
BOT003 = Low Throughput
BOT004 = CPU Bottleneck
BOT005 = Memory Bottleneck
BOT006 = Database Bottleneck

Metrics:

{json.dumps(scenario["metrics"], indent=2)}

Return ONLY JSON.

{{
    "bottleneck_id":"",
    "severity":"",
    "reason":"",
    "recommendation":""
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content

    print("=" * 70)
    print("Scenario :", scenario["name"])
    print("Expected :", scenario["expected"])
    print("Groq Output:")
    print(result)
    print("=" * 70)