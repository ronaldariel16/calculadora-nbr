# Referencias normativas usadas

Trechos exactos de las normas que sustentan cada cálculo del programa.
Verificados contra los documentos del proyecto (NBR 8800:2024 y NBR 6123:2023).

---

## NBR 8800:2024

### Combinação última normal (4.8.7.2.1)
> "Em cada combinação, devem estar incluídas as ações permanentes e a ação
> variável principal, com seus valores característicos, e as demais ações
> variáveis, consideradas secundárias, com seus valores reduzidos de combinação."

$$F_d = \sum_i (\gamma_{gi} F_{Gi,k}) + \gamma_{q1} F_{Q1,k} + \sum_j (\gamma_{qj}\,\psi_{0j}\,F_{Qj,k})$$

### Coeficientes γg e γq (Tabela 1, combinações normais)
| Ação | γ |
|------|---|
| Peso próprio estruturas de aço | 1,25 |
| Peso próprio pré-moldadas/madeira | 1,30 |
| Peso próprio in loco | 1,35 |
| Elementos construtivos em geral | 1,50 |
| Sobrecarga (demais ações variáveis) | 1,50 |
| Vento | 1,40 |
| Temperatura | 1,20 |

Valor favorável à segurança (entre parênteses na norma): 1,00.

### Fatores ψ₀ (Tabela 2)
| Ação | ψ₀ |
|------|-----|
| Sobrecarga residencial (acesso restrito) | 0,5 |
| Sobrecarga locais com público | 0,7 |
| Bibliotecas, depósitos, garagens, coberturas | 0,8 |
| Vento | 0,6 |
| Temperatura | 0,6 |
| Vigas de rolamento de pontes rolantes | 1,0 |
| Pilares que suportam vigas de rolamento | 0,7 |

### Coeficientes de resistência (Tabela 3, combinações normais)
| Coeficiente | Valor | Aplicação |
|-------------|-------|-----------|
| γa1 | 1,10 | Escoamento e instabilidade |
| γa2 | 1,35 | Ruptura |

### Tração — estados-limite (5.2.2)
$$\text{Escoamento: } N_{t,Rd} = \frac{A_g f_y}{\gamma_{a1}}$$
$$\text{Ruptura: } N_{t,Rd} = \frac{A_e f_u}{\gamma_{a2}}, \quad A_e = C_t A_n$$

### Área líquida com zigue-zague (5.2.4.1-b)
$$A_n = A_g - \sum(d_f \cdot t) + \sum\frac{s^2}{4g}\cdot t$$

### Dimensão do furo (5.2.4.1-a) ⚠️ MUDANÇA vs 2008
> "a largura dos furos deve ser considerada 2,0 mm maior que a dimensão
> máxima desses furos, perpendicular à direção da força aplicada. Se o furo
> for feito com broca, a largura pode ser considerada igual à dimensão."

- Furo padrão (puncionado): **df = d + 2,0 mm**
- Furo com broca: **df = d**
- (A NBR 8800:2008 usava +3,5 mm para puncionado — NÃO usar na 2024.)

### Compressão — resistência (5.3.2)
$$N_{c,Rd} = \frac{\chi\,A_{ef}\,f_y}{\gamma_{a1}}$$

### Fator χ (5.3.3.1)
$$\chi = 0{,}658^{\lambda_0^2} \text{ se } \lambda_0 \le 1{,}5$$
$$\chi = \frac{0{,}877}{\lambda_0^2} \text{ se } \lambda_0 > 1{,}5$$

### Esbeltez reduzida (5.3.3.2)
$$\lambda_0 = \sqrt{\frac{A_g f_y}{N_e}}, \quad N_e = \frac{\pi^2 E I}{L^2}$$

### Flambagem local — (b/t)lim (Tabela 4)
| Elemento | Grupo | (b/t)lim |
|----------|-------|----------|
| Abas de cantoneiras | 3 | 0,45·√(E/fy) |
| Mesas I/H/T/U laminadas | 4 | 0,56·√(E/fy) |
| Mesas I/H/T/U soldadas | 5 | 0,64·√(E/fy)·(usar kc) |
| Almas de I/H/U | 2 | 1,49·√(E/fy) |
| Almas de T | 6 | 0,75·√(E/fy) |

### Limite de esbeltez
- Compressão (5.3.7.1): λ ≤ 200 (recomendado)
- Tração (5.2.8.1): λ ≤ 300 (recomendado)

---

## NBR 6123:2023

### Velocidade característica (5.1)
$$V_k = V_0 \cdot S_1 \cdot S_2 \cdot S_3$$

### Pressão dinâmica (4.2-c)
$$q = 0{,}613 \cdot V_k^2 \quad (V_k \text{ em m/s}, q \text{ em N/m}^2)$$

### Fator S₂ (5.3.3)
$$S_2 = b \cdot F_r \cdot (z/10)^p$$
> Fr é sempre o correspondente à Categoria II. S₂ é constante até z = 10 m
> em Categoria V (e na prática para categorias altas).

### Parâmetros b, Fr, p (Tabela 1)
Categoria IV, Classe B: **b = 0,85 · Fr = 0,98 · p = 0,125** → b·Fr = 0,833

### Fator estatístico S₃ (Tabela 3)
| Grupo | S₃ |
|-------|-----|
| 1 — hospitais, bombeiros | 1,10 |
| 2 — hotéis, residências, comércio | 1,00 |
| 3 — depósitos, silos | 0,95 |
| 4 — vedações | 0,88 |
| 5 — temporárias | 0,83 |

### Força de arrasto (6.1)
$$F_a = C_a \cdot q \cdot A_e$$
> Ca obtido da Figura 4 (baixa turbulência) ou Figura 5 (alta turbulência),
> em função de L₁/L₂ e h/L₁.

---

*Todas las referencias verificadas contra los archivos del proyecto.*
