# Documento 31: Formalizacion Computable de la Secuencia de Emergencia

| Metrica | Resultado |
|---------|-----------|
| Herramienta | `scripts/emergence_analysis.py` |
| Dualidades analizadas | 7 (Existir, Espacio, Tiempo, Posibilidad, Identidad, Movimiento, Orden) |
| Primitivos ancla | 35 (7 dualidades x ~5 anclas) |
| Analisis ejecutados | 5 (dependency matrix, DAG rank, D-rate, ejes, counterfactual) |
| Triangularidad de la matriz | 0.833 |
| Spearman depth vs circulo | +0.321 (p ~ 0.50) |
| Spearman D-rate vs circulo | +0.107 (p ~ 0.50) |
| Pares con dependencia confirmada | 14/21 (67%) |
| Tensiones detectadas | 4 pares |
| Veredicto | PARCIALMENTE SOPORTADA |
| Dependencias | Solo stdlib Python (json, math, sys, os, collections) |

**Script:** `scripts/emergence_analysis.py`
**Datos:** `data/primitivos.json`, `data/reference_domains.json`, `data/dualidad_primitivo_map.json`

---

## I. La pregunta

El documento del 20 de marzo propone que las 7 dualidades del circulo siguen una secuencia de emergencia logica:

**Existir -> Espacio -> Tiempo -> Posibilidad -> Identidad -> Movimiento -> Orden**

Pero esta secuencia fue postulada narrativamente. La pregunta central es: se puede verificar computacionalmente si esta secuencia emerge de la estructura del DAG de 63 primitivos y de los datos empiricos de 9 dominios?

La hipotesis nula es que el orden del circulo es arbitrario: cualquier permutacion de las 7 dualidades seria igualmente compatible con los datos.

---

## II. Metodo

### Mapeo dualidad-primitivo

Cada dualidad se asocia a 2-4 primitivos "ancla" (los que encarnan directamente el concepto) y 0-3 secundarios. El mapeo completo esta en `data/dualidad_primitivo_map.json`.

| Dualidad | Anclas | Secundarios |
|----------|--------|-------------|
| D1 Existir | vacio, informacion, uno | — |
| D2 Espacio | eje_profundidad, eje_vertical, eje_lateral | contencion, equilibrio |
| D3 Tiempo | posicion_temporal, flujo_temporal | porque, si_entonces |
| D4 Posibilidad | puede, debe, tal_vez | libertad, control |
| D5 Identidad | tipo_de, algunos, muchos, todo | individual, colectivo |
| D6 Movimiento | mover, hacer | fuerza, creacion, destruccion |
| D7 Orden | orden, caos | bien, mal, verdad, mentira |

Los 28 primitivos restantes son "emergentes compuestos" que dependen de multiples dualidades sin encarnar ninguna en particular.

### Cinco analisis computacionales

1. **Dependency matrix 7x7:** Para cada par (Di, Dj), que fraccion de anclas de Dj dependen transitivamente de anclas de Di.
2. **DAG emergence rank:** Profundidad promedio de anclas por dualidad, comparada con la posicion en el circulo via correlacion de Spearman.
3. **D-rate empirico:** Universalidad de cada dualidad medida como fraccion de dominios donde sus anclas son "D" (directas).
4. **Ejes duales:** Asignacion de los 12 ejes_duales a dualidades.
5. **Counterfactual necessity:** Si invertimos la relacion Di->Dj (anclas de Dj=D, anclas de Di=N), colapsa la monotonicity?

---

## III. Resultados

### Dependency matrix

```
              D1_exis  D2_espa  D3_tiem  D4_posi  D5_iden  D6_movi  D7_orde
D1_exis            —     1.00     1.00     1.00     1.00     1.00     1.00
D2_espa         0.00        —     1.00     1.00     0.25     1.00     1.00
D3_tiem         0.00     0.00        —     0.00     0.25     0.00     1.00
D4_posi         0.00     0.00     0.00        —     0.00     0.00     0.00
D5_iden         0.00     0.00     0.00     0.00        —     0.00     0.00
D6_movi         0.00     0.00     1.00     1.00     0.25        —     1.00
D7_orde         0.00     0.00     0.00     0.00     0.25     0.00        —
```

La fila D1 es toda 1.00 — todo depende de Existir. Esto confirma D1 como raiz absoluta.

La fila D6 (Movimiento) muestra dependencias fuertes hacia D3, D4 y D7. Esto es la tension central: el circulo coloca D6 en posicion 6, pero el DAG muestra que Tiempo, Posibilidad y Orden dependen transitivamente de mover/hacer.

