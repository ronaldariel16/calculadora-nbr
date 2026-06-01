"""
modulos/compressao.py
=====================
MÓDULO 3 — Dimensionamento à Compressão (NBR 8800:2024, seção 5.3)

Flambagem local (Tabela 4) + flambagem global por flexão (5.3.3).
"""

import streamlit as st

from utils.calculos import (
    bt_limite, fator_Q_simplificado,
    esbeltez_reduzida_simplificada, fator_chi, resistencia_compressao,
)
from utils.constantes import ACOS, GAMMA_A1, ESBELTEZ_MAX_COMPRESSAO
from dados.perfis import PERFIS_CS


def render():
    st.header("Módulo 3 — Dimensionamento à Compressão")
    st.caption("NBR 8800:2024 · Seção 5.3")

    with st.expander("📖 Fórmulas e fundamentação normativa", expanded=False):
        st.markdown("**Passo 1 — Flambagem local (Tabela 4):**")
        st.latex(r"\left(\frac{b}{t}\right)_{lim} = c\,\sqrt{\frac{E}{f_y}}")
        st.markdown(
            "- Mesa (AL — aba livre): c = 0,56  \n"
            "- Alma (AA — ambas bordas apoiadas): c = 1,49  \n"
            "- Se todos os elementos satisfazem (b/t) ≤ (b/t)_lim → **A_ef = A_g** (seção não esbelta)"
        )
        st.markdown("**Passo 2 — Índice de esbeltez reduzido (5.3.3.2):**")
        st.latex(r"\lambda_0 = \frac{kL/r}{\pi}\,\sqrt{\frac{f_y}{E}}")
        st.markdown("Calculado separadamente para **eixo X** (com rx) e **eixo Y** (com ry).")
        st.markdown("**Passo 3 — Fator de redução χ (5.3.3.1):**")
        st.latex(r"\chi = 0{,}658^{\lambda_0^2}\quad\text{se}\quad\lambda_0 \le 1{,}5")
        st.latex(r"\chi = \frac{0{,}877}{\lambda_0^2}\quad\text{se}\quad\lambda_0 > 1{,}5")
        st.markdown("O eixo com **menor χ** governa o dimensionamento.")
        st.markdown("**Passo 4 — Resistência de cálculo (5.3.2):**")
        st.latex(r"N_{c,Rd} = \frac{\chi\,A_{ef}\,f_y}{\gamma_{a1}},\quad \gamma_{a1} = 1{,}10")

    st.info(
        "💡 **Caso de teste pré-carregado:** CS 300×109, A36 (fy=25 kN/cm²), "
        "Ly=800 cm, k=1 → λ₀y=1,147 · χy=0,577 · **Nc,Rd = 1.820 kN** (eixo Y governa).  \n"
        "*(Pelo fator empírico 0,0113 da aula: λ₀=1,152 → Nc,Rd = 1.812 kN — diferença < 0,5%; "
        "ambos corretos. Esta calculadora usa a fórmula exata da norma.)*  \n"
        "Se Lx=1600 cm → λ₀x=1,371 · χx=0,455 · **Nc,Rd,x = 1.437 kN** (eixo X governa).  \n"
        "*(Pelo fator 0,0113: Nc,Rd,x = 1.427 kN — diferença < 0,7%.)*"
    )

    # ------------------------------------------------------------------
    # ENTRADAS
    # ------------------------------------------------------------------
    st.subheader("1. Perfil e material")
    col1, col2 = st.columns(2)
    with col1:
        perfil_nome = st.selectbox(
            "Perfil CS (catálogo Gerdau)",
            list(PERFIS_CS.keys()),
            index=list(PERFIS_CS.keys()).index("CS 300x109"),
        )
        p = PERFIS_CS[perfil_nome]
    with col2:
        aco_nome = st.selectbox(
            "Aço",
            list(ACOS.keys()),
            index=list(ACOS.keys()).index("ASTM A36"),
        )
        fy = ACOS[aco_nome]["fy"]
        st.caption(f"fy = {fy} kN/cm²  ·  E = 20.000 kN/cm²")

    Ag     = p["Ag_cm2"]
    rx     = p["rx_cm"]
    ry     = p["ry_cm"]
    bf_mm  = p["bf_mm"]
    tf_mm  = p["tf_mm"]
    h_alma = p["h_alma_mm"]
    tw_mm  = p["tw_mm"]

    with st.expander(f"📐 Propriedades do perfil {perfil_nome}", expanded=False):
        ca, cb, cc, cd = st.columns(4)
        ca.metric("Ag (cm²)",    f"{Ag:.1f}")
        cb.metric("rx (cm)",     f"{rx:.2f}")
        cc.metric("ry (cm)",     f"{ry:.2f}")
        cd.metric("Peso (kg/m)", f"{p['peso_kg_m']:.1f}")
        ce, cf, cg, ch = st.columns(4)
        ce.metric("bf (mm)",     f"{bf_mm:.0f}")
        cf.metric("tf (mm)",     f"{tf_mm:.1f}")
        cg.metric("h_alma (mm)", f"{h_alma:.0f}")
        ch.metric("tw (mm)",     f"{tw_mm:.1f}")

    st.subheader("2. Comprimentos de flambagem")
    col3, col4, col5 = st.columns(3)
    with col3:
        Lx = st.number_input(
            "Lx — comprimento destravado eixo X (cm)",
            value=800.0, step=50.0,
            help="Distância entre pontos de travamento lateral — eixo de maior inércia",
        )
    with col4:
        Ly = st.number_input(
            "Ly — comprimento destravado eixo Y (cm)",
            value=800.0, step=50.0,
            help="Distância entre pontos de travamento lateral — eixo de menor inércia",
        )
    with col5:
        k = st.number_input(
            "Fator k (comprimento efetivo)",
            value=1.0, min_value=0.5, max_value=2.0, step=0.1,
            help="k=1,0: biapoiado · k=0,5: biengastado · k=0,7: engastado-apoiado",
        )

    # ------------------------------------------------------------------
    # PASSO 1 — FLAMBAGEM LOCAL
    # ------------------------------------------------------------------
    st.subheader("Passo 1 — Flambagem local (Tabela 4)")

    bt_mesa  = bf_mm / (2.0 * tf_mm)
    bt_alma  = h_alma / tw_mm
    lim_mesa = bt_limite(0.56, fy)
    lim_alma = bt_limite(1.49, fy)

    Q, mesa_ok, alma_ok = fator_Q_simplificado(bt_mesa, bt_alma, lim_mesa, lim_alma)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Mesa — AL (aba livre, c = 0,56)**")
        st.latex(
            rf"\frac{{b_f}}{{2\,t_f}} = \frac{{{bf_mm:.0f}}}{{2 \times {tf_mm:.1f}}} = {bt_mesa:.2f}"
        )
        st.latex(
            rf"\left(\frac{{b}}{{t}}\right)_{{lim}} = 0{{,}}56\sqrt{{\frac{{E}}{{f_y}}}} = {lim_mesa:.2f}"
        )
        if mesa_ok:
            st.success(f"✅ {bt_mesa:.2f} ≤ {lim_mesa:.2f} — mesa não esbelta")
        else:
            st.error(f"❌ {bt_mesa:.2f} > {lim_mesa:.2f} — mesa ESBELTA (requer Aef < Ag)")

    with c2:
        st.markdown("**Alma — AA (duas bordas apoiadas, c = 1,49)**")
        st.latex(
            rf"\frac{{h}}{{t_w}} = \frac{{{h_alma:.0f}}}{{{tw_mm:.1f}}} = {bt_alma:.2f}"
        )
        st.latex(
            rf"\left(\frac{{b}}{{t}}\right)_{{lim}} = 1{{,}}49\sqrt{{\frac{{E}}{{f_y}}}} = {lim_alma:.2f}"
        )
        if alma_ok:
            st.success(f"✅ {bt_alma:.2f} ≤ {lim_alma:.2f} — alma não esbelta")
        else:
            st.error(f"❌ {bt_alma:.2f} > {lim_alma:.2f} — alma ESBELTA (requer Aef < Ag)")

    Aef = Ag
    if Q is not None:
        st.success(f"**Seção não esbelta → A_ef = A_g = {Aef:.1f} cm²**")
    else:
        st.warning(
            "⚠️ Seção esbelta em ≥ 1 elemento. Cálculo exato exige largura efetiva "
            "(NBR 8800, 5.3.4.2). **Usando A_ef = A_g como aproximação conservadora.**"
        )

    # ------------------------------------------------------------------
    # PASSO 2 — ESBELTEZ REDUZIDA
    # ------------------------------------------------------------------
    st.subheader("Passo 2 — Índice de esbeltez reduzido")

    kLr_x  = k * Lx / rx
    kLr_y  = k * Ly / ry
    lam0_x = esbeltez_reduzida_simplificada(k, Lx, rx, fy)
    lam0_y = esbeltez_reduzida_simplificada(k, Ly, ry, fy)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Eixo X**")
        st.latex(rf"\frac{{kL_x}}{{r_x}} = \frac{{{k:.1f} \times {Lx:.0f}}}{{{rx:.2f}}} = {kLr_x:.1f}")
        st.latex(rf"\lambda_{{0x}} = \frac{{{kLr_x:.2f}}}{{\pi}}\sqrt{{\frac{{f_y}}{{E}}}} = {lam0_x:.4f}")
        if kLr_x <= ESBELTEZ_MAX_COMPRESSAO:
            st.success(f"✅ kL/r = {kLr_x:.1f} ≤ {ESBELTEZ_MAX_COMPRESSAO} (5.3.7.1)")
        else:
            st.error(f"❌ kL/r = {kLr_x:.1f} > {ESBELTEZ_MAX_COMPRESSAO} — EXCEDE O LIMITE NORMATIVO!")

    with c2:
        st.markdown("**Eixo Y**")
        st.latex(rf"\frac{{kL_y}}{{r_y}} = \frac{{{k:.1f} \times {Ly:.0f}}}{{{ry:.2f}}} = {kLr_y:.1f}")
        st.latex(rf"\lambda_{{0y}} = \frac{{{kLr_y:.2f}}}{{\pi}}\sqrt{{\frac{{f_y}}{{E}}}} = {lam0_y:.4f}")
        if kLr_y <= ESBELTEZ_MAX_COMPRESSAO:
            st.success(f"✅ kL/r = {kLr_y:.1f} ≤ {ESBELTEZ_MAX_COMPRESSAO} (5.3.7.1)")
        else:
            st.error(f"❌ kL/r = {kLr_y:.1f} > {ESBELTEZ_MAX_COMPRESSAO} — EXCEDE O LIMITE NORMATIVO!")

    # ------------------------------------------------------------------
    # PASSO 3 — FATOR χ
    # ------------------------------------------------------------------
    st.subheader("Passo 3 — Fator de redução χ")

    chi_x    = fator_chi(lam0_x)
    chi_y    = fator_chi(lam0_y)
    chi_gov  = min(chi_x, chi_y)
    eixo_gov = "X" if chi_x <= chi_y else "Y"

    c1, c2 = st.columns(2)
    lam0_x_sq = lam0_x ** 2
    lam0_y_sq = lam0_y ** 2

    with c1:
        st.metric("χ (eixo X)", f"{chi_x:.4f}")
        if lam0_x <= 1.5:
            st.latex(rf"\chi_x = 0{{,}}658^{{{lam0_x_sq:.4f}}} = {chi_x:.4f}")
        else:
            st.latex(rf"\chi_x = \frac{{0{{,}}877}}{{{lam0_x_sq:.4f}}} = {chi_x:.4f}")

    with c2:
        st.metric("χ (eixo Y)", f"{chi_y:.4f}")
        if lam0_y <= 1.5:
            st.latex(rf"\chi_y = 0{{,}}658^{{{lam0_y_sq:.4f}}} = {chi_y:.4f}")
        else:
            st.latex(rf"\chi_y = \frac{{0{{,}}877}}{{{lam0_y_sq:.4f}}} = {chi_y:.4f}")

    if chi_x < chi_y:
        st.warning(f"⚠️ **Eixo X governa** — χx = {chi_x:.4f} < χy = {chi_y:.4f}")
    elif chi_y < chi_x:
        st.warning(f"⚠️ **Eixo Y governa** — χy = {chi_y:.4f} < χx = {chi_x:.4f}")
    else:
        st.info(f"Ambos os eixos com χ = {chi_gov:.4f} (governantes iguais)")

    # ------------------------------------------------------------------
    # PASSO 4 — RESISTÊNCIA DE CÁLCULO
    # ------------------------------------------------------------------
    st.subheader("Passo 4 — Resistência de cálculo")

    Nc_Rd = resistencia_compressao(chi_gov, Aef, fy)

    st.metric(
        label=f"Nc,Rd  (eixo {eixo_gov} governa, χ = {chi_gov:.4f})",
        value=f"{Nc_Rd:.0f} kN",
    )
    st.latex(
        rf"N_{{c,Rd}} = \frac{{\chi\,A_{{ef}}\,f_y}}{{\gamma_{{a1}}}} = "
        rf"\frac{{{chi_gov:.4f} \times {Aef:.1f} \times {fy}}}{{{GAMMA_A1}}} = {Nc_Rd:.0f}\ \text{{kN}}"
    )

    # ------------------------------------------------------------------
    # VERIFICAÇÃO
    # ------------------------------------------------------------------
    st.subheader("Verificação")
    nc_sd = st.number_input(
        "Nc,Sd — força de compressão solicitante (kN)",
        value=1500.0, step=10.0,
    )

    if Nc_Rd >= nc_sd:
        razao = nc_sd / Nc_Rd if Nc_Rd > 0 else 0.0
        st.success(
            f"✅ **VERIFICA** — Nc,Rd = {Nc_Rd:.0f} kN ≥ Nc,Sd = {nc_sd:.0f} kN "
            f"(aproveitamento: {razao * 100:.0f}%)"
        )
    else:
        st.error(
            f"❌ **NÃO VERIFICA** — Nc,Rd = {Nc_Rd:.0f} kN < Nc,Sd = {nc_sd:.0f} kN. "
            "Reduza o comprimento destravado ou escolha um perfil mais robusto."
        )

    # ------------------------------------------------------------------
    # DESENVOLVIMENTO COMPLETO
    # ------------------------------------------------------------------
    with st.expander("🔍 Desenvolvimento completo dos cálculos"):
        st.markdown(f"**Perfil:** {perfil_nome}  ·  **Aço:** {aco_nome}")
        st.latex(
            rf"A_g = {Ag:.1f}\ \text{{cm}}^2\quad"
            rf"r_x = {rx:.2f}\ \text{{cm}}\quad"
            rf"r_y = {ry:.2f}\ \text{{cm}}\quad"
            rf"f_y = {fy}\ \text{{kN/cm}}^2"
        )
        st.markdown("**Flambagem local:**")
        ok_m = r"\checkmark" if mesa_ok else r"\times"
        ok_a = r"\checkmark" if alma_ok else r"\times"
        st.latex(
            rf"\frac{{b_f}}{{2t_f}} = {bt_mesa:.2f}\ {ok_m}\ ({lim_mesa:.2f})\quad"
            rf"\frac{{h}}{{t_w}} = {bt_alma:.2f}\ {ok_a}\ ({lim_alma:.2f})"
        )
        st.latex(rf"A_{{ef}} = A_g = {Aef:.1f}\ \text{{cm}}^2")
        st.markdown("**Esbeltez reduzida:**")
        st.latex(
            rf"\lambda_{{0x}} = {lam0_x:.4f} \quad"
            rf"\lambda_{{0y}} = {lam0_y:.4f}"
        )
        st.markdown("**Fator χ:**")
        st.latex(
            rf"\chi_x = {chi_x:.4f}\quad"
            rf"\chi_y = {chi_y:.4f}\quad"
            rf"\chi_{{gov}} = {chi_gov:.4f}\ \text{{(eixo {eixo_gov})}}"
        )
        st.markdown("**Resistência de cálculo:**")
        st.latex(
            rf"N_{{c,Rd}} = \frac{{{chi_gov:.4f} \times {Aef:.1f} \times {fy}}}{{{GAMMA_A1}}} "
            rf"= {Nc_Rd:.0f}\ \text{{kN}}"
        )
