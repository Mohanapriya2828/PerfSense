import pandas as pd

df = pd.read_csv("analysis/output/metrics_summary.csv")

assert len(df) == 3
assert (df["Average(ms)"] > 0).all()
assert (df["Requests"] > 0).all()

print("All analysis tests passed ")