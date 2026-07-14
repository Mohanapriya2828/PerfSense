import json

from analysis.analyzer import analyze
from ai.groq_client import classify
from ai.gemini_client import generate_report


def main():

    print("=" * 60)
    print("PerfSense AI Performance Pipeline")
    print("=" * 60)

    print("\nStep 1 : Analyzing k6 Results...")
    metrics = analyze()
    print("✓ Analysis Complete")

    print("\nStep 2 : Running Groq Root Cause Analysis...")
    bottleneck = classify(metrics)
    print("✓ Root Cause Identified")

    print("\nStep 3 : Generating Gemini Optimization Report...")
    report = generate_report(metrics, bottleneck)
    print("✓ Report Generated")

    print("\nPipeline Completed Successfully!")

    print("\nSummary")
    print("-" * 30)

    print(metrics)

    print("\nGroq Output")

    print(json.dumps(bottleneck, indent=4))

    print("\nReport saved to:")
    print("reports/performance_report.md")


if __name__ == "__main__":
    main()