import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from functools import lru_cache

st.set_page_config(page_title="Indicador Vivienda – Chile (v2.1)", layout="wide")

# =========================
# Utilidades y carga de datos
# =========================
@st.cache_data
def load_csv(path, parse_dates=None, dtype=None):
    return pd.read_csv(path, parse_dates=parse_dates, dtype=dtype)

@st.cache_data
def enrich_series(df: pd.DataFrame) -> pd.DataFrame:
    """Añade variaciones y medias móviles a la serie nacional."""
    s = df.copy()
    s = s.sort_values("date").reset_index(drop=True)
    s["value"] = pd.to_numeric(s["value"], errors="coerce")
    # Variaciones
    s["var_qoq_%"] = s["value"].pct_change() * 100
    s["var_yoy_%"] = s["value"].pct_change(4) * 100
    # Medias móviles (4 y 8 trimestres)
    s["mm_4t"] = s["value"].rolling(4).mean()
    s["mm_8t"] = s["value"].rolling(8).mean()
    return s

# =========================
# Carga
# =========================
serie = load_csv("data/serie_vivienda_BCCh.csv", parse_dates=["date"])
forecast = load_csv("data/forecast.csv", parse_dates=["date"])
comunas = load_csv("data/tabla_comunas_base.csv", dtype=str)

serie_enriched = enrich_series(serie)

# =========================
# Sidebar (controles)
# =========================
with st.sidebar:
    st.header("Controles")
    horizonte = st.selectbox("Horizonte a mostrar", ["Histórico", "Forecast (1 año)", "Ambos"], index=2)
    suavisado = st.selectbox("Suavizado (media móvil)", ["Sin suavizado", "4 trimestres", "8 trimestres"], index=0)
    st.divider()
    st.caption("Exploración territorial")
    regiones = ["(todas)"] + sorted(comunas["NOM_REG"].dropna().unique().tolist())
    region_sel = st.selectbox("Región", regiones, index=0)
    st.caption("Fuente: Banco Central de Chile (BCCh) y SUBDERE 2023.")

st.title("Indicador de Vivienda – Chile (v2.1)")

# =========================
# KPIs
# =========================
last_row = serie_enriched.dropna(subset=["value"]).iloc[-1]
last_val = last_row["value"]
last_date = last_row["date"].date()

qoq = serie_enriched["var_qoq_%"].iloc[-1]
yoy = serie_enriched["var_yoy_%"].iloc[-1]

colA, colB, colC, colD = st.columns(4)
colA.metric("Último valor", f"{last_val:,.2f}", help=f"Fecha: {last_date}")
colB.metric("Δ trimestral (QoQ)", f"{qoq:+.2f} %")
colC.metric("Δ interanual (YoY)", f"{yoy:+.2f} %")
colD.metric("Observaciones históricas", f"{len(serie)}")

# =========================
# Gráfico principal (Plotly)
# =========================
st.subheader("Serie histórica y pronóstico del stock de viviendas nuevas en Chile")

df_plot = serie_enriched[["date", "value", "mm_4t", "mm_8t"]].copy()
fig = px.line(
    df_plot,
    x="date",
    y="value",
    labels={
        "date": "Fecha",
        "value": "Evolución del stock de viviendas nuevas"
    },
    title=None
)
fig.update_traces(name="Histórico", showlegend=True)

# Suavizado
if suavisado == "4 trimestres":
    fig.add_scatter(
        x=df_plot["date"], y=df_plot["mm_4t"], mode="lines",
        name="Media móvil (4T)", line=dict(dash="dash")
    )
elif suavisado == "8 trimestres":
    fig.add_scatter(
        x=df_plot["date"], y=df_plot["mm_8t"], mode="lines",
        name="Media móvil (8T)", line=dict(dash="dot")
    )

# Forecast
if horizonte in ["Forecast (1 año)", "Ambos"] and not forecast.empty:
    fut = forecast[forecast["y_real"].isna()].copy()
    if not fut.empty:
        fig.add_scatter(
            x=fut["date"], y=fut["y_pred"], mode="lines",
            name="Pronóstico (futuro)", line=dict(color="crimson", dash="dash")
        )

fig.update_layout(height=420, legend_title_text="")
st.plotly_chart(fig, use_container_width=True)

# =========================
# Descargas
# =========================
st.subheader("Descargas")
col1, col2 = st.columns(2)
with col1:
    st.download_button("⬇️ Descargar forecast.csv",
                       forecast.to_csv(index=False).encode("utf-8"),
                       "forecast.csv", "text/csv")
with col2:
    st.download_button("⬇️ Descargar serie_enriquecida.csv",
                       serie_enriched.to_csv(index=False).encode("utf-8"),
                       "serie_enriquecida.csv", "text/csv")

# =========================
# Exploración territorial (tabla simple por región)
# =========================
st.divider()
st.subheader("Exploración territorial (SUBDERE 2023)")

if region_sel != "(todas)":
    df_reg = comunas[comunas["NOM_REG"] == region_sel].copy()
    st.write(f"**Región seleccionada:** {region_sel} — Comunas: {len(df_reg)}")
    st.dataframe(df_reg[["COD_COM", "NOM_COM", "COD_PROV", "NOM_PROV"]]
                 .sort_values(["NOM_PROV", "NOM_COM"])
                 .reset_index(drop=True), use_container_width=True, height=320)
else:
    st.write(f"**Todas las regiones** — Comunas: {len(comunas)}")
    st.dataframe(comunas[["COD_REG", "NOM_REG", "COD_COM", "NOM_COM"]]
                 .sort_values(["COD_REG", "COD_COM"])
                 .reset_index(drop=True), use_container_width=True, height=320)

st.caption("Esta sección usa la división político-administrativa (SUBDERE 2023). En futuras versiones puede integrarse forecast por región/comuna.")
