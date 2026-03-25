
from tools.k8s_logs import get_logs

def run(state):
    logs = get_logs(state["namespace"], state["pod_name"])
    return {**state, "logs": logs}
