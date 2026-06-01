"""
modulos/vento.py
================
MÓDULO 4 — Força de Arrasto do Vento (NBR 6123:2023)

Calcula Fa por faixas de altura (uma por pavimento), exibe tabela,
gráfico plotly e verificação de área de exposição.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.calculos import fator_S2, velocidade_caracteristica, pressao_dinamica, forca_arrasto
from utils.constantes import VENTO_PARAMS, S3_GRUPOS, V0_CIDADES


def render():
    st.header("Módulo 4 — Força de Arrasto do Vento")
    st.caption("NBR 6123:2023")

    with st.expander("📖 Fórmulas e fundamentação normativa", expanded=False):
        st.markdown("**Sequência de cálculo (uma iteração por pavimento):**")
        st.latex(r"S_2 = b\,F_r\,\left(\frac{z}{10}\right)^p \quad\text{(Tabela 1 — rugosidade/altura)}")
        st.latex(r"V_k = V_0\,S_1\,S_2\,S_3 \quad\text{(velocidade característica, m/s)}")
        st.latex(
            r"q = 0{,}613\,V_k^2 \quad\text{(N/m}^2\text{)}"
            r"\quad\longrightarrow\quad"
            r"q\ \text{em kN/m}^2\ (\div\,1000)"
        )
        st.latex(r"F_a = C_a\,q\,A_e \quad\text{(kN por faixa)}")
        st.markdown(
            "A edificação é dividida em **faixas** iguais (uma por pavimento). "
            "O **topo** de cada faixa define a altura *z* de cálculo do fator S₂. "
            "Para categorias III, IV e V (p ≥ 0,12), S₂ é mantido constante abaixo de z = 10 m."
        )

    st.info(
        "💡 **Caso de teste pré-carregado:** h=50 m · planta 25×25 m · "
        "Cat IV / Classe B · V₀=50 m/s · 15 pavimentos · S₁=1,0 · S₃=1,0 · Ca=1,2  \n"
        "→ **Fa,total esperado = 1.998 kN**  ·  Σ Ae = 1.250 m²."
    )

    # ------------------------------------------------------------------
    # ENTRADAS — PARÂMETROS DO VENTO
    # ------------------------------------------------------------------
    st.subheader("1. Parâmetros do vento")

    col1, col2, col3 = st.columns(3)

    with col1:
        cidade = st.selectbox("Cidade (V₀ de referência)", list(V0_CIDADES.keys()), index=0)
        if V0_CIDADES[cidade] > 0:
            V0 = float(V0_CIDADES[cidade])
            st.caption(f"V₀ = {V0:.0f} m/s (isopleta NBR 6123)")
        else:
            V0 = st.number_input(
                "V₀ manual (m/s)", value=45.0, min_value=20.0, max_value=70.0, step=1.0
            )

    with col2:
        categoria = st.selectbox(
            "Categoria de rugosidade",
            ["I", "II", "III", "IV", "V"],
            index=3,
            help=(
                "I = mar/lago aberto  ·  II = terr. aberto/plano  ·  "
                "III = subúrbios/bosques  ·  IV = urbano denso  ·  V = centro de metrópole"
            ),
        )
        classe = st.selectbox(
            "Classe da edificação",
            ["A", "B", "C"],
            index=1,
            help="A: menor dimensão ≤ 20 m  ·  B: 20–50 m  ·  C: > 50 m",
        )
        params = VENTO_PARAMS[categoria][classe]
        b_v, Fr_v, p_v = params["b"], params["Fr"], params["p"]
        st.caption(f"b = {b_v}  ·  Fr = {Fr_v}  ·  p = {p_v}")

    with col3:
        grupo_s3 = st.selectbox(
            "Grupo S₃ (fator estatístico, Tabela 3)",
            list(S3_GRUPOS.keys()),
            index=1,
        )
        S3 = S3_GRUPOS[grupo_s3]
        S1 = st.number_input(
            "S₁ — fator topográfico",
            value=1.0, min_value=0.8, max_value=1.35, step=0.05,
            help="Terreno plano: S₁=1,0  ·  Elevações e escarpas: ver NBR 6123 §5.3.1",
        )
        st.caption(f"S₃ = {S3}  ·  S₁ = {S1}")

    turbulencia = st.radio(
        "Coeficiente de arrasto Ca (NBR 6123, §6):",
        [
            "Baixa turbulência — Ca = 1,2  (edificação isolada, face de barlavento)",
            "Alta turbulência  — Ca = 0,95 (edificação em grupo)",
        ],
    )
    Ca = 1.2 if turbulencia.startswith("Baixa") else 0.95

    # ------------------------------------------------------------------
    # ENTRADAS — GEOMETRIA
    # ------------------------------------------------------------------
    st.subheader("2. Geometria da edificação")

    col4, col5, col6 = st.columns(3)
    with col4:
        h = st.number_input("h — altura total (m)", value=50.0, min_value=1.0, step=1.0)
    with col5:
        L1 = st.number_input(
            "L₁ — largura frontal (m)", value=25.0, min_value=1.0, step=1.0,
            help="Dimensão perpendicular ao vento — define Ae de cada faixa",
        )
        L2 = st.number_input(
            "L₂ — profundidade (m)", value=25.0, min_value=1.0, step=1.0,
            help="Dimensão paralela ao vento (referência para planta)",
        )
    with col6:
        n_pav = int(
            st.number_input("Número de pavimentos", value=15, min_value=1, max_value=200, step=1)
        )

    # ------------------------------------------------------------------
    # CÁLCULO POR FAIXA
    # ------------------------------------------------------------------
    h_pav    = h / n_pav        # altura de cada pavimento (m)
    Ae_faixa = L1 * h_pav       # área de exposição por faixa (m²)

    linhas = []
    for i in range(1, n_pav + 1):
        z   = i * h_pav
        s2  = fator_S2(b_v, Fr_v, p_v, z)
        vk  = velocidade_caracteristica(V0, S1, s2, S3)
        q   = pressao_dinamica(vk)          # kN/m²
        fa  = forca_arrasto(q, Ca, Ae_faixa)
        linhas.append({
            "Faixa":     i,
            "z (m)":     round(z,  2),
            "S₂":        round(s2, 4),
            "Vk (m/s)":  round(vk, 2),
            "q (kN/m²)": round(q,  4),
            "Ae (m²)":   round(Ae_faixa, 2),
            "Fa (kN)":   round(fa, 1),
        })

    df       = pd.DataFrame(linhas)
    Fa_total = df["Fa (kN)"].sum()
    Ae_total = df["Ae (m²)"].sum()

    # ------------------------------------------------------------------
    # TABELA
    # ------------------------------------------------------------------
    st.subheader("Resultados por faixa")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ------------------------------------------------------------------
    # GRÁFICO PLOTLY — curva do vento
    # ------------------------------------------------------------------
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Fa (kN)"],
        y=df["z (m)"],
        mode="lines+markers",
        name="Fa por faixa",
        line=dict(color="#1b5e20", width=2),
        marker=dict(size=7, color="#1b5e20", symbol="circle"),
    ))
    fig.update_layout(
        title="Curva do Vento — Força de Arrasto por Altura",
        xaxis_title="Fa (kN)",
        yaxis_title="Altura z (m)",
        height=420,
        plot_bgcolor="#f0f2f6",
        paper_bgcolor="#ffffff",
        font=dict(color="#262730"),
        xaxis=dict(gridcolor="#cccccc", zeroline=True, zerolinecolor="#aaaaaa"),
        yaxis=dict(gridcolor="#cccccc"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------------
    # RESULTADOS FINAIS
    # ------------------------------------------------------------------
    st.subheader("Resultado final")
    r1, r2 = st.columns(2)
    r1.metric("Fa,total", f"{Fa_total:.0f} kN")
    r2.metric("Σ Ae", f"{Ae_total:.1f} m²")

    Ae_esperado = L1 * h
    if abs(Ae_total - Ae_esperado) < 0.1:
        st.caption(
            f"✅ Verificação de área: Σ Ae = {Ae_total:.1f} m² "
            f"= L₁ × h = {L1:.0f} × {h:.0f} = {Ae_esperado:.0f} m² ✓"
        )
    else:
        st.caption(
            f"⚠️ Σ Ae = {Ae_total:.1f} m²  (esperado L₁ × h = {Ae_esperado:.0f} m²)"
        )

    # ------------------------------------------------------------------
    # DESENVOLVIMENTO
    # ------------------------------------------------------------------
    with st.expander("🔍 Parâmetros utilizados no cálculo"):
        st.latex(
            rf"V_0 = {V0:.0f}\ \text{{m/s}}\quad"
            rf"S_1 = {S1}\quad"
            rf"S_3 = {S3}\quad"
            rf"C_a = {Ca}"
        )
        st.latex(
            rf"b = {b_v}\quad"
            rf"F_r = {Fr_v}\quad"
            rf"p = {p_v}\quad"
            rf"\text{{(Categoria {categoria}, Classe {classe})}}"
        )
        st.latex(
            rf"h_{{pav}} = \frac{{{h:.0f}}}{{{n_pav}}} = {h_pav:.3f}\ \text{{m}}\quad"
            rf"A_e^{{faixa}} = {L1:.0f} \times {h_pav:.3f} = {Ae_faixa:.2f}\ \text{{m}}^2"
        )
        if p_v >= 0.12:
            st.markdown(
                f"Para Cat. **{categoria}** (p={p_v} ≥ 0,12): "
                "S₂ mantido constante até z = 10 m (piso de 10 m aplicado em `fator_S2`)."
            )
        st.markdown(
            f"Fa,total = **{Fa_total:.1f} kN**  ·  "
            f"Faixas 1–{n_pav} com z_topo de {h_pav:.2f} m a {h:.1f} m."
        )
