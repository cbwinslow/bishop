import time
import logging
from agent_zero.core.agents.orchestrator import Orchestrator

def autonomous_loop(orchestrator: Orchestrator, interval_seconds=60):
    """The main autonomous loop for proactive agent actions."""
    logger = logging.getLogger("AutonomousLoop")
    logger.info("Starting autonomous loop...")

    while True:
        try:
            # 1. Self-healing check
            healer = orchestrator.agents["Healer"]
            # In a real scenario, this prompt would be more sophisticated
            healer.chat("Are there any errors in the logs? If so, please analyze and fix them.")

            # 2. Proactive monitoring
            analyst = orchestrator.agents["Analyst"]
            analyst.chat("Proactively monitor systems and report any anomalies.")

            # 3. Continuous learning
            librarian = orchestrator.agents["Librarian"]
            librarian.chat("Index recent logs and conversations for future retrieval.")

            logger.info(f"Autonomous cycle complete. Waiting for {interval_seconds} seconds.")
            time.sleep(interval_seconds)

        except Exception as e:
            logger.error(f"Error in autonomous loop: {e}", exc_info=True)
            time.sleep(interval_seconds) # Wait before retrying
