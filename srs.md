# Software Requirements Specification (SRS)

**Project Codename:** `agent‑zero`\
**Subtitle:** Terminal‑resident AI Desktop Companion with Modular Plugins, Ollama LLM & e2b Code‑Interpreter Containers

---

| Version   | Date (YYYY‑MM‑DD) | Author           | Summary               |
| --------- | ----------------- | ---------------- | --------------------- |
| 0.1‑draft | 2025‑07‑13        | CBW & ChatGPT‑o3 | Initial specification |

---

## 1. Introduction

### 1.1 Purpose

`agent‑zero` is a professionally engineered Terminal‑User‑Interface (TUI) application that acts as an extensible desktop companion.  It provides:

- **AI‑assisted workflows** powered by a local Ollama LLM (default `gemma:2b` or `mistral:7b`),
- **Secure code interpretation** via sandboxed **e2b containers**,
- **Modular plug‑and‑play tooling** (GitHub manager, MCP control, file utils, etc.),
- **Persistent memory, autonomous self‑improvement, self‑healing & internet access** capabilities.

### 1.2 Scope

The system will run on any modern POSIX terminal (Linux, macOS, WSL).  It will manage GitHub repositories, execute MCP server commands, run arbitrary code in isolated sandboxes, and provide a conversational side‑panel chat interface.  The project will grow by loading additional plugins without touching the core.

### 1.3 Definitions, Acronyms & Abbreviations

| Term       | Definition                                                                         |
| ---------- | ---------------------------------------------------------------------------------- |
| **TUI**    | Terminal User Interface (Textual framework)                                        |
| **LLM**    | Large Language Model                                                               |
| **Ollama** | Local LLM server exposing REST endpoints                                           |
| **e2b**    | "Execution‑to‑Behavior" container platform for secure sandboxing                   |
| **MCP**    | "Micro‑Control Program"; CBW’s utility servers/tools                               |
| **Plugin** | Self‑registering Python module that extends agent‑zero                             |
| **Memory** | Combination of short‑term (in‑process) & long‑term (JSON/TinyDB/Redis) persistence |

### 1.4 References

