import re
import json
import re
from pathlib import Path

from analysis.analyzer import analyze
from pipeline.langchain_orchestrator import run_ai_orchestration


def main():
    print("=" * 60)
    print("PerfSense AI Performance Pipeline")
    print("=" * 60)

    print("\nStep 1 : Analyzing k6 Results...")
    metrics = analyze()
    print("✓ Analysis Complete")

    print("\nStep 2 : Running LangChain AI Orchestration...")
    bottleneck, report = run_ai_orchestration(metrics)
    print("✓ LangChain Analysis and Report Complete")

    print("\nStep 3 : Exporting AI Metrics for Grafana...")

    health_match = re.search(
        r"Overall Health Score.*?\**(\d+)\s*/\s*100",
        report,
        re.IGNORECASE | re.DOTALL
    )

    health_score = int(health_match.group(1)) if health_match else 0

    severity_map = {
        "Low": 1,
        "Moderate": 2,
        "High": 3,
        "Critical": 4
    }

    severity_text = bottleneck.get("severity", "Low")
    severity_value = severity_map.get(severity_text, 1)

    p95_latency = float(metrics["P95(ms)"].max())

    grafana_data = {
        "health_score": health_score,
        "severity": severity_text,
        "severity_value": severity_value,
        "p95_latency_ms": p95_latency,
        "bottleneck_id": bottleneck.get("bottleneck_id", "UNKNOWN"),
        "reason": bottleneck.get("reason", ""),
        "recommendation": bottleneck.get("recommendation", "")
    }

    output_path = Path("analysis/output/grafana_ai_metrics.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(grafana_data, f, indent=4)

    print("✓ Grafana AI Metrics Exported")

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
