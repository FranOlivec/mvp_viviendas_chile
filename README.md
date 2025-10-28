# Indicador de Vivienda – Chile (MVP)

App simple en Streamlit que muestra la serie nacional del Banco Central
(stock de viviendas nuevas) y un pronóstico SARIMAX a 1 año.

## Estructura
- app.py
- requirements.txt
- data/
    - serie_vivienda_BCCh.csv
    - forecast.csv
    - tabla_comunas_base.csv
 ---

## Descripción del proyecto

Este proyecto es un **MVP (producto mínimo viable)** desarrollado por **Francisca Olivares** como demostración de análisis y modelado de datos abiertos en Chile.  
El objetivo es **visualizar y proyectar el comportamiento del stock nacional de viviendas nuevas**, utilizando información pública del **Banco Central de Chile (BCCh)** y la **Subsecretaría de Desarrollo Regional (SUBDERE)**.

La aplicación combina:
- **Extracción de datos desde API REST del Banco Central de Chile**  
- **Limpieza y análisis exploratorio (EDA) con Python**  
- **Modelado temporal SARIMAX** para generar pronósticos trimestrales a 1 año  
- **Visualización interactiva** mediante **Streamlit**

El resultado es una app ligera y funcional que permite:
- Analizar la evolución histórica del stock nacional de viviendas nuevas.  
- Visualizar la proyección estadística a corto plazo.  
- Descargar los resultados para su uso en análisis complementarios o reportes.

---

## Objetivo y proyección

El propósito de este MVP es **mostrar el potencial del uso de datos abiertos y técnicas de machine learning** para apoyar la toma de decisiones en el ámbito habitacional y territorial.  
En futuras versiones, se contempla extender el modelo a nivel regional y comunal, incorporando variables como precios, permisos de edificación y densidad poblacional.

---

## 👩‍💻 **Autora**

**Francisca Olivares Vecchiola**  
🌱 Ingeniera Ambiental & Data Scientist  
💡 Enfocada en sostenibilidad, datos abiertos y ciencia aplicada.  
📫 [LinkedIn](https://www.linkedin.com/in/franciscaolivaresvecchiola/)  

📊 *Proyecto demostrativo de análisis predictivo con datos abiertos de Chile.*