**Triangularidad:** 0.833 (peso arriba-diagonal: 12.50, peso abajo-diagonal: 2.50). La matriz es predominantemente triangular pero no perfecta.

### DAG emergence rank

| Dualidad | Avg.Depth | Rank | Circulo | Delta |
|----------|-----------|------|---------|-------|
| D1 Existir | 0.00 | 1 | 1 | 0 |
| D2 Espacio | 1.67 | 3 | 2 | +1 |
| D3 Tiempo | 3.00 | 7 | 3 | +4 |
| D4 Posibilidad | 2.33 | 6 | 4 | +2 |
| D5 Identidad | 1.50 | 2 | 5 | -3 |
| D6 Movimiento | 2.00 | 4 | 6 | -2 |
| D7 Orden | 2.00 | 5 | 7 | -2 |

**Spearman rho = +0.321** (p ~ 0.50). Correlacion debil, no significativa. El orden del DAG por profundidad no reproduce bien el circulo.

Notar: D3 (Tiempo) tiene la mayor profundidad promedio (3.0) porque posicion_temporal y flujo_temporal estan en capa 3 y dependen de mover. D5 (Identidad) tiene profundidad baja (1.5) porque tipo_de, algunos y muchos estan en capa 4 pero con pocos niveles de dependencia.

### D-rate empirico

| Dualidad | Avg.D-rate | Rank | Circulo | Delta |
|----------|-----------|------|---------|-------|
| D1 Existir | 0.889 | 1 | 1 | 0 |
| D2 Espacio | 0.259 | 7 | 2 | +5 |
| D3 Tiempo | 0.889 | 2 | 3 | -1 |
| D4 Posibilidad | 0.407 | 6 | 4 | +2 |
| D5 Identidad | 0.417 | 5 | 5 | 0 |
| D6 Movimiento | 0.778 | 4 | 6 | -2 |
| D7 Orden | 0.833 | 3 | 7 | -4 |

**Spearman rho = +0.107** (p ~ 0.50). Correlacion practicamente nula. La universalidad empirica no sigue el orden del circulo.

Observacion notable: D2 (Espacio) tiene el D-rate mas bajo (0.259) porque sus anclas (eje_profundidad, eje_vertical, eje_lateral) son frecuentemente "A" (analogicas) en dominios abstractos como Matematicas o Filosofia. D7 (Orden) tiene D-rate alto (0.833) porque orden y caos son directos en casi todos los dominios.

### Ejes duales

| Dualidad | Ejes asignados |
|----------|---------------|
| D1 Existir | 0 |
| D2 Espacio | 0 |
| D3 Tiempo | 0 |
| D4 Posibilidad | 1 (libertad/control) |
| D5 Identidad | 1 (individual/colectivo) |
| D6 Movimiento | 1 (creacion/destruccion) |
| D7 Orden | 3 (bien/mal, orden/caos, verdad/mentira) |

6 ejes no asignados (union/separacion, vida/muerte, placer/dolor, consciente/ausente, temporal_obs/eterno_obs, receptivo/creador_obs). Estos pertenecen a primitivos de capas 5-6 que son "emergentes compuestos".

D7 concentra 3/6 ejes asignados, reforzando su rol como dualidad integradora.

### Counterfactual necessity

| Tipo | Conteo |
|------|--------|
| NECESSARY (mono < 0.80) | 6/21 (todos involucran D1) |
| UNCERTAIN (mono se mantiene alta) | 15/21 |

Solo los pares D1->Dx son estructuralmente necesarios. Esto tiene sentido: D1 contiene las 3 raices del DAG (vacio, informacion, uno). Invertir la relacion con cualquier otro nodo colapsa la monotonicity porque viola la direccion fundamental del grafo.

Los demas pares mantienen monotonicity alta bajo inversion, sugiriendo que la dependencia entre D2-D7 es mas debil de lo esperado al nivel de anclas.

---

## IV. Tensiones descubiertas

### Tension principal: D6 (Movimiento) vs D3, D4, D5

El circulo coloca Movimiento en posicion 6 (penultima). Pero el DAG muestra que:

- **D3 Tiempo depende de D6:** posicion_temporal depende de mover (depth 2). flujo_temporal depende de mover y posicion_temporal (depth 3). Es decir: sin movimiento, no hay tiempo.
- **D4 Posibilidad depende de D6:** puede depende de hacer+libertad. debe depende de hacer+control. tal_vez depende de puede. La modalidad requiere accion.
- **D5 Identidad (parcial):** tipo_de depende transitivamente de mover via orden.

