"""
app.py
======
Calculadora Estrutural — NBR 8800:2024 / NBR 6123:2023
Entrada principal e navegação entre módulos.

Para rodar:  streamlit run app.py
"""

import streamlit as st

from modulos import combinacoes, tracao, compressao, vento

# ---------------------------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Calculadora Estrutural NBR",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inicializa session_state (para passar Sd entre módulos)
if "Sd_modulo1" not in st.session_state:
    st.session_state["Sd_modulo1"] = None

# ---------------------------------------------------------------------------
# Barra lateral — navegação
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("🏗️ Calculadora Estrutural")
    st.caption("NBR 8800:2024 · NBR 6123:2023")
    st.divider()

    modulo = st.radio(
        "Selecione o módulo:",
        [
            "1 · Combinação de Ações",
            "2 · Tração",
            "3 · Compressão",
            "4 · Vento",
        ],
    )

    st.divider()
    st.caption(
        "Ferramenta **educacional**. Resultados devem ser verificados "
        "por engenheiro responsável habilitado."
    )
    if st.session_state.get("Sd_modulo1"):
        st.success(f"Sd em memória: {st.session_state['Sd_modulo1']:.2f} kN")

# ---------------------------------------------------------------------------
# Cabeçalho principal
# ---------------------------------------------------------------------------
st.title("Calculadora Estrutural — NBR 8800 / NBR 6123")
st.caption("Desenvolvido por **Ronald Ariel** — Engenharia Civil, UNILA")
st.divider()

# ---------------------------------------------------------------------------
# Roteamento de módulos
# ---------------------------------------------------------------------------
if modulo.startswith("1"):
    combinacoes.render()
elif modulo.startswith("2"):
    tracao.render()
elif modulo.startswith("3"):
    compressao.render()
elif modulo.startswith("4"):
    vento.render()

# ---------------------------------------------------------------------------
# Rodapé
# ---------------------------------------------------------------------------
st.divider()
st.caption(
    "📚 Baseado em ABNT NBR 8800:2024, NBR 6123:2023 e Catálogo Gerdau. "
    "Esta ferramenta não substitui o julgamento de um engenheiro responsável."
)
