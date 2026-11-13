import random
import streamlit as st
from estetica.estilos import aplicar_estilos
from funcional.almacenamiento import (
    cargar_playlists,
    guardar_playlists,
    formatear_duracion
)
from funcional.busqueda import buscar_canciones
from funcional.tendencias import (
    obtener_top_artistas,
    obtener_elementos_chart,
    obtener_top_global
)
from funcional.generos import (
    obtener_generos_lista,
    obtener_tracks_genero
)
from funcional.artistas import (
    obtener_datos_artista,
    obtener_top_canciones,
    obtener_canciones_similares
)
from funcional.enfoque import obtener_musica_instrumental

st.set_page_config(page_title="deezer", layout="centered")
aplicar_estilos()

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "inicio"

playlists = cargar_playlists()

def normalizar_datos_track(cancion):
    art_nombre = ""
    art_id = 0
    if isinstance(cancion.get("artist"), dict):
        art_nombre = cancion["artist"].get("name", "")
        art_id = cancion["artist"].get("id", 0)
    elif isinstance(cancion.get("artist"), str):
        art_nombre = cancion.get("artist", "")
        art_id = cancion.get("artist_id", 0)

    alb_nombre = ""
    cov = ""
    if isinstance(cancion.get("album"), dict):
        alb_nombre = cancion["album"].get("title", "")
        cov = cancion["album"].get("cover_medium", "")
    elif isinstance(cancion.get("album"), str):
        alb_nombre = cancion.get("album", "")
        cov = cancion.get("cover", "")

    return {
        "id": cancion.get("id", 0),
        "title": cancion.get("title", ""),
        "artist": art_nombre,
        "artist_id": art_id,
        "album": alb_nombre,
        "duration": cancion.get("duration", 0),
        "cover": cov or cancion.get("cover", ""),
        "preview": cancion.get("preview", ""),
        "link": cancion.get("link", "")
    }

def guardar_en_playlist(nombre_pl, cancion_datos):
    if nombre_pl not in playlists:
        playlists[nombre_pl] = []
    ya_existe = any(t["id"] == cancion_datos["id"] for t in playlists[nombre_pl])
    if not ya_existe:
        playlists[nombre_pl].append(cancion_datos)
        guardar_playlists(playlists)
        st.toast(f"guardada en {nombre_pl}")
        st.rerun()
    else:
        st.toast("la cancion ya esta en la playlist")

def es_favorito(cancion_id):
    favs = playlists.get("favoritos", [])
    return any(t["id"] == cancion_id for t in favs)

def conmutar_favorito(cancion_datos):
    if "favoritos" not in playlists:
        playlists["favoritos"] = []
    favs = playlists["favoritos"]
    existe = any(t["id"] == cancion_datos["id"] for t in favs)
    if existe:
        playlists["favoritos"] = [t for t in favs if t["id"] != cancion_datos["id"]]
        guardar_playlists(playlists)
        st.toast("eliminada de favoritos")
    else:
        playlists["favoritos"].append(cancion_datos)
        guardar_playlists(playlists)
        st.toast("agregada a favoritos")
    st.rerun()

def reproducir_pista(track, lista=None, indice=0):
    st.session_state["reproduciendo_track"] = normalizar_datos_track(track)
    if lista is not None:
        st.session_state["cola_reproduccion"] = [normalizar_datos_track(t) for t in lista]
        st.session_state["cola_indice"] = indice

def cambiar_cancion_cola(direccion):
    cola = st.session_state.get("cola_reproduccion", [])
    idx = st.session_state.get("cola_indice", 0)
    if cola:
        nuevo_idx = (idx + direccion) % len(cola)
        st.session_state["cola_indice"] = nuevo_idx
        st.session_state["reproduciendo_track"] = cola[nuevo_idx]
        st.rerun()

