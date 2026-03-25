# MCP K8s Server (Kind Deployable)

## Build Image (Kind)

kind load docker-image mcp-k8s:latest

## OR build first
docker build -t mcp-k8s:latest .

## Deploy

kubectl apply -f k8s.yaml

## Access

kubectl get svc mcp-k8s

http://<node-ip>:30007/tools

## Test

curl http://localhost:30007/tools

curl -X POST http://localhost:30007/call \
 -H "Content-Type: application/json" \
 -d '{"tool":"list_pods","arguments":{"namespace":"default"}}'
