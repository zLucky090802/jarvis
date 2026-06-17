def search_in_browser(query: str) -> str:
    """Busca cualquier término directo en el navegador web predeterminado."""
    import webbrowser
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Buscando '{query}' en el navegador."