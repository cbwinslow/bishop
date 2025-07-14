import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, TextLog, Button, DirectoryTree
from textual.containers import Vertical, Horizontal
from agent_zero.core.agents.orchestrator import Orchestrator
from agent_zero.core.agents.team_builder import create_data_science_team, create_devops_team
import importlib

class WorkflowSelector(Vertical):
    def __init__(self, orchestrator: Orchestrator, log: TextLog, **kwargs):
        super().__init__(**kwargs)
        self.orchestrator = orchestrator
        self.log = log

    def compose(self) -> ComposeResult:
        yield Static("[b]Workflows[/b]")
        yield Button("Data Analysis", id="data_analysis_wf")
        yield Button("Code Generation", id="code_gen_wf")
        yield Button("Team Creation", id="team_creation_wf")

    async def on_button_pressed(self, event: Button.Pressed):
        workflow_module_name = f"workflows.{event.button.id.replace('_wf', '')}_workflow"
        self.log.write(f"Running {workflow_module_name}...")
        try:
            workflow_module = importlib.import_module(workflow_module_name)
            workflow_function = getattr(workflow_module, f"run_{event.button.id.replace('_wf', '')}_workflow")
            # This is a simplified way to run the workflow.
            # In a real application, you'd likely run this in a separate process
            # and stream the output to the TUI.
            asyncio.create_task(self.run_workflow(workflow_function))
        except (ModuleNotFoundError, AttributeError) as e:
            self.log.write(f"[red]Error running workflow: {e}[/red]")

    async def run_workflow(self, workflow_function):
        # In a real app, you would capture stdout and display it in the log
        workflow_function()
        self.log.write(f"[green]Workflow finished.[/green]")


class AgentZeroTUI(App):
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orchestrator = Orchestrator()

    def compose(self) -> ComposeResult:
        yield Header()
        log = TextLog(highlight=True, markup=True)
        with Horizontal():
            yield WorkflowSelector(self.orchestrator, log)
            yield Vertical(
                Static("[b]Logs[/b]"),
                log
            )
        yield Footer()

def run_app():
    AgentZeroTUI().run()
