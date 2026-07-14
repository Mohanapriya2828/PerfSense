import os
import json
import time
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use the stable model available to your account
MODEL_NAME = "gemini-flash-lite-latest"

model = genai.GenerativeModel(MODEL_NAME)


def generate_report(metrics_df, bottleneck):
    """
    Generate a performance report using Gemini.
    """

    prompt = f"""
You are a Senior Performance Engineer.

Analyze the following performance test results.

==============================
Performance Metrics
==============================

{metrics_df.to_string(index=False)}

==============================
Root Cause (Groq)
==============================

{json.dumps(bottleneck, indent=2)}

Generate a professional report with the following sections.

# Executive Summary

# Performance Metrics

# Root Cause Analysis

# Performance Recommendations

# API Optimization Suggestions

# Infrastructure Recommendations

# Database Optimization Suggestions

# Overall Health Score (0-100)

# Conclusion

Return ONLY Markdown.
"""

    response = None

    # Retry up to 3 times if Gemini is temporarily unavailable
    for attempt in range(3):
        try:
            print(f"Calling Gemini (Attempt {attempt+1})...")
            response = model.generate_content(prompt)
            break
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt == 2:
                raise
            time.sleep(5)

    report = response.text

    os.makedirs("reports", exist_ok=True)

    report_path = "reports/performance_report.md"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nReport saved to {report_path}")

    return report


if __name__ == "__main__":

    import pandas as pd

    metrics = pd.read_csv("analysis/output/metrics_summary.csv")

    with open("analysis/output/groq_analysis.json", "r") as f:
        bottleneck = json.load(f)

    report = generate_report(metrics, bottleneck)

    print(report)