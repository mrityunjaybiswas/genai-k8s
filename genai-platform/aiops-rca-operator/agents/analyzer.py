
def run(state):
    logs = state["logs"]
    if "OOMKilled" in logs:
        return {**state, "analysis": "OOMKilled"}
    if "CrashLoopBackOff" in logs:
        return {**state, "analysis": "CrashLoopBackOff"}
    return {**state, "analysis": "Unknown"}
