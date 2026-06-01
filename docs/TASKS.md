# TASKS — Plan de desarrollo

Lista de tareas para construir y validar la calculadora. Marca cada caja
a medida que avances. El orden está pensado para ir de lo más fácil de
demostrar a lo más complejo.

---

## Fase 0 — Setup (1 hora)

- [ ] Crear repositorio en GitHub (`calculadora-nbr`)
- [ ] Clonar y abrir en VS Code
- [ ] Crear ambiente virtual: `python -m venv .venv`
- [ ] Activar e instalar: `pip install -r requirements.txt`
- [ ] Verificar que la estructura de carpetas está completa
- [ ] Adjuntar los 3 PDFs (NBR 8800, NBR 6123, Gerdau) en Claude Code

---

## Fase 1 — Módulos 1 y 2 (ya implementados, solo validar)

- [ ] Ejecutar `streamlit run app.py` sin errores
- [ ] **Módulo 1:** confirmar que el caso de prueba da **Sd = 117,82 kN**
- [ ] **Módulo 1:** probar el botón "Usar este Sd no Módulo 2"
- [ ] **Módulo 2:** confirmar que el caso de prueba da **Nt,Rd = 429,0 kN**
- [ ] **Módulo 2:** verificar que la seção 2-2 aparece destacada como crítica
- [ ] **Módulo 2:** probar el sanity check (poner espesura en mm para forzar error)
- [ ] Revisar que las fórmulas LaTeX renderizan bien

---

## Fase 2 — Módulo 3: Compressão (~1 tarde)

Las funciones ya existen en `utils/calculos.py`. Falta la interfaz en
`modulos/compressao.py`.

- [ ] Selector de perfil CS desde el catálogo (`dados/perfis.py`)
- [ ] Inputs: Lx, Ly (comprimentos destravados), k, aço
- [ ] Calcular flambagem local (mesa AL y alma AA) → mostrar si Aef = Ag
- [ ] Calcular Ne para eje X y eje Y por separado
- [ ] Calcular λ₀ y χ para ambos ejes
- [ ] Identificar qué eje governa (menor χ)
- [ ] Mostrar Nc,Rd final con verificación VERIFICA/NÃO VERIFICA
- [ ] **Validar contra el caso:** CS 300×109, Ly=800 → **Nc,Rd = 1.812 kN**
- [ ] **Validar eje X:** si Lx=1600 → Nc,Rd,x = 1.427 kN (X governa)
- [ ] Verificar limite de esbeltez λ ≤ 200

---

## Fase 3 — Módulo 4: Vento (~1 tarde)

Las funciones y parámetros ya existen. Falta interfaz + gráfico en
`modulos/vento.py`.

- [ ] Dropdown de ciudad (V₀ desde `V0_CIDADES`)
- [ ] Selectores: categoria (I-V), classe (A/B/C), grupo S₃
- [ ] Inputs: h, L₁, L₂, número de pavimentos
- [ ] Selector de turbulência (Ca baixa=1,2 o alta=0,95)
- [ ] Calcular tabla por faixa (z, S₂, Vk, q, Ae, Fa)
- [ ] Mostrar tabla con pandas
- [ ] **Gráfico plotly:** curva del vento (Fa eje X, z eje Y)
- [ ] Mostrar Fa,total con st.metric
- [ ] Verificación de control: Σ Ae = área frontal
- [ ] **Validar contra el caso:** edif. 50 m, Cat IV/B, 15 pav → **Fa ≈ 1.998 kN**

---

## Fase 4 — Pulido y deploy (~2 horas)

- [ ] Reemplazar `[SEU NOME]` en `app.py` y `README.md`
- [ ] Tomar screenshot del app funcionando → agregar al README
- [ ] Revisar todos los docstrings
- [ ] Commit y push a GitHub
- [ ] Deploy en Streamlit Cloud (share.streamlit.io)
- [ ] Probar la URL pública
- [ ] Agregar el link del deploy al README

---

## Fase 5 — Extras (opcional, suma puntos al portafolio)

- [ ] Exportar relatório en PDF (con reportlab o weasyprint)
- [ ] Agregar más perfis al catálogo (W, HP)
- [ ] Módulo de flexão (NBR 8800 seção 5.4)
- [ ] Tests automatizados con pytest (validar los 4 casos de prueba)
- [ ] Modo claro/escuro

---

## Validación final (antes de publicar)

Los 4 números que DEBEN salir exactos:

| Módulo | Resultado esperado |
|--------|--------------------|
| 1 | Sd = 117,82 kN |
| 2 | Nt,Rd = 429,0 kN |
| 3 | Nc,Rd = 1.812 kN |
| 4 | Fa,total ≈ 2.037 kN |

Si alguno no coincide, revisar `docs/CASOS_DE_PRUEBA.md` para el cálculo
paso a paso y encontrar dónde está la diferencia.

---

## Pendientes que dependen de tu profesor (NO del código)

- [ ] Confirmar espaçamentos s y g de la figura del examen (Módulo 2)
- [ ] Confirmar qué eje governa según el pórtico real (Módulo 3)
- [ ] Confirmar V₀ de Foz do Iguaçu (45 o 50 m/s) (Módulo 4)
