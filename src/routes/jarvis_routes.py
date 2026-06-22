from fastapi import APIRouter, UploadFile, File
from src.service.audio_service import AudioService
from src.service.agent_service import AgentService

router = APIRouter()

audio_service = AudioService()
agent_service = AgentService()

@router.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    # 1. Transcribir el archivo de audio recibido
    text_prompt = await audio_service.transcript_audio(file)
    print(f'Jarvis escucho; {text_prompt}')
    
    # 2. Ejecutar el comando de forma asíncrona y sin estado (stateless)
    agent_response = await agent_service.execute_command(text_prompt)
    
    # 🚨 NOTA: Eliminamos la línea del clear() porque execute_command
    # maneja su propio contexto efímero y se destruye solo al retornar.
    
    return {
        "success": True,
        "transcription": text_prompt,
        "agent_response": agent_response
    }
    
    