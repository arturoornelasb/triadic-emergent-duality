# Tests Empiricos Completos
## Orden de activacion, principio holografico, abstraccion-zeros, y extraccion del poset
### J. Arturo Ornelas Brand — Marzo 2026

---

## Resumen

Este documento ejecuta los cuatro tests empiricos pendientes del manuscrito. Los resultados contienen dos confirmaciones y dos sorpresas:

1. **Test de orden de activacion** (Doc 09): PARCIALMENTE CONFIRMADO. Las dependencias ontologicas aumentan la co-activacion 1.5-6x por encima del azar en ~50% de los pares, pero el sistema de anclas codifica *prominencia*, no clausura transitiva.

2. **Test holografico** (Doc 06): DEBIL. La determinacion holografica estricta falla (2.3% exacto), pero la periferia contiene 3.13x mas informacion sobre el interior que el azar.

3. **Test abstraccion-zeros** (Doc 06): **REFUTADO**. La correlacion es *negativa* (r = -0.470): los conceptos abstractos tienen *mas* bits activos, no menos. El ~42% de zeros no aplica a anclas.

4. **Extraccion del poset** (Doc 05): CONFIRMADO como DAG, pero **NO ES LATTICE**. El poset de 63 primitivos es un DAG general con 3 raices, 32 hojas, anchura maxima 21, cadena maxima 8. La afirmacion de lattice en Doc 05 debe corregirse.

---

## I. Test de Orden de Activacion de Bits

### 1.1 Protocolo

Para cada par de dependencia (hijo, padre) en `primitivos.json`, se calculo:
- Cuantas de las 155 anclas (v1 + v2) tienen el hijo activo
- De esas, cuantas tambien tienen el padre activo
- Tasa de consistencia = ambos_activos / hijo_activo
- Comparacion con baseline aleatorio: P(padre) en todo el corpus

### 1.2 Resultado global

**Consistencia ponderada: 21.7%** (373 de 1,722 instancias).

Solo 2 pares tienen 100% de consistencia:
- `pensar → consciente` (6/6)
- `porque → posición_temporal` (2/2)

### 1.3 Interpretacion: por que la consistencia es baja

La baja consistencia global **no refuta** las dependencias ontologicas. El sistema de anclas codifica **rasgos salientes**, no la clausura transitiva de dependencias. Cuando "democracia" tiene `consciente` activo pero no `vida`, no es que la democracia exista sin seres vivos — es que `vida` no es un rasgo *prominente* de la democracia.

**Distincion critica**:
- `primitivos.json` = estructura **ontologica** (que requiere que para existir)
- `anclas_v2.json` = estructura **fenomenica** (que es saliente al pensar en el concepto)

### 1.4 Resultado clave: test contra baseline aleatorio

El test verdaderamente informativo no es la consistencia absoluta sino la comparacion con el azar. Para cada par de dependencia:

$$\text{Ratio} = \frac{P(\text{padre} | \text{hijo activo})}{P(\text{padre})}$$

Un ratio > 1.0 significa que la dependencia ontologica *aumenta* la co-activacion por encima del azar.

**Distribucion de ratios** (pares con hijo activo en >= 2 anclas):

| Rango | N pares | Interpretacion |
|-------|---------|---------------|
| > 3.0x | 15 | Fuerte efecto de dependencia |
| 2.0-3.0x | 9 | Efecto moderado |
| 1.0-2.0x | 24 | Efecto debil pero presente |
| < 1.0x | 32 | Sin efecto o efecto inverso |
| = 0.0 | 23 | Padre nunca co-activo |

**48 de 80 pares testables (60%) muestran ratio > 1.0.** La dependencia ontologica tiene un efecto real y medible sobre la co-activacion conceptual.

### 1.5 Top 10 pares con mayor efecto

| Hijo | Padre | Ratio | N |
|------|-------|-------|---|
| mover → eje_profundidad | 6.20x | 25 |
| saber → información | 5.74x | 9 |
| flujo_temporal → posición_temporal | 4.84x | 16 |
| muerte → destrucción | 4.43x | 10 |
| mal → separación | 4.40x | 11 |
| aire → libertad | 4.31x | 9 |
| creador_obs → hacer | 4.24x | 8 |
| verdad → orden | 3.99x | 14 |
| mentira → caos | 3.88x | 4 |
| tacto → contención | 3.87x | 5 |

### 1.6 Pares con ratio = 0 (padre nunca co-activo)

Los pares con ratio 0 son mayoritariamente casos donde el padre es un primitivo *estructural* (uno, posición_temporal, eje_profundidad) que rara vez aparece como rasgo saliente. `uno` aparece en solo 7 de 155 anclas (4.5%), porque la unidad es presupuesta, no mencionada.

