# -*- coding: utf-8 -*-
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

AMARILLO = "#FFCD11"
NEGRO    = "#1A1A1A"
GRIS     = "#626A70"
VERDE    = "#16A34A"
ROJO     = "#DC2626"

def _layout(titulo):
    return dict(
        title=dict(
            text=titulo, x=0.5, xanchor="center",
            font=dict(size=15, color=NEGRO, family="Arial, sans-serif")
        ),
        plot_bgcolor="#FBFBF9",
        paper_bgcolor="#FBFBF9",
        font=dict(color=NEGRO, size=12, family="Arial, sans-serif"),
        height=470,
        margin=dict(l=82, r=22, t=82, b=82),
        xaxis=dict(
            color=NEGRO,
            title_font=dict(color=NEGRO, size=13, family="Arial, sans-serif"),
            tickfont=dict(color=NEGRO, size=12, family="Arial, sans-serif"),
            gridcolor="#D9DBD8",
            linecolor=NEGRO,
            linewidth=1.5,
            zerolinecolor="#A7ACA8",
            automargin=True,
        ),
        yaxis=dict(
            color=NEGRO,
            title_font=dict(color=NEGRO, size=13, family="Arial, sans-serif"),
            tickfont=dict(color=NEGRO, size=12, family="Arial, sans-serif"),
            gridcolor="#D9DBD8",
            linecolor=NEGRO,
            linewidth=1.5,
            zerolinecolor="#A7ACA8",
            automargin=True,
        ),
        hoverlabel=dict(bgcolor="#1A1A1A", font_color="#FFFFFF"),
    )


def _aplicar_ejes(fig, titulo_x, titulo_y):
    """Fuerza títulos y marcas oscuras y legibles en pantallas móviles."""
    fig.update_xaxes(
        title=dict(
            text=titulo_x,
            font=dict(color=NEGRO, size=13, family="Arial, sans-serif"),
            standoff=16,
        ),
        tickfont=dict(color=NEGRO, size=12, family="Arial, sans-serif"),
        color=NEGRO,
        linecolor=NEGRO,
        linewidth=1.5,
        automargin=True,
    )
    fig.update_yaxes(
        title=dict(
            text=titulo_y,
            font=dict(color=NEGRO, size=13, family="Arial, sans-serif"),
            standoff=16,
        ),
        tickfont=dict(color=NEGRO, size=12, family="Arial, sans-serif"),
        color=NEGRO,
        linecolor=NEGRO,
        linewidth=1.5,
        automargin=True,
    )
    return fig

def grafica_produccion_diaria(q_dia_litros, dias):
    dias_arr = list(range(1, dias + 1))
    acum     = [q_dia_litros * d for d in dias_arr]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dias_arr, y=acum,
        mode="lines+markers",
        line=dict(color=AMARILLO, width=4),
        marker=dict(size=7, color=AMARILLO, line=dict(color=NEGRO, width=1)),
        name="Producción acumulada (L)"
    ))
    fig.update_layout(
        **_layout("Producción acumulada por día"),
    )
    return _aplicar_ejes(fig, "Días", "Litros")

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
        **_layout("Producción acumulada por hora<br>de operación"),
    )
    return _aplicar_ejes(fig, "Hora", "Litros")

def grafica_comparacion_unidades(litros, m3, barriles):
    fig = go.Figure(go.Bar(
        x=["Litros", "m³", "Barriles"],
        y=[litros, m3, barriles],
        marker_color=[AMARILLO, NEGRO, GRIS],
        text=[f"{litros:,.1f}", f"{m3:,.4f}", f"{barriles:,.3f}"],
        textposition="outside",
        textfont=dict(color=NEGRO, size=12),
    ))
    fig.update_layout(**_layout("Producción total por unidad de medida"))
    return _aplicar_ejes(fig, "Unidad de medida", "Producción total")

def grafica_meta(produccion_bbl, meta_bbl):
    pct = min((produccion_bbl / meta_bbl) * 100, 100)
    color = VERDE if produccion_bbl >= meta_bbl else ROJO
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=produccion_bbl,
        domain={"x": [0, 1], "y": [0, 0.86]},
        delta={"reference": meta_bbl},
        number={"suffix": " bbl", "font": {"color": NEGRO}},
        gauge={
            "axis": {"range": [0, meta_bbl * 1.2], "tickfont": {"color": NEGRO}},
            "bar":  {"color": color},
            "threshold": {
                "line": {"color": NEGRO, "width": 3},
                "thickness": 0.75,
                "value": meta_bbl,
            },
        },
        title={
            "text": "Cumplimiento de meta (bbl)",
            "font": {"color": NEGRO, "size": 13, "family": "Arial, sans-serif"},
        },
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
        line=dict(color=AMARILLO, width=4),
        name="Producción (bbl)"
    ))
    fig.update_layout(
        **_layout("Sensibilidad: producción vs.<br>ciclos por minuto"),
    )
    return _aplicar_ejes(fig, "Ciclos por minuto", "Producción total (bbl)")
