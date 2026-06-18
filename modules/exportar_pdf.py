# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable,
                                 Image as RLImage, PageBreak)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.barcharts import VerticalBarChart
from datetime import datetime
import os, io, math

AMARILLO   = colors.HexColor("#F2B705")
AZUL       = colors.HexColor("#4A90C2")
NEGRO      = colors.HexColor("#1F2937")
GRIS       = colors.HexColor("#4B5563")
GRIS_CLARO = colors.HexColor("#F5F8FC")
BLANCO     = colors.white

def _estilos():
    titulo  = ParagraphStyle("Titulo",  fontSize=17, textColor=NEGRO,
                              alignment=TA_CENTER, fontName="Helvetica-Bold", spaceAfter=3)
    sub     = ParagraphStyle("Sub",     fontSize=11, textColor=AZUL,
                              alignment=TA_CENTER, fontName="Helvetica-Bold", spaceAfter=2)
    slogan  = ParagraphStyle("Slogan",  fontSize=9,  textColor=AMARILLO,
                              alignment=TA_CENTER, fontName="Helvetica-Oblique", spaceAfter=8)
    seccion = ParagraphStyle("Seccion", fontSize=11, textColor=NEGRO,
                              fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=5,
                              borderPad=3)
    normal  = ParagraphStyle("Normal",  fontSize=9,  textColor=GRIS,
                              fontName="Helvetica",  spaceAfter=2, leading=14)
    footer  = ParagraphStyle("Footer",  fontSize=7,  textColor=GRIS,
                              alignment=TA_CENTER, fontName="Helvetica")
    footer2 = ParagraphStyle("Footer2", fontSize=7,  textColor=AMARILLO,
                              alignment=TA_CENTER, fontName="Helvetica-Oblique")
    return titulo, sub, slogan, seccion, normal, footer, footer2

def _tabla(datos, col1=7*cm, cab_amarillo=False):
    t = Table(datos, colWidths=[col1, "*"])
    base = [
        ("FONTNAME",      (0,1), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",      (1,1), (1,-1), "Helvetica"),
        ("FONTSIZE",      (0,0), (-1,-1), 8),
        ("TEXTCOLOR",     (0,1), (0,-1), NEGRO),
        ("TEXTCOLOR",     (1,1), (1,-1), GRIS),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [BLANCO, GRIS_CLARO]),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#E5E7EB")),
        ("PADDING",       (0,0), (-1,-1), 5),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]
    if cab_amarillo:
        base += [
            ("BACKGROUND", (0,0), (-1,0), AMARILLO),
            ("TEXTCOLOR",  (0,0), (-1,0), NEGRO),
            ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ]
    else:
        base += [
            ("BACKGROUND", (0,0), (-1,0), AZUL),
            ("TEXTCOLOR",  (0,0), (-1,0), BLANCO),
            ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ]
    t.setStyle(TableStyle(base))
    return t

def _logo(path, w, h):
    if path and os.path.exists(path):
        try:
            return RLImage(path, width=w, height=h)
        except Exception:
            pass
    return None

def _grafica_linea(titulo, valores, etiqueta_x):
    dibujo = Drawing(470, 225)
    dibujo.add(String(
        235, 208, titulo, textAnchor="middle",
        fontName="Helvetica-Bold", fontSize=10, fillColor=NEGRO
    ))
    grafica = LinePlot()
    grafica.x, grafica.y = 55, 38
    grafica.width, grafica.height = 390, 145
    grafica.data = [[(i + 1, float(valor)) for i, valor in enumerate(valores)]]
    grafica.xValueAxis.valueMin = 1
    grafica.xValueAxis.valueMax = max(2, len(valores))
    grafica.xValueAxis.labels.fontSize = 7
    grafica.yValueAxis.valueMin = 0
    grafica.yValueAxis.valueMax = max(max(valores) * 1.10, 1)
    grafica.yValueAxis.labels.fontSize = 7
    grafica.lines[0].strokeColor = AZUL
    grafica.lines[0].strokeWidth = 2.2
    dibujo.add(grafica)
    dibujo.add(String(235, 15, etiqueta_x, textAnchor="middle", fontSize=7, fillColor=GRIS))
    return dibujo

