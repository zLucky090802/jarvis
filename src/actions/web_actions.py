import webbrowser

def search_in_browser(query: str) -> str:
    """
    Busca cualquier término, pregunta, consulta, partido de fútbol o información en tiempo real 
    directamente en el navegador web de Google. Úsala cuando no sepas la respuesta a algo.
    """
    url = f"https://www.google.com/search?q={query.strip()}"
    webbrowser.open(url)
    print(f"🌐 Jarvis abrió el navegador para buscar: '{query}'")
    return f"Éxito: He abierto tu navegador para buscar información sobre '{query}'."