from agent_zero.core.agents.agent_core import AgentCore

class Team:
    def __init__(self, name, agents):
        self.name = name
        self.agents = agents

    def get_agent(self, role):
        return self.agents.get(role)

def create_data_science_team():
    """Creates a data science team with specialized agents."""
    data_scientist = AgentCore("DataScientist", model_name="mistral:7b")
    data_engineer = AgentCore("DataEngineer", model_name="gemma:2b")

    team = Team("Data Science Team", {
        "DataScientist": data_scientist,
        "DataEngineer": data_engineer
    })
    return team

def create_devops_team():
    """Creates a DevOps team for infrastructure management."""
    sys_admin = AgentCore("SysAdmin", model_name="gemma:2b")
    security_specialist = AgentCore("SecuritySpecialist", model_name="gemma:2b")

    team = Team("DevOps Team", {
        "SysAdmin": sys_admin,
        "SecuritySpecialist": security_specialist
    })
    return team