**Patron**: los primitivos de capas 1-2 que son prerequisitos universales tienen baja frecuencia en anclas. Son como el oxigeno del sistema — necesarios pero invisibles.

### 1.7 Veredicto

**El test de orden de activacion es PARCIALMENTE POSITIVO:**
- 60% de los pares muestran efecto de dependencia (ratio > 1.0)
- Los pares con mayor efecto corresponden a dependencias intuitivamente fuertes (saber→información, verdad→orden, aire→libertad)
- La consistencia absoluta es baja (21.7%) pero esto se explica por la diferencia entre codificacion ontologica y fenomenica
- El test no refuta el marco; lo matiza: las dependencias ontologicas son reales pero no se manifiestan como co-activacion obligatoria en el nivel fenomenico

---

## II. Test Holografico

### 2.1 Protocolo

Se clasificaron los 63 primitivos en:
- **Perifericos** (24): los 12 ejes duales × 2 polos (bien/mal, orden/caos, etc.)
- **Interiores** (39): todos los demas (fuerza, mover, contención, etc.)

Para cada ancla, se extrajo su perfil periferico y su perfil interior. Se agrupo por perfil periferico identico y se verifico si los perfiles interiores coinciden.

### 2.2 Resultado estricto

- Perfiles perifericos distintos: 85 de 104 anclas
- Grupos con >1 ancla (mismo perfil periferico): 10
- Pares con periferia identica: 44
- **Pares con interior identico: 1 de 44 (2.3%)**
- El unico par identico: `piedra` y `hierro` (ambos: interior = {contención, fuerza, tierra})

**La determinacion holografica estricta FALLA.** La periferia no determina univocamente el interior.

### 2.3 Resultado relajado

| Metrica | Valor |
|---------|-------|
| Jaccard similarity (misma periferia) | 0.248 |
| Jaccard similarity (pares aleatorios) | 0.079 |
| **Ratio** | **3.13x** |

La periferia contiene **3.13 veces mas informacion** sobre el interior que el azar. No es determinacion completa, pero es determinacion parcial significativa.

### 2.4 Analisis de los grupos

El grupo mas grande (8 anclas) comparte el perfil periferico **vacio** (ningun polo dual activo): gravedad, velocidad, masa, luz, alto, bajo, pesado, visible. Estos son conceptos fisicos basicos que operan en capas pre-duales. Sus interiores son muy diversos — la periferia vacia no predice nada.

Los grupos con perfil no vacio muestran mayor coherencia interior. Por ejemplo:
- `{consciente, dolor}` agrupa irritación y aburrimiento — interiores diferentes pero ambos negativos
- `{orden}` agrupa piedra, hierro, nitrógeno, silencio — todos estructurados

### 2.5 Poder predictivo de la periferia

Para cada primitivo interior, se calculo que polo periferico lo predice mejor (F1 score):

| Interior | Mejor predictor periferico | F1 |
|----------|--------------------------|-----|
| vacío | ausente | 0.59 |
| hacer | individual | 0.46 |
| interocepción | vida | 0.47 |
| más | control | 0.42 |
| decir | creador_obs | 0.40 |
| querer | consciente | 0.36 |
| contención | individual | 0.35 |

Ningun predictor supera F1 = 0.60. La periferia *sugiere* el interior pero no lo determina.

### 2.6 Veredicto

**El principio holografico es DEBIL pero real:**
- La determinacion estricta falla (2.3%)
- La determinacion parcial es 3.13x mejor que el azar
- Los mejores predictores periferico→interior tienen F1 < 0.60
- **Conclusion**: la periferia codifica informacion parcial sobre el interior, no informacion completa. El principio holografico funciona como *tendencia*, no como *ley*.

**Implicacion para Doc 06**: La analogia del agujero negro se debilita en su componente holografico. La periferia no "determina" el interior; lo *constrañe*. Mejor analogia: la periferia es un *filtro* que reduce el espacio de interiores posibles a ~1/3 del total.

---

## III. Test de Abstraccion-Zeros

### 3.1 Protocolo

Para cada ancla, se calculo:
- Numero de bits activos
- Porcentaje de zeros (bits inactivos)
- Nivel promedio de capa de los bits activos (proxy para abstraccion)

Se computo la correlacion de Pearson entre nivel de capa y porcentaje de zeros.

### 3.2 Resultado

**Pearson r = -0.470: CORRELACION NEGATIVA.**

