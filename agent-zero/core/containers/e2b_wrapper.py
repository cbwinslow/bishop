"""Wrapper around e2b Sandbox for secure code execution."""
import os
from e2b import Sandbox
from typing import Tuple

E2B_API_KEY = os.environ.get("E2B_API_KEY")

def run_code(code: str, template: str = "python3", timeout: int = 60) -> Tuple[str, str]:
    """Execute code inside an e2b sandbox and return (stdout, stderr)."""
    try:
        with Sandbox(template=template, api_key=E2B_API_KEY, timeout=timeout) as sandbox:
            result = sandbox.process.start_and_wait(code)
            return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)

def create_preloaded_container(container_name: str, dockerfile_content: str):
    """Creates a new e2b container template from a Dockerfile."""
    # This is a conceptual implementation.
    # e2b's Python SDK doesn't directly support building new templates.
    # This would typically be done via the e2b CLI or web interface.
    print(f"Requesting creation of container '{container_name}' with Dockerfile:\n{dockerfile_content}")
    # In a real implementation, you would use the e2b CLI or API to build and push the container.
    # e.g., subprocess.run(["e2b", "build", "-f", "Dockerfile", "-t", container_name])

# Example pre-loaded containers
PRELOADED_CONTAINERS = {
    "python-data-analysis": """
        FROM ubuntu:22.04
        RUN apt-get update && apt-get install -y python3 python3-pip
        RUN pip3 install pandas numpy scikit-learn
    """,
    "node-scraping": """
        FROM mcr.microsoft.com/playwright/python:v1.32.0-focal
        RUN npm install axios
    """
}

def provision_containers():
    """Provisions the pre-loaded containers."""
    for name, dockerfile in PRELOADED_CONTAINERS.items():
        create_preloaded_container(name, dockerfile)
