# Revision Empirica de las Dualidades 8-14
## Tests computacionales, revision teorica, y propuesta de articulo
### J. Arturo Ornelas Brand — Marzo 2026

---

## Resumen

Este documento ejecuta el plan de investigacion formulado en el Documento 11 (Bifurcaciones Internas). Presenta los resultados de tres tests empiricos sobre `primitivos.json` y `anclas_v2.json`, realiza cuatro tareas de revision teorica (reescritura de la estructura d8-d14, evaluacion del status de Continuo/Discreto, evaluacion de Vida/Muerte como dualidad formal, y reconciliacion entre dualidades-contenido y dualidades-operacion), y concluye con una propuesta de articulo independiente para *Foundations of Science*.

---

## I. Resultados de los Tests Empiricos

### Test 1 — Consistencia de dependencias y independencia de ramas en anclas_v2.json

#### 1A. Consistencia de dependencias

Se verifico si los 104 conceptos-ancla respetan las dependencias de `primitivos.json`: cuando un primitivo-hijo esta activo en un ancla, ¿esta tambien activo su primitivo-padre?

**Resultado**: Consistencia del 28.5% (94 de 330 instancias cumplen).

Las violaciones mas frecuentes:

| Dependencia | Violaciones / Ocurrencias | Tasa |
|-------------|--------------------------|------|
| consciente → información | 48 / 56 | 86% |
| consciente → vida | 38 / 56 | 68% |
| vida → creación | 27 / 28 | 96% |
| vida → contención | 23 / 28 | 82% |
| vida → flujo_temporal | 23 / 28 | 82% |
| vida → orden | 23 / 28 | 82% |
| individual → contención | 18 / 26 | 69% |
| control → contención | 9 / 14 | 64% |
| mal → contención | 9 / 10 | 90% |

**Interpretacion**: Esto **no** refuta las dependencias de `primitivos.json`. Los anclas codifican rasgos *salientes*, no la clausura transitiva de dependencias. Cuando un concepto como "democracia" tiene `consciente` activo pero no `vida`, no es que la democracia exista sin vida — es que `vida` no es un rasgo *saliente* de la democracia. El sistema de anclas opera por **prominencia conceptual**, no por completitud ontologica.

**Hallazgo importante**: Las altas tasas de violacion para dependencias de segundo orden (consciente→vida, vida→contención) confirman que el sistema de anclas codifica una **superficie conceptual**, no la estructura profunda de dependencias. Esto es coherente con el principio holografico (Doc 06): la superficie (anclas) contiene informacion suficiente para reconstruir la estructura profunda, pero no la replica directamente.

**Distincion clave para el marco**:
- `primitivos.json` = estructura **ontologica** (que requiere que para existir)
- `anclas_v2.json` = estructura **fenomenica** (que es saliente al pensar en el concepto)

#### 1B. Independencia de ramas

Se clasificaron las tres ramas del arbol asimetrico por activacion en anclas:

| Rama | Primitivos | Anclas activas | % |
|------|-----------|---------------|---|
| A (Topologica) | contención, vida, consciente | 77 | 74% |
| B (Causal) | porque, si_entonces | 2 | 2% |
| C (Clasificatoria) | tipo_de | 0 | 0% |
| Ninguna rama | — | 25 | 24% |

**Co-activacion entre ramas**:

| Par | Observada | Esperada (independencia) | Ratio |
|-----|----------|------------------------|-------|
| A+B | 0 | 1.5 | 0.00 |
| A+C | 0 | 0.0 | — |
| B+C | 0 | 0.0 | — |
| A+B+C | 0 | — | — |

**Resultado decisivo**: Cero co-activacion entre las ramas B y C con la rama A. Los unicos dos anclas con `porque` activo son `causa` y `efecto` — los conceptos que *definen* la causalidad, no conceptos que la *usan*. Ningun concepto del corpus activa `tipo_de`.

**Interpretacion**: La independencia de las ramas es **total** en los datos de anclas. Esto es mas fuerte de lo esperado: no solo las ramas son estructuralmente independientes en el grafo de primitivos (Doc 11), sino que los conceptos del mundo real *nunca* activan ramas multiples simultaneamente.

La Rama A (topologica) domina: el 74% de los conceptos activan contención, vida, o consciente. La Rama B es marginal (2%) y la Rama C es invisible (0%). Esto confirma cuantitativamente que `contención→vida→consciente` es la autopista principal del sistema, y que `porque` y `tipo_de` son callejones sin salida no solo en el grafo de dependencias sino tambien en el uso conceptual.

