# -*- coding: utf-8 -*-
"""Estilos visuales de Petrobalancín.

La interfaz usa una sola paleta industrial para evitar conflictos entre el
tema de Streamlit y reglas CSS antiguas.
"""

CSS = """
<style>
:root {
    color-scheme: light;
    --cat-yellow: #FFCD11;
    --cat-yellow-hover: #F2B800;
    --cat-ink: #1A1A1A;
    --cat-graphite: #222629;
    --cat-steel: #5F666B;
    --cat-canvas: #F4F5F2;
    --cat-surface: #FFFFFF;
    --cat-line: #D4D7D2;
    --cat-soft: #ECEEEA;
}

/* Base */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    color-scheme: light !important;
    background: var(--cat-canvas) !important;
    color: var(--cat-ink) !important;
    font-family: "Inter", "Segoe UI", Arial, sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stMainBlockContainer"] { color: var(--cat-ink) !important; }
[data-testid="stMainBlockContainer"] h1,
[data-testid="stMainBlockContainer"] h2,
[data-testid="stMainBlockContainer"] h3,
[data-testid="stMainBlockContainer"] p,
[data-testid="stMainBlockContainer"] label { color: var(--cat-ink) !important; }

/* Barra lateral */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A1D1F 0%, #292D30 100%) !important;
    border-right: 1px solid #464B4E !important;
}
[data-testid="stSidebar"] * { color: #F7F7F4 !important; }
[data-testid="stSidebar"] hr { border-color: #484E51 !important; }
[data-testid="stSidebar"] .stRadio label {
    padding: 7px 0 !important;
    color: #F7F7F4 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] .stRadio label:hover,
[data-testid="stSidebar"] [aria-checked="true"] { color: var(--cat-yellow) !important; }

.sidebar-brand {
    margin: 0 4px 8px;
    padding: 18px 12px 12px;
    text-align: center;
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.11);
    border-radius: 16px;
}
.sidebar-brand img {
    width: 76px !important;
    height: 76px !important;
    padding: 8px;
    object-fit: contain;
    background: #FFFFFF;
    border: 1px solid #D8DAD6;
    border-radius: 14px;
    box-sizing: border-box;
}
.sidebar-institucional {
    width: calc(100% - 20px);
    margin: 8px auto 12px;
    padding: 12px 8px 9px;
    text-align: center;
    background: #FFFFFF !important;
    border: 1px solid #C9CCC8 !important;
    border-radius: 14px;
    box-sizing: border-box;
}
.sidebar-institucional img { opacity: .95 !important; }
.sidebar-institucional span { color: #33383B !important; }
.st-key-btn_sidebar_inicio {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
}
.st-key-btn_sidebar_inicio div[data-testid="stButton"] { width: min(100%, 215px) !important; }

/* Botón visible para abrir el menú lateral en teléfonos */
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
[data-testid="stExpandSidebarButton"] {
    position: fixed !important;
    top: 12px !important;
    left: 12px !important;
    z-index: 999999 !important;
    width: auto !important;
    min-width: 92px !important;
    height: 44px !important;
    padding: 0 13px !important;
    background: var(--cat-yellow) !important;
    color: var(--cat-ink) !important;
    border: 2px solid var(--cat-ink) !important;
    border-radius: 11px !important;
    box-shadow: 0 7px 18px rgba(0,0,0,.22) !important;
}
[data-testid="stSidebarCollapsedControl"]::after,
[data-testid="collapsedControl"]::after,
[data-testid="stExpandSidebarButton"]::after {
    content: "MENÚ";
    margin-left: 7px;
    color: var(--cat-ink) !important;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: .5px;
}
[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="collapsedControl"] svg,
[data-testid="stExpandSidebarButton"] svg {
    fill: var(--cat-ink) !important;
    color: var(--cat-ink) !important;
}

/* Encabezado */
.header-petro {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    width: 100%;
    padding: 10px 16px;
    background: linear-gradient(105deg, #FFFFFF 0%, #F4F5F2 100%) !important;
    border: 1px solid var(--cat-line);
    border-top: 5px solid var(--cat-yellow);
    border-radius: 13px;
    box-shadow: 0 7px 20px rgba(26,26,26,.09);
    box-sizing: border-box;
}
.header-petro .logo-app,
.header-petro .logo-unica { display: flex; flex-shrink: 0; align-items: center; }
.header-petro .logo-app img { width: 48px; height: 48px; object-fit: contain; }
.header-petro .logo-unica {
    padding: 5px 8px;
    background: #FFFFFF;
    border: 1px solid #D7D9D6;
    border-radius: 10px;
}
.header-petro .logo-unica img { width: 42px; height: 42px; object-fit: contain; }
.header-petro .titulo-bloque { flex: 1 1 180px; min-width: 0; padding: 0 10px; }
.header-petro .titulo-principal {
    overflow: hidden;
    color: var(--cat-ink) !important;
    font-size: 20px;
    font-weight: 900;
    line-height: 1.2;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.header-petro .titulo-sub {
    overflow: hidden;
    color: var(--cat-steel) !important;
    font-size: 12px;
    font-weight: 650;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.header-divider { margin: 6px 0 16px; border: 0; border-bottom: 1px solid #C8CBC7; }

/* Pantalla de bienvenida */
.inicio-logo img { width: 118px; height: 118px; object-fit: contain; }
.inicio-titulo { color: var(--cat-ink) !important; font-size: 36px; font-weight: 900; line-height: 1.15; }
.inicio-subtitulo { margin-top: 7px; color: var(--cat-steel) !important; font-size: 16px; }
.inicio-eslogo { margin-top: 13px; color: #4F565A !important; font-size: 13px; font-style: italic; font-weight: 650; }

/* Secciones y tarjetas */
.seccion-titulo {
    margin: 20px 0 12px;
    padding-left: 11px;
    color: var(--cat-ink) !important;
    border-left: 5px solid var(--cat-yellow);
    font-size: 17px;
    font-weight: 900;
    letter-spacing: .2px;
    text-transform: uppercase;
}
.card-resultado,
.export-card,
.guia-box {
    height: 100%;
    padding: 18px;
    background: #FFFFFF !important;
    color: var(--cat-ink) !important;
    border: 1px solid var(--cat-line) !important;
    border-radius: 14px;
    box-shadow: 0 5px 16px rgba(26,26,26,.07);
    box-sizing: border-box;
}
.card-resultado .label,
.card-principal .label {
    margin-bottom: 6px;
    color: var(--cat-steel) !important;
    font-size: 11px;
    font-weight: 850;
    letter-spacing: .8px;
    text-transform: uppercase;
}
.card-resultado .valor { color: var(--cat-ink) !important; font-size: 24px; font-weight: 900; line-height: 1.2; }
.card-resultado .valor-acento { color: #5B4800 !important; font-size: 24px; font-weight: 900; line-height: 1.2; }
.card-resultado .unidad,
.card-principal .unidad { margin-top: 5px; color: #676E72 !important; font-size: 12px; line-height: 1.45; }
.card-principal {
    height: 100%;
    padding: 21px;
    background: linear-gradient(135deg, #292D30, #17191A) !important;
    color: #FFFFFF !important;
    border: 1px solid #3E4447;
    border-radius: 14px;
    box-shadow: 0 7px 20px rgba(0,0,0,.14);
    box-sizing: border-box;
}
.card-principal .label { color: #D6D9D5 !important; }
.card-principal .valor,
.card-principal strong { color: var(--cat-yellow) !important; font-size: 30px; font-weight: 900; }
.card-principal .unidad { color: #D4D7D3 !important; }

.guia-box { margin: 14px 0; border-left: 5px solid var(--cat-yellow) !important; line-height: 1.75; }
.guia-box .guia-titulo {
    margin-bottom: 7px;
    color: #5B4800 !important;
    font-size: 13px;
    font-weight: 900;
    letter-spacing: .4px;
    text-transform: uppercase;
}
.interpretacion-box {
    margin: 12px 0;
    padding: 18px 20px;
    background: #FFF9DE !important;
    color: var(--cat-ink) !important;
    border: 1px solid #E3CA62;
    border-left: 5px solid var(--cat-yellow);
    border-radius: 12px;
    line-height: 1.7;
}
.conclusion-box {
    margin-top: 14px;
    padding: 17px 20px;
    background: #202426 !important;
    color: #FFFFFF !important;
    border-left: 5px solid var(--cat-yellow);
    border-radius: 12px;
    line-height: 1.65;
}
.conclusion-box strong { color: var(--cat-yellow) !important; }
.badge-ok,
.badge-fail {
    display: inline-block;
    margin-bottom: 8px;
    padding: 8px 16px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 800;
}
.badge-ok { background: #DDF4E5; color: #14532D; border: 1px solid #86C99D; }
.badge-fail { background: #FFF2BF; color: #5C4600; border: 1px solid #E5C54A; }
.export-card ul { margin: 10px 0 0; padding-left: 20px; color: #4C5357; line-height: 1.9; }

/* Controles */
div[data-baseweb="input"],
div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: var(--cat-ink) !important;
    border-color: #858B8F !important;
}
div[data-baseweb="input"] input,
div[data-baseweb="select"] * {
    color: var(--cat-ink) !important;
    -webkit-text-fill-color: var(--cat-ink) !important;
}

/* Campos numéricos: fuerza modo claro en Safari/iOS y Android */
[data-testid="stNumberInput"],
[data-testid="stNumberInput"] [data-baseweb="input"],
[data-testid="stNumberInput"] [data-baseweb="base-input"] {
    color-scheme: light !important;
    background-color: #FFFFFF !important;
}
[data-testid="stNumberInput"] [data-baseweb="input"] {
    overflow: hidden !important;
    border: 2px solid #4B5053 !important;
    border-radius: 11px !important;
    box-shadow: 0 2px 7px rgba(26,26,26,.10) !important;
}
[data-testid="stNumberInput"] input,
[data-testid="stNumberInput"] input[type="number"] {
    min-height: 48px !important;
    background: #FFFFFF !important;
    color: #1A1A1A !important;
    caret-color: #1A1A1A !important;
    -webkit-text-fill-color: #1A1A1A !important;
    -webkit-appearance: none !important;
    opacity: 1 !important;
    font-weight: 700 !important;
}
[data-testid="stNumberInput"] button {
    min-width: 46px !important;
    background: #303437 !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: 0 !important;
    border-left: 2px solid #17191A !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}
[data-testid="stNumberInput"] button:hover {
    background: #343A3E !important;
    color: #FFCD11 !important;
    -webkit-text-fill-color: #FFCD11 !important;
}
[data-testid="stNumberInput"] button svg {
    fill: currentColor !important;
    color: currentColor !important;
}
[data-testid="stNumberInput"]:focus-within [data-baseweb="input"] {
    border-color: #B28A00 !important;
    box-shadow: 0 0 0 2px rgba(255,205,17,.28) !important;
}
.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    min-height: 46px !important;
    padding: 11px 22px !important;
    background: var(--cat-yellow) !important;
    color: var(--cat-ink) !important;
    -webkit-text-fill-color: var(--cat-ink) !important;
    border: 1px solid #AA8500 !important;
    border-radius: 10px !important;
    box-shadow: 0 6px 14px rgba(26,26,26,.16) !important;
    font-size: 15px !important;
    font-weight: 850 !important;
}
.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    background: var(--cat-yellow-hover) !important;
    color: #111111 !important;
    border-color: #715800 !important;
}
.stButton > button:disabled,
.stFormSubmitButton > button:disabled {
    background: #E5D68D !important;
    color: #343434 !important;
    -webkit-text-fill-color: #343434 !important;
    opacity: 1 !important;
}

/* Gráficas */
[data-testid="stPlotlyChart"] {
    margin-top: 8px;
    padding: 4px;
    overflow: hidden;
    background: #FFFFFF !important;
    border: 1px solid var(--cat-line);
    border-radius: 14px;
    box-shadow: 0 7px 18px rgba(26,26,26,.08);
}

/* Pie */
.footer-petro {
    margin-top: 40px;
    padding: 24px 0 8px;
    text-align: center;
    color: #7A8083;
    border-top: 1px solid var(--cat-line);
    font-size: 12px;
}
.footer-petro .accent { color: #5B4800 !important; font-weight: 750; }
.footer-petro .sub { color: #7A8083 !important; font-size: 11px; }

@media (max-width: 640px) {
    [data-testid="stMainBlockContainer"] {
        padding-top: 72px !important;
        padding-right: 18px !important;
        padding-left: 18px !important;
    }
    [data-testid="stMainBlockContainer"] h2 { font-size: 34px !important; line-height: 1.08 !important; }
    .header-petro { padding: 10px 12px !important; }
    .header-petro .titulo-principal { font-size: 16px; }
    .header-petro .titulo-sub { font-size: 10px; }
    .header-petro .logo-app img { width: 38px; height: 38px; }
    .header-petro .logo-unica img { width: 34px; height: 34px; }
    .inicio-titulo { font-size: 26px; }
    .inicio-logo img { width: 96px; height: 96px; }
    .inicio-subtitulo { font-size: 13px; }
    .inicio-eslogo { font-size: 12px; }
    .card-resultado .valor,
    .card-resultado .valor-acento { font-size: 20px; }
    .card-principal .valor { font-size: 26px; }
    .interpretacion-box,
    .conclusion-box,
    .guia-box { font-size: 13px; }
    .stButton > button,
    .stFormSubmitButton > button,
    .stDownloadButton > button { min-height: 50px !important; font-size: 15px !important; }
}
@media (max-width: 400px) {
    .inicio-titulo { font-size: 22px; }
    .header-petro .titulo-bloque { display: none; }
}
</style>
"""


def inyectar_css():
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)


def aplicar_estilos():
    inyectar_css()
