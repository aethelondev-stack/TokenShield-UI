# Universal Agent Rule: GUI Interaction & Token Shield Mandate

> Copy and paste this rule into your agent configuration (GEMINI.md, .cursorrules, .windsurfrules, or Claude System Prompt) to enforce zero-token GUI interactions.

## GUI INTERACTION & TOKEN SHIELD MANDATE

When observing or interacting with the host operating system (Windows Desktop), File Explorer, or Android emulators (BlueStacks / TvBox):

- NEVER capture raw full-screen screenshots or load raw display images into multimodal LLM context (via view_file, screenshot, or adb screencap).
- ALWAYS query the local smart-ui-proxy MCP server (smart_ui_scan, smart_ui_click, smart_ui_desktop_items) to receive compact, structured JSON scene graphs.
- If CIRCUIT_BREAKER_TRIGGERED is returned, halt actions immediately to prevent token burnout on frozen or unresponsive interfaces.

### RECOVERY & LOOP-PREVENTION PROTOCOL:
1. Max Retry Threshold (Hard Cap = 2):
   If smart-ui-proxy returns an error, fails to detect the target element, or the action does not alter the screen state, the agent is permitted a MAXIMUM of 2 consecutive attempts. The agent MUST NOT continuously re-try in an autonomous loop.
2. Reset Loop Prohibition:
   The agent MUST NEVER call smart_ui_reset() in an automated loop to bypass the circuit breaker. smart_ui_reset() may only be invoked ONCE after diagnosing the failure cause.
3. Graceful Fallback & User Escalation:
   If local grounding fails after 2 attempts (e.g. local Python engine crash, unrecognized UI state, or connection loss):
   - Immediately HALT further autonomous actions.
   - Mark task state as BLOCKED: LOCAL_GROUNDING_FAILED.
   - Report the exact failure to the user and request manual guidance.
   - Only take a single emergency fallback screenshot if explicitly approved by the user.
