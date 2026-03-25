# MCP Kubernetes Python POC

This is a simple MCP-style service that interacts with a Kubernetes cluster (Kind) and exposes APIs. Now with multi-cluster support!

## Features
- List Pods (from a specific cluster or all clusters)
- Get Pod Logs (from a specific cluster)
- List Nodes (from a specific cluster)
- List Services (from a specific cluster)
- List available clusters

## Prerequisites
- Python 3.9+
- Kind Cluster running
- kubectl configured

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload --port 8000
```

## Multi-Cluster Usage

This MCP server can connect to multiple Kubernetes clusters.

1.  **Add Clusters:**
    - Create a `kubeconfigs` directory inside the `genai-platform/mcp_k8s_poc` directory.
    - For each cluster you want to manage, add its kubeconfig file to the `kubeconfigs` directory.
    - The name of the file (without the `.yaml` or `.yml` extension) will be used as the `cluster_id`.
    - For example: `kubeconfigs/my-gke-cluster.yaml`, `kubeconfigs/eks-cluster.yml`.

2.  **List Clusters:**
    - To see the list of available clusters, use the `/clusters` endpoint:
      ```bash
      curl http://localhost:8000/clusters
      ```
    - The `default` cluster is the one configured in your local `~/.kube/config` file.

3.  **Target a Specific Cluster:**
    - Use the `cluster_id` query parameter to specify which cluster you want to interact with.
    - If you don't provide a `cluster_id`, it will default to the `default` cluster.

## Test APIs

### List Clusters
```bash
curl http://localhost:8000/clusters
```

### List Pods
- From the default cluster:
  ```bash
  curl http://localhost:8000/pods
  ```
- From a specific cluster:
  ```bash
  curl "http://localhost:8000/pods?cluster_id=<cluster-id>"
  ```
- From a specific namespace in a specific cluster:
  ```bash
  curl "http://localhost:8000/pods?cluster_id=<cluster-id>&namespace=<namespace>"
  ```

### Get Pod Logs
```bash
curl "http://localhost:8000/pod_logs?cluster_id=<cluster-id>&name=<pod-name>&namespace=<namespace>"
```

### List Nodes
```bash
curl "http://localhost:8000/nodes?cluster_id=<cluster-id>"
```

## VS Code Usage

1. Open folder in VS Code
2. Install Python extension
3. Run terminal:
```bash
uvicorn main:app --reload
```
