import json
import os

def cargar_playlists():
    if not os.path.exists("playlists.json"):
        return {}
    with open("playlists.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

def guardar_playlists(playlists):
    with open("playlists.json", "w", encoding="utf-8") as archivo:
        json.dump(playlists, archivo, indent=2, ensure_ascii=False)

def formatear_duracion(segundos):
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segs = segundos % 60
    if horas > 0:
        return f"{horas}h {minutos:02d}m {segs:02d}s"
    return f"{minutos}:{segs:02d}"
