
from kubernetes import client, config

def get_logs(namespace, pod):
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()

    v1 = client.CoreV1Api()
    return v1.read_namespaced_pod_log(name=pod, namespace=namespace, tail_lines=100)
