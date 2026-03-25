import os
import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession
import openai

MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL", "http://mcp-server-svc.genai.svc.cluster.local:8000/sse")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

async def analyze_cluster():
    print("Starting Autonomous AI Agent RCA Pipeline...")
    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY is not set. The Agent cannot perform analysis.")
        return

    try:
        # Step 1: Connect to the MCP Server over SSE
        print(f"Connecting to MCP Server at {MCP_SERVER_URL}...")
        async with sse_client(MCP_SERVER_URL) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                # Step 2: Use the MCP Tool to retrieve cluster state
                print("Querying live Kubernetes pod state via MCP Tool 'get_pods_in_namespace'...")
                result = await session.call_tool("get_pods_in_namespace", arguments={"namespace": "genai"})
                
                pod_info = result.content[0].text
                print(f"\n--- Retrieved Cluster State ---\n{pod_info}\n-------------------------------")
                
                # Step 3: Pass the data to the LLM for Automated RCA
                print("\nInitiating LLM Analysis for RCA...")
                client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
                
                prompt = f"""
                You are an autonomous Kubernetes Reliability Agent.
                You are monitoring the 'genai' namespace. Here is the current pod status:
                
                {pod_info}
                
                Perform a Root Cause Analysis (RCA). 
                - If any pods are failing (e.g., ImagePullBackOff, CrashLoopBackOff, Error), highlight them clearly and suggest precise remediation steps.
                - If all pods are running smoothly, verify that the system is healthy.
                Keep your analysis concise and actionable for an SRE.
                """
                
                response = await client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=250
                )
                
                analysis = response.choices[0].message.content
                print("\n====================================")
                print("    AI AGENT ROOT CAUSE ANALYSIS    ")
                print("====================================")
                print(analysis)
                print("====================================")
                
    except Exception as e:
        print(f"Failed to execute agent pipeline: {e}")

if __name__ == "__main__":
    asyncio.run(analyze_cluster())