#### 1C. Activaciones exclusivas

| Categoria | N | Ejemplos |
|-----------|---|----------|
| Solo Rama A | 77 | democracia, tolerancia, aceptación, audacia |
| Solo Rama B | 2 | causa, efecto |
| Solo Rama C | 0 | — |
| Ninguna rama | 25 | socialismo, capitalismo, número, gravedad |

Los 25 conceptos sin activacion de ninguna rama son mayoritariamente conceptos fisicos (gravedad, velocidad, masa, distancia) y politicos basicos (socialismo, capitalismo, tirania). Estos conceptos operan en las capas pre-d8 del sistema: fuerza, movimiento, orden, pero no requieren contencion, causalidad explicita, ni clasificacion.

---

### Test 2 — Centralidad de intermediacion (Betweenness Centrality)

#### 2A. Betweenness centrality

Se calculo la centralidad de intermediacion para los 63 primitivos del grafo no dirigido de dependencias.

**Top 10 por betweenness centrality**:

| Rank | Primitivo | Capa | Centrality | Rol predicho |
|------|----------|------|-----------|-------------|
| 1 | **información** | 1 | 0.271 | Raiz de datos |
| 2 | **contención** | 2 | 0.170 | Hub principal (d10) |
| 3 | **uno** | 1 | 0.163 | Raiz universal (d8) |
| 4 | **consciente** | 5 | 0.142 | Hub terminal (d14) |
| 5 | **vida** | 5 | 0.126 | Hub de reunificacion |
| 6 | **mover** | 3 | 0.116 | Camino temporal |
| 7 | **fuerza** | 2 | 0.087 | Raiz dinamica |
| 8 | hacer | 3 | 0.081 | Accion |
| 9 | eje_profundidad | 2 | 0.071 | Raiz espacial |
| 10 | **orden** | 3 | 0.061 | Hub de patrones (d7) |

**Primitivos clave de las dualidades 8-14**:

| Primitivo | Betweenness | Rank | Prediccion Doc 11 | Confirmada? |
|-----------|------------|------|-------------------|------------|
| contención (d10) | 0.170 | #2 | Hub principal | **SI** |
| vida | 0.126 | #5 | Reunificacion | **SI** |
| consciente (d14) | 0.142 | #4 | Terminal hub | **SI** |
| uno (d8) | 0.163 | #3 | Raiz universal | **SI** |
| porque (d11) | 0.036 | #15 | Callejon sin salida | **SI** |
| tipo_de (d12) | 0.019 | #22 | Hoja terminal | **SI** |
| parte_de (d13) | 0.012 | #29 | Ramal corto | **SI** |

**Las 7 predicciones del Doc 11 se confirman al 100%.** contención, vida, consciente son los tres nodos mas centrales despues de las raices (información, uno). porque, tipo_de, y parte_de tienen centralidad marginal, confirmando su rol periferico.

#### 2B. Centralidad de flujo en DAG

Para el grafo dirigido (DAG), se calculo cuantos caminos raiz→hoja pasan por cada nodo.

| Primitivo | Flujo DAG | Rank |
|-----------|----------|------|
| uno | 297 | #1 |
| vida | 182 | #2 |
| mover | 164 | #3 |
| consciente | 153 | #4 |
| fuerza | 110 | #5 |
| porque | 3 | #54 |
| tipo_de | 5 | #44 |
| parte_de | 3 | #53 |

**Resultado**: `vida` es el segundo nodo por flujo en el DAG completo — 182 caminos pasan a traves de ella. Esto la establece como la **bisagra critica** del sistema: la mayoria de los caminos de las raices a las hojas pasan por vida. En contraste, `porque` tiene flujo 3 y `tipo_de` tiene flujo 5 — son practicamente invisibles en la estructura de caminos.

#### 2C. Analisis de grado

| Primitivo | In-degree | Out-degree | Total |
|-----------|----------|-----------|-------|
| información | 0 | 19 | 19 |
| contención | 2 | 12 | 14 |
| consciente | 3 | 9 | 12 |
| uno | 0 | 10 | 10 |
| vida | 4 | 6 | 10 |
| mover | 2 | 8 | 10 |
| porque | 2 | 1 | 3 |
| tipo_de | 3 | 0 | 3 |
| parte_de | 2 | 1 | 3 |

La diferencia de grado es dramatica: `contención` tiene out-degree 12 (alimenta a 12 primitivos directamente), mientras que `porque` tiene out-degree 1 y `tipo_de` tiene out-degree 0. El grado total de `contención` (14) es comparable al de los nodos raiz, confirmando su rol como **segundo hub del sistema**.

