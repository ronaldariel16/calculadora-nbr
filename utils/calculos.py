"""
calculos.py
===========
Funções de cálculo reutilizáveis, conforme ABNT NBR 8800:2024 e NBR 6123:2023.

Cada função tem docstring indicando:
  - O que calcula
  - A seção/equação da norma de referência
  - Unidades dos parâmetros (padrão: kN, cm, kN/cm²)
"""

import math
from utils.constantes import (
    GAMMA_A1, GAMMA_A2, E_ACO, COEF_PRESSAO_DINAMICA,
)


# =============================================================================
# MÓDULO 1 — COMBINAÇÃO DE AÇÕES
# =============================================================================

def combinacao_ultima_normal(esforcos, coefs_gamma, coefs_psi, principal):
    """
    Calcula Sd para uma combinação última normal, tratando 'principal'
    como a ação variável principal.

    NBR 8800:2024, seção 4.8.7.2.1, equação:
        Sd = Σ(γgi·FGi,k) + γq1·FQ1,k + Σ(γqj·ψ0j·FQj,k)

    Parâmetros
    ----------
    esforcos : dict {nome_acao: esforço_na_barra_kN}
        Esforço que cada ação produz NA BARRA (não a carga bruta).
    coefs_gamma : dict {nome_acao: γ}
        Coeficiente de ponderação de cada ação.
    coefs_psi : dict {nome_acao: ψ0}
        Fator de combinação de cada ação variável.
    principal : str
        Nome da ação variável tratada como principal nesta combinação.

    Retorna
    -------
    float : Sd em kN
    """
    sd = 0.0
    for acao, esforco in esforcos.items():
        if acao == "permanente":
            # Permanente sempre entra com γg cheio
            sd += coefs_gamma[acao] * esforco
        elif acao == principal:
            # Variável principal entra com γq cheio (sem ψ0)
            sd += coefs_gamma[acao] * esforco
        else:
            # Variáveis secundárias entram com γq · ψ0
            sd += coefs_gamma[acao] * coefs_psi.get(acao, 1.0) * esforco
    return sd


# =============================================================================
# MÓDULO 2 — TRAÇÃO
# =============================================================================

def resistencia_escoamento(Ag, fy):
    """
    Força axial resistente de cálculo — escoamento da seção bruta.
    NBR 8800:2024, eq. 5.2.2-a):  Nt,Rd = Ag·fy / γa1

    Ag em cm², fy em kN/cm². Retorna kN.
    """
    return (Ag * fy) / GAMMA_A1


def resistencia_ruptura(Ae, fu):
    """
    Força axial resistente de cálculo — ruptura da seção líquida efetiva.
    NBR 8800:2024, eq. 5.2.2-b):  Nt,Rd = Ae·fu / γa2

    Ae em cm², fu em kN/cm². Retorna kN.
    """
    return (Ae * fu) / GAMMA_A2


def diametro_furo(d_parafuso_mm, folga_mm):
    """
    Dimensão do furo para cálculo de área líquida.
    NBR 8800:2024, 5.2.4.1-a):  df = d + folga
    folga = 2.0 mm (puncionado) ou 0.0 mm (broca).

    Retorna em mm.
    """
    return d_parafuso_mm + folga_mm


def area_liquida_secao(Ag, n_furos, df_cm, t_cm, ligacoes_diagonais=None):
    """
    Área líquida de UMA seção (linha de ruptura), incluindo zigue-zague.
    NBR 8800:2024, 5.2.4.1-b):
        An = Ag − Σ(df·t) + Σ(s²/4g)·t

    Parâmetros
    ----------
    Ag : float — área bruta (cm²)
    n_furos : int — número de furos cortados por esta linha
    df_cm : float — dimensão do furo (cm)
    t_cm : float — espessura da chapa (cm)
    ligacoes_diagonais : list de tuplas (s_cm, g_cm)
        Cada trecho diagonal entre dois furos. s e g em cm.

    Retorna
    -------
    float : An em cm²
    """
    An = Ag - n_furos * (df_cm * t_cm)
    if ligacoes_diagonais:
        for (s_cm, g_cm) in ligacoes_diagonais:
            if g_cm > 0:
                An += (s_cm ** 2 / (4 * g_cm)) * t_cm
    return An


def area_liquida_efetiva(An, Ct):
    """
    Área líquida efetiva.
    NBR 8800:2024, 5.2.3:  Ae = Ct · An

    An em cm², Ct adimensional. Retorna cm².
    """
    return Ct * An


# =============================================================================
# MÓDULO 3 — COMPRESSÃO
# =============================================================================

def bt_limite(coef, fy, E=E_ACO):
    """
    Limite (b/t)lim para flambagem local.
    NBR 8800:2024, Tabela 4:  (b/t)lim = coef · √(E/fy)

    Retorna adimensional.
    """
    return coef * math.sqrt(E / fy)


