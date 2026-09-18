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
Virtually **all standard autonomous AI agents and computer-use tools** (including Anthropic Computer Use, GPT-4o Vision agents, OSWorld, OpenClaw, and desktop automation assistants) rely on capturing and streaming full raw screenshots directly into the LLM context at every single interaction step.

In real-world deployment, this creates **two severe bottlenecks**:
1. **Severe Token Bleeding:**  
   Sending a single 1080p or 4K frame to cloud multimodal models (GPT-4o, Claude 3.5 Sonnet, etc.) consumes **1,500 to 2,500 tokens per action**. A routine 40-step form submission or navigation task easily burns **100,000+ tokens within minutes**, quickly exhausting API budgets.
2. **The Infinite Loop Trap (Freeze Blindness):**  
   When an application crashes, freezes, or encounters an unclickable button, vision agents often fail to detect the lack of state progression. They repeatedly capture identical screens and hammer the same coordinates, burning hundreds of dollars in loops before human intervention.

### 💡 How TokenShield-UI Solves This
* **Local Eyes on Your Hardware (Local GPU):** Screenshots **NEVER** leave your machine. A lightweight local vision model (**Microsoft Florence-2-base**, occupying only **~680 MB VRAM** on an NVIDIA RTX GPU) parses screen elements in under 100 milliseconds.
* **Text-Only Delivery to Agents:** Instead of raw image payloads, the agent receives a compact, structured JSON scene graph containing only actionable elements and focus coordinates (**~45 tokens**).
* **Desktop & File Explorer Grounding (Zero Mouse Hijacking & Zero Window Disruption):**
  * **Clicking Desktop Elements:** When an agent needs to click an icon or launch a program from your desktop, traditional tools blindly minimize all your open windows (`Win + D`), interrupting your active workflow and throwing your mouse cursor wildly across the screen. TokenShield-UI uses a combination of virtual desktop peeking and Windows Shell API enumeration (`smart_ui_desktop_items`) to discover shortcuts, app names, and exact screen bounds directly in the background—launching or interacting with them without stealing your mouse focus.
  * **Searching & Locating Documents Inside Folders:** When navigating inside File Explorer or folder directories to find a specific document, Florence-2 uses local dense phrase grounding. Rather than uploading heavy 4K screenshots of your folder view to expensive cloud LLMs, the local model parses filenames, search bars, navigation breadcrumbs, and document icons into clean coordinate bounding boxes. The agent receives a concise, structured answer:
    ```json
    {
      "search_bar": {"center": [1240, 75], "type": "input_field"},
      "target_file": {"label": "financial_report.xlsx", "center": [412, 380], "type": "file_item"}
    }
    ```
    The agent can immediately double-click the document or type into the search bar using **~35 tokens**, without a single pixel leaving your machine.
* **pHash Circuit Breaker:** Calculates the perceptual hash (*pHash*) of the target window. If 3 consecutive actions produce identical perceptual signatures, the circuit breaker trips, halting execution and preventing token burnout.
* **Android TV / TvBox & BlueStacks Native Support:** Detects Cyan/Blue remote focus outlines and generates direct D-Pad navigation sequences (`DPAD_UP`, `DPAD_RIGHT`, `DPAD_CENTER`).
* **Silent Background Execution:** Interacts with BlueStacks and ADB targets in the background without stealing mouse focus or minimizing active user windows.

### 📊 Token & Cost Efficiency Comparison

| Metric | All Standard AI Screen Agents (Raw Screen Captures to LLM) | TokenShield-UI Grounding Layer (Aethelion) |
| :--- | :--- | :--- |
| **Vision Inference** | Cloud Multimodal LLM (Paid API) | **Local GPU (RTX / CUDA - 100% Free)** |
| **Tokens per Action** | ~1,800 - 2,500 Tokens | **~40 - 60 Tokens (Structured JSON)** |
| **50-Step Task Cost** | ~100,000 Tokens (~$1.20) | **~2,500 Tokens (~$0.02)** |
| **Token Reduction** | Baseline (0%) | **~97.5% REDUCTION ACROSS ALL AGENTS 🎯** |
| **Freeze / Loop Protection** | None (Blind loop token burn) | **Active (pHash halts at 3 consecutive identical states)** |

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

