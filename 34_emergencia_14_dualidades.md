# Doc 34: Emergencia — 14 Dualidades

**Script:** `scripts/emergence_analysis_14.py`
**Alcance:** 14 dualidades × 65 primitivos × 133 aristas × 9 dominios
**Prerequisito:** Docs 31, 33 (integración post-33: 0 huérfanos)

---

## 1. Matriz de dependencia 14×14

La matriz se imprime en 4 bloques. Valor = fracción de anclas de Dj que tienen al menos un ancla de Di como ancestro transitivo.

### Bloque 1: Círculo × Círculo (D1-D7)

| | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
|---|---|---|---|---|---|---|---|
| **D1** | — | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| **D2** | 0 | — | 1.00 | 1.00 | 0.25 | 1.00 | 1.00 |
| **D3** | 0 | 0 | — | 0 | 0.25 | 0 | 1.00 |
| **D4** | 0 | 0 | 0 | — | 0 | 0 | 0 |
| **D5** | 0 | 0 | 0 | 0 | — | 0 | 0 |
| **D6** | 0 | 0 | 1.00 | 1.00 | 0.25 | — | 1.00 |
| **D7** | 0 | 0 | 0 | 0 | 0.25 | 0 | — |

**Triangularidad:** 0.833 (above=12.50, below=2.50)

### Bloque 4: Espiral × Espiral (D8-D14)

| | D8 | D9 | D10 | D11 | D12 | D13 | D14 |
|---|---|---|---|---|---|---|---|
| **D8** | — | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| **D9** | 0 | — | 1.00 | 1.00 | 0 | 0 | 1.00 |
| **D10** | 0 | 0 | — | 1.00 | 0 | 0 | 1.00 |
| **D11** | 0 | 0 | 0 | — | 0 | 0 | 1.00 |
| **D12** | 0 | 0 | 0 | 0 | — | 0 | 0 |
| **D13** | 0 | 0 | 0 | 0 | 0 | — | 0 |
| **D14** | 0 | 0 | 0 | 0 | 0 | 0 | — |

**Triangularidad:** 1.000 — perfectamente triangular.

### Métricas globales

| Métrica | Valor |
|---------|-------|
| Triangularidad general 14×14 | 0.829 |
| Acople círculo→espiral | 22.00 (peso total) |
| Acople espiral→círculo | 7.08 (peso total) |

La espiral depende fuertemente del círculo (22.00 vs 7.08). El acoplamiento inverso se explica por **D8 (uno/muchos)**, cuyo ancla `uno` es también ancla de D1.

---

## 2. Rango DAG (profundidad)

| Grupo | ρ Spearman | p |
|-------|------------|---|
| Círculo D1-D7 | +0.321 | 0.482 |
| Espiral D8-D14 | +0.643 | 0.119 |
| Combinado D1-D14 | −0.130 | 0.659 |

La espiral muestra mejor correlación profundidad↔posición que el círculo. La correlación combinada cae porque las escalas de profundidad no son conmensurables: D8-D14 tienen anclas en capas bajas (D8 usa `uno`, capa 1) mientras D3-D4 usan anclas en capas 3-4.

---

## 3. Universalidad empírica (D-rate)

| Grupo | ρ Spearman | p |
|-------|------------|---|
| Círculo D1-D7 | +0.107 | 0.819 |
| Espiral D8-D14 | +0.214 | 0.645 |
| Combinado D1-D14 | +0.336 | 0.240 |

Correlaciones bajas en ambos subconjuntos. Las anclas de D2 (ejes espaciales) tienen D-rate bajo (0.259) pese a ser posición 2 del círculo, arrastrando la correlación.

---

## 4. Mapeo de ejes

**13/13 ejes asignados a dualidades:**

| Dualidad | # Ejes | Ejes |
|----------|--------|------|
| D4_posibilidad | 1 | libertad/control |
| D5_identidad | 1 | individual/colectivo |
| D6_movimiento | 2 | creación/destrucción, mover/quietud |
| D7_orden | 3 | bien/mal, orden/caos, verdad/mentira |
| D9_dentro_fuera | 1 | unión/separación |
| D11_vida_muerte | 2 | vida/muerte, placer/dolor |
| D14_sujeto_objeto | 3 | consciente/ausente, temporal/eterno, receptivo/creador |

D7 y D14 concentran 3 ejes cada una, coherente con su rol como dualidades de "alto nivel".

---

## 5. Test contrafactual

De C(14,2) = 91 pares:
- **NECESSARY:** 12 (todos involucran D1_existir)
- **WEAK:** 1 (D1→D8)
- **UNCERTAIN:** 78

D1 es la única dualidad cuya eliminación rompe la monotonicidad por debajo de 0.80, confirmando su rol como raíz ontológica absoluta.

---

## 6. Verificación del árbol D8-D14

| Arista esperada | dep_matrix | Status |
|-----------------|-----------|--------|
| D8 → D9 | 1.00 | OK |
| D9 → D10 | 1.00 | OK |
| D10 → D11 | 1.00 | OK |
| D8 → D12 | 1.00 | OK |
| D8 → D13 | 1.00 | OK |
| D11 → D14 | 1.00 | OK |

