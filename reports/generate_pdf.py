from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

doc = SimpleDocTemplate("reports/performance_report.pdf")

story = []

with open("reports/performance_report.md", "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            story.append(Paragraph(line.replace("\n", "<br/>"), styles["BodyText"]))

doc.build(story)

print("PDF Generated Successfully")