"""
constantes.py
=============
Coeficientes e parâmetros normativos da ABNT NBR 8800:2024 e NBR 6123:2023.

TODOS os valores aqui foram extraídos diretamente das normas. As referências
de seção/tabela estão indicadas em cada bloco para rastreabilidade.

Unidades padrão do projeto: kN e cm (resistências em kN/cm²).
"""

# =============================================================================
# COEFICIENTES DE PONDERAÇÃO DAS AÇÕES — ELU
# NBR 8800:2024, Tabela 1 (combinações normais)
# γf = γf1 · γf3, representado por γg (permanentes) ou γq (variáveis)
# =============================================================================

# Ações permanentes (γg) — combinações normais
GAMMA_G = {
    "peso_proprio_aco": 1.25,          # estruturas de aço e equipamentos
    "peso_proprio_premoldado": 1.30,   # pré-moldadas, madeira, industrializados
    "peso_proprio_in_loco": 1.35,      # moldadas in loco e empuxos permanentes
    "peso_proprio_geral": 1.50,        # elementos construtivos em geral
}
# Valor favorável à segurança (alívio): usar 1.00 (Tabela 1, entre parênteses)
GAMMA_G_FAVORAVEL = 1.00

# Ações variáveis (γq) — combinações normais (Tabela 1)
GAMMA_Q = {
    "sobrecarga": 1.50,        # demais ações variáveis (uso e ocupação)
    "vento": 1.40,             # ação do vento
    "viga_rolamento": 1.50,    # cargas móveis (ver Tabela 2 para ψ0)
    "temperatura": 1.20,       # variação térmica da atmosfera
}

# =============================================================================
# FATORES DE COMBINAÇÃO ψ0 (= γf2)
# NBR 8800:2024, Tabela 2
# =============================================================================

PSI_0 = {
    "sobrecarga_residencial": 0.5,     # locais sem predominância de pesos fixos
    "sobrecarga_publico": 0.7,         # locais com concentração de pessoas
    "sobrecarga_deposito": 0.8,        # bibliotecas, depósitos, garagens, coberturas
    "vento": 0.6,                      # pressão dinâmica do vento
    "temperatura": 0.6,                # variações uniformes de temperatura
    "viga_rolamento_ponte": 1.0,       # vigas de rolamento de pontes rolantes
    "pilar_suporte_rolamento": 0.7,    # pilares que suportam vigas de rolamento
}

# Fatores de redução para ELS (Tabela 2) — para uso futuro
PSI_1 = {"sobrecarga_residencial": 0.4, "vento": 0.3, "viga_rolamento_ponte": 0.8}
PSI_2 = {"sobrecarga_residencial": 0.3, "vento": 0.0, "viga_rolamento_ponte": 0.5}

# =============================================================================
# COEFICIENTES DE PONDERAÇÃO DAS RESISTÊNCIAS — ELU
# NBR 8800:2024, Tabela 3 (combinações normais)
# =============================================================================

GAMMA_A1 = 1.10   # aço: escoamento e instabilidade
GAMMA_A2 = 1.35   # aço: ruptura

# =============================================================================
# PROPRIEDADES DOS AÇOS ESTRUTURAIS (kN/cm²)
# fy = limite de escoamento, fu = limite de resistência (ruptura)
# E  = módulo de elasticidade = 20000 kN/cm² (NBR 8800)
# =============================================================================

E_ACO = 20000.0   # módulo de elasticidade do aço (kN/cm²)
G_ACO = 7700.0    # módulo de elasticidade transversal (kN/cm²)

ACOS = {
    # Aços nacionais comuns
    "MR-250":   {"fy": 25.0, "fu": 40.0, "desc": "ABNT (≈ ASTM A36)"},
    "AR-350":   {"fy": 35.0, "fu": 45.0, "desc": "ABNT (≈ ASTM A572 G50)"},
    "AR-415":   {"fy": 41.5, "fu": 52.0, "desc": "ABNT alta resistência"},
    # Aços ASTM (catálogo Gerdau)
    "ASTM A36":        {"fy": 25.0, "fu": 40.0, "desc": "padrão"},
    "ASTM A572-G50":   {"fy": 34.5, "fu": 45.0, "desc": "Gerdau pronta entrega"},
    "ASTM A572-G60":   {"fy": 41.5, "fu": 52.0, "desc": "sob encomenda"},
    "ASTM A992":       {"fy": 34.5, "fu": 45.0, "desc": "perfis W"},
}
# Nota: fy e fu convertidos de MPa para kN/cm² (1 MPa = 0.1 kN/cm²).
# A36: 250 MPa → 25.0 ; 400 MPa → 40.0. Confirmado catálogo Gerdau.

# =============================================================================
# FUROS — ACRÉSCIMO À DIMENSÃO DO FURO
# NBR 8800:2024, seção 5.2.4.1-a)
# "a largura dos furos deve ser considerada 2,0 mm maior que a dimensão
#  máxima desses furos. Se o furo for feito com broca, igual à dimensão."
# IMPORTANTE: A versão 2024 unificou em +2,0 mm (a versão 2008 usava +3,5 mm).
# =============================================================================

