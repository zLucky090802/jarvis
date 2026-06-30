from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.workflow import Context
from llama_index.llms.groq import Groq
from functools import wraps
from src.actions.os_actions import open_application
from src.actions.web_actions import search_in_browser
from src.actions.media_actions import play_spotify_song
from src.actions.monday_actions import delete_item_tool, add_item_tool, create_board_tool, create_worskpace_tool

class AgentService:
    def __init__(self):
        # Mantenemos el cliente del LLM instanciado de forma global
        self.llm = Groq(model='llama-3.3-70b-versatile') 
        
    def _make_once(self, func, tools_ejecutadas: set):
        """Convierte cualquier función en una que solo se ejecuta una vez."""
        @wraps(func)  # Preserva nombre y docstring — importante para LlamaIndex
        def wrapper(*args, **kwargs):
            if func.__name__ in tools_ejecutadas:
                return "TAREA_YA_EJECUTADA."
            tools_ejecutadas.add(func.__name__)
            return func(*args, **kwargs)
        return wrapper

    async def execute_command(self, user_msg: str) -> str:
        """
        Crea un agente fresco en cada petición, ejecuta el comando de forma 
        asíncrona mediante el Workflow de LlamaIndex y destruye el contexto 
        al terminar para evitar bucles infinitos por feedback de audio.
        """
        try:
            tools_ejecutadas = set()
            # 🚨 EL ROMPE-BUCLES DEFINITIVO: Instanciamos un agente y contexto limpios CADA VEZ
            agent = FunctionAgent(
               llm=self.llm,
                tools=[
                    self._make_once(play_spotify_song, tools_ejecutadas),
                    self._make_once(open_application, tools_ejecutadas),
                    self._make_once(search_in_browser, tools_ejecutadas),
                    self._make_once(create_worskpace_tool, tools_ejecutadas),
                    self._make_once(create_board_tool, tools_ejecutadas),
                    self._make_once(delete_item_tool, tools_ejecutadas),
                    self._make_once(add_item_tool, tools_ejecutadas)
                ],
                allow_parallel_tool_calls=False, 
                system_prompt=(
                    "Eres Jarvis, un asistente virtual inteligente para Windows.\n"
                    "Analiza la petición del usuario y llama a la función correspondiente:\n\n"
                    "- Si el usuario quiere escuchar una canción, música, poner un tema o un artista, "
                    "llama exclusivamente a la función 'play_spotify_song' UNA SOLA VEZ.\n"
                    "- Si el usuario pide abrir un programa genérico en Windows, usa 'open_application'.\n"
                    "- Si te hacen preguntas generales, usa 'search_in_browser'.\n\n"
                    "⚠️ REGLA CRÍTICA #1: Llama a cada herramienta MÁXIMO UNA VEZ por petición.\n"
                    "⚠️ REGLA CRÍTICA #2: Cuando una herramienta retorne un mensaje que contenga "
                    "'TAREA_COMPLETADA', detente inmediatamente y responde al usuario confirmando la acción. "
                    "NUNCA vuelvas a invocar una herramienta después de recibir ese mensaje.\n"
                    "⚠️ REGLA CRÍTICA #3: Si el texto del usuario contiene solo ruido o palabras sueltas "
                    "sin una orden clara, no ejecutes ninguna acción."
                ),
                max_function_calls = 1,
                verbose=True,
            )
            
            # Contexto efímero que morirá al finalizar esta función
            contexto_fresco = Context(agent)
            
            print(f"🤖 Jarvis procesando comando asíncrono stateless: '{user_msg}'")
            
            # Ejecución nativa del Workflow
            response = await agent.run(
                user_msg=user_msg,
                ctx=contexto_fresco
            )
            return str(response)
            
        except Exception as e:
            print(f"❌ [AgentService Error]: {e}")
            return "Lo siento, tuve un problema interno al procesar ese comando."

    def procesar_comando(self, mensaje_texto: str) -> str:
        """
        Método síncrono de respaldo (Legacy). Mantiene la misma lógica libre de memoria.
        """
        agent = FunctionAgent(
            llm=self.llm,
            tools=[open_application, search_in_browser, play_spotify_song],
            allow_parallel_tool_calls=False,
            system_prompt="Eres Jarvis, un asistente virtual inteligente para Windows."
        )
        contexto_fresco = Context(agent)
        response = agent.chat(mensaje_texto, chat_ctx=contexto_fresco)
        return str(response)