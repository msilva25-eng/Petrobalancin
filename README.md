# Petrobalancín — Analizador técnico de capacidad petrolera

> Cada ciclo cuenta: convierte operación en producción.

## Descripcion

Aplicación web desarrollada con Streamlit para calcular la producción de petróleo
de un balancín a partir de sus parámetros de operación.

## Estructura del proyecto

```
petrobalancin/
├── app.py
├── requirements.txt
├── README.md
├── assets/
│   ├── logo_petrobalancin.png
│   └── logo_unica.png
├── data/
│   └── historial.csv
├── modules/
│   ├── __init__.py
│   ├── calculos.py
│   ├── graficas.py
│   ├── historial.py
│   ├── exportar_pdf.py
│   └── estilos.py
└── reports/
```

## Instalacion y ejecucion

```bash
cd petrobalancin
pip install -r requirements.txt
streamlit run app.py
```

## Logos

Coloca los logos en la carpeta `assets/`:
- `assets/logo_petrobalancin.png` — Logo principal de la app
- `assets/logo_unica.png` — Logo institucional de UNICA

## Funcionalidades

- Cálculo de producción en litros, m³ y barriles
- Comparación contra meta de producción
- Gráficas interactivas con Plotly
- Historial de cálculos (CSV y Excel)
- Reporte PDF con ReportLab
- Diseno responsive para movil y escritorio

## Publicacion en Streamlit Cloud

1. Sube el proyecto a GitHub.
2. Ve a https://share.streamlit.io
3. Selecciona el repositorio y el archivo `app.py`.
4. Haz clic en Deploy.
