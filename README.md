# 🛡️ TokenShield-UI: Smart UI Proxy & Grounding Middleware
### *By Aethelion*

> **A local GPU-accelerated UI grounding middleware, D-Pad navigation engine, and perceptual circuit breaker designed to prevent autonomous AI agents from burning excessive tokens on raw screen captures.**

[![GitHub Repo](https://img.shields.io/badge/GitHub-TokenShield--UI-181717?logo=github)](https://github.com/aethelondev-stack/TokenShield-UI)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-CUDA%20Ready-red.svg)](https://pytorch.org/)
[![Model](https://img.shields.io/badge/Model-Microsoft%20Florence--2-green.svg)](https://huggingface.co/microsoft/Florence-2-base)
[![MCP](https://img.shields.io/badge/Protocol-FastMCP%20Standard-purple.svg)]()
[![Token Savings](https://img.shields.io/badge/Token%20Savings-%20~97.5%25-brightgreen.svg)]()

---

> ⚠️ **This Documentation Features Dual-Audience Architecture:**
> * 👤 **Section 1: If a Human Developer is reading** (System architecture, token crisis resolution, setup, and usage guide).
> * 🤖 **Section 2: If an AI Agent / LLM is reading** (Operational system directives, Model Context Protocol integration, error recovery, and decision protocol).

---

## 👤 SECTION 1: IF A HUMAN IS READING THIS

### 📌 The Problem: Why Did I Build This?
Modern autonomous AI agents (**OpenClaw, Anthropic Computer Use, OSWorld, Vision-based GUI Agents**) capture full-screen screenshots at every single interaction step.

In real-world deployment, this creates **two severe bottlenecks**:
1. **Severe Token Bleeding:**  
   Sending a single 1080p or 4K frame to cloud multimodal models (GPT-4o, Claude 3.5 Sonnet, etc.) consumes **1,500 to 2,500 tokens per action**. A routine 40-step form submission or navigation task easily burns **100,000+ tokens within minutes**, quickly exhausting API budgets.
2. **The Infinite Loop Trap (Freeze Blindness):**  
   When an application crashes, freezes, or encounters an unclickable button, vision agents often fail to detect the lack of state progression. They repeatedly capture identical screens and hammer the same coordinates, burning hundreds of dollars in loops before human intervention.

### 💡 How TokenShield-UI Solves This
* **Local Eyes on Your Hardware (Local GPU):** Screenshots **NEVER** leave your machine. A lightweight local vision model (**Microsoft Florence-2-base**, occupying only **~680 MB VRAM** on an NVIDIA RTX GPU) parses screen elements in under 100 milliseconds.
* **Text-Only Delivery to Agents:** Instead of raw image payloads, the agent receives a compact, structured JSON scene graph containing only actionable elements and focus coordinates (**~45 tokens**).
* **pHash Circuit Breaker:** Calculates the perceptual hash (*pHash*) of the target window. If 3 consecutive actions produce identical perceptual signatures, the circuit breaker trips, halting execution and preventing token burnout.
* **Android TV / TvBox & BlueStacks Native Support:** Detects Cyan/Blue remote focus outlines and generates direct D-Pad navigation sequences (DPAD_UP, DPAD_RIGHT, DPAD_CENTER).
* **Silent Background Execution:** Interacts with BlueStacks and ADB targets in the background without stealing mouse focus or minimizing active user windows.

### 📊 Token & Cost Efficiency Comparison

| Metric | Traditional Vision Agents (OpenClaw, etc.) | TokenShield-UI (Aethelion) |
| :--- | :--- | :--- |
| **Vision Inference** | Cloud LLM (Paid API) | **Local GPU (RTX / CUDA - 100% Free)** |
| **Tokens per Action** | ~1,800 - 2,500 Tokens | **~40 - 60 Tokens (Structured JSON)** |
| **50-Step Task Cost** | ~100,000 Tokens (~.20) | **~2,500 Tokens (~.02)** |
| **Token Reduction** | - | **~97.5% SAVINGS 🎯** |
| **Freeze / Loop Protection** | None (Loops indefinitely) | **Hardware-Level (pHash halts at 3 consecutive identical states)** |

---

### 🚀 Human Developer Quickstart

#### 1. Clone the Repository & Install Dependencies
`ash
git clone https://github.com/aethelondev-stack/TokenShield-UI.git
cd TokenShield-UI

# Install dependencies (PyTorch with CUDA recommended)
pip install -r requirements.txt
`

#### 2. One-Click Toggle Switch (Gaming & Privacy Mode)
Need to play games or reclaim VRAM instantly?
* Double-click **	oggle_shield.bat** in the project directory to toggle the middleware on/off.

#### 3. Connect via MCP (Cursor, Antigravity, Claude Desktop, Windsurf)
Add the server definition to your tool's MCP configuration file (mcp_config.json or claude_desktop_config.json):

`json
{
  "mcpServers": {
    "smart-ui-proxy": {
      "command": "python",
      "args": [
        "C:\\PATH_TO\\TokenShield-UI\\server.py"
      ],
      "env": {}
    }
  }
}
`

---

## 🤖 SECTION 2: IF AN AI AGENT IS READING THIS
*(FOR AUTONOMOUS AI AGENTS, CURSOR AGENT, ANTIGRAVITY, CLAUDE DESKTOP, WINDSURF)*

`yaml
agent_instruction_type: system_guidelines
target_agent: LLM / Autonomous Agent / Coding Assistant
middleware_name: TokenShield-UI
protocol: Model Context Protocol (MCP)
primary_objective: Zero-token-waste GUI perception, background execution, loop prevention
`

### 🎯 Operational Directives

When instructed to interact with the host operating system (Windows Desktop) or an Android emulator / device (BlueStacks, Android TV):

#### 1. DO NOT Request Raw Screenshots:
* Do not call screenshot or 	ake_screenshot tools.
* These tools clutter your context window with 2,000+ token images and deplete user API credits.
* Always query **smart_ui_scan** instead.

#### 2. Parse Structured Screen Grounding (smart_ui_scan):
* Calling smart_ui_scan(source="bluestacks"|"desktop") returns structured coordinates:
  `json
  {
    "screen_dimensions": [1920, 1080],
    "active_focus": {
      "box": [47, 540, 285, 883],
      "center": [166, 711],
      "status": "Cyan Highlight Verified"
    },
    "cards": [
      {"box": [624, 98, 753, 310], "center": [688, 204]},
      {"box": [790, 98, 1013, 368], "center": [901, 233]}
    ]
  }
  `
* Consume these target centers directly in your decision pipeline.

#### 3. Action Protocol (smart_ui_click):
* **D-Pad / TV Navigation:** When ctive_focus is present, navigate by setting method="dpad" with calculated dpad_steps (e.g., ["DPAD_UP", "DPAD_RIGHT", "DPAD_CENTER"]).
* **Direct Pointer Interaction:** For touch or mouse targets, supply method="tap" and coords=[x, y].

#### 4. Circuit Breaker Protocol (CIRCUIT_BREAKER):
* If the tool responds with:
  `json
  {"status": "CIRCUIT_BREAKER_TRIGGERED", "error": "Screen state remained identical across 3 consecutive actions..."}
  `
  * **DO NOT attempt clicking the same target again.**
  * Halt your loop immediately.
  * Inform the user that the target application appears frozen or unresponsive.
  * Await user confirmation before invoking smart_ui_reset().

#### 5. Background Application Launching (smart_ui_desktop_items):
* When requested to open an application from the desktop, avoid minimizing foreground work.
* Query smart_ui_desktop_items(launch="App Name") to launch programs directly via system handlers without displacing active windows.

---

## 📁 Repository Structure

`
TokenShield-UI/
├── engine.py              # Core perception engine (Florence-2, OpenCV, Cyan focus tracker)
├── fallback_handler.py    # Perceptual hash tracker, fallback UI parser & Circuit Breaker
├── agent_ui_tool.py       # CLI benchmarking & testing harness
├── server.py              # FastMCP JSON-RPC server endpoint
├── toggle_shield.py       # Programmatic on/off configuration switch
├── toggle_shield.bat      # Windows one-click toggle launcher
├── requirements.txt       # Python package dependencies
├── .gitignore             # Git ignore specification
├── LICENSE                # MIT License
└── README.md              # Dual-audience technical documentation
`

---

## 📄 License & Attribution

* **Author:** Aethelion
* **License:** Licensed under the [MIT License](LICENSE). You are free to use, modify, distribute, and integrate this software in commercial and private projects.
