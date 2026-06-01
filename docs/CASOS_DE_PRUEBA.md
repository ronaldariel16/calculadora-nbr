# Casos de Prueba Verificados — Calculadora Estructural
## NBR 8800:2024 + NBR 6123:2023

> ⚠️ **IMPORTANTE:** Estos valores fueron recalculados con código Python y
> corrigen errores aritméticos de versiones anteriores del documento.
> Estos son los valores DEFINITIVOS contra los que validar el programa.

---

## Correcciones respecto a versiones anteriores

| Módulo | Valor anterior (erróneo) | Valor correcto |
|--------|--------------------------|----------------|
| 2 | Nt,Rd = 430,2 kN | **429,0 kN** (An 2-2 = 14,48 no 14,52) |
| 3 | Nc,Rd = 1.638,5 kN | **1.812 kN** (χ = 0,574 no 0,519) |
| 4 | Fa = 2.037 kN | **1.998 kN** (sin redondeo acumulado) |

El error del Módulo 3 era el más grave: χ = 0,658^1,325 = **0,574**, no 0,519.
Alguien calculó mal esa potencia y el error se arrastró.

---

## MÓDULO 1 — Combinação Última Normal

### Entrada
| Parámetro | Valor |
|---|---|
| F_permanente (esforço NA barra) | 24,3 kN |
| F_sobrecarga | 58,3 kN |
| F_vento | 0 kN |
| F_viga_rolamento | 0 kN |

### Cálculo (SC principal governa)
Sd = 1,25(24,3) + 1,5(58,3) + 1,4·0,6(0) + 1,5·0,8(0)
Sd = 30,375 + 87,45 = **117,82 kN**

### ✅ Resultado esperado: **Sd = 117,82 kN** ✓ (verificado por código)

---

## MÓDULO 2 — Tração (NBR 8800:2024 §5.2)

### Entrada
| Parámetro | Valor |
|---|---|
| Chapa | 240 × 8 mm = 24,0 × 0,8 cm |
| Aço | MR-250: fy = 25, fu = 40 kN/cm² |
| Parafuso | d = 19 mm, puncionado → folga +2,0 mm |
| df | 19 + 2,0 = 21,0 mm = 2,10 cm |
| s ; g | 32 mm ; 64 mm |
| Ct | 1,0 (chapa) |

### Áreas líquidas (df = 2,10 cm, t = 0,8 cm, s²/4g = 0,40 cm)
| Seção | Furos | Diagonais | An (cm²) |
|---|---|---|---|
| 1-1 | 2 | 0 | 19,2 − 2(1,68) = **15,84** |
| 2-2 | 3 | 1 | 19,2 − 3(1,68) + 0,32 = **14,48** ← governa |
| 3-3 | 3 | 2 | 19,2 − 5,04 + 0,64 = **14,80** |

### Resistências
- Escoamento: (19,2 × 25)/1,1 = **436,4 kN**
- Ruptura: (14,48 × 40)/1,35 = **429,0 kN** ← governa

### ✅ Resultado esperado: **Nt,Rd = 429,0 kN** ✓ (verificado por código)

---

## MÓDULO 3 — Compressão (NBR 8800:2024 §5.3)

### Entrada
| Parámetro | Valor |
|---|---|
| Perfil | CS 300×109 |
| Ag | 138,9 cm² |
| rx ; ry | 13,13 ; 7,85 cm |
| bf ; tf | 300 ; 19 mm |
| h ; tw | 262 ; 9,5 mm |
| Aço | A36: fy = 25, E = 20.000 kN/cm² |
| Ly | 800 cm ; k = 1 |

### Flambagem local (Aef = Ag, seção não esbelta)
- Mesa: bf/2tf = 7,89 ≤ 0,56√(E/fy) = 15,84 ✓
- Alma: h/tw = 27,6 ≤ 1,49√(E/fy) = 42,13 ✓

### Esbeltez e χ (método de clase, factor 0,0113)
- λ₀ = 0,0113·(800/7,85) = **1,1516**
- χ = 0,658^(1,1516²) = 0,658^1,326 = **0,574**
- Nc,Rd = (0,574 × 138,9 × 25)/1,1 = **1.812 kN**

### Verificação eixo X (se Lx = 1600 cm)
- λ₀x = 0,0113·(1600/13,13) = 1,377
- χx = 0,658^(1,377²) = **0,452**
- Nc,Rd,x = (0,452 × 138,9 × 25)/1,1 = **1.427 kN**

