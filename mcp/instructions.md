# Smart UI Proxy & Token Shield Best Practices

When interacting with the user's desktop, BlueStacks, Android TV, or any GUI application:

1. **Token Conservation Priority**:
   - NEVER invoke raw screenshot tools (`windows-desktop-control:screenshot`) directly unless explicitly requested as an emergency fallback.
   - Always call `smart_ui_scan` to observe the current UI state. It runs local computer vision on the user's RTX 2060 GPU and returns a compact (<60 tokens) JSON scene graph.

2. **D-Pad vs Tap Action**:
   - In Android TV / TvBox contexts where D-Pad focus is visible (e.g. Cyan border), use remote control navigation (`smart_ui_click` with `method="dpad"` and `dpad_steps`).
   - For direct desktop interaction, use `smart_ui_click` with `method="tap"`.

3. **Loop Prevention & Circuit Breakers**:
   - The middleware tracks screen perceptual hash (pHash). If the screen does not change after 3 consecutive actions, it automatically halts with `CIRCUIT_BREAKER_TRIGGERED` to prevent burning tokens in an infinite loop.
   - If tripped, analyze why the UI did not respond before calling `smart_ui_reset`.