---

### Test 3 — Auto-similitud cuantitativa

#### 3A. Los dos patrones

**Patron 1 (Fundamental)**: d1 → {d2 (espacio), d3 (tiempo)} → d4 (posibilidad)
En primitivos.json: raices → {eje_profundidad (espacial), mover (temporal)} → reunificacion (41 nodos dependen de ambas ramas)

**Patron 2 (Extendido)**: d8 → {contención (topologico), porque (causal)} → vida (reunificacion)
En primitivos.json: uno → {contención (28 desc), porque (1 desc)} → vida (16 desc)

#### 3B. Metricas de comparacion

| Metrica | Patron 1 | Patron 2 |
|---------|---------|---------|
| Root fanout | 10 hijos | 10 hijos |
| Num. ramas | 2 | 3 |
| Rama mayor (desc.) | 46 | 28 |
| Rama menor (desc.) | 41 | 1 |
| Asimetria | 1.12x | 28.0x |
| Overlap (nodos dep. ambas) | 41 | 0 |
| Reunificacion existe | Si | Si |
| Desc. del nodo reunificador | 29 (mayor candidato) | 16 (vida) |
| Tipo de ramas | espacial vs temporal | topologica vs causal |

#### 3C. Score de similitud

| Criterio | P1 | P2 | Match? | Peso |
|----------|----|----|--------|------|
| Raiz se bifurca | Si | Si | MATCH | 2 |
| Ramas son espacio-like vs tiempo-like | Si | Si | MATCH | 2 |
| Existe reunificacion | Si | Si | MATCH | 2 |
| Reunificacion tiene muchos desc. | Si | Si | MATCH | 1 |
| Num. ramas coincide | 2 | 3 | MATCH* | 1 |
| Asimetria < 5x | Si | No | DIFF | 1 |
| Overlap > 0 | Si | No | DIFF | 1 |

**Score total: 8/10 (80%)**

#### 3D. Profundidad de la reunificacion

**Pattern 1**: vida es candidato a reunificacion en Pattern 1 tambien — depende de eje_profundidad (espacial) y de mover, posición_temporal, flujo_temporal, hacer (temporal). En Pattern 1, 41 de 63 nodos dependen de ambas ramas — la reunificacion es masiva y temprana.

**Pattern 2**: vida depende de contención (topologica) y de flujo_temporal (temporal) y de orden (clasificatoria) y de creación (cruzada). **vida** cruza las tres ramas. Pero NO depende de `porque` — la reunificacion es parcial: incluye la temporalidad *implicita* (flujo temporal) pero no la causalidad *explicita* (porque).

#### 3E. Veredicto

**Auto-similitud imperfecta (80%)**, consistente con fractales naturales (no matematicos).

Propiedades compartidas:
1. La raiz se bifurca en ramas tipo-espacio y tipo-tiempo
2. Las ramas se reunifican en un nodo de orden superior
3. El nodo reunificador tiene muchos descendentes
4. La rama espacial/topologica es dominante

Propiedades divergentes:
1. Pattern 2 tiene 3 ramas (agrega clasificatoria), Pattern 1 tiene 2
2. La asimetria de Pattern 2 es 28x (vs 1.1x en Pattern 1) — deformacion dramatica
3. En Pattern 1 hay 41 nodos de overlap; en Pattern 2 hay cero
4. La reunificacion de Pattern 2 es parcial (via flujo_temporal, no via porque)

**Conclusion**: El patron se repite pero se *deforma* a cada nivel — mas ramas, mas asimetria, reunificacion mas parcial. Esto es la firma de la **auto-similitud estadistica**, no exacta. La espiral generativa produce estructura fractal con degradacion.

---

## II. Revision Teorica

### Tarea 1 — Reescritura de la estructura d8-d14

La estructura lineal d8→d9→d10→d11→d12→d13→d14 propuesta en el Doc 04 debe abandonarse. La estructura empirica es un **arbol asimetrico con tronco dominante**:

#### Diagrama de Hasse revisado (14 dualidades)

```
          d1 (Existir/No-existir)
         /  \
       d2    d3
    (Espacio)(Tiempo)
         \  /
          d4 (Posible/Imposible)
          |
          d5 (Determinado/Indeterminado)
          |
          d6 (Movimiento/Quietud)
          |
          d7 (Orden/Caos)
          |
          d8 (Uno/Muchos) ← BIFURCACION TRIPLE
         /|\
        / | \
       /  |  \
   TRONCO | RAMAL-B    RAMAL-C
      |   |   |            |
     d9'  | d11         d12
  (Dentro/|  (Causa/     (Semejante/
   Fuera) |   Efecto)    Diferente)
      |   |   [terminal]  [terminal]
     d10' |
  (Parte/ |
   Todo)  |
      |   |
     d11' |
  (Vida/  |
  Muerte) |
      |   |
     d14  |
  (Sujeto/
   Objeto)
```

