import requests

def obtener_musica_instrumental(estilo):
    url = f"https://api.deezer.com/search?q={estilo}+instrumental&limit=15"
    respuesta = requests.get(url)
    return respuesta.json().get("data", [])