Esto genera 3 de las 4 tensiones detectadas. En el circulo, Movimiento es "tardio" (pos 6), pero en el DAG, Movimiento es "temprano" — sus anclas (mover capa 3, hacer capa 3) alimentan a Tiempo, Posibilidad y Orden.

### Tension secundaria: D7 -> D5

tipo_de depende transitivamente de orden, creando una dependencia D7->D5 que invierte el circulo.

### Interpretacion

Estas tensiones no son necesariamente contradicciones. Revelan una distincion entre dos niveles:

1. **Nivel DAG (mecanico):** mover es un primitivo de capa 3 que alimenta muchas dependencias. Es operacionalmente temprano.
2. **Nivel conceptual (circulo):** "Movimiento como dualidad" (movimiento/quietud como categoria ontologica) requiere que ya existan Espacio, Tiempo, Posibilidad e Identidad como marcos de referencia.

La tension es real: el primitivo mover es anterior al primitivo posicion_temporal en el DAG, pero la dualidad Movimiento es posterior a la dualidad Tiempo en el circulo. Esto sugiere que el circulo opera en un nivel de abstraccion diferente al DAG de dependencias.

---

## V. Interpretacion: cadena o lattice?

### No es una cadena estricta

Una cadena estricta implicaria que cada dualidad depende unicamente de las anteriores. Los datos muestran:

- 14/21 pares confirmados en la direccion esperada (67%)
- 4/21 pares con dependencia inversa
- 3/21 pares independientes (D3-D4, D4-D5, D4-D7)
- 0 pares bidireccionales

### No es un lattice completo

No hay pares bidireccionales (donde Di depende de Dj Y Dj depende de Di simultaneamente). El grafo inter-dualidades es un DAG, no un lattice.

### Es un orden parcial con ramas

La estructura real es:

```
D1 (Existir)
├── D2 (Espacio)
│   ├── D6 (Movimiento)
│   │   ├── D3 (Tiempo)
│   │   │   └── D7 (Orden)
│   │   └── D4 (Posibilidad)
│   └── D5 (Identidad) ← parcialmente independiente
```

El circulo aplana esta estructura arborescente en una secuencia lineal. La linealizacion D1-D2-D3-D4-D5-D6-D7 no es la unica compatible con el DAG. Una linealizacion mas fiel al DAG seria: D1-D2-D6-D3-D5-D4-D7 o D1-D2-D5-D6-D3-D4-D7.

---

## VI. Que significa para el framework

### Lo que se confirma

1. **D1 es raiz absoluta.** Toda dualidad depende transitivamente de Existir. Esto es irrefutable.
2. **D2 es segunda.** Espacio depende solo de D1 y alimenta a las demas.
3. **D7 cierra.** Orden depende de Tiempo y Movimiento, confirmando su posicion final.
4. **La estructura general es un orden parcial**, no un conjunto desordenado.

### Lo que se cuestiona

1. **La posicion de D6 (Movimiento).** El DAG la coloca como 3ra o 4ta, no 6ta. La narrativa "Movimiento viene despues de Identidad" no se sostiene en las dependencias de primitivos.
2. **La independencia D3-D4 y D4-D5.** El circulo implica una transicion Tiempo->Posibilidad->Identidad, pero no hay dependencia directa entre ellas en el DAG.
3. **El D-rate no sigue el circulo.** La universalidad empirica no confirma el orden propuesto.

### Implicacion constructiva

El circulo de dualidades puede ser valido como **estructura conceptual** (el orden en que los conceptos se necesitan para *entenderse*) aunque no coincida con el **orden de dependencias** (el orden en que los primitivos se construyen en el DAG). Son dos ordenes diferentes sobre el mismo conjunto de 7 elementos.

La fase siguiente podria explorar si existe una metrica diferente — quizas basada en informacion mutua o en la estructura de los dominios — que reproduzca mejor el orden del circulo.

---

## VII. Archivos generados

| Archivo | Descripcion |
|---------|-------------|
| `data/dualidad_primitivo_map.json` | Mapeo 7 dualidades -> primitivos ancla y secundarios |
| `scripts/emergence_analysis.py` | Script de analisis (~310 lineas, solo stdlib) |
| `31_formalizacion_emergencia.md` | Este documento |
