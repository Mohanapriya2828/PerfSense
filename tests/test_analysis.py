import os

from analysis.analyzer import analyze


def test_analysis():

    df = analyze()

    assert df is not None

    assert not df.empty

    assert "Average(ms)" in df.columns

    assert "Requests" in df.columns

    assert os.path.exists("analysis/output/metrics_summary.csv")