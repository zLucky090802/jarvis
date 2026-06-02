import subprocess
import os

APPS_COMMANDS = {
    "chrome": "start chrome",
    "edge": "start msedge",
    "spotify": "start spotify:",
    "whatsapp": "start whatsapp:",
    "calculadora": "start calc",
    "notero": "start notepad",
    "code": "start code"
}


def open_application (app_name: str):
    """Intenta abrir una aplicacion usando comandos nativos de windows"""
    
    app_name = app_name.lower().strip()
    
    if app_name in APPS_COMMANDS:
        command = APPS_COMMANDS[app_name]
        try:
            subprocess.run(command, shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            print(f'Error: no se pudo ejecutar el comando para {app_name}')
            return False
    
    else:
        print(f'la aplicacion {app_name} no esta registrada en el assitente.')
        return False
    