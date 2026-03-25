
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")

def run(state):
    prompt = f"Plan debugging for pod {state['pod_name']}"
    return {**state, "plan": llm.invoke(prompt).content}
