import requests

def obtener_generos_lista():
    return [
        {"id": 132, "name": "pop"},
        {"id": 152, "name": "rock"},
        {"id": 116, "name": "hip hop"},
        {"id": 106, "name": "electro"},
        {"id": 122, "name": "reggaeton"},
        {"id": 165, "name": "r&b"},
        {"id": 85, "name": "alternativo"},
        {"id": 129, "name": "jazz"}
    ]

def obtener_tracks_genero(id_genero):
    url = f"https://api.deezer.com/chart/{id_genero}/tracks?limit=10"
    respuesta = requests.get(url)
    return respuesta.json().get("data", [])
