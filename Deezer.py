import deezer

def obtener_top_10_artista(nombre_artista):
    client = deezer.Client()
    print(f"Buscando a: {nombre_artista}...")
    resultados_busqueda = client.search_artists(nombre_artista)
    if not resultados_busqueda:
        print("No se encontro al artista.")
        return
    artista = resultados_busqueda[0]
    print(f"Artista encontrado: {artista.name} (ID: {artista.id})")
    print("-" * 30)
    top_tracks = artista.get_top()
    print(f"Top 10 canciones de {artista.name}:")
    for i, track in enumerate(top_tracks[:10], 1):
        minutos = track.duration // 60
        segundos = track.duration % 60
        print(f"{i}. {track.title}")
        print(f"   Album: {track.album.title}")
        print(f"   Duracion: {minutos}:{segundos:02d}")
        print(f"   Link: {track.link}")
        print("-" * 20)

if __name__ == "__main__":
    nombre = input("Introduce el nombre del artista: ")
    obtener_top_10_artista(nombre)
