import unittest
import os
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, '.')
from core.agents.agent_core import AgentCore
from core.database import init_db, get_db_connection

class TestAgentCore(unittest.TestCase):

    def setUp(self):
        # Use an in-memory SQLite DB for tests
        self.db_conn = get_db_connection(":memory:")
        init_db(":memory:")

        # Mock external services
        os.environ["E2B_API_KEY"] = "test_key"
        self.mock_llm = MagicMock()
        self.mock_vector_store = MagicMock()
        self.mock_e2b = patch('core.containers.e2b_wrapper.Sandbox').start()

    def tearDown(self):
        patch.stopall()

    @patch('core.agents.agent_core.Ollama')
    @patch('core.database.get_vector_store')
    def test_agent_initialization(self, mock_get_vector_store, mock_ollama):
        mock_ollama.return_value = self.mock_llm
        mock_get_vector_store.return_value = self.mock_vector_store
        agent = AgentCore("TestAgent")
        self.assertEqual(agent.agent_id, "TestAgent")
        self.assertIsNotNone(agent.agent)

    @patch('core.agents.agent_core.Ollama')
    @patch('core.database.get_vector_store')
    def test_chat_functionality(self, mock_get_vector_store, mock_ollama):
        mock_ollama.return_value = self.mock_llm
        mock_get_vector_store.return_value = self.mock_vector_store
        self.mock_llm.return_value = "Test response"

        agent = AgentCore("TestAgent")
        agent.agent.run = MagicMock(return_value="Test response")

        response = agent.chat("Hello")
        self.assertEqual(response, "Test response")
        agent.agent.run.assert_called_with("Hello")

    @patch('core.agents.agent_core.Ollama')
    @patch('core.database.get_vector_store')
    def test_self_healing_logic(self, mock_get_vector_store, mock_ollama):
        mock_ollama.return_value = self.mock_llm
        mock_get_vector_store.return_value = self.mock_vector_store
        self.mock_llm.side_effect = ["fixed code", "successful execution"]

        agent = AgentCore("TestAgent")

        # Mock run_code to simulate an error then success
        with patch('core.agents.agent_core.run_code') as mock_run_code:
            mock_run_code.side_effect = [
                ("", "Syntax error"),  # Initial failure
                ("Success", "")       # Success after fixing
            ]

            agent.execute_and_log("broken code")

            # Check that the LLM was called to fix the code
            self.mock_llm.assert_any_call("The following code failed with the error: Syntax error. Please fix it.\n\nCode:\nbroken code")

            # Check that the fixed code was executed
            mock_run_code.assert_called_with("fixed code")

if __name__ == '__main__':
    unittest.main()
