from dotenv import load_dotenv
import os

from llama_index.core import Settings
from llama_index.llms.groq import Groq
from llama_index.core.agent.workflow import (
    ReActAgent,
    AgentStream,
    ToolCallResult,
    FunctionAgent
)

load_dotenv()

api_key_groq = os.getenv('GROQ_API_KEY')
llm = Groq(
    model='llama-3.1-8b-instant',
    api_key=api_key_groq
)

Settings.llm = llm



def main():
    
    
    print("Hello from jarvis!")


if __name__ == "__main__":
    main()
