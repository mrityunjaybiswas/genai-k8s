import subprocess

def get_pod_logs(namespace: str, pod_name: str, container: str = None):
    try:
        cmd = ["kubectl", "logs", pod_name, "-n", namespace]

        if container:
            cmd.extend(["-c", container])

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return f"Error: {result.stderr}"

        return result.stdout[:5000]

    except Exception as e:
        return str(e)
