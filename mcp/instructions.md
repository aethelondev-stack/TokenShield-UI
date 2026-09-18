# Smart UI Proxy & Token Shield Best Practices

When interacting with the user's desktop, BlueStacks, Android TV, or any GUI application:

1. **Token Conservation Priority**:
   - NEVER invoke raw screenshot tools (windows-desktop-control:screenshot, db screencap, or iew_file on images) directly.
   - Always call smart_ui_scan to observe the current UI state. It runs local computer vision on the user's RTX GPU and returns a compact (<50 tokens) structured JSON scene graph.

2. **D-Pad vs Tap Action**:
   - In Android TV / TvBox contexts where D-Pad focus is visible (e.g. Cyan border), use remote control navigation (smart_ui_click with method="dpad" and dpad_steps).
   - For direct desktop interaction, use smart_ui_click with method="tap" and coords=[x, y].
   - For launching desktop apps, use smart_ui_desktop_items(launch="App Name") directly without displacing windows.

3. **Loop Prevention & Circuit Breakers**:
   - The middleware tracks screen perceptual hash (pHash). If the screen does not change after 3 consecutive actions, it automatically halts with CIRCUIT_BREAKER_TRIGGERED to prevent burning tokens in an infinite loop.
   - If tripped, analyze why the UI did not respond before calling smart_ui_reset().

4. **Recovery & Loop-Prevention Protocol**:
   - **Max 2 Retries**: If local grounding fails or coordinates do not change the UI state, attempt at most 2 times.
   - **No Automated Reset Loops**: Do NOT call smart_ui_reset() in an autonomous loop to bypass the circuit breaker.
   - **Graceful Fallback**: After 2 failures, HALT immediately, set status to BLOCKED: LOCAL_GROUNDING_FAILED, and ask the user for manual guidance.