def mostrar_item_cancion(raw_track, lista_cola=None, indice_cola=0, clave_prefijo="tr"):
    t = normalizar_datos_track(raw_track)
    col_cov, col_txt, col_ply, col_fav, col_pop = st.columns([1, 5, 1, 1, 1])
    with col_cov:
        if t.get("cover"):
            st.image(t["cover"], width=52)
    with col_txt:
        st.write(f"**{t['title']}**")
        sub = f"{t['artist']} - {formatear_duracion(t['duration'])}"
        if t.get("link"):
            sub += f" - [deezer]({t['link']})"
        st.caption(sub)
    with col_ply:
        st.write("")
        if st.button("▶", key=f"{clave_prefijo}_ply_{t['id']}_{indice_cola}"):
            reproducir_pista(t, lista_cola, indice_cola)
            st.rerun()
    with col_fav:
        st.write("")
        cor = "❤️" if es_favorito(t["id"]) else "🤍"
        if st.button(cor, key=f"{clave_prefijo}_fav_{t['id']}_{indice_cola}"):
            conmutar_favorito(t)
    with col_pop:
        st.write("")
        with st.popover("+", key=f"{clave_prefijo}_pop_{t['id']}_{indice_cola}"):
            if playlists:
                st.caption("agregar a playlist:")
                sel_p = st.selectbox("elegir", list(playlists.keys()), key=f"{clave_prefijo}_sel_{t['id']}_{indice_cola}")
                if st.button("agregar", key=f"{clave_prefijo}_add_{t['id']}_{indice_cola}"):
                    guardar_en_playlist(sel_p, t)
                st.divider()
                n_pl = st.text_input("nueva playlist", key=f"{clave_prefijo}_inp_{t['id']}_{indice_cola}", placeholder="nombre...")
                if st.button("crear y agregar", key=f"{clave_prefijo}_cadd_{t['id']}_{indice_cola}"):
                    if n_pl.strip():
                        guardar_en_playlist(n_pl.strip(), t)
            else:
                st.caption("crear primera playlist:")
                n_pl = st.text_input("nombre playlist", key=f"{clave_prefijo}_inp1_{t['id']}_{indice_cola}", placeholder="nombre...")
                if st.button("crear y agregar", key=f"{clave_prefijo}_cadd1_{t['id']}_{indice_cola}"):
                    if n_pl.strip():
                        guardar_en_playlist(n_pl.strip(), t)
    st.divider()

c_logo, c_vacio = st.columns([1, 5])
with c_logo:
    if st.button("deezer", key="btn_logo"):
        st.session_state["pagina"] = "inicio"
        st.session_state["buscar_track"] = ""
        st.session_state["artista_activo"] = None
        st.session_state["subvista_inicio"] = "tendencias"
        st.rerun()

