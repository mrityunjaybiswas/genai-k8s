import requests

BASE_URL = "http://localhost:8000"

def list_tools():
    return requests.get(f"{BASE_URL}/tools").json()

def call_tool(tool, args):
    return requests.post(
        f"{BASE_URL}/call",
        json={"tool": tool, "arguments": args}
    ).json()

if __name__ == "__main__":
    print("Tools:", list_tools())
    print("Pods:", call_tool("list_pods", {}))
