import os
import streamlit as st

def aplicar_estilos():
    ruta_css = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(ruta_css):
        with open(ruta_css, "r", encoding="utf-8") as archivo:
            st.markdown(f"<style>{archivo.read()}</style>", unsafe_allow_html=True)
