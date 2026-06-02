from llama_index.core.agent.workflow import (
    ReActAgent,
    AgentStream,
    ToolCallResult,
    FunctionAgent,
)
import os
from llama_index.core import Settings
from llama_index.llms.groq import Groq
from src.actions.os_actions import open_application
from llama_index.core.workflow import Context

api_key_groq = os.getenv('GROQ_API_KEY')
llm = Groq(
    model='llama-3.1-8b-instant',
    api_key=api_key_groq
)

def setting_agent():
    agent = FunctionAgent(
        llm=llm,
        tools=[open_application],
        allow_parallel_tool_calls= True
    )
    
    context = Context(agent)
    
    return agent, context
    
 