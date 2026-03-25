# MCP Server Design: From POC to Multi-Cluster

This document outlines a plan to evolve the current proof-of-concept (POC) into a basic multi-cluster MCP server.

## 1. Goal

The goal is to extend the existing single-cluster API server to be able to connect to and manage resources on multiple Kubernetes clusters.

## 2. Architecture

The MCP server will be a central service that can communicate with a fleet of Kubernetes clusters.

- **Cluster Configuration:** The server will need a mechanism to store and manage the connection details (kubeconfig files) for multiple clusters.
- **API:** The API will be extended to be "cluster-aware", allowing users to specify which cluster they want to interact with.

## 3. Proposed API Changes

### 3.1. List Available Clusters

A new endpoint will be created to list the clusters that the MCP server can manage.

- **Endpoint:** `GET /clusters`
- **Response:**
  ```json
  [
    {
      "id": "cluster1",
      "name": "cluster1"
    },
    {
      "id": "cluster2",
      "name": "cluster2"
    }
  ]
  ```

### 3.2. Cluster-Specific Resource Operations

Existing endpoints will be modified to accept a `cluster_id` query parameter to target a specific cluster.

- `GET /pods?cluster_id=<cluster-id>&namespace=<namespace>`
- `GET /pod_logs?cluster_id=<cluster-id>&name=<pod-name>&namespace=<namespace>`
- `GET /nodes?cluster_id=<cluster-id>`
- `GET /services?cluster_id=<cluster-id>&namespace=<namespace>`

If `cluster_id` is not provided, the server could either default to a predefined "default" cluster or return an error. For this design, we will assume it will default to the local kubeconfig context.

## 4. Implementation Plan

### 4.1. Cluster Configuration Management

- We will create a `kubeconfigs` directory within the `genai-platform/mcp_k8s_poc` directory.
- Each file in this directory will be a kubeconfig file for a specific Kubernetes cluster. The filename (without the extension) will be used as the `cluster_id`.
- For example: `kubeconfigs/cluster1.yaml`, `kubeconfigs/cluster2.yaml`.

### 4.2. Code Implementation

1.  **Create a `ClusterManager`:**
    - A Python class `ClusterManager` will be created.
    - This class will be responsible for:
      - Scanning the `kubeconfigs` directory at startup.
      - Loading each kubeconfig file and creating a Kubernetes API client for it.
      - Storing the clients in a dictionary, keyed by `cluster_id`.
      - Providing a method to get a client for a given `cluster_id`.

2.  **Update `main.py`:**
    - Instantiate the `ClusterManager` when the application starts.
    - Implement the `GET /clusters` endpoint to return the list of cluster IDs from the `ClusterManager`.
    - Modify the existing API endpoint functions (`list_pods`, `get_pod_logs`, etc.) to:
      - Accept an optional `cluster_id` parameter.
      - Use the `ClusterManager` to get the appropriate Kubernetes client.
      - If `cluster_id` is not provided, it will use the default `kubeconfig` from `~/.kube/config`.

### 4.3. Testing

- To test the multi-cluster functionality, we can create multiple `kind` clusters and save their kubeconfig files into the `kubeconfigs` directory.
- We can then use `curl` to test the new cluster-aware API endpoints.
