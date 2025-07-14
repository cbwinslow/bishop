from agent_zero.core.agents.orchestrator import Orchestrator

def run_code_generation_workflow():
    """
    This workflow demonstrates how to use the Coder agent to generate code.
    """
    orchestrator = Orchestrator()

    # Task for the Coder agent
    coding_task = (
        "Write a Python script that uses the requests library to fetch data from an API "
        "and saves it to a JSON file. The API endpoint is https://api.example.com/data."
    )

    # Delegate the task to the Coder agent
    generated_code = orchestrator.delegate_task(coding_task)

    print("Generated Code:")
    print(generated_code)

    # You can then execute this code in an e2b container
    # from agent_zero.core.containers.e2b_wrapper import run_code
    # stdout, stderr = run_code(generated_code)
    # print("Execution Output:", stdout)

if __name__ == "__main__":
    run_code_generation_workflow()
