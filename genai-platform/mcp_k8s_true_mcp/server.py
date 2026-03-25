from fastapi import FastAPI
from pydantic import BaseModel
from kubernetes import client, config

app = FastAPI(title="K8s MCP Server")

config.load_kube_config()
v1 = client.CoreV1Api()

class MCPRequest(BaseModel):
    tool: str
    arguments: dict = {}

# ---- Tool Implementations ----
def list_pods(namespace: str = None):
    if namespace:
        pods = v1.list_namespaced_pod(namespace)
    else:
        pods = v1.list_pod_for_all_namespaces()
    return [p.metadata.name for p in pods.items]

def get_pod_logs(name: str, namespace: str = "default"):
    return v1.read_namespaced_pod_log(name=name, namespace=namespace)

def list_nodes():
    nodes = v1.list_node()
    return [n.metadata.name for n in nodes.items]

# ---- Tool Registry (MCP Standard) ----
TOOLS = {
    "list_pods": {
        "description": "List pods. If namespace is provided, lists pods in that namespace. Otherwise, lists pods in all namespaces.",
        "input_schema": {
            "type": "object",
            "properties": {
                "namespace": {"type": "string"}
            }
        },
        "function": list_pods
    },
    "get_pod_logs": {
        "description": "Get logs of a pod",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "namespace": {"type": "string", "default": "default"}
            },
            "required": ["name"]
        },
        "function": get_pod_logs
    },
    "list_nodes": {
        "description": "List cluster nodes",
        "input_schema": {
            "type": "object",
            "properties": {}
        },
        "function": list_nodes
    }
}

# ---- MCP Endpoints ----
@app.get("/tools")
def get_tools():
    return [
        {
            "name": name,
            "description": tool["description"],
            "input_schema": tool["input_schema"]
        }
        for name, tool in TOOLS.items()
    ]

@app.post("/call")
def call_tool(req: MCPRequest):
    if req.tool not in TOOLS:
        return {"error": f"Unknown tool: {req.tool}"}

    try:
        func = TOOLS[req.tool]["function"]
        result = func(**req.arguments)
        return {
            "tool": req.tool,
            "result": result
        }
    except Exception as e:
        return {"error": str(e)}
