
import kopf
from graph import graph

@kopf.on.create('aiops.example.com', 'v1', 'rcarequests')
def create_fn(spec, status, namespace, **kwargs):
    pod = spec.get("podName")
    ns = spec.get("namespace", namespace)

    result = graph.invoke({
        "namespace": ns,
        "pod_name": pod,
        "plan": "",
        "logs": "",
        "analysis": "",
        "fix": ""
    })

    return {
        "phase": "Completed",
        "analysis": result["analysis"],
        "fix": result["fix"]
    }
