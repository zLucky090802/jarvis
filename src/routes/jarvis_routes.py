from fastapi import APIRouter, UploadFile,File
from src.service.audio_service import AudioService
from src.service.agent_service import AgentService

router = APIRouter()

audio_service = AudioService()
agent_service = AgentService()

@router.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    text_prompt = await audio_service(file)
    print(f'Jarvis escucho; {text_prompt}')
    
    agent_response = await agent_service.execute_command(text_prompt)
    return {
        "success": True,
        "transcription": text_prompt,
        "agent_response": agent_response
    }