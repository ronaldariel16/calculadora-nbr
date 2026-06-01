# Calculadora Estrutural — NBR 8800 / NBR 6123

Aplicação web em **Streamlit** para dimensionamento de estruturas metálicas
conforme as normas brasileiras vigentes. Desenvolvida como ferramenta
educacional para estudantes de Engenharia Civil.

> **Status:** Módulos 1 e 2 implementados. Módulos 3 e 4 no roadmap.

---

## O que esta calculadora faz

| Módulo | Norma | Função |
|--------|-------|--------|
| 1. Combinação de Ações | NBR 8800:2024 | Combinação última normal (ELU) |
| 2. Tração | NBR 8800:2024 | Escoamento + ruptura (com furos em zigue-zague) |
| 3. Compressão | NBR 8800:2024 | Flambagem local + global (roadmap) |
| 4. Vento | NBR 6123:2023 | Força de arrasto + curva do vento (roadmap) |

---

## Instalação

Requer Python 3.10 ou superior.

```bash
# 1. Clonar o repositório
git clone https://github.com/SEU_USUARIO/calculadora-nbr.git
cd calculadora-nbr

# 2. (Opcional, recomendado) criar ambiente virtual
python -m venv .venv
source .venv/bin/activate     # Linux/Mac
.venv\Scripts\activate        # Windows

# 3. Instalar dependências
pip install -r requirements.txt
```

---

## Como rodar

```bash
streamlit run app.py
```

O navegador abre automaticamente em `http://localhost:8501`.

---

## Deploy no Streamlit Cloud (grátis)

1. Suba o projeto para um repositório público no GitHub.
2. Acesse [share.streamlit.io](https://share.streamlit.io) e faça login com GitHub.
3. Clique em **New app**, selecione o repositório e o arquivo `app.py`.
4. Clique em **Deploy**. Em ~2 minutos a aplicação fica online com URL própria.

---

## Estrutura do projeto

```
calculadora_nbr/
├── app.py                  # Entrada principal e navegação
├── requirements.txt        # Dependências
├── .gitignore
├── README.md
├── .streamlit/
│   └── config.toml         # Tema visual
├── modulos/
│   ├── combinacoes.py      # Módulo 1
│   ├── tracao.py           # Módulo 2
│   ├── compressao.py       # Módulo 3 (placeholder)
│   └── vento.py            # Módulo 4 (placeholder)
├── dados/
│   └── perfis.py           # Tabelas de perfis Gerdau
├── utils/
│   ├── constantes.py       # Coeficientes normativos
│   └── calculos.py         # Funções de cálculo reutilizáveis
└── docs/
    ├── CASOS_DE_PRUEBA.md  # Casos de validação verificados
    └── REFERENCIAS_NORMA.md # Trechos da norma usados
```

---

## Validação

Todos os módulos têm casos de teste verificados manualmente contra a norma.
Ver `docs/CASOS_DE_PRUEBA.md`. Cada módulo carrega um exemplo por padrão
e mostra o resultado esperado para o usuário comparar.

| Módulo | Caso | Resultado esperado |
|--------|------|--------------------|
| 1 | Treliça (barra 2-3) | Sd = 117,82 kN |
| 2 | Chapa 240×8 mm | Nt,Rd = 429,0 kN |
| 3 | CS 300×109 | Nc,Rd = 1.812 kN |
| 4 | Edifício 50 m | Fa,total = 1.998 kN |

---

## Limitações

Esta ferramenta **não** cobre:

- Ligações soldadas (apenas parafusadas)
- Flexão, cisalhamento ou esforços combinados
- Análise estrutural (cálculo de esforços) — use Ftool ou similar
- Perfis fora do catálogo Gerdau incluído
- Estados-limite de serviço (deslocamentos, vibrações)
- Verificação de fadiga

Os esforços solicitantes (Sd) devem ser obtidos previamente por análise
estrutural. Esta calculadora faz a **verificação de resistência**, não a análise.

---

## Roadmap

- [x] Módulo 1 — Combinação de ações
- [x] Módulo 2 — Tração
- [ ] Módulo 3 — Compressão (flambagem)
- [ ] Módulo 4 — Vento (força de arrasto + curva)
- [ ] Exportação de relatório em PDF
- [ ] Módulo de flexão (NBR 8800 seção 5.4)

---

## Aviso legal

Ferramenta **educacional**. Os resultados devem sempre ser verificados por
um engenheiro responsável habilitado. Os autores não se responsabilizam pelo
uso dos resultados em projetos reais.

---

## Créditos

- **ABNT NBR 8800:2024** — Projeto de estruturas de aço e mistas de aço e concreto
- **ABNT NBR 6123:2023** — Forças devidas ao vento em edificações
- **Catálogo Gerdau** — Perfis Estruturais (W, HP, CS)

Desenvolvido por **Ronald Ariel** — Engenharia Civil, UNILA.
