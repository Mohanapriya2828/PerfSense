import pandas as pd

from ai.groq_client import classify


def test_groq():

    metrics = pd.DataFrame([
        {
            "Average(ms)": 200,
            "Requests": 100,
            "Minimum(ms)": 100,
            "Maximum(ms)": 350,
            "P95(ms)": 250
        }
    ])

    result = classify(metrics)

    assert result is not None

    assert isinstance(result, dict)