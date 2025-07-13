"""Textual TUI frontend for agent-zero."""

import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, TextLog
from textual.containers import Horizontal
from textual.reactive import reactive

class RepoList(Static):
    repos = reactive([])

    def compose(self) -> ComposeResult:
        yield Static("[b]Repo List[/b]\n(press g to load)", id="repo-list")

class ChatPane(TextLog):
    pass

class AgentZeroApp(App):
    BINDINGS = [("q", "quit", "Quit"), ("g", "load_repos", "Load Repos"), ("ctrl+a", "toggle_chat", "Chat")]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            self.repo_widget = RepoList()
            self.chat_widget = ChatPane(highlight=False)
            yield self.repo_widget
            yield self.chat_widget
        yield Footer()

    async def action_load_repos(self):
        self.repo_widget.update("[green]Loading repos...[/green]")
        await asyncio.sleep(1)
        self.repo_widget.update("- sample/repo1\n- sample/repo2")

    def action_toggle_chat(self):
        self.chat_widget.visible = not self.chat_widget.visible

def run_app():
    AgentZeroApp().run()
