
import streamlit as st
import pandas as pd

# Cargar base de datos desde archivo Excel
df = pd.read_excel("Leyes_base.xlsx", dtype=str).fillna("")

# Configuración de la app
st.set_page_config(page_title="Buscador Legal", layout="centered")
st.title("📘 InfoContable")

# Barra lateral para buscar por palabra clave
with st.sidebar:
    st.header("🔍 Búsqueda por palabra")
    palabra = st.text_input("Escribe una palabra clave (por ejemplo: inmueble, renta, etc.)")
    buscar = st.button("Buscar")
    limpiar = st.button("Limpiar")

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
        for _, row in resultados.iterrows():
            with st.expander(f"{row['Ley']} - Art. {row['Articulo']}"):
                st.markdown(row["Descripcion"])
# Acción para limpiar búsqueda
if limpiar:
    st.experimental_rerun()
