ROOT_CAUSE_PROMPT = """
You are an expert performance engineer.

Analyze the following performance metrics and classify the primary bottleneck.

Metrics:
{metrics}

Possible Bottleneck IDs:
BOT001 - High Response Time
BOT002 - High Error Rate
BOT003 - Low Throughput
BOT004 - CPU Bottleneck
BOT005 - Memory Bottleneck
BOT006 - Database Bottleneck

Return ONLY JSON in this format:

{{
    "bottleneck_id":"",
    "severity":"",
    "reason":"",
    "recommendation":""
}}
"""