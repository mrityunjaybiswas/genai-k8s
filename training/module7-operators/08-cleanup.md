# Exercise 8: Cleanup

Use this exercise after you finish the module.

## Delete the Sample Custom Resources

```bash
cd /home/arjun/genai-k8s/training/module7-operators
kubectl delete -f config/samples/ai_v1alpha1_aiapp.yaml --ignore-not-found
kubectl delete -f config/samples/ai_v1alpha1_aiapp_minimal.yaml --ignore-not-found
```

## Uninstall the CRD

```bash
export PATH="/home/arjun/.local/bin:/home/arjun/.local/lib/go-toolchain/go/bin:$PATH"
make uninstall
```

## Delete the Lab Namespace

```bash
kubectl delete namespace ai-operators-lab --ignore-not-found
```

## What Just Happened?

Cleanup removes both the custom resources and the API extension itself. Once the CRD is uninstalled, Kubernetes no longer recognizes `AIApp` objects.