if st.session_state.get("reproduciendo_track"):
    track_rep = st.session_state["reproduciendo_track"]
    cola = st.session_state.get("cola_reproduccion", [])
    idx_rep = st.session_state.get("cola_indice", 0)

    st.markdown('<div class="player-bar-container">', unsafe_allow_html=True)
    c_pimg, c_ptxt, c_pprev, c_pnext, c_pfav, c_pclose = st.columns([1, 4, 1, 1, 1, 1])
    with c_pimg:
        if track_rep.get("cover"):
            st.image(track_rep["cover"], width=52)
    with c_ptxt:
        st.write(f"**{track_rep['title']}**")
        st.caption(f"{track_rep['artist']}")
    with c_pprev:
        st.write("")
        if st.button("⏮", key="btn_rep_prev"):
            cambiar_cancion_cola(-1)
    with c_pnext:
        st.write("")
        if st.button("⏭", key="btn_rep_next"):
            cambiar_cancion_cola(1)
    with c_pfav:
        st.write("")
        cor = "❤️" if es_favorito(track_rep["id"]) else "🤍"
        if st.button(cor, key="btn_rep_fav"):
            conmutar_favorito(track_rep)
    with c_pclose:
        st.write("")
        if st.button("✕", key="btn_rep_close"):
            st.session_state["reproduciendo_track"] = None
            st.rerun()

    if track_rep.get("preview"):
        st.audio(track_rep["preview"], autoplay=True)
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state["pagina"] == "inicio":
    if st.session_state.get("artista_activo"):
        art_id = st.session_state["artista_activo"]
        art_datos = obtener_datos_artista(art_id)
        if art_datos:
            c_v1, c_v2 = st.columns([1, 4])
            with c_v1:
                if st.button("< volver", key="btn_art_back"):
                    st.session_state["artista_activo"] = None
                    st.rerun()

            foto_art = art_datos.get("picture_big") or art_datos.get("picture_medium") or ""
            fans = art_datos.get("nb_fan", 0)

            st.markdown(f'''
            <div class="artista-header">
                <img src="{foto_art}" width="160" height="160" />
                <div class="portada-titulo" style="font-size: 1.5rem;">{art_datos.get("name", "")}</div>
                <div style="color: #98989f; font-size: 0.85rem; margin-top: 4px;">{fans:,} fans en deezer</div>
            </div>
            ''', unsafe_allow_html=True)

            top_art = obtener_top_canciones(art_datos["id"])[:5]
            top_art_norm = [normalizar_datos_track(t) for t in top_art]

            col_top_t, col_top_b = st.columns([3, 2])
            with col_top_t:
                st.markdown('<div class="seccion-label">canciones mas populares:</div>', unsafe_allow_html=True)
            with col_top_b:
                if top_art_norm and st.button("reproducir top 5", key="btn_play_top_art"):
                    reproducir_pista(top_art_norm[0], top_art_norm, 0)
                    st.rerun()

            for idx, t in enumerate(top_art_norm):
                mostrar_item_cancion(t, top_art_norm, idx, "art_top")

    else:
        chart_datos = obtener_elementos_chart()
        albums_chart = chart_datos.get("albums", {}).get("data", [])
        tracks_chart = chart_datos.get("tracks", {}).get("data", [])

        if "album_inicio" not in st.session_state and albums_chart:
            st.session_state["album_inicio"] = random.choice(albums_chart)
        if "track_inicio" not in st.session_state and tracks_chart:
            st.session_state["track_inicio"] = random.choice(tracks_chart)

        termino = st.text_input("buscar cancion o artista", key="buscar_track", placeholder="escribe aqui...")

        artistas_top = obtener_top_artistas()
        st.caption("toca un artista para ver su perfil y canciones:")
        if artistas_top:
            fila1 = st.columns(5)
            for i, art in enumerate(artistas_top[:5]):
                with fila1[i]:
                    if st.button(art["name"], key=f"btn_art_{art['id']}"):
                        st.session_state["artista_activo"] = art["id"]
                        st.rerun()
            fila2 = st.columns(5)
            for i, art in enumerate(artistas_top[5:10]):
                with fila2[i]:
                    if st.button(art["name"], key=f"btn_art_{art['id']}"):
                        st.session_state["artista_activo"] = art["id"]
                        st.rerun()

        st.divider()

        termino_activo = termino.strip()
        if termino_activo:
            canciones = buscar_canciones(termino_activo)
            st.caption(f"resultados para: {termino_activo}")
            if not canciones:
                st.write("no se encontraron resultados.")
            else:
                norm_list = [normalizar_datos_track(c) for c in canciones]
                if st.button("reproducir resultados", key="btn_play_search"):
                    reproducir_pista(norm_list[0], norm_list, 0)
                    st.rerun()
                for idx, c in enumerate(norm_list):
                    mostrar_item_cancion(c, norm_list, idx, "search")
        else:
            if "subvista_inicio" not in st.session_state:
                st.session_state["subvista_inicio"] = "tendencias"

            sub_activa = st.session_state["subvista_inicio"]
            c_sub1, c_sub2, c_sub3 = st.columns(3)
            with c_sub1:
                txt1 = f"> tendencias" if sub_activa == "tendencias" else "tendencias"
                if st.button(txt1, key="btn_subnav_tend"):
                    st.session_state["subvista_inicio"] = "tendencias"
                    st.rerun()
            with c_sub2:
                txt2 = f"> top global" if sub_activa == "top_global" else "top global"
                if st.button(txt2, key="btn_subnav_top"):
                    st.session_state["subvista_inicio"] = "top_global"
                    st.rerun()
            with c_sub3:
                txt3 = f"> generos" if sub_activa == "generos" else "generos"
                if st.button(txt3, key="btn_subnav_gen"):
                    st.session_state["subvista_inicio"] = "generos"
                    st.rerun()

            st.write("")

            if sub_activa == "tendencias":
                album_actual = st.session_state.get("album_inicio")
                if album_actual:
                    portada_url = album_actual.get("cover_big") or album_actual.get("cover_medium") or ""
                    st.markdown(f'''
                    <div class="portada-contenedor">
                        <img src="{portada_url}" width="240" height="240" />
                        <div class="portada-titulo">{album_actual["title"]}</div>
                        <div class="portada-artista">{album_actual.get("artist", {}).get("name", "")}</div>
                    </div>
                    ''', unsafe_allow_html=True)

                total_playlists = len(playlists)
                total_canciones = sum(len(c) for c in playlists.values())
                total_segundos = sum(track["duration"] for c in playlists.values() for track in c)

                st.markdown(f'''
                <div class="stats-row">
                    <div class="stat-item">
                        <span class="stat-num">{total_playlists:02d}</span>
                        <span class="stat-label">playlists</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-num">{total_canciones:02d}</span>
                        <span class="stat-label">canciones</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-num">{formatear_duracion(total_segundos)}</span>
                        <span class="stat-label">tiempo total</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

                track_actual = st.session_state.get("track_inicio")
                if track_actual:
                    t_norm = normalizar_datos_track(track_actual)
                    puntos = track_actual.get("rank", 0)
                    c_info, c_dado = st.columns([6, 1])
                    with c_info:
                        st.markdown(f'''
                        <div class="destacado-card">
                            <div class="destacado-tag">cancion con alta popularidad</div>
                            <div class="destacado-nombre">{t_norm["title"]}</div>
                            <div style="color: #98989f; font-size: 0.84rem; margin-top: 4px;">
                                {t_norm["artist"]} - {puntos:,} puntos en deezer
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
                    with c_dado:
                        st.write("")
                        if st.button("🎲", key="btn_dado"):
                            if tracks_chart:
                                st.session_state["track_inicio"] = random.choice(tracks_chart)
                            st.rerun()

                    c_act1, c_act2, c_act3 = st.columns([2, 1, 3])
                    with c_act1:
                        if st.button("▶ reproducir", key="btn_play_dest"):
                            reproducir_pista(t_norm, [t_norm], 0)
                            st.rerun()
                    with c_act2:
                        cor = "❤️" if es_favorito(t_norm["id"]) else "🤍"
                        if st.button(cor, key="btn_fav_dest"):
                            conmutar_favorito(t_norm)

                if playlists:
                    st.markdown('<div class="seccion-label">tus listas de reproduccion:</div>', unsafe_allow_html=True)
                    for nombre_pl, canciones_pl in playlists.items():
                        dur_pl = sum(item["duration"] for item in canciones_pl)
                        etiqueta_pl = f"❤️ {nombre_pl}" if nombre_pl == "favoritos" else nombre_pl
                        st.markdown(f'''
                        <div class="playlist-item">
                            <span class="playlist-item-nombre">{etiqueta_pl}</span>
                            <span class="playlist-item-meta">{len(canciones_pl)} temas - {formatear_duracion(dur_pl)}</span>
                        </div>
                        ''', unsafe_allow_html=True)

            elif sub_activa == "top_global":
                st.markdown('<div class="seccion-label">top 10 canciones mundiales:</div>', unsafe_allow_html=True)
                if "top_global_cache" not in st.session_state:
                    st.session_state["top_global_cache"] = obtener_top_global()

                top_tracks = st.session_state["top_global_cache"]
                norm_top = [normalizar_datos_track(t) for t in top_tracks]

                if norm_top and st.button("reproducir todo el top 10", key="btn_play_all_top"):
                    reproducir_pista(norm_top[0], norm_top, 0)
                    st.rerun()

                for idx, t in enumerate(norm_top):
                    st.markdown(f'<span class="rank-badge">#{idx+1}</span>', unsafe_allow_html=True)
                    mostrar_item_cancion(t, norm_top, idx, "top_glob")

            elif sub_activa == "generos":
                st.markdown('<div class="seccion-label">explorar por genero:</div>', unsafe_allow_html=True)
                generos = obtener_generos_lista()

                if "genero_activo" not in st.session_state:
                    st.session_state["genero_activo"] = generos[0]["id"]

                gen_id_sel = st.session_state["genero_activo"]

                filas_gen = st.columns(4)
                for i, g in enumerate(generos[:4]):
                    with filas_gen[i]:
                        txt_g = f"> {g['name']}" if g["id"] == gen_id_sel else g["name"]
                        if st.button(txt_g, key=f"btn_gen_{g['id']}"):
                            st.session_state["genero_activo"] = g["id"]
                            st.session_state["cache_tracks_gen"] = None
                            st.rerun()

                filas_gen2 = st.columns(4)
                for i, g in enumerate(generos[4:]):
                    with filas_gen2[i]:
                        txt_g = f"> {g['name']}" if g["id"] == gen_id_sel else g["name"]
                        if st.button(txt_g, key=f"btn_gen_{g['id']}"):
                            st.session_state["genero_activo"] = g["id"]
                            st.session_state["cache_tracks_gen"] = None
                            st.rerun()

                if not st.session_state.get("cache_tracks_gen"):
                    st.session_state["cache_tracks_gen"] = obtener_tracks_genero(gen_id_sel)

                tracks_gen = st.session_state.get("cache_tracks_gen", [])
                norm_gen = [normalizar_datos_track(t) for t in tracks_gen]

                st.write("")
                if norm_gen and st.button("reproducir todo este genero", key="btn_play_all_gen"):
                    reproducir_pista(norm_gen[0], norm_gen, 0)
                    st.rerun()

                for idx, t in enumerate(norm_gen):
                    st.markdown(f'<span class="rank-badge">#{idx+1}</span>', unsafe_allow_html=True)
                    mostrar_item_cancion(t, norm_gen, idx, "gen_tr")

elif st.session_state["pagina"] == "enfoque":
    st.markdown('<div class="portada-titulo" style="margin-top: 1.5rem; text-align: center; font-size: 1.6rem; letter-spacing: -0.04em;">enfoque</div>', unsafe_allow_html=True)

    if "estilo_enfoque" not in st.session_state:
        st.session_state["estilo_enfoque"] = "lofi"

    estilo_sel = st.session_state["estilo_enfoque"]

    c_esp1, c_amb1, c_amb2, c_amb3, c_esp2 = st.columns([1, 2, 2, 2, 1])
    with c_amb1:
        txt_lofi = f"> lofi" if estilo_sel == "lofi" else "lofi"
        if st.button(txt_lofi, key="btn_amb_lofi"):
            st.session_state["estilo_enfoque"] = "lofi"
            st.session_state["track_enfoque"] = None
            st.rerun()
    with c_amb2:
        txt_piano = f"> piano" if estilo_sel == "piano" else "piano"
        if st.button(txt_piano, key="btn_amb_piano"):
            st.session_state["estilo_enfoque"] = "piano"
            st.session_state["track_enfoque"] = None
            st.rerun()
    with c_amb3:
        txt_ambient = f"> ambient" if estilo_sel == "ambient" else "ambient"
        if st.button(txt_ambient, key="btn_amb_ambient"):
            st.session_state["estilo_enfoque"] = "ambient"
            st.session_state["track_enfoque"] = None
            st.rerun()

    if "cache_enfoque" not in st.session_state or st.session_state.get("estilo_previo") != estilo_sel:
        st.session_state["cache_enfoque"] = obtener_musica_instrumental(estilo_sel)
        st.session_state["estilo_previo"] = estilo_sel
        if st.session_state["cache_enfoque"]:
            st.session_state["track_enfoque"] = random.choice(st.session_state["cache_enfoque"])

    pistas_enfoque = st.session_state.get("cache_enfoque", [])
    track_enf = st.session_state.get("track_enfoque")

    if track_enf:
        track_enf_datos = normalizar_datos_track(track_enf)
        c_tarjeta, c_dado_enf = st.columns([6, 1])
        with c_tarjeta:
            st.markdown(f'''
            <div class="destacado-card">
                <div class="destacado-tag">ambiente instrumental - {estilo_sel}</div>
                <div class="destacado-nombre">{track_enf_datos["title"]}</div>
                <div style="color: #98989f; font-size: 0.84rem; margin-top: 4px;">
                    {track_enf_datos["artist"]} - {formatear_duracion(track_enf_datos["duration"])}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        with c_dado_enf:
            st.write("")
            if st.button("🎲", key="btn_dado_enfoque"):
                if pistas_enfoque:
                    st.session_state["track_enfoque"] = random.choice(pistas_enfoque)
                st.rerun()

        c_enf1, c_enf2 = st.columns([1, 1])
        with c_enf1:
            if st.button("▶ reproducir", key="btn_play_enf"):
                reproducir_pista(track_enf_datos, pistas_enfoque, 0)
                st.rerun()
        with c_enf2:
            cor = "❤️" if es_favorito(track_enf_datos["id"]) else "🤍"
            if st.button(cor, key="btn_fav_enf"):
                conmutar_favorito(track_enf_datos)

        with st.popover("+ agregar a playlist", key="pop_enf_main"):
            if playlists:
                st.caption("agregar a playlist:")
                sel_pl_enf = st.selectbox("elegir playlist", list(playlists.keys()), key="sel_pop_enf")
                if st.button("agregar", key="btn_enf_add"):
                    guardar_en_playlist(sel_pl_enf, track_enf_datos)
                st.divider()
                nuevo_nom = st.text_input("o nueva playlist", key="input_pop_enf", placeholder="nombre...")
                if st.button("crear y agregar", key="btn_enf_new"):
                    if nuevo_nom.strip():
                        guardar_en_playlist(nuevo_nom.strip(), track_enf_datos)
            else:
                st.caption("crear primera playlist:")
                nuevo_nom = st.text_input("nombre de playlist", key="input_pop_enf_first", placeholder="nombre...")
                if st.button("crear y agregar", key="btn_enf_first"):
                    if nuevo_nom.strip():
                        guardar_en_playlist(nuevo_nom.strip(), track_enf_datos)

elif st.session_state["pagina"] == "playlists":
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        nuevo_nombre = st.text_input("nombre de la nueva playlist", key="input_nueva_pl", placeholder="escribe el nombre...")
    with col_btn:
        st.write("")
        st.write("")
        if st.button("crear"):
            if nuevo_nombre.strip() and nuevo_nombre not in playlists:
                playlists[nuevo_nombre] = []
                guardar_playlists(playlists)
                st.toast("playlist creada")
                st.rerun()

    st.divider()

    if not playlists:
        st.caption("no hay playlists creadas todavia.")
    else:
        pl_seleccionada = st.selectbox("seleccionar playlist", list(playlists.keys()))
        canciones_pl = playlists[pl_seleccionada]
        duracion_total = sum(c["duration"] for c in canciones_pl)

        col_info, col_play_pl, col_del = st.columns([3, 2, 1])
        with col_info:
            tit_pl = f"❤️ {pl_seleccionada}" if pl_seleccionada == "favoritos" else pl_seleccionada
            st.write(f"**{tit_pl}**")
            st.caption(f"{len(canciones_pl)} canciones - {formatear_duracion(duracion_total)} duracion total")
        with col_play_pl:
            st.write("")
            if canciones_pl and st.button("▶ reproducir lista", key="btn_play_pl_all"):
                reproducir_pista(canciones_pl[0], canciones_pl, 0)
                st.rerun()
        with col_del:
            st.write("")
            if pl_seleccionada != "favoritos":
                if st.button("eliminar"):
                    del playlists[pl_seleccionada]
                    guardar_playlists(playlists)
                    st.toast("playlist eliminada")
                    st.rerun()
            else:
                if st.button("vaciar"):
                    playlists["favoritos"] = []
                    guardar_playlists(playlists)
                    st.toast("favoritos vaciados")
                    st.rerun()

        if pl_seleccionada != "favoritos":
            c_renom, c_dupl = st.columns([3, 1])
            with c_renom:
                nom_ed = st.text_input("renombrar playlist actual", key=f"ren_{pl_seleccionada}", placeholder="escribe nuevo nombre...")
                if st.button("guardar nuevo nombre"):
                    if nom_ed.strip() and nom_ed.strip() not in playlists:
                        playlists[nom_ed.strip()] = playlists.pop(pl_seleccionada)
                        guardar_playlists(playlists)
                        st.toast("playlist renombrada")
                        st.rerun()
            with c_dupl:
                st.write("")
                st.write("")
                if st.button("duplicar playlist"):
                    copia_nom = f"{pl_seleccionada} copia"
                    playlists[copia_nom] = [dict(t) for t in canciones_pl]
                    guardar_playlists(playlists)
                    st.toast("playlist duplicada")
                    st.rerun()

        st.divider()

        filtro_pl = st.text_input("buscar en esta playlist", key="filtro_pl_input", placeholder="filtrar por cancion o artista...")
        canciones_filtradas = canciones_pl
        if filtro_pl.strip():
            f_txt = filtro_pl.strip().lower()
            canciones_filtradas = [c for c in canciones_pl if f_txt in c["title"].lower() or f_txt in c["artist"].lower()]

        if not canciones_filtradas:
            st.caption("no se encontraron canciones en esta playlist.")
        for idx, item in enumerate(canciones_filtradas):
            t_item = normalizar_datos_track(item)
            col1, col2, col_ply, col_fav, col3 = st.columns([1, 4, 1, 1, 1])
            with col1:
                if t_item.get("cover"):
                    st.image(t_item["cover"], width=50)
            with col2:
                st.write(f"**{t_item['title']}** - {t_item['artist']}")
                subtexto = f"{t_item.get('album', '')} - {formatear_duracion(t_item['duration'])}"
                if t_item.get("link"):
                    subtexto += f" - [deezer]({t_item['link']})"
                st.caption(subtexto)
            with col_ply:
                st.write("")
                if st.button("▶", key=f"pl_ply_{t_item['id']}_{idx}"):
                    reproducir_pista(t_item, canciones_pl, idx)
                    st.rerun()
            with col_fav:
                st.write("")
                cor = "❤️" if es_favorito(t_item["id"]) else "🤍"
                if st.button(cor, key=f"pl_fav_{t_item['id']}_{idx}"):
                    conmutar_favorito(t_item)
            with col3:
                st.write("")
                if st.button("quitar", key=f"del_{t_item['id']}_{idx}"):
                    canciones_pl.pop(idx)
                    guardar_playlists(playlists)
                    st.toast("cancion quitada")
                    st.rerun()

            with st.expander("canciones similares"):
                art_id = t_item.get("artist_id", 0)
                if art_id:
                    similares = obtener_canciones_similares(art_id)
                else:
                    similares = buscar_canciones(t_item["artist"])
                if not similares:
                    st.caption("no se encontraron recomendaciones.")
                for sim in similares[:4]:
                    sim_norm = normalizar_datos_track(sim)
                    c_s1, c_s2, c_s3 = st.columns([4, 1, 1])
                    with c_s1:
                        st.write(f"**{sim_norm['title']}** - {sim_norm['artist']}")
                        if sim_norm.get("preview"):
                            st.audio(sim_norm["preview"])
                    with c_s2:
                        st.caption(formatear_duracion(sim_norm.get("duration", 0)))
                    with c_s3:
                        if st.button("agregar", key=f"sim_add_{sim_norm['id']}_{idx}"):
                            guardar_en_playlist(pl_seleccionada, sim_norm)

            st.divider()

st.write("")
col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    if st.button("enfoque", key="btn_nav_enfoque"):
        st.session_state["pagina"] = "enfoque"
        st.rerun()
with col_nav2:
    if st.button("playlists", key="btn_nav_playlists"):
        st.session_state["pagina"] = "playlists"
        st.rerun()