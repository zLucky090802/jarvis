from dotenv import load_dotenv
import os
import asyncio
from llama_index.core import Settings
from llama_index.llms.groq import Groq
from llama_index.core.agent.workflow import (
    ReActAgent,
    AgentStream,
    ToolCallResult,
    FunctionAgent
)
from src.service.agent_service import setting_agent

load_dotenv()

api_key_groq = os.getenv('GROQ_API_KEY')
llm = Groq(
    model='llama-3.1-8b-instant',
    api_key=api_key_groq
)

Settings.llm = llm



async def main():
    
    
   agent, context =  setting_agent(llm)

   response = await agent.run(
       'open spotify',
       ctx=context,
    )
   
   print(response)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 