#### 5. Desktop & File Explorer Navigation Protocol (`smart_ui_desktop_items` & Local Grounding):
* When requested to open an application or locate a document on the Desktop or inside a folder:
  * **Zero Window Minimizing:** Avoid blindly triggering `Win + D` or minimizing the user's active work windows.
  * **Direct Application Launching:** Query `smart_ui_desktop_items(launch="App Name")` to launch desktop programs directly via background system handlers without moving the mouse pointer.
  * **Document & Folder Search:** When File Explorer or directory windows are active, call `smart_ui_scan(source="desktop")` to receive localized coordinates for search inputs, folder items, and filenames. Use the returned `center` coordinates with `smart_ui_click(coords=[x, y])` to interact directly.

### 📋 How to Integrate This Mandate into Your AI Agent Rules

To ensure an AI agent (or subagent) never reverts to expensive raw screenshots, add this rule block to your environment's rule configuration file:
* **Antigravity**: Add to `~/.gemini/GEMINI.md`
* **Cursor**: Add to `.cursorrules` or Project Rules
* **Windsurf**: Add to `.windsurfrules`
* **Claude Desktop / Custom LLM Agents**: Add to System Prompt / Custom Instructions
* *(Also available as a standalone drop-in file: [`mcp/agent_rules.md`](mcp/agent_rules.md))*

```markdown
## GUI INTERACTION & TOKEN SHIELD MANDATE

When observing or interacting with the host operating system (Windows Desktop), File Explorer, or Android emulators (BlueStacks / TvBox):

- NEVER capture raw full-screen screenshots or load raw display images into multimodal LLM context (via `view_file`, `screenshot`, or `adb screencap`).
- ALWAYS query the local `smart-ui-proxy` MCP server (`smart_ui_scan`, `smart_ui_click`, `smart_ui_desktop_items`) to receive compact, structured JSON scene graphs.
- SOURCE DISAMBIGUATION: When the user refers to their PC, computer screen, desktop, or Windows ('bilgisayarım / ekranım / masaüstüm'), pass `source="desktop"` to `smart_ui_scan`. NEVER substitute BlueStacks or ADB when the user asks about their PC screen. When the user refers to BlueStacks, Android, TvBox, or mobile games, pass `source="bluestacks"`.
- If `CIRCUIT_BREAKER_TRIGGERED` is returned, halt actions immediately to prevent token burnout on frozen or unresponsive interfaces.

### RECOVERY & LOOP-PREVENTION PROTOCOL:
1. **Max Retry Threshold (Hard Cap = 2):**
   If `smart-ui-proxy` returns an error, fails to detect the target element, or the action does not alter the screen state, the agent is permitted a MAXIMUM of 2 consecutive attempts. The agent MUST NOT continuously re-try in an autonomous loop.
2. **Reset Loop Prohibition:**
   The agent MUST NEVER call `smart_ui_reset()` in an automated loop to bypass the circuit breaker. `smart_ui_reset()` may only be invoked ONCE after diagnosing the failure cause.
3. **Graceful Fallback & User Escalation:**
   If local grounding fails after 2 attempts (e.g. local Python engine crash, unrecognized UI state, or connection loss):
   - Immediately HALT further autonomous actions.
   - Mark task state as `BLOCKED: LOCAL_GROUNDING_FAILED`.
   - Report the exact failure to the user and request manual guidance.
   - Only take a single emergency fallback screenshot if explicitly approved by the user.
```

---

## 📁 Repository Structure

`
TokenShield-UI/
├── engine.py              # Core perception engine (Florence-2, OpenCV, Cyan focus tracker)
├── fallback_handler.py    # Perceptual hash tracker, fallback UI parser & Circuit Breaker
├── server.py              # FastMCP JSON-RPC server endpoint (smart_ui_scan, click, reset)
├── agent_ui_tool.py       # CLI benchmarking & testing harness
├── toggle_shield.py       # Programmatic on/off configuration switch
├── toggle_shield.bat      # Windows one-click toggle launcher
├── mcp/                   # MCP schemas, directives, and configuration templates
│   ├── instructions.md
│   ├── agent_rules.md
│   ├── mcp_config.example.json
│   ├── smart_ui_scan.json
│   ├── smart_ui_click.json
│   ├── smart_ui_desktop_items.json
│   └── smart_ui_reset.json
├── requirements.txt       # Python package dependencies
├── llms.txt               # Machine-readable context for AI agents
├── .gitignore             # Git ignore specification
├── LICENSE                # MIT License
└── README.md              # Dual-audience technical documentation
`

---

## 📄 License & Attribution

* **Author:** Aethelion
* **License:** Licensed under the [MIT License](LICENSE). You are free to use, modify, distribute, and integrate this software in commercial and private projects.
