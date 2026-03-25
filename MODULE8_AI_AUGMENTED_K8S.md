# Module 8: AI-Augmented Kubernetes using kubectl-ai and MCP

In this module, you will learn how to integrate Artificial Intelligence directly into your Kubernetes workflows. By using tools like `kubectl-ai` and the Model Context Protocol (MCP), you can interact with your cluster using natural language to generate manifests, troubleshoot issues, and gain deeper insights without needing to memorize complex API objects.

## Prerequisites

- A running Kubernetes cluster (e.g., KIND)
- `kubectl` installed and configured
- An OpenAI API Key (or equivalent LLM provider API Key) for `kubectl-ai`

---

## Part 1: Installing and Configuring `kubectl-ai`

`kubectl-ai` is a kubectl plugin that allows you to generate Kubernetes manifests using OpenAI's GPT models.

### 1. Install Krew (if not already installed)

Krew is the plugin manager for `kubectl`.

```bash
(
  set -x; cd "$(mktemp -d)" &&
  OS="$(uname | tr '[:upper:]' '[:lower:]')" &&
  ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')" &&
  KREW="krew-${OS}_${ARCH}" &&
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz" &&
  tar zxvf "${KREW}.tar.gz" &&
  ./"${KREW}" install krew
)
export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"
```

To avoid having to run the export command every time you open a new terminal, add it to your bash profile:
```bash
echo 'export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 2. Install the `kubectl-ai` Plugin

```bash
kubectl krew install ai
```

### 3. Configure API Credentials

You must provide an API key for your chosen LLM provider. `kubectl-ai` supports multiple providers including OpenAI and Google AI (Gemini).

**For Google AI (Gemini)**
Set your Gemini API Key and specify the Google provider:
```bash
export GEMINI_API_KEY=""
export KUBECTL_AI_PROVIDER="google"
```

**For OpenAI (Default)**
```bash
export OPENAI_API_KEY=""
```

*Note: `kubectl-ai` also supports Azure OpenAI, Vertex AI, and local models if configured appropriately.*

---

## Part 2: Generating Manifests with AI Slash Commands

Now that `kubectl-ai` is installed, you can use natural language to generate resources.

### 1. Basic Manifest Generation

Ask AI to create a simple NGINX deployment:

```bash
kubectl ai "create an nginx deployment with 3 replicas"
```

The plugin will output the YAML manifest and prompt you:
**`Would you like to apply this? [y/N]`**

Type `N` for now to just inspect the output, or `y` to deploy it.

### 2. Complex Manifest Generation

Let's ask for something more complex, like a deployment and a service combined:

```bash
kubectl ai "create a redis deployment and expose it internally on port 6379"
```

This demonstrates how the AI understands Kubernetes architectural patterns and can scaffold multiple related resources at once.

---

## Part 3: Setting up a Kubernetes MCP Server

The Model Context Protocol (MCP) allows AI assistants (like Claude Desktop, Cursor, or custom agents) to securely interact with external systems. A Kubernetes MCP Server bridges your AI assistant with your cluster.

### 1. Running an MCP Server

There are community-provided Kubernetes MCP servers. If you have Node.js installed, you can run a popular MCP server directly using `npx`:

```bash
npx -y @smithery/cli run @smithery/mcp-kubernetes
```

*(Note: Depending on your AI assistant, you may need to add this command to your assistant's MCP configuration file, often located at `~/.mcp/config.json` or within the application settings).*

### 2. Interacting via MCP

Once connected, your AI assistant can now read from your cluster. You can ask your AI:
- "List all failing pods in the genai namespace."
- "What is the CPU usage of the api-deployment?"
- "Check the logs of the ollama pod for any errors."

The AI will translate your natural language into API calls via the MCP server and return the analyzed results.

---

## Part 4: Interactive Troubleshooting and Log Analysis

Using AI for debugging can significantly reduce mean time to resolution (MTTR).

### 1. Build Custom Prompts for Cluster Insight

Instead of manually digging through events, you can pipe Kubernetes output to an AI CLI tool or use an MCP-connected assistant. 

For example, using a CLI tool like `llm` (if installed) or piping to a custom script:

```bash
kubectl get events -n genai | llm "Analyze these events and tell me why my pods are failing"
```

Or with an MCP-enabled assistant, you can simply type:
**"Summarize the recent events in the 'genai' namespace and identify any bottlenecks."**

### 2. Explore Slash Commands (If using a specific AI IDE/Terminal)

In tools like Cursor or GitHub Copilot CLI, you can use specialized slash commands to analyze failures:

- **`/k8s logs pod-name`**: Fetches logs and automatically scans for stack traces.
- **`/k8s describe pod-name`**: Reads the pod description and highlights misconfigurations (e.g., OOMKilled, ImagePullBackOff).

## Exercise: The Failing Pod Scenario

1. Apply a broken manifest to simulate a failure:
   ```bash
   kubectl create deployment broken-app --image=nginx:non-existent-tag
   ```
2. Wait a few seconds, then verify it is failing:
   ```bash
   kubectl get pods
   ```
3. Use a natural language prompt with your MCP-enabled assistant or an AI CLI tool to diagnose the issue. For example:
   *"Why is the deployment 'broken-app' not starting?"*
4. Notice how the AI checks the pod status, reads the events (identifying `ErrImagePull`), and suggests the fix (correcting the image tag).
5. Clean up the broken deployment:
   ```bash
   kubectl delete deployment broken-app
   ```

## Summary
You have successfully augmented your Kubernetes operations with AI! You can now generate manifests effortlessly, securely expose your cluster state to AI assistants via MCP, and leverage natural language for rapid troubleshooting.
