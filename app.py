# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import os
import io
import importlib
from datetime import datetime

st.set_page_config(
    page_title="Petrobalancín",
    page_icon="assets/logo_petrobalancin.png",
    layout="wide",
    initial_sidebar_state="auto"
)

from modules.estilos import inyectar_css
from modules.calculos import calcular_produccion
from modules.graficas import (
    grafica_produccion_diaria, grafica_por_hora,
    grafica_comparacion_unidades, grafica_meta, grafica_sensibilidad
)
from modules.historial import (
    cargar_historial, guardar_en_historial,
    borrar_historial, historial_a_excel
)
import modules.exportar_pdf as exportar_pdf

inyectar_css()

# ── Utilidad: cargar imagen en base64 ────────────────────────────────────────
def b64img(path):
    import base64
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# ── Inicializar session_state ─────────────────────────────────────────────────
defaults = {
    "app_started":    False,
    "seccion_actual": "Inicio",
    "resultados":     None,
    "params":         None,
    "meta":           None,
    "calculo_listo":  False,
    "interpretacion": "",
    "pdf_listo":      False,
    "pdf_bytes":      None,
    "pdf_nombre":     "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ════════════════════════════════════════════════════════════════════════════
# PANTALLA DE BIENVENIDA
# ════════════════════════════════════════════════════════════════════════════
if not st.session_state["app_started"]:
    logo_b64  = b64img("assets/logo_petrobalancin.png")
    unica_b64 = b64img("assets/logo_unica.png")

    logo_html = (
        f'<div class="inicio-logo"><img src="data:image/png;base64,{logo_b64}"></div>'
        if logo_b64 else ""
    )
    unica_html = (
        f'<div class="inicio-unica">'
        f'<img src="data:image/png;base64,{unica_b64}">'
        f'</div>'
        if unica_b64 else ""
    )

    st.markdown(f"""
    <div class="bienvenida-contenedor">
        <div class="bienvenida-tarjeta">
            <div class="bienvenida-franja"></div>
            {unica_html}
            {logo_html}
            <div class="inicio-etiqueta">ANÁLISIS DE CAPACIDAD</div>
            <div class="inicio-titulo">Petrobalancín</div>
            <div class="inicio-subtitulo">Analizador técnico de capacidad petrolera</div>
            <div class="inicio-eslogo">Cada ciclo cuenta: convierte operación en producción.</div>
            <div class="inicio-separador"></div>
        </div>
    </div>
    <style>
    section[data-testid="stMain"] .block-container {{
        max-width: 1100px !important;
        padding-top: 3rem !important;
    }}
    .bienvenida-contenedor {{
        width: 100%;
        display: flex;
        justify-content: center;
        padding: 28px 16px 10px;
        box-sizing: border-box;
    }}
    .bienvenida-tarjeta {{
        position: relative;
        width: min(100%, 680px);
        padding: 38px 48px 30px;
        text-align: center;
        background: linear-gradient(145deg, #FFFFFF 0%, #F4F5F2 100%);
        border: 1px solid #D4D6D3;
        border-radius: 26px;
        box-shadow: 0 22px 55px rgba(31, 41, 55, 0.10);
        overflow: hidden;
        box-sizing: border-box;
    }}
    .bienvenida-franja {{
        position: absolute;
        inset: 0 0 auto 0;
        height: 7px;
        background: linear-gradient(90deg, #1A1A1A 0%, #FFCD11 50%, #1A1A1A 100%);
    }}
    .inicio-unica {{
        position: absolute;
        top: 25px;
        right: 28px;
        padding: 7px 10px;
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        box-shadow: 0 5px 16px rgba(31, 41, 55, 0.07);
    }}
    .inicio-unica img {{
        display: block;
        width: 44px;
        height: 44px;
        object-fit: contain;
        opacity: 0.78;
    }}
    .inicio-etiqueta {{
        display: inline-block;
        margin-top: 14px;
        padding: 5px 12px;
        color: #1A1A1A;
        background: #FFF7D1;
        border: 1px solid #FFCD11;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.2px;
    }}
    .inicio-separador {{
        width: 54px;
        height: 4px;
        margin: 22px auto 0;
        border-radius: 999px;
        background: #FFCD11;
    }}
    .st-key-btn_comenzar_simulacion {{
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        margin-top: 8px !important;
    }}
    .st-key-btn_comenzar_simulacion div[data-testid="stButton"] {{
        width: 290px !important;
    }}
    .st-key-btn_comenzar_simulacion div[data-testid="stButton"] > button {{
        width: 290px !important;
        min-height: 54px !important;
        border-radius: 14px !important;
        font-size: 16px !important;
        box-shadow: 0 10px 24px rgba(32, 36, 40, 0.18) !important;
        transition: transform .2s ease, box-shadow .2s ease !important;
    }}
    .st-key-btn_comenzar_simulacion div[data-testid="stButton"] > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 14px 28px rgba(32, 36, 40, 0.24) !important;
    }}
    @media (max-width: 640px) {{
        section[data-testid="stMain"] .block-container {{ padding-top: 1rem !important; }}
        .bienvenida-contenedor {{ padding: 14px 4px 8px; }}
        .bienvenida-tarjeta {{ padding: 62px 22px 26px; border-radius: 20px; }}
        .inicio-unica {{ top: 18px; right: 18px; }}
        .inicio-unica img {{ width: 36px; height: 36px; }}
        .st-key-btn_comenzar_simulacion div[data-testid="stButton"],
        .st-key-btn_comenzar_simulacion div[data-testid="stButton"] > button {{
            width: min(100%, 290px) !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

    if st.button("Comenzar análisis", key="btn_comenzar_simulacion"):
        st.session_state["app_started"]    = True
        st.session_state["seccion_actual"] = "Inicio"
        st.rerun()
    st.stop()

# ════════════════════════════════════════════════════════════════════════════
# BARRA LATERAL
# ════════════════════════════════════════════════════════════════════════════
SECCIONES = [
    "Inicio",
    "Datos de operación",
    "Resultados",
    "Gráficas",
    "Historial",
    "Exportar reporte",
    "Acerca de la app",
]

with st.sidebar:
    logo_side = b64img("assets/logo_petrobalancin.png")
    if logo_side:
        st.markdown(
            f'<div class="sidebar-brand">'
            f'<img src="data:image/png;base64,{logo_side}" '
            f'style="width:70px;height:70px;object-fit:contain;">'
            f'<div style="font-size:17px;font-weight:900;color:#1F2937;margin-top:6px;">'
            f'Petrobalancín</div>'
            f'<div style="font-size:10px;color:#AEB3B0;font-weight:600;margin-top:2px;">'
            f'Analizador técnico de capacidad petrolera</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    st.markdown("---")

    navegacion_pendiente = st.session_state.pop("navegacion_pendiente", None)
    if navegacion_pendiente:
        st.session_state["nav_radio"] = navegacion_pendiente

    idx_actual = SECCIONES.index(st.session_state["seccion_actual"]) \
        if st.session_state["seccion_actual"] in SECCIONES else 0

    seccion = st.radio(
        "Navegación", SECCIONES,
        index=idx_actual,
        key="nav_radio",
        label_visibility="collapsed"
    )
    st.session_state["seccion_actual"] = seccion

    st.markdown("---")
    unica_side = b64img("assets/logo_unica.png")
    if unica_side:
        st.markdown(
            f'<div class="sidebar-institucional">'
            f'<img src="data:image/png;base64,{unica_side}" '
            f'style="width:60px;height:60px;object-fit:contain;">'
            f'<br><span style="font-size:10px;color:#4B5563;">UNICA</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    if st.button("← Volver a la bienvenida", key="btn_sidebar_inicio"):
        st.session_state["app_started"]    = False
        st.session_state["seccion_actual"] = "Inicio"
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# ENCABEZADO PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════
_lp = b64img("assets/logo_petrobalancin.png")
_lu = b64img("assets/logo_unica.png")
_img_p = (
    f'<img src="data:image/png;base64,{_lp}" '
    f'style="width:44px;height:44px;object-fit:contain;">'
    if _lp else ""
)
_img_u = (
    f'<img src="data:image/png;base64,{_lu}" '
    f'style="width:38px;height:38px;object-fit:contain;">'
    if _lu else ""
)
st.markdown(f"""
<div class="header-petro">
    <div class="logo-app">{_img_p}</div>
    <div class="titulo-bloque">
        <div class="titulo-principal">Petrobalancín</div>
        <div class="titulo-sub">Evaluación de capacidad de producción</div>
    </div>
    <div class="logo-unica">{_img_u}</div>
</div>
<hr class="header-divider">
""", unsafe_allow_html=True)

# ── Alias de seccion activa ───────────────────────────────────────────────────
SA = st.session_state["seccion_actual"]

# ════════════════════════════════════════════════════════════════════════════
# INICIO
# ════════════════════════════════════════════════════════════════════════════
if SA == "Inicio":
    st.markdown("## Bienvenido a Petrobalancín")
    st.markdown(
        "**Petrobalancín** es un analizador técnico de capacidad petrolera que evalúa "
        "la producción de un balancín a partir de sus condiciones reales de operación."
    )
    st.markdown("---")
    st.markdown('<div class="seccion-titulo">Cómo usar la aplicación</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="card-resultado">
        <div class="label">Paso 1</div>
        <div class="valor" style="font-size:16px;">Datos de operación</div>
        <div class="unidad">Ingresa los parámetros del equipo y calcula su capacidad de producción.</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="card-resultado">
        <div class="label">Paso 2</div>
        <div class="valor" style="font-size:16px;">Resultados técnicos</div>
        <div class="unidad">Revisa los indicadores calculados y continúa hacia las gráficas.</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="card-resultado">
        <div class="label">Paso 3</div>
        <div class="valor" style="font-size:16px;">Gráficas y reporte</div>
        <div class="unidad">Analiza el comportamiento y exporta un reporte técnico completo.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="guia-box">
        <div class="guia-titulo">Flujo guiado de análisis</div>
        Ingresa los datos del equipo, revisa los resultados técnicos, analiza las gráficas
        y finaliza exportando el reporte PDF. Los botones de cada etapa te guiarán automáticamente.
    </div>
    """, unsafe_allow_html=True)
    if st.button("Iniciar análisis →", key="btn_iniciar_analisis"):
        st.session_state["seccion_actual"] = "Datos de operación"
        st.session_state["navegacion_pendiente"] = "Datos de operación"
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# DATOS DE OPERACION
# ════════════════════════════════════════════════════════════════════════════
elif SA == "Datos de operación":
    st.markdown("## Datos de operación")
    st.markdown("Ingresa los parámetros del balancín petrolero para calcular su producción.")

    with st.form("form_calculos"):
        st.markdown("### Parámetros principales")
        col1, col2 = st.columns(2)
        with col1:
            diametro   = st.number_input("Diámetro del pistón (cm)",    min_value=0.1,  max_value=100.0,  value=5.0,  step=0.1)
            carrera    = st.number_input("Longitud de carrera (cm)",     min_value=0.1,  max_value=500.0,  value=30.0, step=0.5)
            ciclos     = st.number_input("Ciclos por minuto (CPM)",      min_value=0.1,  max_value=100.0,  value=12.0, step=0.5)
            eficiencia = st.number_input("Eficiencia volumétrica (%)",   min_value=1.0,  max_value=100.0,  value=80.0, step=1.0)
        with col2:
            horas_dia      = st.number_input("Horas de operación por día",   min_value=0.1, max_value=24.0,  value=8.0,  step=0.5)
            dias           = st.number_input("Días de operación",             min_value=1,   max_value=3650,  value=7,    step=1)
            tiempo_activo  = st.number_input("Tiempo activo (%)",             min_value=1.0, max_value=100.0, value=90.0, step=1.0)

        st.markdown("### Parámetros opcionales")
        col3, col4 = st.columns(2)
        with col3:
            densidad = st.number_input("Densidad del petróleo (kg/m³)",  min_value=0.0, max_value=1200.0, value=850.0, step=1.0)
        with col4:
            meta     = st.number_input("Meta de producción (barriles)",  min_value=0.0, value=10.0, step=0.5)

        submitted = st.form_submit_button("Calcular producción")

    if submitted:
        errores = []
        if diametro  <= 0:                  errores.append("El diámetro debe ser mayor que 0.")
        if carrera   <= 0:                  errores.append("La longitud de carrera debe ser mayor que 0.")
        if ciclos    <= 0:                  errores.append("Los ciclos por minuto deben ser mayores que 0.")
        if not (1 <= eficiencia  <= 100):   errores.append("La eficiencia debe estar entre 1% y 100%.")
        if not (1 <= tiempo_activo <= 100): errores.append("El tiempo activo debe estar entre 1% y 100%.")
        if horas_dia <= 0:                  errores.append("Las horas de operación deben ser mayores que 0.")
        if dias      <= 0:                  errores.append("Los días de operación deben ser mayores que 0.")

        if errores:
            for e in errores:
                st.error(e)
        else:
            densidad_val = densidad if densidad > 0 else None
            meta_val     = meta     if meta     > 0 else None

            resultados = calcular_produccion(
                diametro, carrera, ciclos, eficiencia,
                horas_dia, int(dias), tiempo_activo, densidad_val
            )
            st.session_state["resultados"]    = resultados
            st.session_state["params"]        = {
                "diametro_cm":       diametro,
                "carrera_cm":        carrera,
                "ciclos_min":        ciclos,
                "eficiencia_pct":    eficiencia,
                "horas_dia":         horas_dia,
                "dias":              int(dias),
                "tiempo_activo_pct": tiempo_activo,
                "densidad":          densidad_val,
            }
            st.session_state["meta"]          = meta_val
            st.session_state["calculo_listo"] = True

    # ── Mensaje y guia post-calculo ──────────────────────────────────
    if st.session_state.get("calculo_listo") and st.session_state.get("resultados") is not None:
        r = st.session_state["resultados"]
        st.success("Cálculo realizado correctamente.")
        st.markdown(f"""
        <div class="guia-box">
            <div class="guia-titulo">Análisis listo para consultar</div>
            <strong>Producción total calculada:</strong> {r["q_total_barriles"]:.3f} bbl
            ({r["q_total_litros"]:,.1f} L)
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ver resultados →", key="btn_ver_resultados"):
            st.session_state["seccion_actual"] = "Resultados"
            st.session_state["navegacion_pendiente"] = "Resultados"
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# RESULTADOS
# ════════════════════════════════════════════════════════════════════════════
elif SA == "Resultados":
    st.markdown("## Resultados del análisis")
    if not st.session_state["calculo_listo"] or st.session_state["resultados"] is None:
        st.warning("Aún no hay un análisis disponible. Inicia el proceso en Datos de operación.")
    else:
        r    = st.session_state["resultados"]
        p    = st.session_state["params"]
        meta = st.session_state["meta"]

        # Produccion total
        st.markdown('<div class="seccion-titulo">Producción total acumulada</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""<div class="card-principal">
            <div class="label">Total en barriles</div>
            <div class="valor">{r["q_total_barriles"]:,.3f}</div>
            <div class="unidad">bbl (barriles de petróleo)</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="card-resultado">
            <div class="label">Total en litros</div>
            <div class="valor-acento">{r["q_total_litros"]:,.1f}</div>
            <div class="unidad">litros</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div class="card-resultado">
            <div class="label">Total en metros cúbicos</div>
            <div class="valor">{r["q_total_m3"]:,.4f}</div>
            <div class="unidad">m³</div>
            </div>""", unsafe_allow_html=True)

        # Desglose temporal
        st.markdown('<div class="seccion-titulo">Producción por intervalo de tiempo</div>', unsafe_allow_html=True)
        col4, col5, col6, col7 = st.columns(4)
        with col4:
            st.markdown(f"""<div class="card-resultado">
            <div class="label">Por ciclo</div>
            <div class="valor" style="font-size:19px;">{r["v_efectivo_litros"]:.5f}</div>
            <div class="unidad">litros / ciclo</div>
            </div>""", unsafe_allow_html=True)
        with col5:
            st.markdown(f"""<div class="card-resultado">
            <div class="label">Por minuto</div>
            <div class="valor" style="font-size:19px;">{r["q_min_litros"]:.4f}</div>
            <div class="unidad">litros / min</div>
            </div>""", unsafe_allow_html=True)
        with col6:
            st.markdown(f"""<div class="card-resultado">
            <div class="label">Por hora</div>
            <div class="valor" style="font-size:19px;">{r["q_hora_litros"]:.3f}</div>
            <div class="unidad">litros / hora</div>
            </div>""", unsafe_allow_html=True)
        with col7:
            st.markdown(f"""<div class="card-resultado">
            <div class="label">Por día</div>
            <div class="valor" style="font-size:19px;">{r["q_dia_litros"]:.2f}</div>
            <div class="unidad">litros / día</div>
            </div>""", unsafe_allow_html=True)

        # Datos tecnicos
        st.markdown('<div class="seccion-titulo">Datos técnicos del equipo</div>', unsafe_allow_html=True)
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown(f"""<div class="card-resultado">
            <div class="label">Área del pistón</div>
            <div class="valor" style="font-size:18px;">{r["area_piston_cm2"]:.4f}</div>
            <div class="unidad">cm² (diámetro: {p["diametro_cm"]} cm)</div>
            </div>""", unsafe_allow_html=True)
        with col_t2:
            if r.get("masa_kg") and p.get("densidad"):
                st.markdown(f"""<div class="card-resultado">
                <div class="label">Masa extraída (densidad: {p["densidad"]} kg/m³)</div>
                <div class="valor" style="font-size:18px;">{r["masa_kg"]:,.2f}</div>
                <div class="unidad">kilogramos</div>
                </div>""", unsafe_allow_html=True)

        # Meta de produccion
        if meta and meta > 0:
            st.markdown('<div class="seccion-titulo">Cumplimiento de meta de producción</div>', unsafe_allow_html=True)
            pct = (r["q_total_barriles"] / meta) * 100
            col_m1, col_m2 = st.columns([1, 2])
            with col_m1:
                if r["q_total_barriles"] >= meta:
                    st.markdown(
                        f'<div class="badge-ok">Cumple la meta — {pct:.1f}% alcanzado</div>',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        f'<div class="badge-fail">Por debajo de la meta — {pct:.1f}% alcanzado</div>',
                        unsafe_allow_html=True)
            with col_m2:
                st.progress(min(pct / 100, 1.0))
                st.caption(f"Meta: {meta:.2f} bbl   |   Producido: {r['q_total_barriles']:.3f} bbl")

        # Interpretacion tecnica
        st.markdown('<div class="seccion-titulo">Interpretación técnica</div>', unsafe_allow_html=True)
        if meta and meta > 0:
            if r["q_total_barriles"] >= meta:
                meta_txt = (
                    f"La producción de {r['q_total_barriles']:.3f} bbl cumple la meta de {meta:.2f} bbl, "
                    f"lo que indica que el sistema opera dentro de los parámetros esperados."
                )
            else:
                deficit = meta - r["q_total_barriles"]
                meta_txt = (
                    f"La producción de {r['q_total_barriles']:.3f} bbl está {deficit:.3f} bbl por debajo "
                    f"de la meta de {meta:.2f} bbl. Se recomienda revisar la eficiencia volumétrica, "
                    f"las horas de operación o los ciclos por minuto."
                )
        else:
            meta_txt = ""

        interpretacion = (
            f"Con los parámetros ingresados, el balancín extrae {r['v_efectivo_litros']:.5f} L/ciclo "
            f"a una tasa de {r['q_hora_litros']:.3f} L/h. "
            f"En {p['dias']} días de operación ({p['horas_dia']} h/día, "
            f"{p['tiempo_activo_pct']}% de tiempo activo), la producción acumulada es de "
            f"{r['q_total_barriles']:.3f} bbl ({r['q_total_litros']:,.1f} L | "
            f"{r['q_total_m3']:.4f} m3). "
            f"Parámetros clave: D={p['diametro_cm']} cm, carrera={p['carrera_cm']} cm, "
            f"CPM={p['ciclos_min']}, Ef={p['eficiencia_pct']}%."
        )
        if meta_txt:
            interpretacion += " " + meta_txt
        st.session_state["interpretacion"] = interpretacion
        st.markdown(f'<div class="interpretacion-box">{interpretacion}</div>', unsafe_allow_html=True)

        # Conclusion destacada
        tasa_bbl_dia = r["q_dia_litros"] / 158.987
        st.markdown(f"""<div class="conclusion-box">
        <strong>Conclusión:</strong> el sistema produce <strong>{r["q_total_barriles"]:,.3f} bbl</strong>
        en el período analizado. Tasa diaria: <strong>{r["q_dia_litros"]:.2f} L/día
        ({tasa_bbl_dia:.4f} bbl/día)</strong>.
        Operando {p["dias"]} días a {p["horas_dia"]} h/día con {p["tiempo_activo_pct"]}% de tiempo activo
        y eficiencia volumétrica del {p["eficiencia_pct"]}%.
        </div>""", unsafe_allow_html=True)

        # Guardar historial
        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Guardar en historial", key="btn_guardar_res"):
                guardar_en_historial(p, r, meta)
                st.success("Guardado en historial correctamente.")
        with col_b:
            if st.button("Ver gráficas →", key="btn_ver_graficas"):
                st.session_state["seccion_actual"] = "Gráficas"
                st.session_state["navegacion_pendiente"] = "Gráficas"
                st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# GRAFICAS
# ════════════════════════════════════════════════════════════════════════════
elif SA == "Gráficas":
    st.markdown("## Gráficas de producción")
    if not st.session_state["calculo_listo"] or st.session_state["resultados"] is None:
        st.warning("Aún no hay un análisis disponible. Inicia el proceso en Datos de operación.")
    else:
        r    = st.session_state["resultados"]
        p    = st.session_state["params"]
        meta = st.session_state["meta"]
        opciones_grafica = [
            "Producción acumulada por día",
            "Producción acumulada por hora",
            "Comparación por unidad de medida",
        ]
        if meta and meta > 0:
            opciones_grafica.append("Comparación con la meta")
        opciones_grafica.append("Análisis de sensibilidad")

        grafica_seleccionada = st.selectbox(
            "Selecciona la gráfica que deseas consultar",
            opciones_grafica,
            key="selector_grafica"
        )
        st.caption("La gráfica se adapta automáticamente al tamaño de tu pantalla.")
        config_grafica = {"displayModeBar": False, "responsive": True}

        if grafica_seleccionada == "Producción acumulada por día":
            fig1 = grafica_produccion_diaria(r["q_dia_litros"], p["dias"])
            st.plotly_chart(fig1, use_container_width=True, config=config_grafica)
        elif grafica_seleccionada == "Producción acumulada por hora":
            fig2 = grafica_por_hora(r["q_hora_litros"], p["horas_dia"], p["tiempo_activo_pct"])
            st.plotly_chart(fig2, use_container_width=True, config=config_grafica)
        elif grafica_seleccionada == "Comparación por unidad de medida":
            fig3 = grafica_comparacion_unidades(r["q_total_litros"], r["q_total_m3"], r["q_total_barriles"])
            st.plotly_chart(fig3, use_container_width=True, config=config_grafica)
        elif grafica_seleccionada == "Comparación con la meta":
            fig4 = grafica_meta(r["q_total_barriles"], meta)
            st.plotly_chart(fig4, use_container_width=True, config=config_grafica)
        else:
            fig5 = grafica_sensibilidad(
                p["diametro_cm"], p["carrera_cm"], p["eficiencia_pct"],
                p["horas_dia"], p["dias"], p["tiempo_activo_pct"]
            )
            st.plotly_chart(fig5, use_container_width=True, config=config_grafica)

        st.markdown("---")
        if st.button("Exportar reporte PDF →", key="btn_exportar_graficas"):
            st.session_state["seccion_actual"] = "Exportar reporte"
            st.session_state["navegacion_pendiente"] = "Exportar reporte"
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# HISTORIAL
# ════════════════════════════════════════════════════════════════════════════
elif SA == "Historial":
    st.markdown("## Historial de cálculos")
    df = cargar_historial()
    if df.empty:
        st.info("El historial está vacío. Realiza un cálculo y guárdalo desde la sección Resultados.")
    else:
        st.dataframe(df, use_container_width=True)
        st.markdown(f"**Total de cálculos registrados:** {len(df)}")

    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.session_state["calculo_listo"] and st.session_state["resultados"]:
            if st.button("Guardar cálculo actual", key="btn_guardar_hist"):
                guardar_en_historial(
                    st.session_state["params"],
                    st.session_state["resultados"],
                    st.session_state["meta"]
                )
                st.success("Guardado.")
                st.rerun()
    with col2:
        if not df.empty:
            if st.button("Borrar historial", key="btn_borrar_hist"):
                borrar_historial()
                st.success("Historial borrado.")
                st.rerun()
    with col3:
        if not df.empty:
            csv_bytes = df.to_csv(index=False, encoding="utf-8").encode("utf-8")
            st.download_button(
                label="Descargar CSV",
                data=csv_bytes,
                file_name="historial_petrobalancin.csv",
                mime="text/csv"
            )
    with col4:
        if not df.empty:
            try:
                excel_path = historial_a_excel()
                with open(excel_path, "rb") as f:
                    st.download_button(
                        label="Descargar Excel",
                        data=f.read(),
                        file_name="historial_petrobalancin.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"Error generando Excel: {e}")

# ════════════════════════════════════════════════════════════════════════════
# EXPORTAR REPORTE
# ════════════════════════════════════════════════════════════════════════════
elif SA == "Exportar reporte":
    st.markdown("## Exportar reporte PDF")
    if not st.session_state["calculo_listo"] or st.session_state["resultados"] is None:
        st.warning("Aún no hay un análisis disponible. Inicia el proceso en Datos de operación.")
    else:
        r      = st.session_state["resultados"]
        p      = st.session_state["params"]
        meta   = st.session_state["meta"]
        interp = st.session_state.get("interpretacion", "")

        st.markdown("""<div class="export-card">
        <strong>El reporte PDF incluye:</strong>
        <ul>
            <li>Logo de Petrobalancín y UNICA</li>
            <li>Fecha del reporte</li>
            <li>Parámetros de operación ingresados</li>
            <li>Fórmulas aplicadas</li>
            <li>Resultados calculados</li>
            <li>Interpretación técnica</li>
            <li>Gráficas del análisis</li>
        </ul>
        </div>""", unsafe_allow_html=True)

        if st.button("Generar reporte PDF", key="btn_generar_pdf"):
            with st.spinner("Generando reporte PDF..."):
                try:
                    # Recargar el módulo evita conservar una versión anterior
                    # durante las actualizaciones en caliente de Streamlit.
                    importlib.reload(exportar_pdf)
                    pdf_bytes = exportar_pdf.generar_pdf(
                        p, r, meta, interp, incluir_graficas=True
                    )
                    fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.session_state["pdf_bytes"]  = pdf_bytes
                    st.session_state["pdf_nombre"] = f"Reporte_Petrobalancin_{fecha_str}.pdf"
                    st.session_state["pdf_listo"]  = True
                except Exception as e:
                    st.error(f"Error al generar el PDF: {e}")

        if st.session_state.get("pdf_listo") and st.session_state.get("pdf_bytes"):
            st.success("Reporte generado. Descárgalo a continuación.")
            st.download_button(
                label="Descargar reporte PDF",
                data=st.session_state["pdf_bytes"],
                file_name=st.session_state["pdf_nombre"],
                mime="application/pdf",
                use_container_width=True,
                key="btn_dl_pdf"
            )

# ════════════════════════════════════════════════════════════════════════════
# ACERCA DE LA APP
# ════════════════════════════════════════════════════════════════════════════
elif SA == "Acerca de la app":
    st.markdown("## Acerca de la app")
    st.markdown("""
    **Petrobalancín** es un analizador técnico de capacidad petrolera diseñado para evaluar
    el desempeño productivo de un balancín bajo distintas condiciones de operación.

    La aplicación permite ingresar datos relacionados con el diámetro del pistón, la longitud
    de carrera, los ciclos por minuto, la eficiencia volumétrica y el tiempo de operación.
    A partir de estos valores, calcula indicadores como el volumen extraído por ciclo, la
    producción por hora, por día y total, expresados en litros, metros cúbicos y barriles.

    Su objetivo es apoyar la evaluación técnica del equipo mediante indicadores cuantitativos,
    gráficas de comportamiento e interpretaciones de capacidad productiva.
    """)
    st.markdown("---")
    st.markdown("""
    <div class="card-resultado">
        <div class="label">Tecnologías utilizadas</div>
        <div class="valor" style="font-size:15px;color:#5C4A00;">Python + Streamlit</div>
        <div class="unidad">Pandas · Plotly · ReportLab · OpenPyXL</div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# PIE DE PAGINA INSTITUCIONAL
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer-petro">
    <span class="accent">UNICA &middot; Ingeniería Industrial</span><br>
    <span class="sub">Petrobalancín &middot; Analizador técnico de capacidad petrolera</span>
</div>
""", unsafe_allow_html=True)
