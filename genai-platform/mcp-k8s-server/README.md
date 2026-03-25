# MCP Kubernetes Logs Server

## Run

pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8000

## Test

curl -X POST http://localhost:8000/tools/get_pod_logs \
-H "Content-Type: application/json" \
-d '{"namespace":"default","pod_name":"nginx"}'

## kubectl-ai

kubectl-ai \
  --llm-provider ollama \
  --model llama3 \
  --enable-tool-use-shim \
  --mcp-server http://localhost:8000 \
  --tools-file tools.json
