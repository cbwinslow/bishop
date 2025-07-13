"""Wrapper around e2b Sandbox for secure code execution."""
from e2b import Sandbox
from typing import Tuple

def run_code(code: str, template: str = "python", timeout: int = 60) -> Tuple[str, str]:
    """Execute code inside an e2b sandbox and return (stdout, stderr)."""
    sandbox = Sandbox(template=template, timeout=timeout)
    result = sandbox.run(code)
    return result.stdout, result.stderr
