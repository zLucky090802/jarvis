import os
import urllib.parse

def play_spotify_song(song_name: str) -> str:
    """
    Busca y reproduce una canción, artista, banda o álbum directo en la aplicación de escritorio de Spotify.
    Úsala SIEMPRE que el usuario te pida escuchar música, poner un tema o buscar un artista.
    Ejemplos: 'reproduce Blinding Lights', 'pon algo de Linkin Park', 'busca Feid en spotify'.
    """
    # 1. Limpiamos y formateamos el texto para que sea seguro (ej: "starboy weeknd" -> "starboy%20weeknd")
    query_encoded = urllib.parse.quote(song_name.strip())
    
    # 2. Construimos el comando nativo usando el protocolo URI de Spotify para Windows
    # Esto le ordena a la app abrirse y saltar directo al buscador interno con el tema listo
    spotify_uri = f"spotify:search:{query_encoded}"
    
    # 3. Le pedimos al sistema operativo que ejecute el protocolo de escritorio
    os.startfile(spotify_uri)
    
    print(f"🎵 Jarvis ordenó a la app de escritorio buscar: '{song_name}'")
    return f"Éxito: Abriendo la aplicación de escritorio de Spotify para reproducir '{song_name}'."