# Exercise 2: Scaffold the Operator Project

This repository already includes a working operator project, but it is useful to understand how it was created.

## Move Into the Module Directory

```bash
cd /home/arjun/genai-k8s/training/module7-operators
export PATH="/home/arjun/.local/bin:/home/arjun/.local/lib/go-toolchain/go/bin:$PATH"
```

## Recreate the Scaffold From Scratch

These are the commands used to create the project:

```bash
operator-sdk init \
  --domain workshop.io \
  --repo github.com/arjun/genai-k8s/training/module7-operators/ai-workload-operator \
  --project-name ai-workload-operator \
  --plugins go/v4

operator-sdk create api \
  --group ai \
  --version v1alpha1 \
  --kind AIApp \
  --resource \
  --controller \
  --make
```

You do not need to rerun those commands now because the generated project is already in place.

## Inspect the Important Files

```bash
find . -maxdepth 2 -type f | sort
```

Focus on these paths:

- `api/v1alpha1/aiapp_types.go`
- `internal/controller/aiapp_controller.go`
- `cmd/main.go`
- `config/crd/`
- `config/samples/`
- `Makefile`

## What Just Happened?

Operator SDK generated a standard controller-runtime project. That scaffold gives you a CRD, API types, controller wiring, RBAC manifests, and Make targets so you can focus on business logic rather than bootstrapping everything by hand.
