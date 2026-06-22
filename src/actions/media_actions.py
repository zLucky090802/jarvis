import os
import urllib.parse
import time
import pyautogui
import pygetwindow as gw

def play_spotify_song(song_name: str) -> str:
    """
    Busca y reproduce una canción, artista o álbum directo 
    en la aplicación de escritorio de Spotify para Windows.
    """
    try:
        # 1. Lanzamos el buscador de Spotify de escritorio con el protocolo nativo
        query_encoded = urllib.parse.quote(song_name.strip())
        spotify_uri = f"spotify:search:{query_encoded}"
        os.startfile(spotify_uri)
        
        # 2. Esperamos un tiempo prudente para que carguen los resultados en pantalla
        print("⏳ Esperando que Spotify cargue el resultado...")
        time.sleep(2.5) 
        
        # 3. Traemos la ventana al frente de forma obligatoria
        try:
            spotify_windows = gw.getWindowsWithTitle('Spotify')
            if spotify_windows:
                spotify_win = spotify_windows[0]
                if spotify_win.isMinimized:
                    spotify_win.restore()
                spotify_win.activate()
                print("🎯 Ventana de Spotify enfocada.")
                time.sleep(0.5)
        except Exception as win_err:
            print(f"⚠️ Alerta de foco: {win_err}")

        # 4. SELECCIÓN DIRECTA DEL RESULTADO
        print("🎛️ Navegando al primer resultado...")
        pyautogui.press('tab')
        time.sleep(0.3)
        
        pyautogui.press('enter')
        time.sleep(0.5)
        
        pyautogui.press('enter')
        
        print(f"Jarvis forzó la reproducción del nuevo resultado: '{song_name}'")
        
        # 🚨 LA SALIDA INMEDIATA: Cortamos cualquier ejecución posterior aquí mismo
        return f"TAREA_COMPLETADA. '{song_name}' está reproduciéndose en Spotify. No se requiere ninguna acción adicional."

    except Exception as e:
        print(f"❌ ERROR CRÍTICO dentro de play_spotify_song: {e}")
        return f"Error en la herramienta de música: {str(e)}"