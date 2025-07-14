from agent_zero.core.agents.team_builder import create_data_science_team, create_devops_team

def run_team_creation_workflow():
    """
    This workflow demonstrates how to create and use teams of AI agents.

    Use Cases:
    - Data Science Team: Can be used for complex data analysis tasks that require
      both data engineering (cleaning, preparation) and data science (modeling, analysis).
    - DevOps Team: Can be used to manage infrastructure, monitor security, and automate deployments.
    """

    # Create a data science team
    ds_team = create_data_science_team()
    print(f"Created team: {ds_team.name}")

    # Get the data scientist from the team
    data_scientist = ds_team.get_agent("DataScientist")

    # Assign a task to the data scientist
    task = "Build a predictive model using the data in /path/to/data.csv"
    response = data_scientist.chat(task)
    print(f"Data Scientist response: {response}")

    # Create a DevOps team
    devops_team = create_devops_team()
    print(f"Created team: {devops_team.name}")

    # Get the system administrator from the team
    sys_admin = devops_team.get_agent("SysAdmin")

    # Assign a task to the system administrator
    task = "Check the health of the web server and restart it if necessary."
    response = sys_admin.chat(task)
    print(f"SysAdmin response: {response}")

if __name__ == "__main__":
    run_team_creation_workflow()