def fator_Q_simplificado(bf_2tf, ht_w, bt_lim_mesa, bt_lim_alma):
    """
    Verifica flambagem local de forma simplificada (caso Q = 1).
    NBR 8800:2024, 5.3.4.1: se todos os elementos têm b/t ≤ (b/t)lim,
    então Aef = Ag (ou seja, sem redução por flambagem local).

    Retorna (Q, mesa_ok, alma_ok). Q = 1.0 quando ambos verificam.
    Para casos com b/t > limite, o cálculo de largura efetiva (5.3.4.2)
    deve ser implementado separadamente.
    """
    mesa_ok = bf_2tf <= bt_lim_mesa
    alma_ok = ht_w <= bt_lim_alma
    Q = 1.0 if (mesa_ok and alma_ok) else None  # None sinaliza necessidade de Aef
    return Q, mesa_ok, alma_ok


def forca_flambagem_euler(I_cm4, L_cm, E=E_ACO):
    """
    Força axial de flambagem por flexão (Euler).
    NBR 8800:2024, 5.3.5.1:  Ne = π²·E·I / L²

    I em cm⁴, L (comprimento destravado) em cm. Retorna kN.
    """
    return (math.pi ** 2 * E * I_cm4) / (L_cm ** 2)


def esbeltez_reduzida(Ag, fy, Ne):
    """
    Índice de esbeltez reduzido.
    NBR 8800:2024, eq. 5.3.3.2:  λ0 = √(Ag·fy / Ne)

    Ag em cm², fy em kN/cm², Ne em kN. Retorna adimensional.
    """
    return math.sqrt((Ag * fy) / Ne)


def esbeltez_reduzida_simplificada(k, L_cm, r_cm, fy, E=E_ACO):
    """
    Índice de esbeltez reduzido — forma equivalente didática.
    Equivale a λ0 = (kL/r)/π · √(fy/E), que numericamente dá
    λ0 ≈ 0,0113·(kL/r) para fy=25 e E=20000 (método clássico).

    Usar quando se conhece o raio de giração r diretamente, sem calcular Ne.
    k = fator de comprimento de flambagem (geralmente 1,0).
    """
    lambda_fisico = (k * L_cm) / r_cm
    return (lambda_fisico / math.pi) * math.sqrt(fy / E)


def fator_chi(lambda_0):
    """
    Fator de redução χ associado à resistência à compressão.
    NBR 8800:2024, eq. 5.3.3.1:
        χ = 0,658^(λ0²)      se λ0 ≤ 1,5
        χ = 0,877 / λ0²      se λ0 > 1,5

    Retorna adimensional.
    """
    if lambda_0 <= 1.5:
        return 0.658 ** (lambda_0 ** 2)
    else:
        return 0.877 / (lambda_0 ** 2)


def resistencia_compressao(chi, Aef, fy):
    """
    Força axial de compressão resistente de cálculo.
    NBR 8800:2024, eq. 5.3.2:  Nc,Rd = χ·Aef·fy / γa1

    Aef em cm², fy em kN/cm². Retorna kN.
    """
    return (chi * Aef * fy) / GAMMA_A1


# =============================================================================
# MÓDULO 4 — VENTO
# =============================================================================

def fator_S2(b, Fr, p, z):
    """
    Fator S2 (rugosidade, dimensões, altura).
    NBR 6123:2023, 5.3.3:  S2 = b · Fr · (z/10)^p

    z em metros. A norma mantém S2 constante até z = 10 m em categorias
    altas (o tratamento de z < 10 deve usar z = 10 nesses casos, conforme
    prática usual). Retorna adimensional.
    """
    z_calc = max(z, 10.0) if p >= 0.12 else z  # piso de 10 m p/ cat. altas
    return b * Fr * (z_calc / 10.0) ** p


def velocidade_caracteristica(V0, S1, S2, S3):
    """
    Velocidade característica do vento.
    NBR 6123:2023, 5.1:  Vk = V0 · S1 · S2 · S3

    V0 em m/s. Retorna m/s.
    """
    return V0 * S1 * S2 * S3


def pressao_dinamica(Vk):
    """
    Pressão dinâmica do vento.
    NBR 6123:2023, 4.2-c):  q = 0,613 · Vk²   (Vk em m/s, q em N/m²)

    Retorna q em kN/m² (convertido de N/m²).
    """
    q_N = COEF_PRESSAO_DINAMICA * (Vk ** 2)
    return q_N / 1000.0  # N/m² → kN/m²


def forca_arrasto(q_kNm2, Ca, Ae_m2, fv=1.0):
    """
    Força de arrasto sobre uma faixa.
    NBR 6123:2023, 6.1:  Fa = Ca · q · Ae · (fator de vizinhança)

    q em kN/m², Ae em m². Retorna kN.
    """
    return q_kNm2 * Ca * Ae_m2 * fv


# =============================================================================
# SANITY CHECK — validação de ordem de grandeza
# =============================================================================

def sanity_check_tracao(Nt_Rd_kN):
    """
    Verifica se o resultado de tração está em faixa plausível.
    Retorna (ok: bool, mensagem: str).
    Uma chapa/perfil de aço deve dar dezenas a milhares de kN.
    """
    if Nt_Rd_kN < 10:
        return False, ("Resultado muito baixo (< 10 kN). "
                       "Verifique as unidades dos inputs (cm vs mm).")
    if Nt_Rd_kN > 50000:
        return False, ("Resultado muito alto (> 50.000 kN). "
                       "Verifique as unidades dos inputs.")
    return True, "Resultado dentro da faixa esperada."
