import os
import json

from dotenv import load_dotenv
from groq import Groq

from ai.prompts import ROOT_CAUSE_PROMPT

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def classify(metrics_df):
    """
    Sends performance metrics to Groq
    and returns bottleneck classification.
    """

    metrics = metrics_df.to_string(index=False)

    prompt = ROOT_CAUSE_PROMPT.format(
        metrics=metrics
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content

    try:
        parsed = json.loads(result)
    except Exception:
        parsed = {
            "raw_output": result
        }

    os.makedirs("analysis/output", exist_ok=True)

    with open(
        "analysis/output/groq_analysis.json",
        "w"
    ) as f:

        json.dump(
            parsed,
            f,
            indent=4
        )

    return parsed
