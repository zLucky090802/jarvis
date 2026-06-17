import os
import shutil
from fastapi import UploadFile, HTTPException
from groq import Groq


class AudioService:
    def __init__(self):
        
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.allowed_extensions = ('.wav', '.mp3','m4a', '.webm')
        
    async def transcript_audio(self, file: UploadFile) -> str:
        """Valida, guarda temporalmente y transcribe un archivo de audio usando Groq Whisper.
        Retorna el texto extraído."""
        
        if not file.filename.lower().endswith(self.allowed_extensions):
            raise HTTPException(status_code=400, detail='Formato de audio no soportado')
        
        temp_file_path = f'temp_{file.filename}'
        
        try:
            with open(temp_file_path, 'wb') as buffer:
                shutil.copyfileobj(file.file, buffer)
            with open(temp_file_path, 'rb') as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    file=(temp_file_path, audio_file.read()),
                    model='whisper-large-v3',
                    language='es',
                    temperature=0.0
                )
            return transcription.text
        
        except Exception as e:
            print(f'AudioService Error: {e}')
            raise HTTPException(status_code=500, detail='Error al procesar o transcribir audio')
        
        
        finally:
            
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)