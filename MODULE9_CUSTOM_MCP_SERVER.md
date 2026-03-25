# Module 9: Building and Deploying a Custom MCP Server

The Model Context Protocol (MCP) securely exposes data and tools to AI assistants. While you can run an MCP server locally to poke at your Kubernetes cluster (as seen in Module 8), deploying an MCP Server *inside* the cluster lets AI agents safely interact with your environment directly.

In this module, we will build a custom Python MCP server that exposes Kubernetes cluster information (like Nodes, Namespaces, and Pods) to AI.

## 1. Reviewing the Code

Navigate to the `genai-platform/mcp-server/` folder in the repository.

1. **`server.py`**: This uses the `mcp` SDK to create three AI tools:
   - `get_cluster_nodes`
   - `get_namespaces`
   - `get_pods_in_namespace`
2. **`Dockerfile`**: Packages the script and the Kubernetes python client into an image.
3. **`k8s/rbac.yaml`**: Very importantly, your MCP Server acts as an AI proxy, so it needs explicit Kubernetes permissions. This file restricts the server to only `get` and `list` operations, making it safe for AI integration.

## 2. Build the Docker Image

From the `genai-platform/mcp-server` directory, build the image:

```bash
cd /home/arjun/genai-k8s/genai-platform/mcp-server
docker build -t arjunachari12/mcp-k8s-server:1.0.0 .
```

If you are using KIND, load the image into the cluster directly so it doesn't try to pull from the internet:
```bash
kind load docker-image arjunachari12/mcp-k8s-server:1.0.0
```

## 3. Deploy the MCP Server to Kubernetes

Apply the Role-Based Access Control configuration to grant the server read permissions:

```bash
kubectl apply -f k8s/rbac.yaml
```

Deploy the server itself:

```bash
kubectl apply -f k8s/deployment.yaml
```

Verify that it's running:
```bash
kubectl get pods -n genai -l app=mcp-server
```

## 4. Test the Deployed Server

Because this MCP server communicates via Server-Sent Events (SSE) over HTTP, you can verify it locally by forwarding the port:

```bash
kubectl port-forward -n genai svc/mcp-server-svc 8000:80
```

With the port-forward running, your server is accessible at `http://localhost:8000`. If you configure an AI client (like Claude Desktop or Cursor) pointing to `http://localhost:8000/sse`, it will be able to invoke the cluster tools!

### Manual CLI Test

You can manually trigger an MCP SSE endpoint if you have a client or `curl`. Since the SSE protocol negotiates a connection first, let's verify the server is up:

```bash
curl http://localhost:8000/
```
(Expected: The FastMCP server acknowledges it's running or provides the SSE connection stream).

## Summary
You wrote a custom python toolkit, containerized it, gave it the minimum required RBAC permissions, and deployed it. You can extend this template by adding any `@mcp.tool()` function you want to expose specialized actions (e.g., triggering a backup, scaling a deployment) directly to your AI agents!
