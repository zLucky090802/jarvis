import os
from dotenv import load_dotenv

load_dotenv()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llama_index.core import Settings
from llama_index.llms.groq import Groq
from src.routes.jarvis_routes import router

# 1. Cargar variables de entorno


# 2. Configuración global de LlamaIndex (Para que todo el backend use Groq por defecto)
api_key_groq = os.getenv('GROQ_API_KEY')
llm = Groq(
    model='llama-3.1-8b-instant',
    api_key=api_key_groq
)
Settings.llm = llm

# 3. Inicializar la aplicación de FastAPI
app = FastAPI(
    title='Jarvis API',
    description='Backend modular para el asistente virtual Jarvis utilizando LlamaIndex Workflows y Groq',
    version='1.0.0'
)

# 4. Configurar Middleware de CORS (Esencial para conectar con tu Frontend/Script cliente)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # En producción, cámbialo por el dominio de tu interfaz
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# 5. Incluir las rutas de Jarvis
app.include_router(router)

# Nota: Eliminamos por completo async def main() porque Uvicorn se encarga de la ejecución.