**Si Lx = 16 m destravado → eixo X governa (1.427 < 1.812).**

### ✅ Resultado esperado: **Nc,Rd = 1.812 kN** (eixo Y) ✓ (verificado por código)

> ⚠️ Nota sobre métodos: el método de clase usa el factor empírico 0,0113.
> La fórmula general de la norma (λ₀ = √(Ag·fy/Ne) con Ne = π²EI/L²) da
> χ = 0,577 y Nc,Rd = 1.820 kN. Diferencia mínima. Usa el método que
> enseñó tu profesor (clase = 0,0113).

---

## MÓDULO 4 — Força de Arrasto (NBR 6123:2023)

### Entrada
| Parámetro | Valor |
|---|---|
| h | 50 m ; planta 25 × 25 m |
| Pavimentos | 15 (pé-direito 3,333 m) |
| Categoria/Classe | IV / B |
| V₀ | 50 m/s |
| S₁ ; S₃ | 1,0 ; 1,00 |
| Ca | 1,2 (baixa turbulência) |
| b ; Fr ; p | 0,85 ; 0,98 ; 0,125 |

### Tabla por faixa (calculada por código)
| Faixa | z (m) | S₂ | Vk (m/s) | q (kN/m²) | Fa (kN) |
|---|---|---|---|---|---|
| 1 | 3,33 | 0,8330 | 41,65 | 1,063 | 106,3 |
| 2 | 6,67 | 0,8330 | 41,65 | 1,063 | 106,3 |
| 3 | 10,00 | 0,8330 | 41,65 | 1,063 | 106,3 |
| 4 | 13,33 | 0,8635 | 43,18 | 1,143 | 114,3 |
| 5 | 16,67 | 0,8879 | 44,40 | 1,208 | 120,8 |
| 6 | 20,00 | 0,9084 | 45,42 | 1,265 | 126,5 |
| 7 | 23,33 | 0,9261 | 46,30 | 1,314 | 131,4 |
| 8 | 26,67 | 0,9417 | 47,08 | 1,359 | 135,9 |
| 9 | 30,00 | 0,9556 | 47,78 | 1,400 | 139,9 |
| 10 | 33,33 | 0,9683 | 48,41 | 1,437 | 143,7 |
| 11 | 36,67 | 0,9799 | 48,99 | 1,472 | 147,1 |
| 12 | 40,00 | 0,9906 | 49,53 | 1,504 | 150,4 |
| 13 | 43,33 | 1,0006 | 50,03 | 1,534 | 153,4 |
| 14 | 46,67 | 1,0099 | 50,49 | 1,563 | 156,3 |
| 15 | 50,00 | 1,0186 | 50,93 | 1,590 | 159,0 |

### Verificaciones de control
- Σ Ae = 15 × 83,33 = 1.250 m² = 25 × 50 m ✓
- Faixas 1-3: S₂ = 0,833 constante (norma mantém até z=10m) ✓
- Edifício quadrado → 0° = 90° ✓

### ✅ Resultado esperado: **Fa,total = 1.998 kN** ✓ (verificado por código)

> Nota: el valor anterior de 2.037 kN venía de redondear S₂ a 3 decimales
> en cada faixa. El código no redondea intermedios, por eso da 1.998 kN
> (más preciso). Alta turbulência (Ca=0,95): Fa ≈ 1.581 kN.

---

## Tabla resumen de validación (valores definitivos)

| Módulo | Resultado esperado | Status |
|--------|--------------------|--------|
| 1 | Sd = **117,82 kN** | ✓ código |
| 2 | Nt,Rd = **429,0 kN** | ✓ código |
| 3 | Nc,Rd = **1.812 kN** (eixo Y) | ✓ código |
| 4 | Fa,total = **1.998 kN** | ✓ código |

---

## Pendientes que dependen del profesor (NO del código)

- Espaçamentos s, g reales de la figura del examen (Módulo 2)
- Cuál eje governa según longitudes destravadas reales (Módulo 3)
- V₀ de Foz do Iguaçu: 45 o 50 m/s (Módulo 4)

---

*Verificado con código Python contra NBR 8800:2024 y NBR 6123:2023.*
*Ferramenta educacional. Resultados devem ser verificados por engenheiro responsável.*
