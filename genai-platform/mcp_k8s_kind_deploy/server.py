from fastapi import FastAPI
from pydantic import BaseModel
from kubernetes import client, config

app = FastAPI(title="K8s MCP Server")

# In-cluster or local config
try:
    config.load_incluster_config()
except:
    config.load_kube_config()

v1 = client.CoreV1Api()

class MCPRequest(BaseModel):
    tool: str
    arguments: dict = {}

def list_pods(namespace: str = "default"):
    pods = v1.list_namespaced_pod(namespace)
    return [p.metadata.name for p in pods.items]

def get_pod_logs(name: str, namespace: str = "default"):
    return v1.read_namespaced_pod_log(name=name, namespace=namespace)

def list_nodes():
    nodes = v1.list_node()
    return [n.metadata.name for n in nodes.items]

TOOLS = {
    "list_pods": {
        "description": "List all pods in a namespace",
        "input_schema": {
            "type": "object",
            "properties": {
                "namespace": {"type": "string", "default": "default"}
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
        "input_schema": {"type": "object", "properties": {}},
        "function": list_nodes
    }
}

@app.get("/tools")
def tools():
    return [{"name": k, "description": v["description"], "input_schema": v["input_schema"]} for k,v in TOOLS.items()]

@app.post("/call")
def call(req: MCPRequest):
    func = TOOLS.get(req.tool, {}).get("function")
    if not func:
        return {"error": "Unknown tool"}
    try:
        return {"result": func(**req.arguments)}
    except Exception as e:
        return {"error": str(e)}
