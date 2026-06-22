import sounddevice as sd
from scipy.io import wavfile
import numpy as np
import httpx
import os
import time

FREQ = 44100
OUTPUT_FILE = "prueba_micro.wav"
API_URL = "http://127.0.0.1:8000/upload"

# --- Calibra estos valores ---
UMBRAL_VOZ = 800
SEGUNDOS_PARA_ACTIVAR = 0.5
DURACION_COMANDO = 4
TOLERANCIA_SILENCIO = 2
# -----------------------------

def obtener_rms(audio_chunk) -> float:
    return np.sqrt(np.mean(audio_chunk.astype(np.float32) ** 2))

def esperar_voz_humana() -> bool:
    CHUNK = int(FREQ * 0.1)
    chunks_con_voz = 0
    chunks_silencio = 0
    chunks_necesarios = int(SEGUNDOS_PARA_ACTIVAR / 0.1)

    print("👂 Esperando voz... (habla para activar Jarvis)")

    while True:
        chunk = sd.rec(CHUNK, samplerate=FREQ, channels=1, dtype='int16')
        sd.wait()
        rms = obtener_rms(chunk)

        if rms > UMBRAL_VOZ:
            chunks_con_voz += 1
            chunks_silencio = 0
            print(f"🗣️ Voz detectada ({chunks_con_voz}/{chunks_necesarios}) RMS: {rms:.0f}")
            if chunks_con_voz >= chunks_necesarios:
                return True
        else:
            chunks_silencio += 1
            if chunks_silencio > TOLERANCIA_SILENCIO:
                if chunks_con_voz > 0:
                    print("🔇 Reseteando...")
                chunks_con_voz = 0
                chunks_silencio = 0

def registrar_comando() -> np.ndarray:
    print(f"🎙️ ¡Habla! Grabando {DURACION_COMANDO} segundos...")
    audio = sd.rec(int(DURACION_COMANDO * FREQ), samplerate=FREQ, channels=1, dtype='int16')
    for i in range(DURACION_COMANDO, 0, -1):
        print(f"⏱️ {i}s...")
        time.sleep(1)
    sd.wait()
    print("🛑 Grabación finalizada.")
    return audio

def enviar_al_backend(audio_data: np.ndarray):
    wavfile.write(OUTPUT_FILE, FREQ, audio_data)
    print("🚀 Enviando comando a Jarvis...")

    with open(OUTPUT_FILE, "rb") as f:
        files = {"file": (OUTPUT_FILE, f, "audio/wav")}
        try:
            response = httpx.post(API_URL, files=files, timeout=60.0)
            if response.status_code == 200:
                result = response.json()
                print(f"\n✨ Jarvis: {result.get('agent_response')}")
            else:
                print(f"❌ Error ({response.status_code}): {response.text}")
        except httpx.ConnectError:
            print("❌ Backend no disponible.")
            time.sleep(3)

    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

if __name__ == "__main__":
    print("🤖 Jarvis listo. CTRL+C para salir.")
    print(f"📊 Umbral de voz configurado en: {UMBRAL_VOZ} RMS\n")
    try:
        while True:
            esperar_voz_humana()
            audio = registrar_comando()
            enviar_al_backend(audio)
            print("\n🔄 Listo para el siguiente comando...\n")
    except KeyboardInterrupt:
        print("\n👋 Jarvis apagado.")