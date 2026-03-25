from fastapi import FastAPI
from pydantic import BaseModel
from tools.logs import get_pod_logs

app = FastAPI()

class LogRequest(BaseModel):
    namespace: str
    pod_name: str
    container: str = None

@app.post("/tools/get_pod_logs")
def fetch_logs(req: LogRequest):
    logs = get_pod_logs(
        namespace=req.namespace,
        pod_name=req.pod_name,
        container=req.container
    )

    return {
        "tool": "get_pod_logs",
        "output": logs
    }
