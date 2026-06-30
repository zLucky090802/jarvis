import sounddevice as sd
from scipy.io import wavfile
import numpy as np
import httpx
import os
import time

FREQ = 44100
API_URL = "http://127.0.0.1:8000/upload"
OUTPUT_FILE = "comando_jarvis.wav"

# --- Calibración Avanzada de Umbrales ---
UMBRAL_VOZ = 600          # Ajustalo si tu entorno es ruidoso
CHUNK_DURATION = 0.1      # Procesamos el audio en bloques de 100ms
SILENCE_TIMEOUT = 1.5     # Segundos de silencio para asumir que terminaste de hablar
MAX_DURATION = 15         # Tiempo máximo de seguridad por si te olvidas el micro abierto

def obtener_rms(audio_chunk) -> float:
    return np.sqrt(np.mean(audio_chunk.astype(np.float32) ** 2))

def capturar_y_procesar_comando() -> np.ndarray:
    chunk_samples = int(FREQ * CHUNK_DURATION)
    audio_frames = []
    
    # Flags de control de estado
    hablando = False
    inicio_silencio = None
    inicio_grabacion = time.time()
    
    print("👂 Escuchando... (Habla para activar Jarvis)")
    
    # Creamos un stream de entrada continuo y sin bloqueos pesados
    with sd.InputStream(samplerate=FREQ, channels=1, dtype='int16') as stream:
        while True:
            # Leemos el chunk actual del buffer de la tarjeta de sonido
            chunk, _ = stream.read(chunk_samples)
            rms = obtener_rms(chunk)
            
            # Control de tiempo máximo de seguridad
            if time.time() - inicio_grabacion > MAX_DURATION:
                print("🛑 Tiempo máximo alcanzado.")
                break
                
            if not hablando:
                # --- ESTADO 1: ESPERANDO ACTIVACIÓN ---
                if rms > UMBRAL_VOZ:
                    hablando = True
                    audio_frames.append(chunk)
                    inicio_grabacion = time.time() # Seteamos el tiempo real de la frase
                    print("🗣️ ¡Te escucho! Grabando... ", end="", flush=True)
            else:
                # --- ESTADO 2: GRABANDO FRASE ---
                audio_frames.append(chunk)
                
                if rms < UMBRAL_VOZ:
                    if inicio_silencio is None:
                        inicio_silencio = time.time()
                    elif time.time() - inicio_silencio > SILENCE_TIMEOUT:
                        print("\n🔇 Silencio detectado. Procesando comando...")
                        break
                else:
                    # Si vuelve a haber ruido/voz, reseteamos el temporizador de silencio
                    if inicio_silencio is not None:
                        print("✍️...", end="", flush=True) # Feedback visual de que sigues hablando
                    inicio_silencio = None

    # Concatenamos todos los chunks acumulados durante la frase
    return np.concatenate(audio_frames, axis=0) if audio_frames else None

def enviar_al_backend(audio_data: np.ndarray):
    if audio_data is None or len(audio_data) == 0:
        return
        
    wavfile.write(OUTPUT_FILE, FREQ, audio_data)
    print("🚀 Enviando comando a Jarvis...")

    with open(OUTPUT_FILE, "rb") as f:
        files = {"file": (OUTPUT_FILE, f, "audio/wav")}
        try:
            response = httpx.post(API_URL, files=files, timeout=60.0)
            if response.status_code == 200:
                result = response.json()
                print(f"\n✨ Jarvis: {result.get('agent_response')}\n")
            else:
                print(f"❌ Error ({response.status_code}): {response.text}")
        except httpx.ConnectError:
            print("❌ Backend no disponible.")
            time.sleep(2)

    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

if __name__ == "__main__":
    print("🤖 Jarvis Inteligente Activo. CTRL+C para apagar.")
    print(f"📊 Umbral base: {UMBRAL_VOZ} RMS | Tolerancia Silencio: {SILENCE_TIMEOUT}s\n")
    try:
        while True:
            audio = capturar_y_procesar_comando()
            enviar_al_backend(audio)
            print("🔄 Listo para el siguiente comando...\n")
    except KeyboardInterrupt:
        print("\n👋 Jarvis apagado.")