def _grafica_barras(titulo, etiquetas, valores):
    dibujo = Drawing(470, 225)
    dibujo.add(String(
        235, 208, titulo, textAnchor="middle",
        fontName="Helvetica-Bold", fontSize=10, fillColor=NEGRO
    ))
    grafica = VerticalBarChart()
    grafica.x, grafica.y = 55, 38
    grafica.width, grafica.height = 390, 145
    grafica.data = [[float(valor) for valor in valores]]
    grafica.categoryAxis.categoryNames = etiquetas
    grafica.categoryAxis.labels.fontSize = 7
    grafica.valueAxis.valueMin = 0
    grafica.valueAxis.valueMax = max(max(valores) * 1.15, 1)
    grafica.valueAxis.labels.fontSize = 7
    grafica.bars[0].fillColor = AMARILLO
    grafica.bars[0].strokeColor = colors.HexColor("#D99A00")
    dibujo.add(grafica)
    return dibujo

def _graficas_capacidad(params, resultados, meta):
    dias = int(params["dias"])
    horas = max(1, int(params["horas_dia"]))
    graficas = [
        _grafica_linea(
            "Producción acumulada por día (L)",
            [resultados["q_dia_litros"] * dia for dia in range(1, dias + 1)],
            "Días de operación"
        ),
        _grafica_linea(
            "Producción acumulada por hora (L)",
            [resultados["q_hora_litros"] * (params["tiempo_activo_pct"] / 100) * hora
             for hora in range(1, horas + 1)],
            "Horas de operación"
        ),
    ]
    if meta and meta > 0:
        graficas.append(_grafica_barras(
            "Producción calculada frente a la meta (bbl)",
            ["Calculada", "Meta"],
            [resultados["q_total_barriles"], meta]
        ))

    producciones_sensibilidad = []
    area = math.pi * (params["diametro_cm"] / 2) ** 2
    for ciclos in range(1, 31):
        litros = (
            (area * params["carrera_cm"] / 1000)
            * (params["eficiencia_pct"] / 100)
            * ciclos * 60 * params["horas_dia"]
            * (params["tiempo_activo_pct"] / 100) * params["dias"]
        )
        producciones_sensibilidad.append(litros / 158.987)
    graficas.append(_grafica_linea(
        "Sensibilidad de capacidad frente a los ciclos por minuto",
        producciones_sensibilidad,
        "Ciclos por minuto"
    ))
    return graficas

