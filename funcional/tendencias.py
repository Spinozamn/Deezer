import requests

def obtener_elementos_chart():
    url = "https://api.deezer.com/chart/0"
    respuesta = requests.get(url)
    return respuesta.json()

def obtener_top_global():
    url = "https://api.deezer.com/chart/0/tracks?limit=10"
    respuesta = requests.get(url)
    return respuesta.json().get("data", [])

def obtener_top_artistas():
    url = "https://api.deezer.com/chart/0/artists?limit=10"
    respuesta = requests.get(url)
    return respuesta.json().get("data", [])
