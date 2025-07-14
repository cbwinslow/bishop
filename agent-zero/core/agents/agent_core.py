import logging
import sys
import json
from datetime import datetime
from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, Tool, AgentType
from core.containers.e2b_wrapper import run_code
from core.database import get_db_connection, get_vector_store

# Configure logging to send logs to ELK stack (via Filebeat, etc.)
logging.basicConfig(level=logging.INFO,
                    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "agent": "%(name)s", "message": "%(message)s"}',
                    datefmt='%Y-%m-%dT%H:%M:%S%z',
                    handlers=[logging.FileHandler("agent_zero.log"), logging.StreamHandler()])

class AgentCore:
    def __init__(self, agent_id, model_provider="ollama", model_name="gemma:2b"):
        self.agent_id = agent_id
        self.logger = logging.getLogger(self.agent_id)
        self.llm = self.get_llm(model_provider, model_name)
        self.vector_store = get_vector_store()
        self.db_conn = get_db_connection('agent_zero.db')
        self.memory = self.load_state()

        exec_tool = Tool(
            name="Code Interpreter (e2b)",
            func=lambda code: self.execute_and_log(code),
            description="Executes Python code in a sandbox and returns stdout."
        )

        self.agent = initialize_agent(
            tools=[exec_tool],
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
            memory=self.memory
        )

    def get_llm(self, provider, model_name):
        if provider == "ollama":
            return Ollama(model=model_name)
        # Add other providers like LocalAI here
        else:
            raise ValueError(f"Unsupported model provider: {provider}")

    def load_state(self):
        """Loads agent state from the database."""
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT state FROM agent_states WHERE agent_id = ?", (self.agent_id,))
        row = cursor.fetchone()
        return json.loads(row['state']) if row else {}

    def save_state(self):
        """Saves agent state to the database."""
        cursor = self.db_conn.cursor()
        cursor.execute("REPLACE INTO agent_states (agent_id, state) VALUES (?, ?)",
                       (self.agent_id, json.dumps(self.memory)))
        self.db_conn.commit()

    def log_action(self, level, message):
        """Logs an action to both the logger and the database."""
        self.logger.log(level, message)
        cursor = self.db_conn.cursor()
        cursor.execute("INSERT INTO logs (agent_id, level, message) VALUES (?, ?, ?)",
                       (self.agent_id, logging.getLevelName(level), message))
        self.db_conn.commit()

    def execute_and_log(self, code):
        """Executes code and logs the action."""
        self.log_action(logging.INFO, f"Executing code: {code}")
        stdout, stderr = run_code(code)
        if stderr:
            self.log_action(logging.ERROR, f"Code execution error: {stderr}")
            # Trigger self-healing
            self.self_heal(code, stderr)
        else:
            self.log_action(logging.INFO, f"Code execution stdout: {stdout}")
        return stdout

    def self_heal(self, broken_code, error_message):
        """Attempts to self-heal by fixing broken code."""
        self.log_action(logging.WARNING, f"Attempting to self-heal code for error: {error_message}")

        # Simple self-heal: ask the LLM to fix the code
        prompt = f"The following code failed with the error: {error_message}. Please fix it.\n\nCode:\n{broken_code}"
        fixed_code = self.llm(prompt)

        self.log_action(logging.INFO, f"Proposed fix: {fixed_code}")

        # Test the fix in the sandbox
        stdout, stderr = run_code(fixed_code)
        if stderr:
            self.log_action(logging.ERROR, f"Self-heal failed. Error: {stderr}")
        else:
            self.log_action(logging.INFO, f"Self-heal successful. New output: {stdout}")
            # In a real scenario, you might replace the original code
            # For now, just log the success

    def chat(self, prompt: str) -> str:
        """Send a prompt to the agent and return the response."""
        response = self.agent.run(prompt)
        self.save_state()
        return response

def default_excepthook(exc_type, exc_value, exc_traceback):
    """Custom exception hook to log unhandled exceptions."""
    logging.getLogger("Healer").error("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = default_excepthook