def generar_pdf(params, resultados, meta=None, interpretacion="", incluir_graficas=False):
    titulo_s, sub_s, slogan_s, seccion_s, normal_s, footer_s, footer2_s = _estilos()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=1.8*cm, leftMargin=1.8*cm,
        topMargin=1.8*cm,   bottomMargin=1.8*cm
    )
    story = []

    # ── Encabezado con logos ──────────────────────────────────────────
    logo_petro = _logo("assets/logo_petrobalancin.png", 2.5*cm, 2.5*cm)
    logo_unica = _logo("assets/logo_unica.png",         2.0*cm, 2.2*cm)
    celda_petro = logo_petro if logo_petro else Paragraph("Petrobalancín", normal_s)
    celda_unica = logo_unica if logo_unica else Paragraph("UNICA", normal_s)

    t_logos = Table([[celda_petro, "", celda_unica]], colWidths=[3*cm, "*", 3*cm])
    t_logos.setStyle(TableStyle([
        ("ALIGN",  (0,0), (0,0), "LEFT"),
        ("ALIGN",  (2,0), (2,0), "RIGHT"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("PADDING",(0,0), (-1,-1), 0),
    ]))
    story.append(t_logos)
    story.append(Spacer(1, 0.25*cm))
    story.append(Paragraph("Petrobalancín", titulo_s))
    story.append(Paragraph("Analizador técnico de capacidad petrolera", sub_s))
    story.append(Paragraph("Cada ciclo cuenta: convierte operación en producción.", slogan_s))
    story.append(HRFlowable(width="100%", thickness=2, color=AMARILLO, spaceAfter=6))
    story.append(Paragraph(
        f"Reporte generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}    |    UNICA - Ingeniería Industrial",
        normal_s))
    story.append(Spacer(1, 0.3*cm))

    # ── Parametros de operacion ───────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E5E7EB")))
    story.append(Paragraph("Parámetros de operación", seccion_s))
    param_data = [
        ["Parámetro", "Valor"],
        ["Diámetro del pistón",          f"{params['diametro_cm']} cm"],
        ["Longitud de carrera",          f"{params['carrera_cm']} cm"],
        ["Ciclos por minuto",            f"{params['ciclos_min']} ciclos/min"],
        ["Eficiencia volumétrica",       f"{params['eficiencia_pct']} %"],
        ["Horas de operación por día",   f"{params['horas_dia']} h/día"],
        ["Días de operación",            f"{params['dias']} días"],
        ["Tiempo activo",                f"{params['tiempo_activo_pct']} %"],
        ["Densidad del petróleo",
         f"{params['densidad']} kg/m3" if params.get("densidad") else "No especificada"],
        ["Meta de producción",           f"{meta} bbl" if meta else "No especificada"],
    ]
    story.append(_tabla(param_data))
    story.append(Spacer(1, 0.25*cm))

    # ── Formulas ─────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E5E7EB")))
    story.append(Paragraph("Fórmulas aplicadas", seccion_s))
    formulas = [
        "A = pi x (D/2)^2                        Área del pistón (cm2)",
        "V_ciclo = A x Longitud de carrera        Volumen por ciclo (cm3 -> L)",
        "V_ef = V_ciclo x Eficiencia volumétrica  Volumen efectivo por ciclo (L)",
        "Q_min = V_ef x Ciclos/min               Producción por minuto (L/min)",
        "Q_hora = Q_min x 60                      Producción por hora (L/h)",
        "Q_dia = Q_hora x Horas/día x T.activo   Producción diaria (L/día)",
        "Q_total = Q_dia x Días                   Producción total (L)",
        "Conversiones: 1 m3 = 1000 L  |  1 bbl = 158.987 L",
    ]
    for f in formulas:
        story.append(Paragraph(f"  {f}", normal_s))
    story.append(Spacer(1, 0.25*cm))

    # ── Resultados ───────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E5E7EB")))
    story.append(Paragraph("Resultados calculados", seccion_s))
    r = resultados
    res_data = [
        ["Indicador", "Valor"],
        ["Área del pistón",                f"{r['area_piston_cm2']:.4f} cm2"],
        ["Volumen por ciclo",              f"{r['v_ciclo_litros']:.6f} L"],
        ["Volumen efectivo por ciclo",     f"{r['v_efectivo_litros']:.6f} L"],
        ["Producción por minuto",          f"{r['q_min_litros']:.4f} L/min"],
        ["Producción por hora",            f"{r['q_hora_litros']:.4f} L/h"],
        ["Producción por día",             f"{r['q_dia_litros']:.4f} L/día"],
        ["Producción total (litros)",      f"{r['q_total_litros']:.3f} L"],
        ["Producción total (m3)",          f"{r['q_total_m3']:.5f} m3"],
        ["Producción total (barriles)",    f"{r['q_total_barriles']:.4f} bbl"],
    ]
    if r.get("masa_kg"):
        res_data.append(["Masa extraída", f"{r['masa_kg']:.2f} kg"])
    if meta and meta > 0:
        pct = (r["q_total_barriles"] / meta) * 100
        cumple = f"{'Sí' if r['q_total_barriles'] >= meta else 'No'} ({pct:.1f}%)"
        res_data.append(["Cumplimiento de meta", f"{cumple} — meta: {meta:.2f} bbl"])
    story.append(_tabla(res_data, cab_amarillo=True))
    story.append(Spacer(1, 0.25*cm))

    # ── Interpretacion ───────────────────────────────────────────────
    if interpretacion:
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E5E7EB")))
        story.append(Paragraph("Interpretación técnica", seccion_s))
        story.append(Paragraph(interpretacion, normal_s))
        story.append(Spacer(1, 0.25*cm))

    # ── Gráficas del análisis ─────────────────────────────────────────
    if incluir_graficas:
        graficas = _graficas_capacidad(params, resultados, meta)
        story.append(PageBreak())
        story.append(Paragraph("Gráficas del análisis de capacidad", seccion_s))
        story.append(Paragraph(
            "Representación visual de los principales indicadores calculados.",
            normal_s
        ))
        story.append(Spacer(1, 0.2*cm))
        for indice, grafica in enumerate(graficas):
            story.append(grafica)
            story.append(Spacer(1, 0.25*cm))
            if indice % 2 == 1 and indice < len(graficas) - 1:
                story.append(PageBreak())

    # ── Pie de pagina ────────────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=2, color=AMARILLO))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph("UNICA - Ingeniería Industrial", footer_s))
    story.append(Paragraph(
        "Petrobalancín - Analizador técnico de capacidad petrolera", footer2_s))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
