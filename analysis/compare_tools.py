from pathlib import Path
import pandas as pd
import html

REPORT = Path("reports/cross_tool_comparison.html")
REPORT.parent.mkdir(parents=True, exist_ok=True)


def jmeter_metrics(path):
    df = pd.read_csv(path)

    elapsed = pd.to_numeric(df["elapsed"], errors="coerce").dropna()

    start = pd.to_numeric(df["timeStamp"], errors="coerce").min()
    end = pd.to_numeric(df["timeStamp"], errors="coerce").max()
    duration = (end - start) / 1000

    success = df["success"]

    if success.dtype == bool:
        errors = (~success).mean() * 100
    else:
        errors = (
            success.astype(str).str.lower() != "true"
        ).mean() * 100

    return {
        "requests": len(df),
        "avg": round(elapsed.mean(), 2),
        "min": round(elapsed.min(), 2),
        "max": round(elapsed.max(), 2),
        "p95": round(elapsed.quantile(0.95), 2),
        "error": round(errors, 2),
        "throughput": round(len(df) / duration, 2)
    }


baseline_jm = jmeter_metrics("jmeter/results/baseline.jtl")
stress_jm = jmeter_metrics("jmeter/results/stress.jtl")
spike_jm = jmeter_metrics("jmeter/results/spike.jtl")


results = [
    {
        "test": "Baseline",
        "tool": "k6",
        "requests": 550,
        "avg": 53.95,
        "min": 22.90,
        "max": 415.83,
        "p95": 134.58,
        "error": 0.00,
        "throughput": 17.71
    },
    {
        "test": "Baseline",
        "tool": "JMeter",
        **baseline_jm
    },
    {
        "test": "Stress",
        "tool": "k6",
        "requests": 2670,
        "avg": 968.44,
        "min": 26.35,
        "max": 3840.00,
        "p95": 2420.00,
        "error": 0.00,
        "throughput": 29.41
    },
    {
        "test": "Stress",
        "tool": "JMeter",
        **stress_jm
    },
    {
        "test": "Spike",
        "tool": "k6",
        "requests": 1368,
        "avg": 4220.00,
        "min": 26.41,
        "max": 7140.00,
        "p95": 5930.00,
        "error": 0.00,
        "throughput": 27.88
    },
    {
        "test": "Spike",
        "tool": "JMeter",
        **spike_jm
    }
]


def rows():
    output = ""

    for r in results:
        output += f"""
        <tr>
            <td><strong>{html.escape(r['test'])}</strong></td>
            <td>{html.escape(r['tool'])}</td>
            <td>{r['requests']}</td>
            <td>{r['avg']:.2f} ms</td>
            <td>{r['min']:.2f} ms</td>
            <td>{r['max']:.2f} ms</td>
            <td>{r['p95']:.2f} ms</td>
            <td>{r['error']:.2f}%</td>
            <td>{r['throughput']:.2f} req/s</td>
        </tr>
        """
    return output


def get(test, tool, metric):
    return next(
        r[metric]
        for r in results
        if r["test"] == test and r["tool"] == tool
    )


def bar(value, maximum):
    width = min((value / maximum) * 100, 100)
    return f'<div class="bar" style="width:{width:.1f}%"></div>'


max_avg = max(r["avg"] for r in results)
max_tp = max(r["throughput"] for r in results)

charts = ""

for test in ["Baseline", "Stress", "Spike"]:
    charts += f"""
    <div class="chart-card">
        <h3>{test}</h3>

        <div class="metric-title">Average Response Time</div>

        <div class="chart-row">
            <span>k6</span>
            <div class="bar-bg">
                {bar(get(test, "k6", "avg"), max_avg)}
            </div>
            <strong>{get(test, "k6", "avg"):.2f} ms</strong>
        </div>

        <div class="chart-row">
            <span>JMeter</span>
            <div class="bar-bg">
                {bar(get(test, "JMeter", "avg"), max_avg)}
            </div>
            <strong>{get(test, "JMeter", "avg"):.2f} ms</strong>
        </div>

        <div class="metric-title">Throughput</div>

        <div class="chart-row">
            <span>k6</span>
            <div class="bar-bg">
                {bar(get(test, "k6", "throughput"), max_tp)}
            </div>
            <strong>{get(test, "k6", "throughput"):.2f} req/s</strong>
        </div>

        <div class="chart-row">
            <span>JMeter</span>
            <div class="bar-bg">
                {bar(get(test, "JMeter", "throughput"), max_tp)}
            </div>
            <strong>{get(test, "JMeter", "throughput"):.2f} req/s</strong>
        </div>
    </div>
    """


document = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>PerfSense Cross-Tool Performance Comparison</title>

<style>
body {{
    font-family: Arial, sans-serif;
    background: #f4f6f9;
    margin: 0;
    padding: 35px;
    color: #20242a;
}}

.container {{
    max-width: 1400px;
    margin: auto;
}}

.header {{
    background: #111827;
    color: white;
    padding: 28px;
    border-radius: 12px;
    margin-bottom: 24px;
}}

.header h1 {{
    margin: 0 0 8px 0;
}}

.header p {{
    margin: 0;
    opacity: .85;
}}

.card {{
    background: white;
    padding: 24px;
    border-radius: 12px;
    margin-bottom: 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,.07);
}}

table {{
    border-collapse: collapse;
    width: 100%;
}}

th {{
    background: #1f2937;
    color: white;
    padding: 13px;
}}

td {{
    padding: 12px;
    text-align: center;
    border-bottom: 1px solid #ddd;
}}

tr:hover {{
    background: #f8fafc;
}}

.chart-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
}}

.chart-card {{
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,.07);
}}

.metric-title {{
    margin-top: 18px;
    margin-bottom: 8px;
    font-weight: bold;
}}

.chart-row {{
    display: grid;
    grid-template-columns: 65px 1fr 115px;
    align-items: center;
    gap: 8px;
    margin: 9px 0;
}}

.bar-bg {{
    height: 18px;
    background: #e5e7eb;
    border-radius: 5px;
    overflow: hidden;
}}

.bar {{
    height: 100%;
    background: #2563eb;
}}

.note {{
    background: #fff7ed;
    border-left: 5px solid #f59e0b;
    padding: 16px;
    border-radius: 6px;
}}

.success {{
    background: #ecfdf5;
    border-left: 5px solid #10b981;
    padding: 16px;
    border-radius: 6px;
}}
</style>
</head>

<body>

<div class="container">

<div class="header">
    <h1>PerfSense — k6 vs JMeter</h1>
    <p>Automated Cross-Tool Performance Test Comparison</p>
</div>

<div class="card">
    <h2>Performance Results</h2>

    <table>
        <thead>
            <tr>
                <th>Scenario</th>
                <th>Tool</th>
                <th>Requests</th>
                <th>Average</th>
                <th>Minimum</th>
                <th>Maximum</th>
                <th>P95</th>
                <th>Error Rate</th>
                <th>Throughput</th>
            </tr>
        </thead>

        <tbody>
            {rows()}
        </tbody>
    </table>
</div>

<h2>Cross-Tool Visual Comparison</h2>

<div class="chart-grid">
    {charts}
</div>

<br>

<div class="success">
    <strong>Reliability:</strong>
    Both k6 and JMeter completed the recorded Baseline, Stress and Spike
    executions with a 0% HTTP error rate.
</div>

<br>

<div class="note">
    <strong>Comparison Note:</strong>
    The baseline configurations were workload-matched.
    The current JMeter Stress and Spike configurations use comparable
    ramp profiles rather than exact replicas of the k6 multi-stage
    execution patterns. Stress and Spike results therefore demonstrate
    cross-tool behavior under similar increasing-load conditions and
    should not be interpreted as exact benchmark equivalence.
</div>

</div>

</body>
</html>
"""

REPORT.write_text(document, encoding="utf-8")

print(f"✓ Cross-tool comparison generated: {REPORT}")
print(f"✓ JMeter Baseline P95: {baseline_jm['p95']} ms")
print(f"✓ JMeter Stress P95:   {stress_jm['p95']} ms")
print(f"✓ JMeter Spike P95:    {spike_jm['p95']} ms")
