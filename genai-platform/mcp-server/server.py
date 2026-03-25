import os
from mcp.server.fastmcp import FastMCP
from kubernetes import client, config

# Initialize FastMCP Server
mcp = FastMCP("Kubernetes Info Server")

# Load cluster config once at startup
try:
    # This works when running inside a Pod
    config.load_incluster_config()
except config.ConfigException:
    # Fallback to local kubeconfig for local testing outside the cluster
    config.load_kube_config()

v1_api = client.CoreV1Api()

@mcp.tool()
def get_cluster_nodes() -> str:
    """Retrieve a list of all nodes in the Kubernetes cluster."""
    try:
        nodes = v1_api.list_node()
        node_names = [node.metadata.name for node in nodes.items]
        return f"Cluster has {len(node_names)} nodes: {', '.join(node_names)}"
    except Exception as e:
        return f"Error listing nodes: {str(e)}"

@mcp.tool()
def get_namespaces() -> str:
    """Retrieve a list of all namespaces in the Kubernetes cluster."""
    try:
        namespaces = v1_api.list_namespace()
        ns_names = [ns.metadata.name for ns in namespaces.items]
        return f"Cluster has {len(ns_names)} namespaces: {', '.join(ns_names)}"
    except Exception as e:
        return f"Error listing namespaces: {str(e)}"

@mcp.tool()
def get_pods_in_namespace(namespace: str = "default") -> str:
    """Retrieve a list of all running pods in a specific namespace.
    
    Args:
        namespace: The Kubernetes namespace to inspect.
    """
    try:
        pods = v1_api.list_namespaced_pod(namespace)
        pod_details = [f"{p.metadata.name} (Status: {p.status.phase})" for p in pods.items]
        if not pod_details:
            return f"No pods found in namespace '{namespace}'"
        return f"Pods in '{namespace}':\n" + "\n".join(pod_details)
    except Exception as e:
        return f"Error listing pods in namespace '{namespace}': {str(e)}"

if __name__ == "__main__":
    import sys
    # FastMCP reads these env vars for SSE transport
    print("Starting K8s MCP Server on 0.0.0.0:8000...", file=sys.stderr)
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
