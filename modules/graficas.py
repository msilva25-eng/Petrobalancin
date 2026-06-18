# -*- coding: utf-8 -*-
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

AMARILLO = "#F2A900"
NEGRO    = "#111827"
GRIS     = "#374151"
VERDE    = "#16A34A"
ROJO     = "#DC2626"

def _layout(titulo):
    return dict(
        title=dict(text=titulo, font=dict(size=14, color=NEGRO)),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(color=GRIS, size=11),
        margin=dict(l=40, r=20, t=50, b=40),
    )

def grafica_produccion_diaria(q_dia_litros, dias):
    dias_arr = list(range(1, dias + 1))
    acum     = [q_dia_litros * d for d in dias_arr]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dias_arr, y=acum,
        mode="lines+markers",
        line=dict(color=AMARILLO, width=2),
        marker=dict(size=4),
        name="Producción acumulada (L)"
    ))
    fig.update_layout(
        **_layout("Producción acumulada por día"),
        xaxis_title="Días",
        yaxis_title="Litros",
    )
    return fig

def grafica_por_hora(q_hora_litros, horas_dia, tiempo_activo_pct):
    horas = list(range(1, int(horas_dia) + 1))
    ta    = tiempo_activo_pct / 100
    prod  = [q_hora_litros * ta * h for h in horas]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=horas, y=prod,
        marker_color=AMARILLO,
        name="Producción por hora (L)"
    ))
    fig.update_layout(
        **_layout("Producción acumulada por hora de operación"),
        xaxis_title="Hora",
        yaxis_title="Litros",
    )
    return fig

def grafica_comparacion_unidades(litros, m3, barriles):
    fig = go.Figure(go.Bar(
        x=["Litros", "m³", "Barriles"],
        y=[litros, m3, barriles],
        marker_color=[AMARILLO, NEGRO, GRIS],
        text=[f"{litros:,.1f}", f"{m3:,.4f}", f"{barriles:,.3f}"],
        textposition="outside",
    ))
    fig.update_layout(**_layout("Producción total por unidad de medida"))
    return fig

def grafica_meta(produccion_bbl, meta_bbl):
    pct = min((produccion_bbl / meta_bbl) * 100, 100)
    color = VERDE if produccion_bbl >= meta_bbl else ROJO
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=produccion_bbl,
        delta={"reference": meta_bbl},
        number={"suffix": " bbl"},
        gauge={
            "axis": {"range": [0, meta_bbl * 1.2]},
            "bar":  {"color": color},
            "threshold": {
                "line": {"color": NEGRO, "width": 3},
                "thickness": 0.75,
                "value": meta_bbl,
            },
        },
        title={"text": "Cumplimiento de meta (bbl)"},
    ))
    fig.update_layout(**_layout("Comparación con la meta de producción"))
    return fig

def grafica_sensibilidad(diametro, carrera, eficiencia, horas, dias, tiempo_activo):
    import math
    ciclos_range = np.linspace(1, 30, 30)
    producciones = []
    for c in ciclos_range:
        r = math.pi * (diametro / 2) ** 2
        v = (r * carrera / 1000) * (eficiencia / 100) * c * 60 * horas * (tiempo_activo / 100) * dias
        producciones.append(v / 158.987)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ciclos_range, y=producciones,
        mode="lines",
        line=dict(color=AMARILLO, width=2),
        name="Producción (bbl)"
    ))
    fig.update_layout(
        **_layout("Sensibilidad: producción vs. ciclos por minuto"),
        xaxis_title="Ciclos por minuto",
        yaxis_title="Producción total (bbl)",
    )
    return fig
