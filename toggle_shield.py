import json
import sys
import os

CONFIG_PATH = r"C:\Users\Korhan\.gemini\config\mcp_config.json"

def toggle():
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: {CONFIG_PATH} not found!")
        return

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    servers = data.get("mcpServers", {})
    
    # Check if smart-ui-proxy is active
    if "smart-ui-proxy" in servers:
        # Disable it (save to backup key)
        servers["_disabled_smart-ui-proxy"] = servers.pop("smart-ui-proxy")
        status = "KAPATILDI (DISABLED)"
    elif "_disabled_smart-ui-proxy" in servers:
        # Enable it
        servers["smart-ui-proxy"] = servers.pop("_disabled_smart-ui-proxy")
        status = "ACILDI (ENABLED)"
    else:
        # Add fresh
        servers["smart-ui-proxy"] = {
            "command": "python",
            "args": [r"C:\Users\Korhan\.gemini\antigravity\mcp\smart-ui-proxy\server.py"],
            "env": {}
        }
        status = "ACILDI (ENABLED)"

    data["mcpServers"] = servers
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n==========================================")
    print(f"  TokenShield (Smart UI Proxy): {status}")
    print(f"==========================================\n")

if __name__ == "__main__":
    toggle()
