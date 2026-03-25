# True MCP Kubernetes Server (Python)

This project implements a **true MCP-style server**:
- Tool discovery (`/tools`)
- Tool execution (`/call`)
- JSON schema-based tools

## Setup

```bash
pip install -r requirements.txt
```

## Run Server

```bash
uvicorn server:app --reload --port 8000
```

## Discover Tools

```bash
curl http://localhost:8000/tools
```

## Call Tool

- **List pods in a specific namespace:**
  ```bash
  curl -X POST http://localhost:8000/call \
    -H "Content-Type: application/json" \
    -d '{"tool":"list_pods","arguments":{"namespace":"default"}}'
  ```

- **List pods in all namespaces:**
  ```bash
  curl -X POST http://localhost:8000/call \
    -H "Content-Type: application/json" \
    -d '{"tool":"list_pods","arguments":{}}'
  ```

## Run Client

```bash
python client.py
```

## Works With
- Kind cluster
- kubeconfig (~/.kube/config)

## MCP Flow

Agent → /tools → discover  
Agent → /call → execute  