Los conceptos "mas abstractos" (cuyo promedio de capa es mas alto) tienen **mas bits activos**, no menos. Esto **contradice** la prediccion del Doc 06.

### 3.3 Datos por categoria

| Categoria | N | Bits activos (avg) | %Zeros | Capa avg |
|-----------|---|-------------------|--------|---------|
| Concretos/Fisicos | 12 | 4.4 | 93.0% | 2.99 |
| Abstractos/Politicos | 11 | 6.0 | 90.5% | 3.92 |
| Emocionales | 10 | 6.1 | 90.3% | 4.14 |
| Roles sociales | 10 | 5.9 | 90.6% | 4.18 |

Los conceptos concretos (piedra, hierro, masa) usan 4.4 bits en promedio. Los abstractos (democracia, tolerancia) usan 6.0. Los emocionales (ira, miedo) usan 6.1.

### 3.4 Interpretacion: por que la prediccion falla

La prediccion del Doc 06 fue: "conceptos abstractos → mas zeros (menos dimensiones relevantes)." Lo que ocurre es lo opuesto: los conceptos abstractos son *mas ricos* conceptualmente — involucran mas dimensiones.

**Explicacion**: La abstraccion no es *vaciamiento* (menos rasgos) sino *integracion* (mas rasgos de capas altas). Un concepto como "democracia" requiere consciencia, libertad, orden, colectividad, bien — muchas dimensiones simultaneas. Una "piedra" solo requiere fuerza, contención, orden, tierra — pocas dimensiones.

**La abstraccion es aditiva, no sustractiva.**

### 3.5 Sobre el ~42% de zeros

El 42% de zeros converge en los **pesos del modelo** durante entrenamiento (BitNet: 42.3%, TriadicGPT: 42.9%). Los anclas tienen 91.5% de zeros, un numero completamente diferente.

Esto se explica: los anclas codifican ~5-6 de 63 bits como *salientes*. Los pesos del modelo distribuyen activaciones sobre todos los 63 bits para cada concepto. Son mediciones de objetos categoricamente distintos:

- **Pesos entrenados**: distribucion de activaciones en el espacio vectorial del modelo
- **Anclas**: seleccion humana de rasgos prominentes

El ~42% deberia testearse sobre **vectores de activacion del modelo**, no sobre anclas. Este test requiere inferencia del modelo entrenado.

### 3.6 Veredicto

**La prediccion abstraccion→mas zeros es REFUTADA para anclas.** La abstraccion es aditiva: los conceptos abstractos activan mas primitivos, no menos. El ~42% de zeros es una propiedad del modelo entrenado, no del sistema de anclas.

---

## IV. Extraccion Formal del Poset de 63 Primitivos

### 4.1 Propiedades basicas

| Propiedad | Valor |
|-----------|-------|
| Nodos | 63 |
| Aristas directas | 128 |
| Aristas de Hasse (red. transitiva) | 97 |
| Aristas transitivamente redundantes | 31 |
| Es DAG | **SI** |
| Es lattice | **NO** |
| Raices | 3 (vacío, información, uno) |
| Hojas | 32 |
| Cadena maxima | 8 |
| Anchura maxima | 21 (capa 5) |
| Componentes conexas | 1 |
| Capas | 6 |

### 4.2 El poset NO es un lattice

El Doc 05 (Seccion I.3) afirma que $(D_7, \leq)$ es un lattice. Esto se verifica para las 7 dualidades. Pero el poset de 63 primitivos **no** es un lattice:

- **137 de 208 pares muestreados** carecen de join (supremo)
- **50 pares** tienen meets (infimos) multiples
- **4 pares** tienen joins multiples

Ejemplo: `información` y `contención` tienen tres joins distintos: {gusto, tacto, vida}. No hay un unico "primer descendente comun."

Ejemplo: `información` y `uno` tienen 12 joins: {creación, destrucción, gusto, mentira, olfato, oído, porque, tacto, tal_vez, tipo_de, verdad, vista}. El grafo diverge desde las raices y se reunifica en multiples puntos sin jerarquia unica.

**Implicacion**: El poset de primitivos es un **DAG general** (directed acyclic graph), no un lattice. La estructura es mas rica y mas desordenada de lo que el marco teorico supone.

### 4.3 Reduccion transitiva

De las 128 aristas directas, 31 son transitivamente redundantes. Las mas notables:

| Arista redundante | Camino alternativo |
|-------------------|--------------------|
| uno → contención | uno → separación → contención |
| uno → muchos | uno → más → muchos |
| información → consciente | información → vista → consciente (via vida) |
| fuerza → hacer | fuerza → mover → hacer |
| mover → flujo_temporal | mover → posición_temporal → flujo_temporal |

