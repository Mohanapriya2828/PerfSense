from analysis.analyzer import analyze
from ai.groq_client import classify
from ai.gemini_client import generate_report

print("Running Analysis...")
metrics = analyze()

print("Running Groq...")
bottleneck = classify(metrics)

print("Generating Gemini Report...")
report = generate_report(metrics, bottleneck)

print("\n==========================")
print("PIPELINE COMPLETED")
print("==========================")