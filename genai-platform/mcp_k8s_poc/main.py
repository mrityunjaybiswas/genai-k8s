from fastapi import FastAPI
from typing import List, Optional

from cluster_manager import ClusterManager

app = FastAPI()

cluster_manager = ClusterManager()

@app.get("/clusters")
def list_clusters():
    return cluster_manager.list_clusters()

@app.get("/pods")
def list_pods(cluster_id: str = "default", namespace: Optional[str] = None):
    v1 = cluster_manager.get_client(cluster_id)
    if not v1:
        return {"error": f"Cluster '{cluster_id}' not found"}
    if namespace:
        pods = v1.list_namespaced_pod(namespace)
    else:
        pods = v1.list_pod_for_all_namespaces()
    return [p.metadata.name for p in pods.items]

@app.get("/pod_logs")
def get_pod_logs(name: str, cluster_id: str = "default", namespace: str = "default"):
    v1 = cluster_manager.get_client(cluster_id)
    if not v1:
        return {"error": f"Cluster '{cluster_id}' not found"}
    return v1.read_namespaced_pod_log(name=name, namespace=namespace)

@app.get("/nodes")
def list_nodes(cluster_id: str = "default"):
    v1 = cluster_manager.get_client(cluster_id)
    if not v1:
        return {"error": f"Cluster '{cluster_id}' not found"}
    nodes = v1.list_node()
    return [n.metadata.name for n in nodes.items]

@app.get("/services")
def list_services(cluster_id: str = "default", namespace: str = "default"):
    v1 = cluster_manager.get_client(cluster_id)
    if not v1:
        return {"error": f"Cluster '{cluster_id}' not found"}
    services = v1.list_namespaced_service(namespace)
    return [s.metadata.name for s in services.items]