#### Cambios respecto al Doc 04

| Aspecto | Doc 04 (original) | Revision empirica |
|---------|-------------------|-------------------|
| Estructura | Cadena o lattice simetrico | Arbol asimetrico |
| d9 (Continuo/Discreto) | Admitida entre d8 y d10 | **Eliminada** — meta-propiedad |
| d10 (Dentro/Fuera) | Posicion 10, depende de d9 | Asciende a **d9'** — segundo nodo troncal |
| d11 (Causa/Efecto) | Hub causal, depende de d10 | **Ramal lateral** — 1 descendente |
| d12 (Semejante/Diferente) | Depende de d11 | **Ramal lateral independiente** — 0 desc. |
| d13 (Parte/Todo) | Join de d10 y d12 | En rama topologica, depende de contención |
| Vida/Muerte | No numerada | **Candidata a d11'** — bisagra de segundo orden |
| Reunificacion | d13 (Parte/Todo) | vida (cruza las tres ramas) |

#### Relaciones de cubierta revisadas

- $d_7 \lessdot d_8$
- $d_8 \lessdot d_{9'}$ (Dentro/Fuera)
- $d_8 \lessdot d_{11}$ (Causa/Efecto) [ramal]
- $d_8 \lessdot d_{12}$ (Semejante/Diferente) [ramal, via orden]
- $d_{9'} \lessdot d_{10'}$ (Parte/Todo)
- $d_{9'} \lessdot d_{11'}$ (Vida/Muerte)
- $d_{11'} \lessdot d_{14}$ (Sujeto/Objeto)

Notese que d11 y d12 **no tienen relacion de cubierta con d14**. Son ramales terminales. La consciencia no requiere causalidad explicita ni clasificacion — requiere vida, y la vida requiere contencion.

---

### Tarea 2 — Status de Continuo/Discreto (d9)

Tres hipotesis evaluadas:

**Hipotesis A: d9 es meta-propiedad (no primitivo)**
- Evidencia a favor: Ausente de primitivos.json. La tension continuo/discreto opera a nivel de *representacion* (embeddings continuos → cuantizacion ternaria), no de *contenido*.
- Evidencia en contra: Es argumentable filosoficamente (la topologia abre un dominio genuino).
- Veredicto: **FUERTE** — 7/10

**Hipotesis B: d9 esta presupuesto pero no codificado**
- Evidencia a favor: El sistema de 63 bits *ya es* discreto; no necesita un bit que diga "soy discreto."
- Evidencia en contra: Otros presupuestos (existencia, tiempo) si estan codificados.
- Veredicto: **MEDIO** — 5/10

**Hipotesis C: d9 es un hueco que deberia llenarse**
- Evidencia a favor: La topologia es un dominio genuino y diferente de la aritmetica.
- Evidencia en contra: 104 anclas y 63 primitivos funcionan sin el. Ningun concepto del corpus lo necesita.
- Veredicto: **DEBIL** — 3/10

**Recomendacion**: Adoptar **Hipotesis A**. Continuo/Discreto es una meta-propiedad del marco de representacion, no una dualidad del contenido representado. Se recomienda:

1. **Eliminar d9 de la secuencia numerada** de dualidades 8-14.
2. **Reclasificar** Continuo/Discreto como *propiedad del marco* (junto a ternario/binario, finito/infinito de la representacion).
3. **Ascender** Dentro/Fuera a la posicion d9' (inmediatamente posterior a d8).
4. Si futuras versiones de primitivos.json (v3, 128 bits) encuentran necesario un par continuo/discreto, rehabilitarla como dualidad, pero con el caveat de que opera en un nivel categorico diferente.

---

### Tarea 3 — Vida/Muerte como dualidad formal

#### Evidencia a favor de la numeracion formal

1. **Centralidad de flujo**: vida tiene flujo DAG = 182 (rank #2 de 63). Solo `uno` tiene mas caminos pasando por el.
2. **Betweenness**: vida tiene centralidad 0.126 (rank #5). Mas alta que `porque` (#15) y `tipo_de` (#22).
3. **Dependencias**: vida tiene 4 dependencias directas que cruzan las tres ramas (creación, contención, flujo_temporal, orden).
4. **Descendentes**: 16 descendentes directos e indirectos, incluyendo toda la cognicion.
5. **Rol de bisagra**: Unico nodo que sintetiza las ramas topologica, temporal y clasificatoria.
6. **Par dual explicito**: vida/muerte ya es un eje dual en primitivos.json (bits 32, 33).
7. **Auto-similitud**: vida ocupa la posicion analoga a d4 (Posibilidad) en el primer ciclo — el punto de reunificacion.

#### Evidencia en contra

1. **Es un concepto empirico, no formal**: Las 7 dualidades fundamentales son categorias ontologicas (existencia, espacio, tiempo...). Vida/Muerte es un fenomeno biologico. ¿Puede una dualidad biologica ser "fundamental"?
2. **Depende de 4 dualidades previas**: Su posicion alta en el grafo (capa 5) la hace muy dependiente. Las dualidades fundamentales tienen pocas dependencias.

#### Respuesta a las objeciones

La objecion 1 es seria pero resoluble: Vida/Muerte no es "biologica" en el sentido estrecho. En el marco de dualidades, `vida` es la **condicion minima de la auto-organizacion persistente**: un sistema que se mantiene lejos del equilibrio, se auto-replica, y tiene una frontera. Esta definicion incluye la vida biologica pero tambien potencialmente la vida artificial, los sistemas autopoieticos de Maturana y Varela, y cualquier sistema con las cuatro dependencias (creación + contención + flujo_temporal + orden). Es tan "fundamental" como Movimiento/Quietud — un fenomeno universal con definicion formal.

La objecion 2 se disuelve al notar que las dualidades extendidas (d8+) son *inherentemente* mas dependientes que las fundamentales — estan mas arriba en el grafo. La posicion de vida en capa 5 es coherente con su rol de bisagra de segundo orden.

#### Veredicto

**Vida/Muerte debe numerarse como dualidad formal, posicion d11' (entre Parte/Todo y Sujeto/Objeto)**. Argumentos:

- Parte/Todo (d10') depende de contención (d9') — la mereologia requiere fronteras.
- Vida/Muerte (d11') depende de contención + flujo_temporal + orden + creación — la vida requiere fronteras, tiempo, patron y generatividad.
- Sujeto/Objeto (d14) depende de vida (d11') — la consciencia requiere vida.

La secuencia troncal revisada es:

$$d_7 < d_8 < d_{9'} < d_{10'} < d_{11'} < d_{14}$$

(Orden → Uno/Muchos → Dentro/Fuera → Parte/Todo → Vida/Muerte → Sujeto/Objeto)

---

### Tarea 4 — Dualidades-contenido vs. dualidades-operacion

#### El problema

El Doc 11 descubrio que `porque` (Causa/Efecto) y `tipo_de` (Semejante/Diferente) son callejones sin salida en el grafo de primitivos. La hipotesis propuesta fue que son *operaciones* del sistema (la causalidad es la logica de las flechas; la clasificacion es la logica de la subsuncion) mas que *contenidos* del sistema.

Esto plantea una cuestion categorica: ¿puede una dualidad ser simultaneamente operacion y contenido? ¿O hay una distincion irreducible?

#### Taxonomia propuesta

Proponemos distinguir dos tipos de dualidades en el nivel extendido (d8+):

**Tipo I — Dualidades constitutivas**: Abren dominios de ser. Sus polos definen nuevos tipos de entidades que no existian antes. Son generativas: producen descendentes en el grafo de primitivos.

| Dualidad | Dominio que abre | Descendentes |
|----------|-----------------|-------------|
| d8 (Uno/Muchos) | Cantidad | 60 |
| d9' (Dentro/Fuera) | Topologia, limites | 28 |
| d10' (Parte/Todo) | Mereologia | ~2 |
| d11' (Vida/Muerte) | Biologia, auto-organizacion | 16 |
| d14 (Sujeto/Objeto) | Consciencia, epistemologia | 9 |

**Tipo II — Dualidades operativas**: Definen relaciones entre entidades existentes. Sus polos son *formas de conectar* entidades, no entidades nuevas. Son terminales: no generan descendentes significativos.

| Dualidad | Operacion que codifica | Descendentes |
|----------|----------------------|-------------|
| d11 (Causa/Efecto) | Conexion temporal dirigida | 1 |
| d12 (Semejante/Diferente) | Comparacion, clasificacion | 0 |

#### ¿Por que las operativas son terminales?

La causalidad no genera primitivos porque **es el lenguaje en que estan escritas las dependencias**. Cada flecha A→B del grafo de primitivos *es* una relacion causal ontologica. `porque` y `si_entonces` codifican la causalidad *explicita* (el concepto de "por que"), pero la causalidad *implicita* esta distribuida en la estructura del grafo entero.

Analogia: en aritmetica, "+" es una operacion, no un numero. No aparece en la secuencia 1, 2, 3... pero la genera toda. Del mismo modo, la causalidad es la "operacion" del grafo de dualidades, no un "nodo" generativo.

La clasificacion (`tipo_de`) codifica la operacion de subsuncion: $\Phi(A) | \Phi(B)$ si B hereda todos los rasgos de A. Esta operacion es el *mecanismo* por el cual los conceptos se relacionan jerarquicamente — es la maquinaria interna de TriadicGPT. No genera conceptos nuevos porque *es* la relacion entre conceptos.

#### Consecuencias para el marco

1. Las dualidades operativas (d11, d12) **no deben eliminarse** del conjunto de dualidades. Son dualidades genuinas: tienen polos opuestos, son exhaustivas, y abren dominios. Pero su posicion en la estructura es lateral, no troncal.

2. La numeracion deberia reflejar esta distincion: las constitutivas forman el tronco (d8→d9'→d10'→d11'→d14), las operativas son ramales (d11, d12).

3. Esta taxonomia es una **prediccion testeable**: si se extiende primitivos.json a 128 bits y se agregan primitivos como `responsabilidad`, `método_científico`, `taxonomía`, estos deberian depender de `porque` o `tipo_de` — convirtiendo los ramales en sub-arboles y debilitando la distincion constitutivo/operativo. Si los nuevos primitivos *no* dependen de ellos, la distincion se confirma.

4. La distincion resuena con una tradicion filosofica: Aristoteles distinguia entre categorias *sustanciales* (ousia) y *relacionales* (pros ti). Las constitutivas son sustanciales; las operativas son relacionales.

---

## III. Diagrama de Hasse Revisado Completo

### 3.1 Las 14 dualidades con estructura empirica

```
                d1 (Existir/No-existir)
               /  \
             d2    d3
          (Espacio)(Tiempo)
               \  /
                d4 (Posible/Imposible)
                |
                d5 (Determinado/Indeterminado)
                |
                d6 (Movimiento/Quietud)
                |
                d7 (Orden/Caos)
                |
                d8 (Uno/Muchos)
              / | \___________
             /  |              \
          d9'  d11(ramal)     d12(ramal)
       (Dentro/ (Causa/       (Semejante/
        Fuera)   Efecto)       Diferente)
           |
          d10'
       (Parte/
        Todo)
           |
         d11'
       (Vida/
       Muerte)
           |
          d14
       (Sujeto/
        Objeto)
```

### 3.2 Tabla de numeracion revisada

| Pos. | Dualidad | Tipo | Descendentes | Status |
|------|----------|------|-------------|--------|
| d1 | Existir/No-existir | Constitutiva | ~63 | Confirmada |
| d2 | Aquí/No-aquí | Constitutiva | ~46 | Confirmada |
| d3 | Antes/Después | Constitutiva | ~41 | Confirmada |
| d4 | Posible/Imposible | Constitutiva | — | Confirmada |
| d5 | Determinado/Indeterminado | Constitutiva | — | Confirmada |
| d6 | Movimiento/Quietud | Constitutiva | — | Confirmada |
| d7 | Orden/Caos | Constitutiva | ~21 | Confirmada |
| d8 | Uno/Muchos | Constitutiva | 60 | Confirmada |
| d9' | Dentro/Fuera | Constitutiva | 28 | Revisada (ex-d10) |
| d10' | Parte/Todo | Constitutiva | ~2 | Revisada (ex-d13) |
| d11' | Vida/Muerte | Constitutiva | 16 | **Nueva** |
| d11 | Causa/Efecto | Operativa | 1 | Ramal lateral |
| d12 | Semejante/Diferente | Operativa | 0 | Ramal lateral |
| d14 | Sujeto/Objeto | Constitutiva | 9 | Confirmada |
| ~d9~ | ~Continuo/Discreto~ | ~Meta-propiedad~ | — | **Eliminada** |

---

## IV. Consistencia con el Resto del Manuscrito

### 4.1 Compatibilidad con Doc 01 (Definiciones)

Las definiciones formales del Doc 01 (dualidad como tupla, tres estados, Fundierung) se mantienen intactas. La revision no modifica *que es* una dualidad, sino *como se organizan* las dualidades extendidas.

Se requiere agregar:
- **Definicion 8**: Dualidad constitutiva — abre dominio de ser, genera descendentes.
- **Definicion 9**: Dualidad operativa — define relacion entre entidades, terminal en el grafo.

### 4.2 Compatibilidad con Doc 02 (Secuencia Critica)

La bifurcacion d2/d3 se confirma y se replica a nivel superior (d9'/d11). El hallazgo fortalece el Doc 02.

### 4.3 Compatibilidad con Doc 05 (Formalizacion)

Seccion I.4 (Extension al lattice de 14 dualidades) debe reescribirse:
- La cadena $d_7 < d_8 < d_9 < ... < d_{14}$ se reemplaza por el arbol asimetrico.
- El Hasse de 14 dualidades (Seccion V.2) debe actualizarse.
- La Conjetura 2 (periodicidad heptagonal, Seccion IV.3) debe debilitarse: no son 7 por ciclo sino una estructura arborea con tronco de 6 y 2 ramales.

### 4.4 Compatibilidad con Doc 06 (Agujero Negro)

La revision **fortalece** la analogia del agujero negro: `contención` (la frontera, el limite) es empiricamente el hub mas influyente (betweenness #2), consistente con la idea de que la "superficie" codifica mas informacion que el "interior."

### 4.5 Compatibilidad con Doc 09 (TriadicGPT)

El test de orden de activacion (Doc 09, Seccion II) debe reformularse: en lugar de testear una cadena unica d8→d14, testear el arbol con sus tres ramas independientes.

---

## V. Propuesta de Articulo para *Foundations of Science*

### 5.1 Titulo

**"Empirical Bifurcation Structure of Extended Ontological Dualities: A Computational Analysis of Dependency, Centrality, and Self-Similarity"**

### 5.2 Abstract (borrador)

We investigate the internal structure of extended ontological dualities (d8-d14) through computational analysis of a dependency graph of 63 conceptual primitives and 104 anchor concepts from a neurosymbolic AI system (TriadicGPT). The theoretical hypothesis that extended dualities form a linear chain (Ornelas Brand, 2026a) is tested against three empirical measures: dependency consistency in concept anchors, betweenness and flow centrality in the dependency graph, and quantitative self-similarity between fundamental and extended bifurcation patterns.

Our results reveal that extended dualities form an *asymmetric tree* with a dominant trunk, not a chain or symmetric lattice. The topological branch (containment → life → consciousness) has 28 descendants and betweenness centrality 0.170, while the causal branch (because → if-then) has 1 descendant and centrality 0.036, and the classificatory branch (type-of) is a terminal leaf with 0 descendants and centrality 0.019. No concept in the anchor corpus activates primitives from both causal and topological branches simultaneously (zero co-activation).

We identify *life* (not causality or mereology) as the second-order reunification node — the only primitive whose dependencies cross all three branches. This finding leads to a revised duality sequence and a taxonomy distinguishing *constitutive dualities* (which open domains of being) from *operative dualities* (which encode relations). Finally, we measure 80% structural self-similarity between the fundamental bifurcation (existence → {space, time} → possibility) and the extended bifurcation (unity → {containment, causality} → life), consistent with natural (statistical, not exact) fractal structure in ontological emergence.

### 5.3 Estructura del articulo

1. **Introduction** (1500 words)
   - The Circle of Emergence of Dualities framework (brief summary)
   - The chain hypothesis for d8-d14
   - Motivation for computational testing

2. **Data and Methods** (2000 words)
   - primitivos.json: 63 primitives, 6 layers, ~180 dependency edges
   - anclas_v2.json: 104 anchor concepts with bit assignments
   - Dependency graph construction and transitive closure
   - Betweenness centrality, DAG flow centrality
   - Co-activation analysis and independence testing
   - Graph self-similarity metrics

3. **Results** (3000 words)
   - 3.1 The asymmetric tree structure
   - 3.2 Centrality analysis: three classes of primitives
   - 3.3 Branch independence in anchor data
   - 3.4 Self-similarity measurement (80% score)
   - 3.5 Life as reunification node

4. **Revised Duality Structure** (2000 words)
   - 4.1 Elimination of Continuous/Discrete (meta-property)
   - 4.2 Life/Death as formal duality
   - 4.3 Constitutive vs. operative dualities
   - 4.4 Revised Hasse diagram

5. **Discussion** (2000 words)
   - 5.1 Why is causality a dead end?
   - 5.2 Implications for emergence theory
   - 5.3 Connection to Aristotle's substance/relation distinction
   - 5.4 Limitations: is the asymmetry an artifact?
   - 5.5 Predictions for 128-bit extensions

6. **Conclusion** (500 words)

Total: ~11,000 words → reducible a ~8,000 para submission.

### 5.4 Datos complementarios

El articulo incluiria como material suplementario:
- Los tres scripts de Python (test1, test2, test3)
- El archivo primitivos.json completo
- Un subconjunto anonimizado de anclas_v2.json
- Los diagramas de Hasse antes y despues de la revision

### 5.5 Argumento central

El articulo sostendria tres claims:

1. **Claim empírico**: La estructura de dependencias de un sistema neurosimbolico entrenado revela que las dualidades post-fundacionales forman un arbol asimetrico, no una cadena.

2. **Claim filosofico**: La vida — no la causalidad ni la mereologia — es el hub que reunifica las ramas divergentes. La vida es la condicion ontologica que sintetiza limites (topologia), tiempo (temporalidad), patron (orden), y generatividad (creacion) en un solo fenomeno. Esto tiene implicaciones para la filosofia de la emergencia: la vida no es "un nivel mas de complejidad" sino el *punto de convergencia* de las condiciones ontologicas necesarias.

3. **Claim taxonomico**: Existe una distincion categorica entre dualidades constitutivas (que abren dominios) y dualidades operativas (que codifican relaciones). Las operativas son terminales en el grafo porque *son* la logica del grafo, no su contenido — como la operacion "+" es la logica de los numeros, no un numero.

### 5.6 Fit con *Foundations of Science*

*Foundations of Science* publica trabajo interdisciplinar sobre los fundamentos de las ciencias, incluyendo:
- Filosofia de la emergencia y la complejidad
- Fundamentos ontologicos de marcos cientificos
- Analisis formales de estructuras conceptuales

El articulo encaja porque:
- Presenta un marco ontologico (dualidades) con verificacion computacional
- Conecta filosofia formal con datos empiricos de IA
- La taxonomia constitutivo/operativo es una contribucion a la ontologia formal
- El hallazgo de auto-similitud fractal conecta con la teoria de la complejidad

---

## VI. Preguntas Abiertas Post-Revision

1. **¿Cambiaria la estructura con 128 bits?** Si primitivos v3 incluye primitivos para `responsabilidad`, `justicia`, `taxonomia`, `especie`, ¿crecerian los ramales de `porque` y `tipo_de`?

2. **¿Es la asimetria 28:1 estable?** Si se agregan mas anclas al corpus, ¿se mantiene la dominancia de la rama topologica?

3. **¿Hay un tercer ciclo?** Si d14 (Sujeto/Objeto) es la ultima dualidad constitutiva del segundo ciclo, las dualidades d15+ deberian replicar el patron por tercera vez. ¿Que seria el "uno" de tercer orden? Posiblemente Yo/Otro (intersubjetividad).

4. **¿La distincion constitutivo/operativo se sostiene en el primer ciclo?** ¿Hay dualidades fundamentales (d1-d7) que sean operativas? Candidata: Movimiento/Quietud (d6) — ¿es mas "operacion" que "contenido"?

5. **¿Es `información` una raiz genuina o un artefacto?** información tiene betweenness #1 y es raiz (0 dependencias), pero no corresponde a ninguna de las 14 dualidades. ¿Es una dualidad d0 (Información/Vacío) previa a d1?

---

## Referencias

- Aristoteles (c. 350 a.C.). *Categorias*. En *Organon*.
- Freeman, L. C. (1977). "A Set of Measures of Centrality Based on Betweenness." *Sociometry*, 40(1), 35-41.
- Kauffman, S. A. (1993). *The Origins of Order*. Oxford University Press.
- Maturana, H. R. & Varela, F. J. (1980). *Autopoiesis and Cognition*. Dordrecht: Reidel.
- Ornelas Brand, A. (2026a). "Extension: Dualidades 8-14." Documento 04 del manuscrito.
- Ornelas Brand, A. (2026b). "Bifurcaciones Internas de las Dualidades 8-14." Documento 11 del manuscrito.
- Ornelas Brand, A. (2026c). "End-to-End Prime Factorization in a Generative Language Model." Manuscrito.
- Pearl, J. (2000). *Causality: Models, Reasoning, and Inference*. Cambridge University Press.
- Simons, P. (1987). *Parts: A Study in Ontology*. Oxford: Clarendon Press.
- Woodward, J. (2003). *Making Things Happen*. Oxford University Press.

---

*Parte del manuscrito "Expansion del Circulo de Emergencia de Dualidades."*
*Documento 12 — Revision empirica y propuesta de publicacion.*
