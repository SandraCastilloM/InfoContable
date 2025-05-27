
import streamlit as st
import pandas as pd

# Cargar base de datos desde archivo Excel
df = pd.read_excel("Leyes_base.xlsx", dtype=str).fillna("")

# Configuración de la app
st.set_page_config(page_title="Buscador Legal", layout="centered")
st.title("📘 InfoContable")

# Barra lateral para buscar por palabra clave
# Encabezado y autor
st.markdown("*Desarrollado por Sandra Castillo Muñoz*")
st.markdown("### 🔍 Buscar por palabra clave")


# Búsqueda superior
col1, col2, col3 = st.columns([4, 1, 1])
with col1:
    palabra = st.text_input("Palabra clave (ej: inmueble, renta...)", key="palabra")
with col2:
    buscar = st.button("Buscar", use_container_width=True)
with col3:
    limpiar = st.button("Limpiar", use_container_width=True)

# Acción para limpiar búsqueda
if limpiar:
    st.rerun()

# Menú desplegable por ley
st.subheader("📚  ¿Qué ley estás buscando?")

leyes = sorted(df["Ley"].dropna().unique())
ley_seleccionada = st.selectbox("Selecciona una ley:", ["-- Selecciona --"] + leyes)

articulo_seleccionado = ""
if ley_seleccionada != "-- Selecciona --":
    articulos = df[df["Ley"] == ley_seleccionada]["Articulo"].unique()
    articulo_seleccionado = st.selectbox("Selecciona un artículo:", ["-- Selecciona --"] + list(articulos))

# Mostrar contenido del artículo seleccionado
if articulo_seleccionado and articulo_seleccionado != "-- Selecciona --":
    resultado = df[(df["Ley"] == ley_seleccionada) & (df["Articulo"] == articulo_seleccionado)]
    if not resultado.empty:
        st.markdown("### 📄 Artículo Seleccionado")
        st.markdown(f"**{resultado.iloc[0]['Ley']} - Artículo {resultado.iloc[0]['Articulo']}**")
        st.markdown(resultado.iloc[0]["Descripcion"])

# Mostrar resultados de búsqueda por palabra clave
if buscar and palabra:
    resultados = df[df["Descripcion"].str.contains(palabra, case=False, na=False)]
    st.subheader(f"🔎 Resultados para: '{palabra}'")
    if resultados.empty:
        st.info("No se encontraron artículos con esa palabra.")
    else:
        import re

    for i, row in resultados.iterrows():
        texto = row["Descripcion"]
        if palabra:
            # Resaltar palabra buscada (respetando mayúsculas/minúsculas)
            texto = re.sub(
                f"({re.escape(palabra)})",
                r"<span style='background-color: yellow; font-weight: bold;'>\1</span>",
                texto,
                flags=re.IGNORECASE
            )
        with st.expander(f"Resultado {i+1}: {row['Ley']} - Art. {row['Articulo']}"):
            st.markdown(texto, unsafe_allow_html=True)

# Acción para limpiar búsqueda
if limpiar:
    st.rerun()
