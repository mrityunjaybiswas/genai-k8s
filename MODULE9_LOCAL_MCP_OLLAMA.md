# Module 9: Local, Private AI-Augmented Kubernetes with Ollama and kubectl-ai

In this module, you will learn how to build a completely private and local AI assistant for Kubernetes. By running a local LLM with Ollama and integrating it with `kubectl-ai`, you can use natural language to manage your cluster without sending any data, credentials, or cluster information to a third-party cloud service.

This setup is ideal for air-gapped environments, developers who prioritize data privacy, or anyone looking to experiment with local LLMs.

## Prerequisites

- A running Kubernetes cluster (e.g., KIND)
- `kubectl` installed and configured
- Docker and Docker Compose installed
- `kubectl-ai` installed (see Module 8 for installation instructions)

---

## Part 1: Setting up a Local Ollama Environment

Ollama is a powerful tool that makes it easy to download and run state-of-the-art LLMs locally. We will use Docker Compose to create a reproducible environment containing Ollama and a custom MCP (Model Context Protocol) server that acts as a bridge to `kubectl-ai`.

### 1. Create the Project Files

First, navigate into the `genai-platform/local-mcp-ollama` directory. We will create three files:
- `docker-compose.yaml`: To define and run our multi-container application.
- `server.py`: A lightweight Python server to translate `kubectl-ai` requests to the Ollama API.
- `requirements.txt`: To specify the Python dependencies for our server.

```bash
cd genai-platform/local-mcp-ollama
touch docker-compose.yaml server.py requirements.txt
```

### 2. Define the Docker Compose Setup

Open `docker-compose.yaml` and add the following configuration. This setup defines two services:
1.  **ollama**: Runs the official Ollama container and exposes its API.
2.  **mcp-server**: A Python-based server that we will build to act as an OpenAI-compatible endpoint for `kubectl-ai`.

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ./ollama_data:/root/.ollama

  mcp-server:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: mcp-server
    ports:
      - "8888:8888"
    depends_on:
      - ollama
    environment:
      - OLLAMA_HOST=ollama
```

### 3. Create the MCP Server

This Python script uses `Flask` to create a simple web server that listens on port 8888. It exposes a `/v1/chat/completions` endpoint, which is the same path `kubectl-ai` uses for the OpenAI API. When `kubectl-ai` sends a request, this server forwards it to the Ollama container and streams the response back.

Open `server.py` and add the following code:

```python
from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)

OLLAMA_HOST = "http://ollama:11434"

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.get_json()
    model = data.get("model", "llama3")
    messages = data.get("messages", [])

    # The actual prompt content is in the last message
    prompt_text = ""
    if messages:
        prompt_text = messages[-1].get("content", "")

    # Ollama API payload
    ollama_payload = {
        "model": model,
        "prompt": prompt_text,
        "stream": True
    }

    # Forward the request to Ollama and stream the response
    def generate():
        response = requests.post(f"{OLLAMA_HOST}/api/generate", json=ollama_payload, stream=True)
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                # We need to format the response to mimic OpenAI's streaming format
                # Ollama's response chunk is a JSON object per line
                ollama_response = json.loads(chunk)
                content = ollama_response.get("response", "")
                
                # Create an OpenAI-compatible streaming chunk
                openai_chunk = {
                    "choices": [{
                        "delta": {
                            "content": content
                        }
                    }]
                }
                yield f"data: {json.dumps(openai_chunk)}\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
```

### 4. Specify Dependencies and Dockerfile

Add the required libraries to `requirements.txt`:

```
flask
requests
```

Create a `Dockerfile` for our server:

```Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY server.py .
CMD ["python", "server.py"]
```

---

## Part 2: Running the Local AI Environment

Now that all the files are in place, we can start our local AI stack.

### 1. Launch the Services

From the `genai-platform/local-mcp-ollama` directory, run:

```bash
docker-compose up -d --build
```

This command will:
- Build the `mcp-server` image.
- Start both the `ollama` and `mcp-server` containers in the background.

### 2. Pull the LLM Model

Before you can use the service, you need to pull a model into the Ollama container. We will use `llama3`.

```bash
docker exec ollama ollama pull llama3
```
This may take a few minutes depending on your internet connection.

### 3. Verify the Setup

You can check the logs to see the progress:

```bash
# Check the MCP server logs
docker logs mcp-server

# Check the Ollama logs
docker logs ollama
```

Once the model is downloaded, you are ready to connect `kubectl-ai`.

---

## Part 3: Integrating with `kubectl-ai`

The final step is to configure `kubectl-ai` to use our local, OpenAI-compatible endpoint instead of hitting a public URL.

### 1. Configure `kubectl-ai`

Run the following `export` commands in your terminal. This tells the plugin to send its requests to our local `mcp-server` on port 8888.

```bash
export KUBECTL_AI_PROVIDER="openai"
export OPENAI_API_BASE="http://localhost:8888/v1"
export OPENAI_API_KEY="local" # A dummy key is required, but not used
```

*To make this permanent, add these lines to your `~/.bashrc` or `~/.zshrc` file.*

### 2. Test the Integration

Now you can use `kubectl-ai` with natural language, and the inference will happen entirely on your local machine.

Ask it to generate a simple manifest:

```bash
kubectl ai "create a deployment for nginx with 2 replicas"
```

The plugin will send the request to your `mcp-server`, which forwards it to Ollama. The generated YAML will be streamed back to your terminal.

**`Would you like to apply this? [y/N]`**

Type `N` for now.

---

## Exercise: Debug a Failing Pod Locally

Let's use our local AI to solve a common Kubernetes problem.

1.  Create a broken deployment that uses a non-existent image tag.
    ```bash
    kubectl create deployment broken-app --image=nginx:1.999-non-existent
    ```

2.  Verify that the pod is failing with an `ImagePullBackOff` error.
    ```bash
    kubectl get pods
    ```

3.  Now, use `kubectl-ai` to diagnose the issue. The `-i` (interactive) flag allows the AI to run commands to gather more context.
    ```bash
    kubectl ai "The 'broken-app' deployment is failing to start. Tell me why and how to fix it." -i
    ```

4.  Observe the output. The local AI should:
    - Identify the failing pod.
    - Describe the pod and see the `ImagePullBackOff` status.
    - Check the events to find the root cause (`Failed to pull image...`).
    - Suggest a solution, such as correcting the image tag.

5.  Clean up the broken deployment.
    ```bash
    kubectl delete deployment broken-app
    ```

## Summary

Congratulations! You have successfully set up a private, local AI assistant for your Kubernetes cluster. All prompts and cluster data remain on your machine, processed by a local LLM running in Ollama. This powerful setup ensures data privacy while still giving you the benefits of AI-augmented operations.
