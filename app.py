import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Indicador Vivienda – Chile", layout="wide")
st.title("Indicador de Vivienda (BCCh) – MVP")

# Cargar datos
serie = pd.read_csv("data/serie_vivienda_BCCh.csv", parse_dates=["date"])
forecast = pd.read_csv("data/forecast.csv", parse_dates=["date"])
comunas = pd.read_csv("data/tabla_comunas_base.csv", dtype=str)

# Panel lateral
with st.sidebar:
    st.header("Controles")
    horizonte = st.selectbox("Horizonte a mostrar", ["Histórico", "Forecast (1 año)", "Ambos"], index=2)

# Gráfico principal
st.subheader("Serie histórica y pronóstico")
fig = plt.figure(figsize=(9,4))
plt.plot(serie["date"], serie["value"], label="Histórico", marker="o", linewidth=1)
if horizonte in ["Forecast (1 año)", "Ambos"]:
    fut = forecast[forecast["y_real"].isna()]
    plt.plot(fut["date"], fut["y_pred"], "--", color="crimson", label="Pronóstico (futuro)")
plt.xlabel("Fecha")
plt.ylabel("Índice")
plt.grid(True, linestyle="--", alpha=0.4)
plt.legend()
st.pyplot(fig)

# Descargar forecast
st.download_button("⬇️ Descargar forecast.csv",
                   forecast.to_csv(index=False).encode("utf-8"),
                   "forecast.csv", "text/csv")

# Info
st.divider()
st.write(f"**Observaciones históricas:** {len(serie)}")
st.write(f"**Filas en tabla comunas:** {len(comunas)}")
st.caption("Fuente: Banco Central de Chile y SUBDERE 2023. MVP demostrativo.")