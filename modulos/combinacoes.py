"""
modulos/combinacoes.py
======================
MÓDULO 1 — Combinação Última Normal (NBR 8800:2024, seção 4.8.7.2.1)

Calcula Sd testando cada ação variável como principal e identifica a
combinação governante.
"""

import streamlit as st
import pandas as pd

from utils.calculos import combinacao_ultima_normal
from utils.constantes import GAMMA_G, GAMMA_Q, PSI_0


def render():
    st.header("Módulo 1 — Combinação Última Normal")
    st.caption("NBR 8800:2024 · Seção 4.8.7.2.1 (Estado-Limite Último)")

    # ---- Explicação da fórmula ----
    with st.expander("📖 Fórmula e fundamentação normativa", expanded=False):
        st.markdown(
            "A combinação última normal verifica o estado-limite último (ELU). "
            "Cada ação variável é testada como **principal** (valor característico "
            "cheio); as demais entram como **secundárias** (reduzidas por ψ₀)."
        )
        st.latex(r"S_d = \sum_i \gamma_{gi}\,F_{Gi,k} + \gamma_{q1}\,F_{Q1,k} + \sum_j \gamma_{qj}\,\psi_{0j}\,F_{Qj,k}")
        st.markdown(
            "**Coeficientes (Tabelas 1 e 2 da norma):**\n"
            "- Permanente (peso próprio de aço): γg = 1,25\n"
            "- Sobrecarga: γq = 1,5 · (ψ₀ = 0,8 como secundária)\n"
            "- Vento: γq = 1,4 · (ψ₀ = 0,6 como secundária)\n"
            "- Viga de rolamento: γq = 1,5 · (ψ₀ = 0,8 como secundária)"
        )

    st.info(
        "💡 **Caso de teste pré-carregado** (treliça, barra 2-3): "
        "F_perm=24,3 · F_SC=58,3 · F_vento=0 · F_VR=0 → **Sd esperado = 117,82 kN**"
    )

    # ---- Entradas ----
    st.subheader("Esforços na barra (kN)")
    st.warning(
        "⚠️ Insira o **esforço que cada ação produz NA BARRA** em análise "
        "(obtido via Ftool ou equilíbrio). **NÃO** insira a carga bruta. "
        "Em uma treliça, cada carga gera um esforço diferente em cada barra."
    )

    col1, col2 = st.columns(2)
    with col1:
        f_perm = st.number_input("Permanente (peso próprio)", value=24.3, step=0.1, format="%.2f")
        f_sc = st.number_input("Sobrecarga", value=58.3, step=0.1, format="%.2f")
    with col2:
        f_vento = st.number_input("Vento", value=0.0, step=0.1, format="%.2f")
        f_vr = st.number_input("Viga de rolamento", value=0.0, step=0.1, format="%.2f")

    # ---- Configuração de coeficientes ----
    esforcos = {
        "permanente": f_perm,
        "sobrecarga": f_sc,
        "vento": f_vento,
        "viga_rolamento": f_vr,
    }
    coefs_gamma = {
        "permanente": GAMMA_G["peso_proprio_aco"],   # 1.25
        "sobrecarga": GAMMA_Q["sobrecarga"],          # 1.5
        "vento": GAMMA_Q["vento"],                    # 1.4
        "viga_rolamento": GAMMA_Q["viga_rolamento"],  # 1.5
    }
    coefs_psi = {
        "sobrecarga": PSI_0["sobrecarga_deposito"],         # 0.8
        "vento": PSI_0["vento"],                            # 0.6
        "viga_rolamento": PSI_0["pilar_suporte_rolamento"], # 0.7 → ajustável
    }
    # Para viga de rolamento sobre pilar, ψ0 = 0,7. Se for a própria viga
    # de rolamento de ponte rolante, usar 1,0. Mantemos 0,8 do caso de prova:
    coefs_psi["viga_rolamento"] = 0.8

    # ---- Cálculo: testar cada variável como principal ----
    nomes_legiveis = {
        "sobrecarga": "Sobrecarga (SC)",
        "vento": "Vento",
        "viga_rolamento": "Viga de rolamento",
    }
    resultados = []
    for var in ["sobrecarga", "vento", "viga_rolamento"]:
        sd = combinacao_ultima_normal(esforcos, coefs_gamma, coefs_psi, principal=var)
        resultados.append({"Variável principal": nomes_legiveis[var], "Sd (kN)": round(sd, 2)})

    df = pd.DataFrame(resultados)
    sd_governante = df["Sd (kN)"].max()
    idx_gov = df["Sd (kN)"].idxmax()
    var_gov = df.loc[idx_gov, "Variável principal"]

    # ---- Saída ----
    st.subheader("Resultados das combinações")

    def destacar(row):
        cor = "background-color: #1b5e20; color: white; font-weight: bold" \
            if row["Sd (kN)"] == sd_governante else ""
        return [cor] * len(row)

    st.dataframe(df.style.apply(destacar, axis=1), use_container_width=True, hide_index=True)

    st.metric(
        label=f"Sd governante (combinação: {var_gov} principal)",
        value=f"{sd_governante:.2f} kN",
    )

    # ---- Desenvolvimento detalhado ----
    with st.expander("🔍 Desenvolvimento de cada combinação"):
        for var in ["sobrecarga", "vento", "viga_rolamento"]:
            sd = combinacao_ultima_normal(esforcos, coefs_gamma, coefs_psi, principal=var)
            st.markdown(f"**{nomes_legiveis[var]} como principal:**")
            termos = []
            for acao, esf in esforcos.items():
                if esf == 0:
                    continue
                if acao == "permanente":
                    termos.append(f"{coefs_gamma[acao]}\\cdot{esf}")
                elif acao == var:
                    termos.append(f"{coefs_gamma[acao]}\\cdot{esf}")
                else:
                    psi = coefs_psi.get(acao, 1.0)
                    termos.append(f"{coefs_gamma[acao]}\\cdot{psi}\\cdot{esf}")
            expr = " + ".join(termos) if termos else "0"
            st.latex(rf"S_d = {expr} = {sd:.2f}\ \text{{kN}}")

    # ---- Passar para o Módulo 2 ----
    if st.button("➡️ Usar este Sd no Módulo 2 (Tração)"):
        st.session_state["Sd_modulo1"] = sd_governante
        st.success(f"Sd = {sd_governante:.2f} kN salvo. Abra o Módulo 2 no menu lateral.")
