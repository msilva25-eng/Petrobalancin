# -*- coding: utf-8 -*-
import math

def calcular_produccion(diametro_cm, carrera_cm, ciclos_min,
                        eficiencia_pct, horas_dia, dias,
                        tiempo_activo_pct, densidad_kg_m3=None):
    radio_cm      = diametro_cm / 2
    area_cm2      = math.pi * radio_cm ** 2
    v_ciclo_cm3   = area_cm2 * carrera_cm
    v_ciclo_L     = v_ciclo_cm3 / 1000

    ef            = eficiencia_pct / 100
    v_efectivo_L  = v_ciclo_L * ef

    q_min_L       = v_efectivo_L * ciclos_min
    q_hora_L      = q_min_L * 60

    ta            = tiempo_activo_pct / 100
    q_dia_L       = q_hora_L * horas_dia * ta
    q_total_L     = q_dia_L * dias

    q_total_m3    = q_total_L / 1000
    q_total_bbl   = q_total_L / 158.987

    masa_kg = None
    if densidad_kg_m3 and densidad_kg_m3 > 0:
        masa_kg = q_total_m3 * densidad_kg_m3

    return {
        "area_piston_cm2":    area_cm2,
        "v_ciclo_litros":     v_ciclo_L,
        "v_efectivo_litros":  v_efectivo_L,
        "q_min_litros":       q_min_L,
        "q_hora_litros":      q_hora_L,
        "q_dia_litros":       q_dia_L,
        "q_total_litros":     q_total_L,
        "q_total_m3":         q_total_m3,
        "q_total_barriles":   q_total_bbl,
        "masa_kg":            masa_kg,
    }
