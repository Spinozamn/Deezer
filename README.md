# Deezer Music App

Aplicacion web interactiva de musica desarrollada en Python y Streamlit que consume la API publica de Deezer en tiempo real. Disenada con arquitectura modular, interfaz moderna y gestion local de playlists.

## Caracteristicas

* **Exploracion y Tendencias:** Portada dinamica del chart global, metricas en vivo de playlists y accesos rapidos a los artistas mas escuchados.
* **Motor de Busqueda:** Consultas en tiempo real de canciones y artistas con reseteo automatico al presionar el logotipo de Deezer.
* **Perfiles de Artista:** Consulta de foto en alta definicion, contador oficial de fans en Deezer y su Top 5 de canciones mas populares.
* **Reproductor Continuo:** Barra superior flotante con cola de reproduccion dinamica, navegacion de canciones anterior/siguiente y autoplay.
* **Favoritos Instantaneos:** Boton rapido de corazon para agregar o quitar canciones de la coleccion fija de favoritos.
* **Explorador de Generos:** Filtros musicales por estilo (Pop, Rock, Hip Hop, Electro, Reggaeton, Jazz, etc.).
* **Modo Enfoque:** Reproductor de musica instrumental sin voces (Lofi, Piano, Ambient) con dado aleatorio para sesiones de estudio o trabajo.
* **Gestion de Playlists:** Creacion, renombrado, duplicado y eliminacion de listas locales, con calculo de duracion total y recomendaciones de canciones similares mediante la radio de Deezer.

## Estructura del Proyecto

* `app.py`: Orquestador principal de la aplicacion y control del estado de sesion.
* `funcional/`:
  * `almacenamiento.py`: Lectura y persistencia local de listas en formato JSON y calculo de duraciones.
  * `busqueda.py`: Consultas acotadas a los endpoints de busqueda de Deezer.
  * `tendencias.py`: Extraccion de charts globales y rankings de popularidad.
  * `generos.py`: Catalogo de generos musicales y canciones destacadas por estilo.
  * `artistas.py`: Metadatos de artistas, canciones top y radios de similitud.
  * `enfoque.py`: Consultas parametrizadas de audio instrumental.
* `estetica/`:
  * `style.css`: Estilos visuales de la aplicacion (Apple Music Glass).
  * `estilos.py`: Inyector de estilos en Streamlit.
* `playlists.json`: Archivo local de almacenamiento de playlists del usuario.
* `iniciar.bat`: Script de inicio rapido para Windows.
* `requirements.txt`: Dependencias del proyecto.

## Instalacion y Ejecucion

1. Clonar el repositorio:
```bash
git clone https://github.com/TU_USUARIO/Deezer.git
cd Deezer
```

2. Crear y activar un entorno virtual:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Iniciar la aplicacion:
```bash
streamlit run app.py
```
O simplemente ejecutar el archivo `iniciar.bat` en Windows.
