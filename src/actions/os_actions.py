import subprocess
import os

STORE_APPS = ["whatsapp", "spotify", "netflix", "instagram", "facebook", "xbox", 'discord']
ALIASES = {
    "wsp": "whatsapp",
    "musica": "spotify",
    "editor": "code",
    "bloc de notas": "notepad",
    "calculadora": "calc"
}

def open_application (app_name: str):
    """Automatiza por completo el comando 'start'. Detecta si la app requiere
    el formato de la Microsoft Store (con ':') o si es un comando directo."""
    
    target = app_name.lower().strip()
    target = ALIASES.get(target, target)
    
    if target in STORE_APPS:
        windows_command = f'{target}:'
        
    else:
        windows_command = target
        
    final_command = f' start {windows_command}'

    try:
        subprocess.run(final_command, shell=True, check=True)
        print(f'jarvios: abriendo {target.capitalize()}')
        return True
    except subprocess.CalledProcessError:
        print(f'jarvis: no encontre ninguna app o comando llamado {windows_command}')
        return False
    

    