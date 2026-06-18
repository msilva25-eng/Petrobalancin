# -*- coding: utf-8 -*-
CSS = """
<style>
/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #F5F8FC !important;
    font-family: 'Inter', 'Segoe UI', sans-serif;
    color: #1F2937;
    overflow-x: hidden;
}
[data-testid="stHeader"] { background: transparent !important; }

/* ── Barra lateral — celeste claro ── */
[data-testid="stSidebar"] {
    background-color: #EAF4FF !important;
    border-right: 2px solid #C7DDF2 !important;
}
[data-testid="stSidebar"] * { color: #1F2937 !important; }
[data-testid="stSidebar"] .stRadio label {
    font-size: 14px !important;
    padding: 7px 0 !important;
    cursor: pointer;
    color: #1F2937 !important;
    font-weight: 500;
}
[data-testid="stSidebar"] .stRadio label:hover {
    color: #4A90C2 !important;
}

/* ── Botones principales (amarillo) ── */
.stButton > button {
    background-color: #F2B705 !important;
    color: #1F2937 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 11px 22px !important;
    width: 100% !important;
    min-height: 46px !important;
    transition: background 0.2s ease, color 0.2s ease;
    white-space: nowrap;
}
.stButton > button:hover {
    background-color: #D99A00 !important;
    color: #1F2937 !important;
}

/* ── Bloque institucional y regreso de la barra lateral ── */
.sidebar-institucional {
    width: calc(100% - 20px);
    margin: 8px auto 12px;
    padding: 12px 8px 9px;
    text-align: center;
    background: rgba(255, 255, 255, 0.72);
    border: 1px solid #D7E6F3;
    border-radius: 14px;
    box-sizing: border-box;
}
.sidebar-institucional img { opacity: 0.72; }
.st-key-btn_sidebar_inicio {
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
}
.st-key-btn_sidebar_inicio div[data-testid="stButton"] {
    width: min(100%, 215px) !important;
}
.st-key-btn_sidebar_inicio button {
    width: 100% !important;
    min-height: 44px !important;
    border-radius: 12px !important;
    box-shadow: 0 7px 18px rgba(242, 183, 5, 0.22) !important;
}

/* ── Encabezado principal ── */
.header-petro {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    background: linear-gradient(90deg, #DCEEFF 0%, #F5F8FC 100%);
    border-radius: 12px;
    padding: 10px 16px;
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
}
.header-petro .logo-app { flex-shrink: 0; display: flex; align-items: center; }
.header-petro .logo-app img {
    width: 48px; height: 48px; object-fit: contain; display: block;
}
.header-petro .titulo-bloque {
    flex: 1 1 180px;
    min-width: 0;
    padding: 0 10px;
}
.header-petro .titulo-bloque .titulo-principal {
    font-size: 20px;
    font-weight: 900;
    color: #1F2937;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.2;
}
.header-petro .titulo-bloque .titulo-sub {
    font-size: 12px;
    color: #4A90C2;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.header-petro .logo-unica {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    opacity: 0.80;
}
.header-petro .logo-unica img {
    width: 42px; height: 42px; object-fit: contain; display: block;
}
.header-divider {
    border: none;
    border-bottom: 3px solid #F2B705;
    margin: 6px 0 16px 0;
}

/* ── Tarjeta estándar ── */
.card-resultado {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(74,144,194,0.08);
    box-sizing: border-box;
    width: 100%;
    overflow: hidden;
}
.card-resultado .label {
    font-size: 10px;
    font-weight: 700;
    color: #4A90C2;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 4px;
}
.card-resultado .valor {
    font-size: 24px;
    font-weight: 800;
    color: #1F2937;
    line-height: 1.2;
    word-break: break-word;
}
.card-resultado .valor-acento {
    font-size: 24px;
    font-weight: 800;
    color: #F2B705;
    line-height: 1.2;
    word-break: break-word;
}
.card-resultado .unidad {
    font-size: 11px;
    color: #9CA3AF;
    margin-top: 2px;
    font-weight: 500;
}

/* ── Tarjeta principal destacada ── */
.card-principal {
    background: linear-gradient(135deg, #4A90C2 0%, #2E6FA3 100%);
    border-radius: 16px;
    padding: 20px 22px;
    margin-bottom: 14px;
    box-sizing: border-box;
    width: 100%;
}
.card-principal .label {
    font-size: 11px;
    font-weight: 700;
    color: #DCEEFF;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 6px;
}
.card-principal .valor {
    font-size: 32px;
    font-weight: 900;
    color: #F2B705;
    line-height: 1.1;
}
.card-principal .unidad {
    font-size: 12px;
    color: #DCEEFF;
    margin-top: 4px;
}

/* ── Subtítulo de sección ── */
.seccion-titulo {
    font-size: 13px;
    font-weight: 700;
    color: #4A90C2;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-left: 4px solid #F2B705;
    padding-left: 10px;
    margin: 18px 0 10px 0;
}

/* ── Pantalla de bienvenida ── */
.inicio-logo img {
    width: 120px; height: 120px; object-fit: contain;
    display: block; margin: 0 auto;
    filter: drop-shadow(0 4px 14px rgba(74,144,194,0.25));
}
.inicio-titulo {
    font-size: 34px;
    font-weight: 900;
    color: #1F2937;
    margin: 14px 0 4px 0;
    letter-spacing: -0.5px;
    line-height: 1.1;
    text-align: center;
}
.inicio-subtitulo {
    font-size: 15px;
    color: #4B5563;
    margin-bottom: 8px;
    text-align: center;
}
.inicio-eslogo {
    font-size: 13px;
    font-style: italic;
    color: #4A90C2;
    font-weight: 600;
    margin-bottom: 30px;
    padding: 0 12px;
    text-align: center;
}

/* ── Inputs ── */
.stNumberInput label, .stSlider label {
    font-weight: 600 !important;
    color: #1F2937 !important;
    font-size: 14px !important;
}

/* ── Caja interpretación ── */
.interpretacion-box {
    background: #EAF4FF;
    border-left: 5px solid #4A90C2;
    border-radius: 10px;
    padding: 16px 18px;
    margin: 14px 0;
    font-size: 14px;
    color: #1F2937;
    line-height: 1.7;
    word-break: break-word;
    box-sizing: border-box;
}

/* ── Caja conclusión ── */
.conclusion-box {
    background: #1F2937;
    border-radius: 12px;
    padding: 18px 20px;
    margin: 14px 0;
    color: #FFFFFF;
    font-size: 14px;
    line-height: 1.7;
    box-sizing: border-box;
}
.conclusion-box strong { color: #F2B705; }

/* ── Caja guía (después de calcular) ── */
.guia-box {
    background: #FFFFFF;
    border: 1px solid #C7DDF2;
    border-left: 5px solid #4A90C2;
    border-radius: 10px;
    padding: 16px 20px;
    margin: 14px 0;
    font-size: 14px;
    color: #1F2937;
    line-height: 1.8;
    box-sizing: border-box;
}
.guia-box .guia-titulo {
    font-weight: 700;
    color: #4A90C2;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    margin-bottom: 8px;
}

/* ── Badges ── */
.badge-ok {
    background: #D1FAE5;
    color: #065F46;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 14px;
    display: inline-block;
    margin-bottom: 8px;
    border: 1px solid #6EE7B7;
}
.badge-fail {
    background: #FEF3C7;
    color: #92400E;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 14px;
    display: inline-block;
    margin-bottom: 8px;
    border: 1px solid #FCD34D;
}

/* ── Exportar ── */
.export-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
    box-sizing: border-box;
}
.export-card ul {
    margin: 10px 0 0 0;
    padding-left: 20px;
    color: #4B5563;
    font-size: 14px;
    line-height: 1.9;
}

/* ── Pie de página ── */
.footer-petro {
    text-align: center;
    padding: 24px 0 8px 0;
    color: #9CA3AF;
    font-size: 12px;
    border-top: 1px solid #E5E7EB;
    margin-top: 40px;
}
.footer-petro span.accent { color: #4A90C2; font-weight: 600; }
.footer-petro span.sub { font-size: 11px; color: #9CA3AF; }

/* ── Responsive ── */
@media (max-width: 640px) {
    .inicio-titulo { font-size: 26px; }
    .inicio-logo img { width: 96px; height: 96px; }
    .inicio-subtitulo { font-size: 13px; }
    .inicio-eslogo { font-size: 12px; }
    .header-petro .titulo-bloque .titulo-principal { font-size: 16px; }
    .header-petro .titulo-bloque .titulo-sub { font-size: 10px; }
    .header-petro .logo-app img { width: 38px; height: 38px; }
    .header-petro .logo-unica img { width: 34px; height: 34px; }
    .card-resultado .valor { font-size: 20px; }
    .card-resultado .valor-acento { font-size: 20px; }
    .card-principal .valor { font-size: 26px; }
    .stButton > button { font-size: 14px !important; padding: 10px 16px !important; }
    .interpretacion-box { font-size: 13px; }
    .conclusion-box { font-size: 13px; }
    .guia-box { font-size: 13px; }
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
