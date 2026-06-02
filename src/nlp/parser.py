import os
import json
from groq import Groq


client = Groq(api_key=os.environ.get('GROQ_API_KEY'))


def parse_command_with_groq(user_transcription: str) -> dict:
    """
    Envía la transcripción a Groq para corregir el nombre de la app
    y extraer la acción de forma estructurada.
    """
    
    system_prompt = """
    Eres el módulo de procesamiento de lenguaje natural de un asistente virtual llamado Jarvis.
    Tu único trabajo es analizar el texto que dice el usuario y extraer dos cosas: la acción y el nombre correcto de la aplicación en minúsculas.
    
    Reglas estrictas de corrección de nombres:
    - Si el usuario dice "wsp", "guazap", "wasap", debes corregirlo a "whatsapp".
    - Si dice "espotifai", "música", "espoty", debes corregirlo a "spotify".
    - Si dice "el navegador", "crom", "gugle", debes corregirlo a "chrome".
    - Si dice "visual", "vsc", "código", "visual studio", debes corregirlo a "code".
    - Si dice "bloc de notas", "nota", debes corregirlo a "notepad".
    
    Debes responder ÚNICAMENTE con un objeto JSON válido, sin textos introductorios ni explicaciones.
    
    Formato de respuesta requerido:
    {
        "action": "open" o "unknown",
        "app_name": "nombre_corregido_de_la_app" o "none"
    }
    """

    try:
        # Usamos un modelo ultra rápido como llama3-8b
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"El usuario dijo: '{user_transcription}'"}
            ],
            # Forzamos a Groq a que responda estrictamente con un JSON
            response_format={"type": "json_object"},
            temperature=0.1 # Temperatura baja para que sea determinista y no invente cosas
        )
        
        # Parseamos la respuesta de la IA
        result = json.loads(completion.choices[0].message.content)
        return result

    except Exception as e:
        print(f"❌ Error al conectar con Groq: {e}")
        return {"action": "unknown", "app_name": "none"}