import requests

def obtener_datos_artista(identificador):
    if isinstance(identificador, int) or (isinstance(identificador, str) and identificador.isdigit()):
        url = f"https://api.deezer.com/artist/{identificador}"
        r = requests.get(url).json()
        if "id" in r:
            return r
    url = f"https://api.deezer.com/search/artist?q={identificador}&limit=1"
    r = requests.get(url).json()
    datos = r.get("data", [])
    if datos:
        id_art = datos[0]["id"]
        return requests.get(f"https://api.deezer.com/artist/{id_art}").json()
    return {}

def obtener_top_canciones(id_artista):
    url = f"https://api.deezer.com/artist/{id_artista}/top?limit=10"
    respuesta = requests.get(url)
    return respuesta.json().get("data", [])

def obtener_canciones_similares(id_artista):
    url = f"https://api.deezer.com/artist/{id_artista}/radio?limit=10"
    respuesta = requests.get(url)
    return respuesta.json().get("data", [])
