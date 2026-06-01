"""
perfis.py
=========
Tabelas de perfis estruturais do Catálogo Gerdau.

Fontes:
  - Cantoneiras de abas iguais (laminadas)
  - Perfis CS (colunas soldadas) — tabela verificada

Unidades: cm, cm², cm⁴.
Campos comuns: Ag (área bruta), rx/ry (raios de giração),
               Ix/Iy (momentos de inércia).
"""

# =============================================================================
# CANTONEIRAS DE ABAS IGUAIS (L)
# Campos: Ag_cm2, rx_cm, ry_cm (= rmin para abas iguais), t_mm, peso_kg_m
# Valores de referência do catálogo. Confirmar bitola específica no projeto.
# =============================================================================

CANTONEIRAS = {
    "L 2x2x1/8 (50,8x50,8x3,2)":   {"Ag_cm2": 3.06,  "rx_cm": 1.57, "ry_cm": 1.57, "t_mm": 3.2,  "peso_kg_m": 2.40},
    "L 2x2x3/16 (50,8x50,8x4,8)":  {"Ag_cm2": 4.48,  "rx_cm": 1.55, "ry_cm": 1.55, "t_mm": 4.8,  "peso_kg_m": 3.52},
    "L 2x2x1/4 (50,8x50,8x6,4)":   {"Ag_cm2": 5.86,  "rx_cm": 1.53, "ry_cm": 1.53, "t_mm": 6.4,  "peso_kg_m": 4.60},
    "L 2.1/2x2.1/2x3/16 (63,5x63,5x4,8)": {"Ag_cm2": 5.68, "rx_cm": 1.96, "ry_cm": 1.96, "t_mm": 4.8, "peso_kg_m": 4.46},
    "L 2.1/2x2.1/2x1/4 (63,5x63,5x6,4)":  {"Ag_cm2": 7.42, "rx_cm": 1.94, "ry_cm": 1.94, "t_mm": 6.4, "peso_kg_m": 5.83},
    "L 3x3x3/16 (76,2x76,2x4,8)":  {"Ag_cm2": 6.89,  "rx_cm": 2.37, "ry_cm": 2.37, "t_mm": 4.8,  "peso_kg_m": 5.41},
    "L 3x3x1/4 (76,2x76,2x6,4)":   {"Ag_cm2": 9.03,  "rx_cm": 2.36, "ry_cm": 2.36, "t_mm": 6.4,  "peso_kg_m": 7.09},
    "L 3x3x5/16 (76,2x76,2x7,9)":  {"Ag_cm2": 11.10, "rx_cm": 2.34, "ry_cm": 2.34, "t_mm": 7.9,  "peso_kg_m": 8.71},
    "L 4x4x1/4 (101,6x101,6x6,4)": {"Ag_cm2": 12.20, "rx_cm": 3.17, "ry_cm": 3.17, "t_mm": 6.4,  "peso_kg_m": 9.59},
    "L 4x4x5/16 (101,6x101,6x7,9)":{"Ag_cm2": 15.10, "rx_cm": 3.15, "ry_cm": 3.15, "t_mm": 7.9,  "peso_kg_m": 11.90},
    # TODO: ampliar com mais bitolas conforme necessidade do catálogo Gerdau
}

# =============================================================================
# PERFIS CS — COLUNAS SOLDADAS (seção H, mesas largas)
# Tabela verificada. Campos: peso_kg_m, Ag_cm2, d_mm (=H), bf_mm (=b),
#   tf_mm (=ef mesa), tw_mm (=ea alma), h_alma_mm, Jx_cm4, Jy_cm4, rx_cm, ry_cm
# =============================================================================

