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



def setting_agent(llm):
    agent = FunctionAgent(
        llm=llm,
        tools=[open_application],
        allow_parallel_tool_calls= True,
        system_prompt=(
            "Eres Jarvis, un asistente virtual avanzado para Windows. Tu objetivo es abrir aplicaciones usando la herramienta 'open_application'.\n\n"
            "CRÍTICO - REGLA DE FORMATO PARA WINDOWS:\n"
            "Antes de llamar a la herramienta, analiza qué tipo de aplicación pide el usuario:\n"
            "1. Si es una aplicación moderna, de la Microsoft Store o de redes sociales (como Discord, Spotify, WhatsApp, Netflix, Instagram, Facebook), "
            "DEBES agregar obligatoriamente dos puntos (:) al final del nombre (ejemplo: 'discord:', 'spotify:', 'whatsapp:').\n"
            "2. Si es una herramienta nativa del sistema o un comando clásico ejecutable (como notepad, calc, mspaint, explorer, code), "
            "DEBES enviar el nombre limpio, SIN los dos puntos.\n\n"
            "Piensa cuidadosamente a qué categoría pertenece la aplicación solicitada antes de invocar la herramienta."
        )
    )
    
    context = Context(agent)
    
    return agent, context
    
