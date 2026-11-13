import requests

def buscar_canciones(termino):
    url = f"https://api.deezer.com/search?q={termino}&limit=10"
    respuesta = requests.get(url)
    return respuesta.json().get("data", [])

def buscar_artistas(termino):
    url = f"https://api.deezer.com/search/artist?q={termino}&limit=5"
    respuesta = requests.get(url)
    return respuesta.json().get("data", [])
