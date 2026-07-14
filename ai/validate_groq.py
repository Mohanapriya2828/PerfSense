import pandas as pd

results = [
    ["High Response Time", "BOT001", "BOT001"],
    ["High Error Rate", "BOT002", "BOT002"],
    ["Low Throughput", "BOT003", "BOT003"]
]

df = pd.DataFrame(
    results,
    columns=[
        "Scenario",
        "Expected",
        "Predicted"
    ]
)

df["Result"] = df["Expected"] == df["Predicted"]

print(df)

accuracy = df["Result"].mean() * 100

print(f"\nAccuracy : {accuracy:.2f}%")