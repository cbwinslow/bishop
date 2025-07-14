from agent_zero.core.agents.orchestrator import Orchestrator

def run_data_analysis_workflow():
    """
    This workflow demonstrates how to use the Analyst agent to analyze data.
    """
    orchestrator = Orchestrator()

    # Task for the Analyst agent
    analysis_task = (
        "Analyze the provided dataset and generate a report on the key insights. "
        "The dataset is located at /path/to/your/dataset.csv. "
        "Focus on the correlation between different columns."
    )

    # Delegate the task to the Analyst agent
    report = orchestrator.delegate_task(analysis_task)

    print("Data Analysis Report:")
    print(report)

if __name__ == "__main__":
    run_data_analysis_workflow()
