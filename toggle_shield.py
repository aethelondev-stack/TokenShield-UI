import json
import sys
import os

CONFIG_PATH = os.path.expanduser("~/.gemini/config/mcp_config.json")
SERVER_PATH = os.path.expanduser("~/.gemini/antigravity/mcp/smart-ui-proxy/server.py")

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
        status = "DISABLED"
    elif "_disabled_smart-ui-proxy" in servers:
        # Enable it
        servers["smart-ui-proxy"] = servers.pop("_disabled_smart-ui-proxy")
        status = "ENABLED"
    else:
        # Add fresh
        servers["smart-ui-proxy"] = {
            "command": "python",
            "args": [SERVER_PATH],
            "env": {}
        }
        status = "ENABLED"

    data["mcpServers"] = servers
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n==========================================")
    print(f"  TokenShield (Smart UI Proxy): {status}")
    print(f"==========================================\n")

if __name__ == "__main__":
    toggle()
