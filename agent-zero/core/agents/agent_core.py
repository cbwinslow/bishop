"""Agent core leveraging LangChain & Ollama."""
from langchain.llms import Ollama
from langchain.agents import initialize_agent, Tool, AgentType
from core.containers.e2b_wrapper import run_code

llm = Ollama(model="gemma:2b")

exec_tool = Tool(
    name="Code Interpreter (e2b)",
    func=lambda code: run_code(code)[0],
    description="Executes Python code in a sandbox and returns stdout."
)

agent = initialize_agent(
    tools=[exec_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

def chat(prompt: str) -> str:
    """Send a prompt to the agent and return the response."""
    return agent.run(prompt)
