from langchain_core.runnables import RunnableLambda

from ai.groq_client import classify
from ai.gemini_client import generate_report


def run_groq_step(state):
    """
    LangChain step 1:
    Analyze performance metrics using Groq.
    """
    print("  [LangChain] Running Groq RCA...")

    bottleneck = classify(state["metrics"])

    return {
        **state,
        "bottleneck": bottleneck
    }


def run_gemini_step(state):
    """
    LangChain step 2:
    Generate optimization report using Gemini.
    """
    print("  [LangChain] Running Gemini report generation...")

    report = generate_report(
        state["metrics"],
        state["bottleneck"]
    )

    return {
        **state,
        "report": report
    }


# LangChain LCEL orchestration pipeline
performance_chain = (
    RunnableLambda(run_groq_step)
    | RunnableLambda(run_gemini_step)
)


def run_ai_orchestration(metrics_df):
    """
    Execute the AI workflow through LangChain.
    """

    print("\nStarting LangChain AI Orchestration...")

    result = performance_chain.invoke({
        "metrics": metrics_df
    })

    print("✓ LangChain AI Orchestration Complete")

    return result["bottleneck"], result["report"]
