import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# 🎨 Configuración del Dashboard
# ==============================
st.set_page_config(page_title="Dashboard FUNCREDES", layout="wide")

# 📌 Colores institucionales
COLOR_PRIMARIO = "#003366"   # Azul oscuro
COLOR_SECUNDARIO = "#4CAF50" # Verde
COLOR_ACENTO = "#FF9800"     # Naranja

# 🖼️ Logotipo FUNCREDES
st.image("logo_funcredes.png", width=180)
st.markdown(
    f"<h1 style='color:{COLOR_PRIMARIO};text-align:center;'>Dashboard Interactivo - FUNCREDES</h1>",
    unsafe_allow_html=True
)
st.write("---")

# 📂 Cargar el archivo Excel
excel_file = "EXPERIENCIAS  FUNCREDES - GLOBAL DE LAS AMERICAS...xlsx"
xls = pd.ExcelFile(excel_file)
sheets = xls.sheet_names

# 📌 Menú lateral
st.sidebar.image("logo_funcredes.png", width=120)
st.sidebar.markdown("## Menú de Navegación")
selected_sheet = st.sidebar.selectbox("Selecciona un área de trabajo", sheets)

# 📂 Cargar la hoja seleccionada
df = pd.read_excel(excel_file, sheet_name=selected_sheet)
df = df.dropna(how="all")  # eliminar filas vacías
df.columns = [str(c).strip() for c in df.columns]  # limpiar nombres de columnas

st.subheader(f"📂 Área seleccionada: {selected_sheet}")

# 🔍 Filtros dinámicos
with st.expander("🎛️ Filtros"):
    for col in df.columns:
        unique_vals = df[col].dropna().unique()
        if len(unique_vals) > 1 and len(unique_vals) < 50:
            selected_vals = st.multiselect(f"Filtrar por {col}", unique_vals)
            if selected_vals:
                df = df[df[col].isin(selected_vals)]

# 📋 Tabla de datos
st.dataframe(df, use_container_width=True)

# ==============================
# 📊 Sección de Resumen
# ==============================
st.markdown(f"<h3 style='color:{COLOR_PRIMARIO};'>📌 Resumen General</h3>", unsafe_allow_html=True)
cols = st.columns(3)

cols[0].markdown(
    f"<div style='background-color:{COLOR_PRIMARIO};padding:15px;border-radius:10px;text-align:center;color:white;'>"
    f"<h4>Total de Registros</h4><h2>{len(df)}</h2></div>", unsafe_allow_html=True
)
cols[1].markdown(
    f"<div style='background-color:{COLOR_SECUNDARIO};padding:15px;border-radius:10px;text-align:center;color:white;'>"
    f"<h4>Columnas</h4><h2>{len(df.columns)}</h2></div>", unsafe_allow_html=True
)
cols[2].markdown(
    f"<div style='background-color:{COLOR_ACENTO};padding:15px;border-radius:10px;text-align:center;color:white;'>"
    f"<h4>Valores Nulos</h4><h2>{df.isna().sum().sum()}</h2></div>", unsafe_allow_html=True
)

# ==============================
# 📈 Visualización de Datos
# ==============================
st.markdown(f"<h3 style='color:{COLOR_PRIMARIO};'>📊 Visualización de Datos</h3>", unsafe_allow_html=True)

cat_cols = df.select_dtypes(include="object").columns
num_cols = df.select_dtypes(include="number").columns

if len(cat_cols) > 0:
    cat_col = st.selectbox("Selecciona una variable categórica", cat_cols)
    chart = px.histogram(df, x=cat_col, title=f"Distribución de {cat_col}",
                         color_discrete_sequence=[COLOR_SECUNDARIO])
    st.plotly_chart(chart, use_container_width=True)

if len(num_cols) > 0:
    num_col = st.selectbox("Selecciona una variable numérica", num_cols)
    chart = px.box(df, y=num_col, title=f"Distribución de {num_col}",
                   color_discrete_sequence=[COLOR_ACENTO])
    st.plotly_chart(chart, use_container_width=True)

# ==============================
# 🌍 Mapa Interactivo
# ==============================
if {"Latitud", "Longitud"}.issubset(df.columns):
    st.markdown(f"<h3 style='color:{COLOR_PRIMARIO};'>🌍 Mapa de Proyectos</h3>", unsafe_allow_html=True)
    fig_map = px.scatter_mapbox(
        df,
        lat="Latitud",
        lon="Longitud",
        hover_name=df.columns[0],
        hover_data=df.columns,
        color_discrete_sequence=[COLOR_SECUNDARIO],
        zoom=5,
        height=500
    )
    fig_map.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig_map, use_container_width=True)

# ==============================
# 📥 Descargar datos
# ==============================
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Descargar datos filtrados en CSV",
    data=csv,
    file_name=f"{selected_sheet}_filtrado.csv",
    mime="text/csv",
)