**Tree fidelity: 6/6 = 1.000** (≥ 0.80 → PASS)

Todas las aristas esperadas del árbol D8-D14 están confirmadas. La arista D10→D11, que faltaba antes de doc 37, fue restaurada al agregar `parte_de` a las dependencias de `vida` (ver doc 37, W2). Las 6 aristas no-esperadas con dep > 0 se explican por transitividad a través de D8.

---

## 7. Análisis cross-espiral

**10 primitivos puente** conectan ambas espirales:

| Primitivo | Círculo | Espiral | Rol |
|-----------|---------|---------|-----|
| uno | D1 (A) | D8 (A) | Raíz ontológica compartida |
| muchos | D5 (A) | D8 (A) | Pluralidad |
| contención | D2 (S) | D9 (A) | Límites |
| porque | D3 (S) | D12 (A) | Causalidad |
| si_entonces | D3 (S) | D12 (A) | Condicionalidad |
| tipo_de | D5 (A) | D13 (A) | Clasificación |
| todo | D5 (A) | D10 (A) | Totalidad |
| algunos | D5 (A) | D10 (S) | Parcialidad |
| individual | D5 (S) | D14 (S) | Singularidad |
| colectivo | D5 (S) | D14 (S) | Comunidad |

D5 (identidad) aporta 6 de los 10 puentes, confirmando su rol de bisagra entre abstracción y concreción.

---

## 8. Before/After: 7×7 vs 14×14

| Métrica | 7×7 (círculo) | 14×14 (todo) |
|---------|---------------|--------------|
| Triangularidad | 0.833 | 0.829 |
| ρ depth | +0.321 | −0.130 |
| ρ D-rate | +0.107 | +0.336 |
| Pares necesarios | 6/21 | 12/91 |
| Pares bidireccionales | 0 | 1 |
| Ejes asignados | 7 | 13 |

La triangularidad se mantiene estable (−0.010). La ρ depth cae al combinar porque las dos espirales operan en escalas de profundidad distintas. La ρ D-rate mejora ligeramente al incluir las 14 dualidades.

---

## 9. Tabla consolidada

| Dualidad | Pos | Depth | D-rate | DepScore | Ejes | Espiral |
|----------|-----|-------|--------|----------|------|---------|
| D1_existir | 1 | 0.00 | 0.889 | — | 0 | C |
| D2_espacio | 2 | 1.67 | 0.259 | 1.00 | 0 | C |
| D3_tiempo | 3 | 3.00 | 0.889 | 1.00 | 0 | C |
| D4_posibilidad | 4 | 2.33 | 0.407 | 0.67 | 1 | C |
| D5_identidad | 5 | 1.50 | 0.417 | 0.38 | 1 | C |
| D6_movimiento | 6 | 2.00 | 0.815 | 0.40 | 2 | C |
| D7_orden | 7 | 2.00 | 0.833 | 0.67 | 3 | C |
| D8_uno_muchos | 8 | 0.50 | 0.500 | 0.07 | 0 | S |
| D9_dentro_fuera | 9 | 1.00 | 0.889 | 0.25 | 1 | S |
| D10_parte_todo | 10 | 1.50 | 0.333 | 0.39 | 0 | S |
| D11_vida_muerte | 11 | 2.00 | 0.667 | 0.80 | 2 | S |
| D12_causa_efecto | 12 | 1.50 | 0.222 | 0.45 | 0 | S |
| D13_semejante_diferente | 13 | 1.00 | 0.778 | 0.50 | 0 | S |
| D14_sujeto_objeto | 14 | 1.50 | 0.389 | 0.69 | 3 | S |

---

## 10. Veredictos

| Grupo | Triangularidad | ρ depth | ρ D-rate | Veredicto |
|-------|----------------|---------|----------|-----------|
| Círculo (D1-D7) | 0.833 | +0.321 | +0.107 | PARTIALLY SUPPORTED |
| Espiral (D8-D14) | 1.000 | +0.643 | +0.214 | PARTIALLY SUPPORTED |
| Combinado (D1-D14) | 0.829 | −0.130 | +0.336 | PARTIALLY SUPPORTED |

- **Tree fidelity:** 1.000 → PASS
- **D1 row check:** PASS (todo depende de Existir)
- **13/13 ejes asignados**
- **Estructura:** PARTIAL LATTICE (1 par bidireccional: D5↔D10)
- **Acoplamiento cross-espiral:** círculo→espiral = 0.449, espiral→círculo = 0.145

### Interpretación

Las 14 dualidades son **parcialmente soportadas** por la estructura del DAG. La espiral (D8-D14) muestra triangularidad perfecta y mejor correlación depth↔posición que el círculo. La correlación combinada cae porque las dos espirales operan en escalas de profundidad distintas — no es un defecto sino un reflejo de que el círculo y la espiral son dos vistas complementarias sobre el mismo DAG.

La arista D10→D11, anteriormente faltante, fue restaurada al agregar `parte_de` como dependencia de `vida` (doc 37, W2). Esto eleva la tree fidelity a 1.000 y la triangularidad global a 0.829. Los p-values fueron recalculados con la función beta regularizada (doc 37, W6), reemplazando la lookup table original.
