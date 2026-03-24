# Module 7: CRDs and Kubernetes Operators

This module uses a real Go operator project so students can move from Kubernetes theory to a working controller.

The custom resource is named `AIApp`. Each `AIApp` object manages:

- one `Deployment`
- one `Service`
- status conditions that report reconciliation progress

## Learning Outcomes

Students will learn how to:

1. install the local toolchain required for Go-based operators
2. register a CRD with the Kubernetes API
3. build a controller using Operator SDK
4. reconcile desired state into Kubernetes resources
5. automate lifecycle management for an AI API workload
6. inspect status, events, and spec changes during reconciliation

## Module Flow

1. [01-prerequisites.md](/home/arjun/genai-k8s/training/module7-operators/01-prerequisites.md)
2. [02-project-scaffold.md](/home/arjun/genai-k8s/training/module7-operators/02-project-scaffold.md)
3. [03-create-the-crd.md](/home/arjun/genai-k8s/training/module7-operators/03-create-the-crd.md)
4. [04-build-the-controller.md](/home/arjun/genai-k8s/training/module7-operators/04-build-the-controller.md)
5. [05-run-the-operator.md](/home/arjun/genai-k8s/training/module7-operators/05-run-the-operator.md)
6. [06-create-custom-resources.md](/home/arjun/genai-k8s/training/module7-operators/06-create-custom-resources.md)
7. [07-reconciliation-patterns.md](/home/arjun/genai-k8s/training/module7-operators/07-reconciliation-patterns.md)
8. [08-cleanup.md](/home/arjun/genai-k8s/training/module7-operators/08-cleanup.md)

## Lab Code

The working operator project for this module lives in this same directory:

- [api/v1alpha1/aiapp_types.go](/home/arjun/genai-k8s/training/module7-operators/api/v1alpha1/aiapp_types.go)
- [internal/controller/aiapp_controller.go](/home/arjun/genai-k8s/training/module7-operators/internal/controller/aiapp_controller.go)
- [config/samples/ai_v1alpha1_aiapp.yaml](/home/arjun/genai-k8s/training/module7-operators/config/samples/ai_v1alpha1_aiapp.yaml)
- [config/samples/ai_v1alpha1_aiapp_minimal.yaml](/home/arjun/genai-k8s/training/module7-operators/config/samples/ai_v1alpha1_aiapp_minimal.yaml)

## Tested Commands

The module was validated on the shared KIND cluster with:

```bash
export PATH="/home/arjun/.local/bin:/home/arjun/.local/lib/go-toolchain/go/bin:$PATH"

make build
make install
make run
kubectl apply -f config/samples/ai_v1alpha1_aiapp.yaml
kubectl patch aiapp aiapp-sample -n ai-operators-lab --type merge -p '{"spec":{"replicas":2}}'
```

## Quick Start

If you want to jump straight to the runnable lab:

```bash
cd /home/arjun/genai-k8s/training/module7-operators
export PATH="/home/arjun/.local/bin:/home/arjun/.local/lib/go-toolchain/go/bin:$PATH"

kubectl create namespace ai-operators-lab --dry-run=client -o yaml | kubectl apply -f -
make build
make install
make run
```

In a second terminal:

```bash
kubectl apply -f config/samples/ai_v1alpha1_aiapp.yaml
kubectl get aiapp -n ai-operators-lab
kubectl get deployment,svc,pods -n ai-operators-lab
```
