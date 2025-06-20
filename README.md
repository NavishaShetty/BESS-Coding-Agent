# BESS Coding Agent

*The **BESS Coding Agent Project** is designed to assist with analyzing Day-Ahead Market (DAM) prices and optimize trading in the energy market with \battery‑energy‑storage system*

---

<div align="center">
  <img src="https://img.shields.io/badge/Built%20with-SmolAgents-blue" alt="SmolAgents" />
  <img src="https://img.shields.io/badge/Telemetry-Arize&nbsp;Phoenix-ff69b4" alt="Phoenix" />
</div>

## ✨ What is it?

**BESS Coding Agent** is an end‑to‑end reference project that shows how an LLM can:

1. **Analyse Day‑Ahead‑Market (DAM) prices** for energy market.
2. **Recommend optimal charge / discharge windows** for a battery‑energy‑storage system (BESS).
3. **Simulate round‑trip profits** under different efficiencies and capacities.
4. **Expose a chat UI** (Gradio) so traders can ask ad‑hoc questions.
5. **Log every step** (agent decisions, tool calls, LLM traces) to a Phoenix dashboard for evaluation.

All of that is wrapped in a clean Python package that you can pip‑install, test, and extend.

---

## 🚀 Quick start

### 1. Install

```bash
# clone + create env (Python ≥ 3.11)
git clone https://github.com/yourusername/navishashetty-bess-coding-agent.git

cd BESS-Coding-Agent

# activate virtual env
python -m venv .venv && source .venv/bin/activate

# install package in editable mode
pip install -e .  
```

### 2. Configure secrets

Create a **.env** file at repo root (refer `.env-example`) and add your API keys for any LLM inference platform:

```
OPENROUTER_API_KEY=abc‑...
```

```bash
export OPENROUTER_API_KEY=
```

### 3. See it in action with monitoring UI + chat UI:

```bash
# Launch Gradio chat UI and Phoenix telemetry dashboard
python agent_in_action.py

# chat UI → browser: http://127.0.0.1:7860/ 
# logs → Phoenix: http://localhost:6006/ 
```

### 4. Run a one‑off task

```bash
python examples/agent.py 
```

### 5. Evaluate tool use across many prompts

```bash
python evaluation.py
# writes evaluation_results.csv to evaluate agent performance  
```

### 6. Example Usage 

```bash
# For Chat UI + Phoenix logs
python examples/agent_ui.py  
# For task that runs only in terminal + Phoenix logs
python examples/agent.py
```

### 7. Data refresh

```bash
# fetch data from Modo energy API 
python energy_agent/data/data_fetcher.py  
```

Point your tools at the new data file to use latest data.

### 8. Testing

```bash
# run test cases
pytest -q 
```

---

## 📖 Features & architecture

| Layer         | File / Module                                               | What it does                                                                                                                            |
| ------------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Agent**     | `energy_agent/energy_agent.py`                              | Builds a `smolagents.CodeAgent` with an OpenAI‑compatible model & all tools.                                                            |
| **Tools**     | `energy_agent/tools.py`                                     | Pure‑Python functions decorated with `@tool` – load price CSV, find extremes, spread, charge/discharge windows, profit calculator, etc. |
| **Data**      | `energy_agent/data/…`                                       | CSV sample + `data_fetcher.py` that pulls fresh DAM prices from Modo Energy and saves them.                                             |
| **Telemetry** | Phoenix launch + `openinference-instrumentation-smolagents` | Every span (LLM, tool call, etc.) streams to a local collector you can inspect.                                                         |
| **UI**        | Gradio (chat)                                               | One click to share with the desk.                                                                                                       |

---

## 📂 Repo layout

```
navishashetty-bess-coding-agent/
├── agent_in_action.py      # start UI + Phoenix
├── evaluation.py           # Evaluating agent
├── examples/               # minimal one‑off runners
├── energy_agent/           
|   ├── energy_agent.py     # package code
│   ├── tools.py            # all @tool‑decorated helpers
│   ├── data/               # CSV data + fetcher code
│   └── config.py           # configuration details
├── tests/                  # pytest unit tests
└── README.md
```

---
