import subprocess
import os

STORE_APPS = ["whatsapp", "spotify", "netflix", "instagram", "facebook", "xbox", 'discord']
ALIASES = {
    "wsp": "whatsapp",
    "musica": "spotify",
    "editor": "code",
    "bloc de notas": "notepad",
    "calculadora": "calc",
    "google": "chrome",  #  Añade esto
    "chrome": "chrome"   #  Añade esto
}

def open_application (app_name: str):
    """Automatiza por completo el comando 'start'. Detecta si la app requiere
    el formato de la Microsoft Store (con ':') o si es un comando directo."""
    
    target = app_name.lower().strip()
    target = ALIASES.get(target, target)
    
  

    try:
        subprocess.run(f'start {target}', shell=True, check=True)
        print(f'jarvios: abriendo {target.capitalize()}')
        return True
    except subprocess.CalledProcessError:
        try:
            subprocess.run(f'start {target}:', shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            print(f"Error: No encontré ninguna aplicación o comando llamado '{target}' en el sistema.")
            return False
    

    