- Ollama Docs [https://ollama.com](https://ollama.com)
- e2b Python SDK [https://docs.e2b.dev](https://docs.e2b.dev)
- Textualize/Textual [https://textual.textualize.io](https://textual.textualize.io)
- LangChain & LangGraph [https://python.langchain.com](https://python.langchain.com)

### 1.5 Overview

Section 2 gives an overall description, Section 3 lists specific requirements, Section 4 details non‑functional qualities, Section 5 defines external interfaces, Section 6 shows system architecture, Section 7 lists future enhancements.

---

## 2. Overall Description

### 2.1 Product Perspective

`agent‑zero` is a standalone CLI app packaged with `pipx` or a self‑contained binary (`shiv`/`pyoxidizer`).  It is the umbrella under which discrete plugins live.  Each plugin provides its own commands, TUI widgets and LangChain Tools.

### 2.2 Product Functions (High‑Level)

1. **TUI Shell** – Textual application with main viewport, sidebar chat, status bar, key‑bindings & theming.
2. **AI Assistant** – Chat panel powered by Ollama; can invoke Tools (function calling) & summarise logs.
3. **Plugin Loader** – Auto‑discovers Python modules in `plugins/` and entry points (`cbw_agent_zero.plugins`).
4. **e2b Container Manager** – Spins up sandboxes per code task; streams stdout/stderr; enforces time & resource limits.
5. **Memory Store** – Persists chat history, plugin state, system metrics; supports TTL cleanup & export.
6. **Scheduler / Autonomy Loop** – Optional background thread that runs diagnostic tasks & proposes improvements.

### 2.3 User Characteristics

- **CBW (primary)** – Power‑user comfortable with command line, Python & Git.
- **Advanced Developers** – Want extendable CLI with AI & secure execution.
- **Casual Users (future)** – May use subset via wrappers; UI must remain intuitive.

### 2.4 Constraints

- Must operate offline (local LLM) when no internet.
- Must use sandbox (e2b) for any AI‑generated code execution.
- Should consume <300 MB idle RAM & <5 % CPU when idle on mid‑range device.

### 2.5 Assumptions & Dependencies

- Python ≥ 3.10 available.
- Docker or Podman installed for e2b container backend.
- Ollama server is running on `localhost:11434`.
- Git installed & authenticated via SSH.

---

## 3. Specific Requirements

### 3.1 Functional Requirements (FR)

| ID        | Description                                                                                                                                               | Priority |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| **FR‑1**  | The system **shall** list GitHub repositories (owned, starred, org) via OAuth token.                                                                      | High     |
| **FR‑2**  | The user **shall** multi‑select repositories and specify a destination directory.                                                                         | High     |
| **FR‑3**  | The system **shall** clone or pull each repo concurrently, displaying progress bars.                                                                      | High     |
| **FR‑4**  | The chat sidebar **shall** accept natural language and route to Ollama for responses.                                                                     | High     |
| **FR‑5**  | The AI **shall** be able to call registered Tools (LangChain actions) including: filesystem read/write, Git operations, MCP commands, e2b code execution. | High     |
| **FR‑6**  | The system **shall** execute arbitrary Python/Bash/Node snippets inside an e2b sandbox and return the output.                                             | High     |
| **FR‑7**  | The system **shall** log every AI‑initiated action with timestamp and result.                                                                             | High     |
| **FR‑8**  | The user **shall** toggle “dry‑run” mode that simulates actions without execution.                                                                        | Medium   |
| **FR‑9**  | The system **shall** persist chat + action logs to a local database (TinyDB/SQLite).                                                                      | Medium   |
| **FR‑10** | The scheduler **shall** run periodic self‑diagnostics and propose improvements via chat.                                                                  | Low      |

### 3.2 Non‑Functional Requirements (NFR)

| ID        | Requirement               | Target                                                               |
| --------- | ------------------------- | -------------------------------------------------------------------- |
| **NFR‑1** | Startup time              |  < 2 s on NVMe SSD                                                   |
| **NFR‑2** | Clone throughput overhead | < 5 % vs `git clone` bare                                            |
| **NFR‑3** | Security                  | No code executed outside e2b; no network calls without user approval |
| **NFR‑4** | Reliability               | 99 % uptime during continuous 24 h tests                             |
| **NFR‑5** | Extensibility             | New plugin added with ≤ 50 LOC boilerplate                           |
| **NFR‑6** | Usability                 | Keyboard‑only navigation, colour‑blind friendly theme                |

### 3.3 External Interface Requirements

- **User Interface** – Textual TUI using keybindings: `F1` Help, `Ctrl+A` Chat, `Space` select, `g` = Clone.
- **Hardware** – Standard terminal, 80×24 minimum (responsive).
- **Software** – REST calls to `https://api.github.com`, `http://localhost:11434`, `e2b` daemon.
- **Communications** – HTTPS over TLS 1.3 for GitHub; local Unix socket for e2b.

---

## 4. System Architecture

```mermaid
flowchart TD
    UI[TUI Frontend (Textual)] -->|events| AgentCore
    AgentCore -->|LLM calls| Ollama[(Ollama LLM)]
    AgentCore -->|Tool invocations| Tools[Plugin Tools]
    Tools --> GitHubAPI
    Tools --> e2bSandbox
    Tools --> MCPCLI
    AgentCore --> MemoryDB[(TinyDB / Redis)]
```

### 4.1 Core Packages

- `core.agents.agent_core` – Wraps LangGraph executor, manages memory.
- `core.containers.e2b_wrapper` – Spawns & manages container lifecycle.
- `core.tui.main_tui` – Textual App subclass; layout: left (repo list), right (chat sidebar).
- `core.plugins` – Namespace for dynamic imports; each plugin registers Tools.

### 4.2 Data Flow

1. **User Input** → TUI → Event → AgentCore or Tool.
2. **Agent Response** → Chat Panel & Log.
3. **Tool** (e.g., Git clone) → Execution → Result → AgentCore → Chat/log.
4. **Memory** persists {prompt, response, actions, outcome} pairs.

---

## 5. Security & Sandboxing

- e2b containers enforce FS/network isolation, CPU/RAM limits.
- Web requests whitelisted; unknown domains require user confirmation.
- Token & keys stored via OS keyring or Bitwarden CLI integration.
- All plugin actions are auditable with unique trace IDs.

---

## 6. Installation & Deployment

```bash
pipx install agent-zero  # future published package
ollama run gemma:2b      # start LLM
agent-zero               # launch TUI
```

Optional dev setup:

```bash
git clone https://github.com/cbwinslow/agent-zero
cd agent-zero
make dev  # installs venv, pre‑commit, tests
```

---

## 7. Future Enhancements

1. **GUI/Web Frontend** – Mirror TUI in a web browser via Textual Web.
2. **Vector Memory** – Use a vector DB (Qdrant) to store embeddings of past chats & files.
3. **Voice Interface** – Speak prompts and responses (TTS & STT).
4. **Plugin Marketplace** – Auto‑discover and install community plugins.
5. **Auto‑Update Mechanism** – Self‑patch via Git pull & test inside e2b, then live‑swap.

---

## 8. Appendices

- **A. Directory Tree** – See Section 2.1 layout.
- **B. Keybindings** – Draft cheat‑sheet to be refined during UI stage.
- **C. API Rate Limits** – GitHub 5k req/h per token; handle errors back‑off.

---

*End of SRS v0.1‑draft*