FOLGA_FURO = {
    "puncionado": 2.0,   # mm — furo padrão (puncionado/perfurado): df = d + 2.0
    "broca": 0.0,        # mm — furo feito com broca: df = d (sem acréscimo)
}

# =============================================================================
# FLAMBAGEM LOCAL — VALORES (b/t)lim
# NBR 8800:2024, Tabela 4
# Multiplicar pelo fator dado por √(E/fy)
# =============================================================================

BT_LIM = {
    # AL (uma borda apoiada, outra livre)
    "mesa_I_H_laminada": 0.56,    # grupo 4: mesas de I,H,T,U laminadas
    "mesa_I_H_soldada": 0.64,     # grupo 5: mesas soldadas (usa kc, ver nota)
    "aba_cantoneira": 0.45,       # grupo 3: abas de cantoneiras
    "alma_T": 0.75,               # grupo 6: almas de seções T
    # AA (duas bordas apoiadas)
    "alma_I_H_U": 1.49,           # grupo 2: almas de I, H, U
    "tubular_retangular": 1.40,   # grupo 1: paredes de tubulares retangulares
}

# Fatores c1 e c2 para largura efetiva (Tabela 5)
FATORES_C = {
    "AA": {"c1": 0.18, "c2": 1.31},
    "tubular_ret": {"c1": 0.20, "c2": 1.38},
    "AL": {"c1": 0.22, "c2": 1.49},
}

# Limite recomendado de esbeltez para compressão (5.3.7.1)
ESBELTEZ_MAX_COMPRESSAO = 200
# Limite recomendado de esbeltez para tração (5.2.8.1)
ESBELTEZ_MAX_TRACAO = 300

# =============================================================================
# NBR 6123:2023 — PARÂMETROS METEOROLÓGICOS (Tabela 1)
# S2 = b · Fr · (z/10)^p
# =============================================================================

# Estrutura: VENTO_PARAMS[categoria][classe] = {"b", "Fr", "p"}
# Fr é sempre o da Categoria II (conforme a norma)
VENTO_PARAMS = {
    "I":   {"A": {"b": 1.10, "Fr": 1.00, "p": 0.06},
            "B": {"b": 1.11, "Fr": 0.98, "p": 0.065},
            "C": {"b": 1.12, "Fr": 0.95, "p": 0.07}},
    "II":  {"A": {"b": 1.00, "Fr": 1.00, "p": 0.085},
            "B": {"b": 1.00, "Fr": 0.98, "p": 0.09},
            "C": {"b": 1.00, "Fr": 0.95, "p": 0.10}},
    "III": {"A": {"b": 0.94, "Fr": 1.00, "p": 0.10},
            "B": {"b": 0.94, "Fr": 0.98, "p": 0.105},
            "C": {"b": 0.93, "Fr": 0.95, "p": 0.115}},
    "IV":  {"A": {"b": 0.86, "Fr": 1.00, "p": 0.12},
            "B": {"b": 0.85, "Fr": 0.98, "p": 0.125},
            "C": {"b": 0.84, "Fr": 0.95, "p": 0.135}},
    "V":   {"A": {"b": 0.74, "Fr": 1.00, "p": 0.15},
            "B": {"b": 0.73, "Fr": 0.98, "p": 0.16},
            "C": {"b": 0.71, "Fr": 0.95, "p": 0.175}},
}

# Fator estatístico S3 (Tabela 3) — valores mínimos por grupo
S3_GRUPOS = {
    "Grupo 1 - hospitais, bombeiros, comunicação": 1.10,
    "Grupo 2 - hotéis, residências, comércio, indústria": 1.00,
    "Grupo 3 - depósitos, silos, construções rurais": 0.95,
    "Grupo 4 - vedações (telhas, vidros)": 0.88,
    "Grupo 5 - construções temporárias": 0.83,
}

# Velocidade básica V0 (m/s) — principais cidades (Figura 1, isopletas)
# Valores aproximados de referência. O usuário deve confirmar no mapa de isopletas.
V0_CIDADES = {
    "Foz do Iguaçu - PR": 50,
    "Curitiba - PR": 40,
    "São Paulo - SP": 40,
    "Rio de Janeiro - RJ": 35,
    "Porto Alegre - RS": 45,
    "Florianópolis - SC": 43,
    "Brasília - DF": 35,
    "Belo Horizonte - MG": 35,
    "Salvador - BA": 30,
    "Recife - PE": 30,
    "Fortaleza - CE": 30,
    "Manaus - AM": 30,
    "Outro (inserir manualmente)": 0,
}

# Constante da pressão dinâmica: q = 0.613 · Vk²  (Vk em m/s, q em N/m²)
# 0.613 = ½ · ρ_ar (ρ = 1.226 kg/m³ a 15°C, 1 atm)
COEF_PRESSAO_DINAMICA = 0.613
