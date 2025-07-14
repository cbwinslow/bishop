#!/usr/bin/env python3
#===============================================================================
#  Script Name   : main.py
#  Date          : 2025-07-13
#  Author        : Blaine Winslow (CBW)
#  Summary       : Entry point for agent-zero TUI application.
#===============================================================================

import threading
from core.tui.main_tui import run_app
from core.autonomous_loop import autonomous_loop
from core.agents.orchestrator import Orchestrator

if __name__ == "__main__":
    # Create a single orchestrator instance
    orchestrator = Orchestrator()

    # Start the autonomous loop in a background thread
    autonomous_thread = threading.Thread(target=autonomous_loop, args=(orchestrator,), daemon=True)
    autonomous_thread.start()

    # Run the TUI
    run_app(orchestrator)
