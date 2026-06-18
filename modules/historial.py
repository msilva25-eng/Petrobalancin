# -*- coding: utf-8 -*-
import pandas as pd
import os
from datetime import datetime

HISTORIAL_PATH = "data/historial.csv"

COLUMNAS = [
    "Fecha y hora", "Diámetro pistón (cm)", "Longitud carrera (cm)",
    "Ciclos/min", "Eficiencia (%)", "Horas/día", "Días",
    "Tiempo activo (%)", "Producción total (L)", "Producción total (m3)",
    "Producción total (bbl)", "Meta (bbl)", "Cumple meta"
]

COLUMNAS_ANTERIORES = dict(zip([
    "Fecha y hora", "Diametro piston (cm)", "Longitud carrera (cm)",
    "Ciclos/min", "Eficiencia (%)", "Horas/dia", "Dias",
    "Tiempo activo (%)", "Produccion total (L)", "Produccion total (m3)",
    "Produccion total (bbl)", "Meta (bbl)", "Cumple meta"
], COLUMNAS))

def cargar_historial():
    os.makedirs("data", exist_ok=True)
    if os.path.exists(HISTORIAL_PATH):
        try:
            return pd.read_csv(HISTORIAL_PATH, encoding="utf-8").rename(columns=COLUMNAS_ANTERIORES)
        except Exception:
            return pd.DataFrame(columns=COLUMNAS)
    return pd.DataFrame(columns=COLUMNAS)

def guardar_en_historial(params, resultados, meta=None):
    df = cargar_historial()
    cumple = ""
    if meta and meta > 0:
        cumple = "Sí" if resultados["q_total_barriles"] >= meta else "No"

    nueva_fila = {
        "Fecha y hora":          datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Diámetro pistón (cm)":  params["diametro_cm"],
        "Longitud carrera (cm)": params["carrera_cm"],
        "Ciclos/min":            params["ciclos_min"],
        "Eficiencia (%)":        params["eficiencia_pct"],
        "Horas/día":             params["horas_dia"],
        "Días":                  params["dias"],
        "Tiempo activo (%)":     params["tiempo_activo_pct"],
        "Producción total (L)":  round(resultados["q_total_litros"], 3),
        "Producción total (m3)": round(resultados["q_total_m3"], 5),
        "Producción total (bbl)":round(resultados["q_total_barriles"], 4),
        "Meta (bbl)":            meta if meta else "",
        "Cumple meta":           cumple
    }
    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    df.to_csv(HISTORIAL_PATH, index=False, encoding="utf-8")
    return df

def borrar_historial():
    if os.path.exists(HISTORIAL_PATH):
        os.remove(HISTORIAL_PATH)
    return pd.DataFrame(columns=COLUMNAS)

def historial_a_excel():
    df = cargar_historial()
    path = "data/historial_petrobalancin.xlsx"
    df.to_excel(path, index=False)
    return path
