import sounddevice as sd
from scipy.io import wavfile
import httpx
import os
import time

# Configuración de la grabación
FREQ = 44100  # Frecuencia de muestreo estándar (CD quality)
DURACION = 4   # Segundos que se quedará escuchando tu micrófono
OUTPUT_FILE = "prueba_micro.wav"
API_URL = "http://127.0.0.1:8000/upload"

def registrar_voz():
    print(f"\n🎙️ [Micrófono Activo] Tienes {DURACION} segundos... ¡HABLA AHORA!")
    print("--------------------------------------------------")
    
    # Captura el audio del micrófono de Windows
    audio_data = sd.rec(int(DURACION * FREQ), samplerate=FREQ, channels=1, dtype='int16')
    
    # Barra de progreso visual en consola
    for i in range(DURACION, 0, -1):
        print(f"⏱️ Grabando... quedan {i} segundos")
        time.sleep(1)
        
    sd.wait()  # Espera a que termine la grabación física por completo
    print("🛑 Grabación finalizada.")
    
    # Guarda el archivo en tu disco duro
    wavfile.write(OUTPUT_FILE, FREQ, audio_data)

def enviar_al_backend():
    print(f"🚀 Enviando '{OUTPUT_FILE}' al servidor local...")
    
    if not os.path.exists(OUTPUT_FILE):
        print("❌ Error: No se encontró el archivo de audio grabado.")
        return

    # Enviamos el archivo simulando un formulario multipart/form-data
    with open(OUTPUT_FILE, "rb") as f:
        files = {"file": (OUTPUT_FILE, f, "audio/wav")}
        try:
            # Ponemos un timeout largo (60s) por si Groq o LlamaIndex tardan un poco en responder
            response = httpx.post(API_URL, files=files, timeout=60.0)
            
            if response.status_code == 200:
                print("\n✨ --- RESPUESTA DE JARVIS --- ✨")
                print(response.json())
            else:
                print(f"❌ Error en el servidor ({response.status_code}): {response.text}")
                
        except httpx.ConnectError:
            print("❌ Error: No se pudo conectar con el backend. ¿Olvidaste encender FastAPI?")
            
    # Limpieza local
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

if __name__ == "__main__":
    registrar_voz()
    enviar_al_backend()
    