import os
from kubernetes import client, config

class ClusterManager:
    def __init__(self, kubeconfig_dir="kubeconfigs"):
        self.kubeconfig_dir = kubeconfig_dir
        self.clients = {}
        self._load_clusters()

    def _load_clusters(self):
        # Load the default cluster from ~/.kube/config
        try:
            config.load_kube_config()
            self.clients["default"] = client.CoreV1Api()
        except Exception as e:
            print(f"Could not load default kubeconfig: {e}")

        if not os.path.exists(self.kubeconfig_dir):
            return

        for filename in os.listdir(self.kubeconfig_dir):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                cluster_id = os.path.splitext(filename)[0]
                kubeconfig_path = os.path.join(self.kubeconfig_dir, filename)
                try:
                    api_client = config.new_client_from_config(kubeconfig_path)
                    self.clients[cluster_id] = client.CoreV1Api(api_client)
                except Exception as e:
                    print(f"Error loading kubeconfig from {kubeconfig_path}: {e}")

    def get_client(self, cluster_id: str = "default") -> client.CoreV1Api:
        return self.clients.get(cluster_id)

    def list_clusters(self):
        return [{"id": c, "name": c} for c in self.clients.keys()]
