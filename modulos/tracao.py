"""
modulos/tracao.py
=================
MÓDULO 2 — Dimensionamento à Tração (NBR 8800:2024, seção 5.2)

Dois estados-limite:
  1. Escoamento da seção bruta  (5.2.2-a)
  2. Ruptura da seção líquida efetiva (5.2.2-b), com furos em zigue-zague.
"""

import streamlit as st
import pandas as pd

from utils.calculos import (
    resistencia_escoamento, resistencia_ruptura, diametro_furo,
    area_liquida_secao, area_liquida_efetiva, sanity_check_tracao,
)
from utils.constantes import ACOS, FOLGA_FURO, GAMMA_A1, GAMMA_A2
from dados.perfis import CANTONEIRAS


def render():
    st.header("Módulo 2 — Dimensionamento à Tração")
    st.caption("NBR 8800:2024 · Seção 5.2")

    with st.expander("📖 Fórmulas e fundamentação normativa"):
        st.markdown("**Dois estados-limite a verificar:**")
        st.latex(r"\text{1. Escoamento:}\quad N_{t,Rd} = \frac{A_g\,f_y}{\gamma_{a1}}\quad(\gamma_{a1}=1{,}10)")
        st.latex(r"\text{2. Ruptura:}\quad N_{t,Rd} = \frac{A_e\,f_u}{\gamma_{a2}}\quad(\gamma_{a2}=1{,}35)")
        st.markdown("Área líquida com furos em zigue-zague (5.2.4.1-b):")
        st.latex(r"A_n = A_g - \sum (d_f\,t) + \sum \frac{s^2}{4g}\,t")
        st.markdown(
            "Dimensão do furo (5.2.4.1-a): **df = d + 2,0 mm** (furo padrão puncionado) "
            "ou **df = d** (furo com broca). _Nota: a NBR 8800:2024 unificou em +2,0 mm; "
            "a versão 2008 usava +3,5 mm para puncionado._"
        )

    st.info(
        "💡 **Caso de teste pré-carregado** (chapa 240×8 mm, MR-250, d=19 mm "
        "puncionado, s=32, g=64): seção 2-2 governa → **Nt,Rd esperado = 429,0 kN**"
    )

    # ===================================================================
    # ENTRADA: solicitação
    # ===================================================================
    st.subheader("1. Esforço solicitante")
    sd_raw = st.session_state.get("Sd_modulo1")
    sd_default = sd_raw if sd_raw is not None else 117.82
    if sd_raw is not None:
        st.success(f"Sd importado do Módulo 1: {sd_default:.2f} kN")
    sd = st.number_input("Sd — força de tração solicitante (kN)", value=float(sd_default), step=1.0)

    # ===================================================================
    # ENTRADA: material e geometria
    # ===================================================================
    st.subheader("2. Material e perfil")
    col1, col2 = st.columns(2)
    with col1:
        aco_nome = st.selectbox("Aço", list(ACOS.keys()),
                                index=list(ACOS.keys()).index("MR-250"))
        fy = ACOS[aco_nome]["fy"]
        fu = ACOS[aco_nome]["fu"]
        st.caption(f"fy = {fy} kN/cm² · fu = {fu} kN/cm²")

        tipo = st.selectbox("Tipo de elemento",
                            ["Chapa", "Cantoneira simples", "Duas cantoneiras"])
    with col2:
        if tipo == "Chapa":
            largura_mm = st.number_input("Largura da chapa (mm)", value=240.0, step=1.0)
            esp_mm = st.number_input("Espessura da chapa (mm)", value=8.0, step=0.5)
            Ag = (largura_mm / 10.0) * (esp_mm / 10.0)  # cm²
            t_cm = esp_mm / 10.0
            Ct = 1.0
            st.caption("Ct = 1,0 (força transmitida diretamente à seção)")
        else:
            perfil_nome = st.selectbox("Cantoneira (catálogo Gerdau)", list(CANTONEIRAS.keys()))
            p = CANTONEIRAS[perfil_nome]
            n_cant = 2 if tipo == "Duas cantoneiras" else 1
            Ag = p["Ag_cm2"] * n_cant
            t_cm = p["t_mm"] / 10.0
            Ct = st.number_input(
                "Ct (coeficiente de redução da área líquida)",
                value=0.85, min_value=0.5, max_value=1.0, step=0.05,
                help="Para cantoneira ligada por uma aba, tipicamente Ct ≈ 0,85 "
                     "(NBR 8800:2024, 5.2.5). Depende do nº de parafusos e geometria.",
            )
        st.metric("Área bruta Ag", f"{Ag:.2f} cm²")

    # ===================================================================
    # ENTRADA: parafusos e furos
    # ===================================================================
    st.subheader("3. Furos e seções de ruptura")
    col3, col4 = st.columns(2)
    with col3:
        d_parafuso = st.number_input("Diâmetro do parafuso (mm)", value=19.0, step=1.0)
        tipo_furo = st.selectbox("Tipo de furo", ["puncionado", "broca"])
    with col4:
        folga = FOLGA_FURO[tipo_furo]
        df_mm = diametro_furo(d_parafuso, folga)
        df_cm = df_mm / 10.0
        st.metric("Dimensão do furo df", f"{df_mm:.1f} mm")
        st.caption(f"df = {d_parafuso} + {folga} = {df_mm} mm (folga: {tipo_furo})")

    st.markdown("**Defina as seções de ruptura a verificar:**")
    st.caption(
        "Para cada seção, informe quantos furos ela corta e quantos trechos "
        "diagonais possui. Trechos diagonais usam s (longitudinal) e g (transversal)."
    )

    n_secoes = st.number_input("Número de seções a analisar", value=3, min_value=1, max_value=6, step=1)

    s_padrao = st.number_input("s padrão — espaçamento longitudinal (mm)", value=32.0, step=1.0)
    g_padrao = st.number_input("g padrão — espaçamento transversal/gabarito (mm)", value=64.0, step=1.0)
    s_cm = s_padrao / 10.0
    g_cm = g_padrao / 10.0

    secoes_dados = []
    for i in range(int(n_secoes)):
        st.markdown(f"**Seção {i+1}-{i+1}:**")
        c1, c2 = st.columns(2)
        with c1:
            nf = st.number_input(f"Nº de furos cortados (seção {i+1})",
                                 value=[2, 3, 3][i] if i < 3 else 2,
                                 min_value=0, max_value=20, step=1, key=f"nf_{i}")
        with c2:
            nd = st.number_input(f"Nº de trechos diagonais (seção {i+1})",
                                 value=[0, 1, 2][i] if i < 3 else 0,
                                 min_value=0, max_value=20, step=1, key=f"nd_{i}")
        diagonais = [(s_cm, g_cm) for _ in range(int(nd))]
        secoes_dados.append({"nome": f"{i+1}-{i+1}", "n_furos": int(nf), "diagonais": diagonais})

    # ===================================================================
    # CÁLCULO
    # ===================================================================
    st.subheader("Resultados")

    # Escoamento
    nt_escoamento = resistencia_escoamento(Ag, fy)

    # Áreas líquidas por seção
    linhas = []
    for sec in secoes_dados:
        An = area_liquida_secao(Ag, sec["n_furos"], df_cm, t_cm, sec["diagonais"])
        linhas.append({
            "Seção": sec["nome"],
            "Furos": sec["n_furos"],
            "Diagonais": len(sec["diagonais"]),
            "An (cm²)": round(An, 2),
        })
    df_secoes = pd.DataFrame(linhas)
    An_min = df_secoes["An (cm²)"].min()
    idx_gov = df_secoes["An (cm²)"].idxmin()
    secao_gov = df_secoes.loc[idx_gov, "Seção"]

    # Ruptura
    Ae = area_liquida_efetiva(An_min, Ct)
    nt_ruptura = resistencia_ruptura(Ae, fu)

    nt_rd = min(nt_escoamento, nt_ruptura)
    modo = "Escoamento" if nt_escoamento < nt_ruptura else "Ruptura"

    # ---- Tabela de seções com destaque ----
    def destacar_gov(row):
        cor = "background-color: #b71c1c; color: white; font-weight: bold" \
            if row["An (cm²)"] == An_min else ""
        return [cor] * len(row)

    st.markdown("**Áreas líquidas por seção:**")
    st.dataframe(df_secoes.style.apply(destacar_gov, axis=1),
                 use_container_width=True, hide_index=True)
    st.caption(f"Seção crítica (menor An): **{secao_gov}** → An = {An_min:.2f} cm²")

    # ---- Métricas dos dois modos ----
    cm1, cm2 = st.columns(2)
    cm1.metric("Escoamento — Nt,Rd", f"{nt_escoamento:.1f} kN")
    cm2.metric("Ruptura — Nt,Rd", f"{nt_ruptura:.1f} kN")

    st.metric(f"Nt,Rd final (governa: {modo})", f"{nt_rd:.1f} kN")

    # ---- Sanity check ----
    ok_sc, msg_sc = sanity_check_tracao(nt_rd)
    if not ok_sc:
        st.warning(f"⚠️ {msg_sc}")

    # ---- Verificação final ----
    if nt_rd >= sd:
        razao = nt_rd / sd if sd > 0 else float("inf")
        st.success(f"✅ **VERIFICA** — Nt,Rd = {nt_rd:.1f} kN ≥ Sd = {sd:.1f} kN "
                   f"(folga de {((razao-1)*100):.0f}%)")
    else:
        st.error(f"❌ **NÃO VERIFICA** — Nt,Rd = {nt_rd:.1f} kN < Sd = {sd:.1f} kN")
        if tipo != "Chapa":
            st.info("💡 Tente um perfil maior do catálogo no seletor acima.")

    # ---- Desenvolvimento ----
    with st.expander("🔍 Desenvolvimento dos cálculos"):
        st.markdown("**Escoamento da seção bruta:**")
        st.latex(rf"N_{{t,Rd}} = \frac{{A_g \cdot f_y}}{{\gamma_{{a1}}}} = "
                 rf"\frac{{{Ag:.2f} \cdot {fy}}}{{{GAMMA_A1}}} = {nt_escoamento:.1f}\ \text{{kN}}")
        st.markdown(f"**Ruptura (seção crítica {secao_gov}):**")
        st.latex(rf"A_e = C_t \cdot A_n = {Ct} \cdot {An_min:.2f} = {Ae:.2f}\ \text{{cm}}^2")
        st.latex(rf"N_{{t,Rd}} = \frac{{A_e \cdot f_u}}{{\gamma_{{a2}}}} = "
                 rf"\frac{{{Ae:.2f} \cdot {fu}}}{{{GAMMA_A2}}} = {nt_ruptura:.1f}\ \text{{kN}}")
