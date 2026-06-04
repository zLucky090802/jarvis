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
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes

load_dotenv()
app = FastAPI(title='Jarvis')
api_key_groq = os.getenv('GROQ_API_KEY')
llm = Groq(
    model='llama-3.1-8b-instant',
    api_key=api_key_groq
)

Settings.llm = llm

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials=True,
    allow_methods=["*"], # Permite POST, GET, OPTIONS, etc.
    allow_headers=["*"], # Permite Content-Type, Authorization, etc.
)



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
