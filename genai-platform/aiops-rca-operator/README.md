
# AIOps RCA Operator (Kubernetes + LangGraph + MCP)

## What this does
- Defines CRD: RCARequest
- Operator watches CRD
- On create → runs LangGraph agents (Planner → Debugger → Analyzer → Fixer)
- Updates CRD status

## Install

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_key
```

## Apply CRD

```bash
kubectl apply -f crd.yaml
```

## Run Operator

```bash
python operator.py
```

## Test

```bash
kubectl apply -f sample.yaml
kubectl get rcarequests -o yaml
```
