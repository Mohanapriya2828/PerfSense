from analysis.analyzer import analyze
from ai.groq_client import classify

metrics = analyze()

result = classify(metrics)

print(result)