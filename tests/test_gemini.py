import pandas as pd

from ai.gemini_client import generate_report


def test_gemini():

    metrics = pd.DataFrame([
        {
            "Average(ms)": 200,
            "Requests": 100,
            "Minimum(ms)": 100,
            "Maximum(ms)": 350,
            "P95(ms)": 250
        }
    ])

    bottleneck = {
        "bottleneck_id": "CPU",
        "reason": "High response time"
    }

    report = generate_report(metrics, bottleneck)

    assert report is not None

    assert len(report) > 50