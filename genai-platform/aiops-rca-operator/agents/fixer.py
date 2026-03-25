
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")

def run(state):
    prompt = f"Logs: {state['logs']} Issue: {state['analysis']} Suggest fix"
    return {**state, "fix": llm.invoke(prompt).content}