Esto sugiere que el diseño original de `primitivos.json` incluyo dependencias tanto inmediatas como transitivas. Las 97 aristas de Hasse son las dependencias *minimas necesarias*.

### 4.4 Cadena maxima

La cadena mas larga tiene 8 nodos:

```
uno → fuerza → mover → hacer → creación → vida → individual → colectivo
```

Esta cadena cruza 6 capas y conecta la unidad (d8) con la colectividad a traves de fuerza, movimiento, accion, creacion, vida, e individualidad. Es el "camino mas largo del sistema" — la secuencia de dependencias mas profunda.

### 4.5 Antichains por capa

Solo las capas 1 y 6 son antichains puros (ningun par comparable). Las capas 2-5 contienen pares comparables internos:
- Capa 2: contención y separación son comparables (contención depende de separación)
- Capa 3: mover y posición_temporal son comparables
- Capa 4: eje_vertical y eje_lateral son comparables
- Capa 5: oído y decir son comparables

Esto confirma que las "capas" de `primitivos.json` no son niveles puros del poset — son agrupaciones por dimensionalidad geometrica, no por profundidad de dependencia.

### 4.6 Veredicto

**El poset de 63 primitivos es un DAG bien formado pero no un lattice.** La estructura es un grafo dirigido aciclico con 3 raices, 32 hojas, profundidad 8, y anchura 21. La afirmacion de lattice en el Doc 05 debe restringirse a las 7 dualidades fundamentales; el poset completo requiere una formalizacion mas general (DAG, no lattice).

---

## V. Tabla Resumen de Todos los Tests

| Test | Doc origen | Prediccion | Resultado | Veredicto |
|------|-----------|-----------|----------|-----------|
| 1. Independencia de ramas (Doc 12) | Doc 11 | Ramas A, B, C independientes | 0 co-activacion A+B | **CONFIRMADO** |
| 2. Betweenness centrality (Doc 12) | Doc 11 | contención > porque > tipo_de | 7/7 predicciones correctas | **CONFIRMADO** |
| 3. Auto-similitud (Doc 12) | Doc 11 | Patron se repite | 80% score | **CONFIRMADO (parcial)** |
| 4. Orden de activacion | Doc 09 | Dependencia → co-activacion | 60% pares > baseline | **PARCIALMENTE CONFIRMADO** |
| 5. Holografico | Doc 06 | Periferia determina interior | 2.3% exacto, 3.13x relajado | **DEBIL** |
| 6. Abstraccion-zeros | Doc 06 | Abstracto → mas zeros | r = -0.470 (opuesto) | **REFUTADO** |
| 7. Poset es lattice | Doc 05 | 63 primitivos forman lattice | 137 pares sin join | **REFUTADO (es DAG)** |

### Balance

- **3 confirmaciones fuertes** (tests 1-3): La estructura arborea con tres ramas es robusta.
- **1 confirmacion parcial** (test 4): Las dependencias son reales pero se manifiestan estadisticamente, no como reglas estrictas.
- **1 resultado debil** (test 5): El principio holografico funciona como tendencia (3x), no como ley.
- **2 refutaciones** (tests 6-7): La abstraccion es aditiva (no sustractiva) y el poset es un DAG general (no un lattice).

---

## VI. Correcciones Requeridas al Manuscrito

| Documento | Seccion | Correccion |
|-----------|---------|------------|
| Doc 05 | I.3 | Restringir afirmacion de lattice a D7; el poset de 63 es DAG general |
| Doc 05 | I.4 | Ya actualizado (Docs 11-12) |
| Doc 05 | I.5 | Agregar: 97 aristas de Hasse, 31 redundantes, no es lattice |
| Doc 06 | III | Debilitar principio holografico: determinacion parcial (3.13x), no completa |
| Doc 06 | VI | Corregir prediccion abstraccion-zeros: refutada; la abstraccion es aditiva |
| Doc 09 | II | Agregar resultados del test de orden de activacion: 60% de pares > baseline |
| Doc 10 | I | Agregar: Claim 2 debilitado (holografico es tendencia); nueva refutacion (abstraccion) |

---

## Referencias

- Freeman, L. C. (1977). "A Set of Measures of Centrality Based on Betweenness." *Sociometry*, 40(1), 35-41.
- Ornelas Brand, A. (2026). Documentos 01-12 del manuscrito "Expansion del Circulo de Emergencia de Dualidades."

---

*Parte del manuscrito "Expansion del Circulo de Emergencia de Dualidades."*
*Documento 13 — Tests empiricos completos.*
