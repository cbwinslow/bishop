from agent_zero.core.agents.agent_core import AgentCore

class Orchestrator(AgentCore):
    def __init__(self, agent_id="Orchestrator"):
        super().__init__(agent_id)
        self.agents = {
            "Librarian": AgentCore("Librarian"),
            "Healer": AgentCore("Healer"),
            "Coder": AgentCore("Coder"),
            "Analyst": AgentCore("Analyst")
        }

    def delegate_task(self, task):
        # Simple delegation logic based on keywords
        if "fix" in task or "error" in task:
            return self.agents["Healer"].chat(task)
        elif "code" in task or "develop" in task:
            return self.agents["Coder"].chat(task)
        elif "analyze" in task or "report" in task:
            return self.agents["Analyst"].chat(task)
        elif "find" in task or "search" in task:
            return self.agents["Librarian"].chat(task)
        else:
            return self.chat(task)
