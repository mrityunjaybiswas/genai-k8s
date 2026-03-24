# Module 7: CRDs and Kubernetes Operators

Module 7 teaches students how to extend Kubernetes with a custom API and automate an AI workload with a simple operator written in Go.

By the end of this module, students will:

- create and register a `CustomResourceDefinition`
- understand the shape of a custom resource spec and status block
- build a controller with Operator SDK
- automate the lifecycle of a GenAI API workload
- observe reconciliation loops in action

Start here:

[training/module7-operators/README.md](/home/arjun/genai-k8s/training/module7-operators/README.md)

Tested environment for this module:

- macOS, Linux, or Windows WSL with Docker and KIND
- KIND cluster context `kind-multi-node-cluster`
- Go `1.26.1`
- Operator SDK `v1.42.2`

The lab materials include prerequisites, step-by-step exercises, the full Go operator code, and sample custom resources that students can apply directly.