PERFIS_CS = {
    "CS 200x34":  {"peso_kg_m": 34.2,  "Ag_cm2": 43.6,  "d_mm": 200, "bf_mm": 200, "tf_mm": 6.3,  "tw_mm": 8.0,  "h_alma_mm": 184, "Jx_cm4": 3278,  "Jy_cm4": 1067,  "rx_cm": 8.67,  "ry_cm": 4.95},
    "CS 200x39":  {"peso_kg_m": 38.8,  "Ag_cm2": 49.4,  "d_mm": 200, "bf_mm": 200, "tf_mm": 6.3,  "tw_mm": 9.5,  "h_alma_mm": 181, "Jx_cm4": 3762,  "Jy_cm4": 1267,  "rx_cm": 8.73,  "ry_cm": 5.06},
    "CS 200x41":  {"peso_kg_m": 41.2,  "Ag_cm2": 52.5,  "d_mm": 200, "bf_mm": 200, "tf_mm": 8.0,  "tw_mm": 9.5,  "h_alma_mm": 181, "Jx_cm4": 3846,  "Jy_cm4": 1267,  "rx_cm": 8.56,  "ry_cm": 4.91},
    "CS 200x50":  {"peso_kg_m": 50.2,  "Ag_cm2": 64.0,  "d_mm": 200, "bf_mm": 200, "tf_mm": 8.0,  "tw_mm": 12.5, "h_alma_mm": 175, "Jx_cm4": 4758,  "Jy_cm4": 1667,  "rx_cm": 8.62,  "ry_cm": 5.10},
    "CS 200x61":  {"peso_kg_m": 60.8,  "Ag_cm2": 77.4,  "d_mm": 200, "bf_mm": 200, "tf_mm": 8.0,  "tw_mm": 16.0, "h_alma_mm": 168, "Jx_cm4": 5747,  "Jy_cm4": 2134,  "rx_cm": 8.61,  "ry_cm": 5.25},
    "CS 250x43":  {"peso_kg_m": 43.0,  "Ag_cm2": 54.7,  "d_mm": 250, "bf_mm": 250, "tf_mm": 6.3,  "tw_mm": 8.0,  "h_alma_mm": 234, "Jx_cm4": 6531,  "Jy_cm4": 2084,  "rx_cm": 10.92, "ry_cm": 6.17},
    "CS 250x49":  {"peso_kg_m": 48.7,  "Ag_cm2": 62.1,  "d_mm": 250, "bf_mm": 250, "tf_mm": 6.3,  "tw_mm": 9.5,  "h_alma_mm": 231, "Jx_cm4": 7519,  "Jy_cm4": 2474,  "rx_cm": 11.01, "ry_cm": 6.31},
    "CS 250x52":  {"peso_kg_m": 51.8,  "Ag_cm2": 66.0,  "d_mm": 250, "bf_mm": 250, "tf_mm": 8.0,  "tw_mm": 9.5,  "h_alma_mm": 231, "Jx_cm4": 7694,  "Jy_cm4": 2475,  "rx_cm": 10.80, "ry_cm": 6.12},
    "CS 250x63":  {"peso_kg_m": 63.2,  "Ag_cm2": 80.5,  "d_mm": 250, "bf_mm": 250, "tf_mm": 8.0,  "tw_mm": 12.5, "h_alma_mm": 225, "Jx_cm4": 9581,  "Jy_cm4": 3256,  "rx_cm": 10.91, "ry_cm": 6.36},
    "CS 250x66":  {"peso_kg_m": 65.8,  "Ag_cm2": 83.9,  "d_mm": 250, "bf_mm": 250, "tf_mm": 9.5,  "tw_mm": 12.5, "h_alma_mm": 225, "Jx_cm4": 9723,  "Jy_cm4": 3257,  "rx_cm": 10.77, "ry_cm": 6.23},
    "CS 250x76":  {"peso_kg_m": 76.5,  "Ag_cm2": 97.4,  "d_mm": 250, "bf_mm": 250, "tf_mm": 8.0,  "tw_mm": 16.0, "h_alma_mm": 218, "Jx_cm4": 11659, "Jy_cm4": 4168,  "rx_cm": 10.94, "ry_cm": 6.54},
    "CS 250x79":  {"peso_kg_m": 79.1,  "Ag_cm2": 100.7, "d_mm": 250, "bf_mm": 250, "tf_mm": 9.5,  "tw_mm": 16.0, "h_alma_mm": 218, "Jx_cm4": 11788, "Jy_cm4": 4168,  "rx_cm": 10.82, "ry_cm": 6.43},
    "CS 250x84":  {"peso_kg_m": 84.2,  "Ag_cm2": 107.3, "d_mm": 250, "bf_mm": 250, "tf_mm": 12.5, "tw_mm": 16.0, "h_alma_mm": 218, "Jx_cm4": 12047, "Jy_cm4": 4170,  "rx_cm": 10.60, "ry_cm": 6.23},
    "CS 250x90":  {"peso_kg_m": 90.4,  "Ag_cm2": 115.1, "d_mm": 250, "bf_mm": 250, "tf_mm": 9.5,  "tw_mm": 19.0, "h_alma_mm": 212, "Jx_cm4": 13456, "Jy_cm4": 4949,  "rx_cm": 10.81, "ry_cm": 6.56},
    "CS 250x95":  {"peso_kg_m": 95.4,  "Ag_cm2": 121.5, "d_mm": 250, "bf_mm": 250, "tf_mm": 12.5, "tw_mm": 19.0, "h_alma_mm": 212, "Jx_cm4": 13694, "Jy_cm4": 4951,  "rx_cm": 10.62, "ry_cm": 6.38},
    "CS 250x108": {"peso_kg_m": 108.1, "Ag_cm2": 137.7, "d_mm": 250, "bf_mm": 250, "tf_mm": 12.5, "tw_mm": 22.4, "h_alma_mm": 205, "Jx_cm4": 15423, "Jy_cm4": 5837,  "rx_cm": 10.58, "ry_cm": 6.51},
    "CS 300x62":  {"peso_kg_m": 62.4,  "Ag_cm2": 79.5,  "d_mm": 300, "bf_mm": 300, "tf_mm": 8.0,  "tw_mm": 9.5,  "h_alma_mm": 281, "Jx_cm4": 13509, "Jy_cm4": 4276,  "rx_cm": 13.04, "ry_cm": 7.33},
    "CS 300x76":  {"peso_kg_m": 76.1,  "Ag_cm2": 97.0,  "d_mm": 300, "bf_mm": 300, "tf_mm": 8.0,  "tw_mm": 12.5, "h_alma_mm": 275, "Jx_cm4": 16894, "Jy_cm4": 5626,  "rx_cm": 13.20, "ry_cm": 7.62},
    "CS 300x92":  {"peso_kg_m": 92.2,  "Ag_cm2": 117.4, "d_mm": 300, "bf_mm": 300, "tf_mm": 8.0,  "tw_mm": 16.0, "h_alma_mm": 268, "Jx_cm4": 20361, "Jy_cm4": 7201,  "rx_cm": 13.26, "ry_cm": 7.83},
    "CS 300x95":  {"peso_kg_m": 95.3,  "Ag_cm2": 121.5, "d_mm": 300, "bf_mm": 300, "tf_mm": 9.5,  "tw_mm": 16.0, "h_alma_mm": 268, "Jx_cm4": 20902, "Jy_cm4": 7202,  "rx_cm": 13.12, "ry_cm": 7.70},
    "CS 300x102": {"peso_kg_m": 101.7, "Ag_cm2": 129.5, "d_mm": 300, "bf_mm": 300, "tf_mm": 12.5, "tw_mm": 16.0, "h_alma_mm": 268, "Jx_cm4": 21383, "Jy_cm4": 7204,  "rx_cm": 12.85, "ry_cm": 7.46},
    "CS 300x109": {"peso_kg_m": 109.0, "Ag_cm2": 138.9, "d_mm": 300, "bf_mm": 300, "tf_mm": 19.0, "tw_mm": 9.5,  "h_alma_mm": 262, "Jx_cm4": 23962, "Jy_cm4": 8552,  "rx_cm": 13.13, "ry_cm": 7.85},
    "CS 300x115": {"peso_kg_m": 115.2, "Ag_cm2": 146.8, "d_mm": 300, "bf_mm": 300, "tf_mm": 19.0, "tw_mm": 12.5, "h_alma_mm": 262, "Jx_cm4": 24412, "Jy_cm4": 8554,  "rx_cm": 12.90, "ry_cm": 7.63},
}
# NOTA: o perfil CS 300x109 da tabela tem tf=19,0 e tw=9,5 (verificado).
# Atenção: a tabela original lista alguns valores que podem ter sido trocados
# entre colunas em fontes secundárias. Sempre confirmar com o catálogo oficial.
