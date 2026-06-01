# PROMPT PARA CLAUDE CODE (VS Code)

Copia todo lo que está dentro del bloque de abajo y pégalo en Claude Code
DESPUÉS de adjuntar los 3 PDFs (NBR 8800, NBR 6123, Catálogo Gerdau) y de
descomprimir el proyecto `calculadora_nbr` en tu carpeta de trabajo.

═══════════════════════════════════════════════════════════════════

Você é um engenheiro estrutural sênior e desenvolvedor Python experiente.

Tenho um projeto Streamlit parcialmente construído na pasta `calculadora_nbr`.
Os Módulos 1 (Combinação) e 2 (Tração) JÁ ESTÃO IMPLEMENTADOS e validados.
Os Módulos 3 (Compressão) e 4 (Vento) são placeholders que preciso completar.

Anexei a este projeto:
- NBR 8800:2024 (estruturas de aço)
- NBR 6123:2023 (vento)
- Catálogo Gerdau (perfis)

LEIA os documentos anexados e o arquivo `docs/CASOS_DE_PRUEBA.md` ANTES de
escrever código. Os valores esperados de validação estão lá.

## ESTRUTURA EXISTENTE (não quebrar)

```
calculadora_nbr/
├── app.py                  # navegação (pronto)
├── utils/
│   ├── constantes.py       # TODOS os coeficientes normativos (pronto)
│   └── calculos.py         # funções dos 4 módulos (PRONTAS, inclusive M3 e M4)
├── dados/perfis.py         # tabelas Gerdau (pronto)
├── modulos/
│   ├── combinacoes.py      # Módulo 1 (pronto, modelo a seguir)
│   ├── tracao.py           # Módulo 2 (pronto, modelo a seguir)
│   ├── compressao.py       # Módulo 3 (PLACEHOLDER - completar)
│   └── vento.py            # Módulo 4 (PLACEHOLDER - completar)
└── docs/                   # casos de prueba e referências
```

IMPORTANTE: as funções de cálculo dos Módulos 3 e 4 JÁ EXISTEM em
`utils/calculos.py`. Você só precisa construir a INTERFACE (render) seguindo
exatamente o mesmo padrão visual de `combinacoes.py` e `tracao.py`:
expander com fórmulas em LaTeX, st.info com caso de teste, inputs em colunas,
st.metric para resultados, st.success/st.error para verificação, expander
com desenvolvimento dos cálculos.

## TAREFA 1 — Completar Módulo 3 (compressao.py)

Use as funções já existentes: `bt_limite`, `forca_flambagem_euler`,
`esbeltez_reduzida_simplificada`, `fator_chi`, `resistencia_compressao`.

Interface:
- Selectbox de perfil CS (de dados/perfis.py PERFIS_CS)
- Selectbox de aço (de constantes.ACOS)
- Inputs: Lx e Ly (comprimentos destravados em cm), fator k
- Passo 1: flambagem local (mesa AL com coef 0,56; alma AA com coef 1,49).
  Mostrar se Aef = Ag.
- Passo 2: calcular λ₀ para eixo X e eixo Y separadamente
  (usar esbeltez_reduzida_simplificada com rx e ry).
- Passo 3: calcular χ de cada eixo, identificar o que GOVERNA (menor χ).
- Passo 4: Nc,Rd = χ·Ag·fy/γa1.
- Verificação de esbeltez λ ≤ 200.
- st.success/error comparando com um Nc,Sd que o usuário insere.

VALIDAÇÃO OBRIGATÓRIA (de docs/CASOS_DE_PRUEBA.md):
CS 300×109, A36 (fy=25), Ly=800 cm, k=1 →
λ₀=1,1516 · χ=0,574 · **Nc,Rd = 1.812 kN** (eixo Y governa).
Se Lx=1600 cm → Nc,Rd,x = 1.427 kN (eixo X governa).
Adicione st.info com esses valores esperados.

## TAREFA 2 — Completar Módulo 4 (vento.py)

Use as funções já existentes: `fator_S2`, `velocidade_caracteristica`,
`pressao_dinamica`, `forca_arrasto`. Parâmetros em constantes.VENTO_PARAMS,
constantes.S3_GRUPOS, constantes.V0_CIDADES.

Interface:
- Selectbox de cidade (V0_CIDADES) + opção manual
- Selectbox categoria (I-V) e classe (A/B/C) → pega b, Fr, p de VENTO_PARAMS
- Selectbox grupo S3 (S3_GRUPOS)
- Inputs: h (m), L1, L2 (m), número de pavimentos
- Radio: turbulência baixa (Ca=1,2) ou alta (Ca=0,95)
- Calcular tabela por faixa: para cada pavimento, z no topo, S2, Vk, q, Fa.
  Ae de cada faixa = L1 × (h/n_pavimentos).
- Mostrar tabela com pandas (st.dataframe).
- GRÁFICO PLOTLY: curva do vento. Eixo X = Fa (kN), eixo Y = altura z (m).
  Linha + marcadores. Título "Curva do Vento — Força de Arrasto por Altura".
- st.metric com Fa,total.
- Verificação de controle: Σ Ae deve ser igual a L1 × h. Mostrar com st.caption.

VALIDAÇÃO OBRIGATÓRIA (de docs/CASOS_DE_PRUEBA.md):
h=50m, planta 25×25m, Cat IV, Classe B, V0=50 m/s, 15 pavimentos,
S1=1, S3=1, Ca=1,2 → **Fa,total = 1.998 kN**.
Σ Ae = 1.250 m². Adicione st.info com esses valores.

## TAREFA 3 — Após completar

1. Rode `streamlit run app.py` e confirme que os 4 módulos funcionam.
2. Confirme que os 4 casos de teste batem com os valores esperados:
   - Módulo 1: Sd = 117,82 kN
   - Módulo 2: Nt,Rd = 429,0 kN
   - Módulo 3: Nc,Rd = 1.812 kN
   - Módulo 4: Fa,total = 1.998 kN
3. Substitua `[SEU NOME]` em app.py e README.md pelo meu nome.
4. Mostre um resumo do que foi feito.

## REGRAS

- NÃO invente valores. Use os documentos anexados e os arquivos existentes.
- NÃO quebre os Módulos 1 e 2 que já funcionam.
- Mantenha o padrão visual dos módulos existentes (LaTeX, métricas, cores).
- Todo trabalho interno em cm e kN.
- Cada função nova com docstring (o que faz, seção da norma, unidades).
- Se algum valor calculado não bater com o caso de teste, PARE e me avise
  antes de continuar — pode ser um dado de entrada a confirmar.

═══════════════════════════════════════════════════════════════════
