import json
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


INPUT_FOLDER = Path("k6/results")
OUTPUT_FOLDER = Path("analysis/output")
CHART_FOLDER = Path("analysis/charts")

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
CHART_FOLDER.mkdir(parents=True, exist_ok=True)


def process_file(file_path):
    """
    Read one k6 JSON result file and extract HTTP request durations.
    """

    response_times = []

    with open(file_path, "r") as f:
        for line in f:

            try:
                record = json.loads(line)

                if (
                    record.get("type") == "Point"
                    and record.get("metric") == "http_req_duration"
                ):
                    response_times.append(record["data"]["value"])

            except Exception:
                continue

    if not response_times:
        return None

    df = pd.DataFrame(response_times, columns=["ResponseTime"])

    summary = {
        "Test": file_path.stem,
        "Requests": len(df),
        "Average(ms)": round(df["ResponseTime"].mean(), 2),
        "Minimum(ms)": round(df["ResponseTime"].min(), 2),
        "Maximum(ms)": round(df["ResponseTime"].max(), 2),
        "P95(ms)": round(df["ResponseTime"].quantile(0.95), 2),
    }

    # Generate response time chart
    plt.figure(figsize=(8, 4))
    plt.plot(df.index, df["ResponseTime"])
    plt.title(f"{file_path.stem} Response Time")
    plt.xlabel("Request Number")
    plt.ylabel("Response Time (ms)")
    plt.grid(True)

    plt.savefig(CHART_FOLDER / f"{file_path.stem}.png")
    plt.close()

    return summary


def analyze():
    """
    Main analysis function.
    Returns the metrics dataframe.
    """

    results = []

    for file in INPUT_FOLDER.glob("*.json"):

        summary = process_file(file)

        if summary:
            results.append(summary)

    metrics_df = pd.DataFrame(results)

    metrics_df.to_csv(
        OUTPUT_FOLDER / "metrics_summary.csv",
        index=False
    )

    return metrics_df


if __name__ == "__main__":

    df = analyze()

    print(df)