from analysis.analyzer import analyze

from ai.groq_client import classify

from ai.gemini_client import generate_report


def test_pipeline():

    metrics = analyze()

    bottleneck = classify(metrics)

    report = generate_report(metrics, bottleneck)

    assert report is not None

    assert len(report) > 50