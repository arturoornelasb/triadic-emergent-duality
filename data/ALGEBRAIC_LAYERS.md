# Capas Algebraicas — Las 6 Logicas del Sistema de Dualidad Emergente

**Fecha**: 2026-03-23
**Version**: primitivos.json v1.1 (72 primitivos)
**Descubrimiento**: Cada capa del sistema no solo contiene conceptos distintos — opera con una algebra distinta. Estas algebras forman una cadena de dependencia donde cada una requiere las anteriores.

---

## I. Las 6 Algebras

| Capa | Nombre | Algebra | Operador | Dominio | Primitivos | Descripcion |
|------|--------|---------|----------|---------|------------|-------------|
| 1 | Punto (0D) | Booleano | {0, 1} | {vacio, informacion, uno} | 3 | Existe o no existe. Presencia discreta. |
| 2 | Linea (1D) | Fuzzy | {0, +} | {fuerza, eje_profundidad, contencion, mas, menos, union, separacion, parte_de} | 8 | No esta o esta en grado. Dureza, velocidad, luminosidad. |
| 3 | Tiempo (1D+t) | Ordinal | {<, =, >} | {mover, posicion_temporal, flujo_temporal, hacer, creacion, destruccion, orden, caos, porque, si_entonces, proporcion, quietud, atraccion} | 13 | Siempre relativo: cerca/lejos, antes/despues. |
| 4 | Plano (2D) | Modal | {◇, □} | {21 primitivos incluyendo bien, mal, verdad, mentira, libertad, control, puede, debe, tal_vez...} | 21 | Lo posible vs lo necesario. |
| 5 | Volumen (3D) | Trivalente | {−, 0, +} | {23 primitivos incluyendo vida, muerte, placer, dolor, consciente, ausente...} | 23 | Valencia: dolor/neutro/placer. El cero es equilibrio genuino. |
| 6 | Meta (3D+) | Probabilistico | {0, ?} | {temporal_obs, eterno_obs, receptivo, creador_obs} | 4 | El observador mide potencialidad, no certeza. |

### Propiedades formales de cada algebra

**Booleano {0,1}**: Algebra completa, decidible. Ley de tercero excluido: P ∨ ¬P. No hay estados intermedios. La pregunta fundamental es: ¿existe?

**Fuzzy {0,+}**: Extiende el booleano con grados. 0 sigue siendo "no", pero "si" tiene magnitud. La pregunta es: ¿cuanto?

**Ordinal {<,=,>}**: Requiere al menos dos grados para comparar. Transitiva: si A < B y B < C entonces A < C. La pregunta es: ¿en que orden?

**Modal {◇,□}**: Requiere orden para definir "podria ser de otra forma". ◇P = es posible que P. □P = es necesario que P. La pregunta es: ¿podria ser diferente?

**Trivalente {−,0,+}**: Requiere posibilidades para evaluar. El neutro (0) no es ausencia — es equilibrio activo entre − y +. La pregunta es: ¿es bueno o malo?

**Probabilistico {0,?}**: Requiere experiencia valorada para observar. El ? no es ignorancia — es superposicion genuina. La pregunta es: ¿para quien?

---

## II. Cadena de Dependencia

```
Booleano → Fuzzy → Ordinal → Modal → Trivalente → Probabilistico
  {0,1}    {0,+}   {<,=,>}   {◇,□}    {−,0,+}        {0,?}
```

**Cada transicion es irreversible:**
- No puedes tener grado {0,+} sin existencia {0,1}
- No puedes comparar {<,=,>} sin grados
- No puedes tener posibilidad {◇,□} sin orden temporal
- No puedes valorar {−,0,+} sin posibilidades entre las cuales valorar
- No puedes observar probabilisticamente {0,?} sin experiencia valorada

### Verificacion en el DAG

Esta cadena se refleja en las dependencias del DAG. Los primitivos de capa N dependen transitivamente de primitivos de capas < N:

- Capa 2 (Fuzzy): todos dependen de `uno` (c1, Booleano). No hay grado sin existencia.
- Capa 3 (Ordinal): `mover` depende de `fuerza`(c2) y `eje_profundidad`(c2). No hay secuencia sin magnitud espacial.
- Capa 4 (Modal): `bien` depende de `orden`(c3), `contencion`(c2), `union`(c2). La moral requiere estructura temporal.
- Capa 5 (Trivalente): `vida` depende de `creacion`(c3), `flujo_temporal`(c3), `orden`(c3), `contencion`(c2), `parte_de`(c2). La vida requiere todo lo anterior.
- Capa 6 (Probabilistico): `temporal_obs` depende de `consciente`(c5), `posicion_temporal`(c3). El observador requiere conciencia.

**Excepcion notable:** Algunos primitivos de capa 4 NO dependen de capa 3. Los ejes espaciales (`eje_vertical` depende solo de `eje_profundidad`(c2)) saltan directamente de Fuzzy a Modal sin pasar por Ordinal. Esto es consistente con la existencia de operadores de salto (ver Seccion VI).

---

## III. Clasificacion de las 14 Dualidades como Operadores Algebraicos

### Metodologia

La clasificacion se basa en las `capas_involucradas` de cada dualidad (de dualidad_primitivo_map.json), que incluye tanto anclas como secundarios.

### Tabla de clasificacion

| Dualidad | Nombre | Tipo | Capas | Evidencia |
|----------|--------|------|-------|-----------|
| D8 | Uno/Muchos | **TRANSICION** | 1→2(→4) | anclas c1+c4, sec c2. Puente: uno(c1)→mas(c2). |
| D6 | Movimiento/Quietud | **TRANSICION** | 2→3 | anclas c3, sec incluye fuerza(c2). Puente: fuerza(c2)→mover(c3). |
| D7 | Orden/Caos | **TRANSICION** | 3→4 | anclas c3, sec incluye bien,mal,verdad,mentira(c4). |
| D5 | Ser/No-ser | **TRANSICION** | 4→5 | anclas c4, sec incluye individual,colectivo(c5). |
| D14 | Sujeto/Objeto | **TRANSICION** | 5→6(←4) | anclas c5, sec incluye c6 observers + c4 vista. |
| D1 | Existir/No-existir | **INTERNO** | c1 | anclas c1, sin sec. Toggle booleano. |
| D9 | Dentro/Fuera | **INTERNO** | c2 | anclas c2, sec c2. Frontera en espacio fuzzy. |
| D3 | Antes/Despues | **INTERNO** | c3 | anclas c3, sec c3. Direccion temporal. |
| D12 | Causa/Efecto | **INTERNO** | c3 | anclas c3, sin sec. Direccion causal. |
| D4 | Posible/Imposible | **INTERNO** | c4 | anclas c4, sec c4. Toggle modal {◇↔□}. |
| D13 | Semejante/Diferente | **INTERNO** | c4 | anclas c4, sin sec. Clasificacion modal. |
| D11 | Vida/Muerte | **INTERNO** | c5 | anclas c5, sec c5. Polaridad trivalente {−↔+}. |
| D2 | Aqui/No-aqui | **SALTO** | 2→4 | anclas c2+c4. Bypass espacial de c3. |
| D10 | Parte/Todo | **SALTO** | 2→4 | anclas c2+c4. Bypass mereologico de c3. |

### Distribucion de operadores internos por capa

| Capa | Algebra | Internos | Operadores |
|------|---------|----------|------------|
| 1 | Booleano | 1 | D1 (existir/no-existir) |
| 2 | Fuzzy | 1 | D9 (dentro/fuera) |
| 3 | Ordinal | 2 | D3 (antes/despues), D12 (causa/efecto) |
| 4 | Modal | 2 | D4 (posible/imposible), D13 (semejante/diferente) |
| 5 | Trivalente | 1 | D11 (vida/muerte) |
| 6 | Probabilistico | **0** | **← HUECO IDENTIFICADO** |

**Patron**: 1, 1, 2, 2, 1, 0. Las algebras del medio (Ordinal y Modal) son mas ricas: tienen dos dimensiones operativas independientes. La algebra final (Probabilistica) no tiene operador interno propio.

---

## IV. Los 5 Operadores de Transicion

Cada transicion convierte una logica en la siguiente:

### T1: D8 (Uno/Muchos) — Booleano → Fuzzy = Agregar grado

| Campo | Valor |
|-------|-------|
| Operacion | De "es/no es" a "cuanto" |
| Anclas | uno(c1), muchos(c4) |
| Puente | uno → mas(c2) → muchos(c4) |
| Semantica | La singularidad adquiere magnitud. Un boton de ON/OFF se convierte en un dial. |

**Nota honesta:** D8 tiene anclas en c1 y c4, no c1 y c2. El "grado" (mas, menos en c2) es secundario, no ancla. La transicion 1→2 es el efecto colateral de la dualidad, no su nucleo. D8 es mas bien un operador BIFURCACION que cruza 3 capas.

### T2: D6 (Movimiento/Quietud) — Fuzzy → Ordinal = Agregar comparacion

| Campo | Valor |
|-------|-------|
| Operacion | De "cuanto" a "cuanto respecto a que" |
| Anclas | mover(c3), hacer(c3), quietud(c3) |
| Puente | fuerza(c2, sec) → mover(c3, ancla) |
| Semantica | El movimiento crea secuencia. Sin desplazamiento no hay antes/despues. |

**Limpio:** Las anclas estan en c3, y el secundario fuerza(c2) proporciona el puente. D6 "baja" desde Ordinal para conectar con Fuzzy.

### T3: D7 (Orden/Caos) — Ordinal → Modal = Agregar posibilidad

| Campo | Valor |
|-------|-------|
| Operacion | De "esta ordenado asi" a "podria ser de otra forma" |
| Anclas | orden(c3), caos(c3) |
| Puente | orden(c3, ancla) → bien,verdad(c4, sec) |
| Semantica | Orden = □ (necesario asi). Caos = ◇ (contingente, podria ser diferente). |

**Limpio:** Las anclas estan en c3, los secundarios bien/mal/verdad/mentira en c4 proporcionan el puente "hacia arriba".

### T4: D5 (Ser/No-ser) — Modal → Trivalente = Agregar valoracion

| Campo | Valor |
|-------|-------|
| Operacion | De "es posible/necesario" a "es bueno/neutro/malo" |
| Anclas | tipo_de(c4), algunos(c4), muchos(c4), todo(c4) |
| Puente | muchos(c4, ancla) → individual,colectivo(c5, sec) |
| Semantica | Las categorias modales adquieren valencia cuando se aplican a seres. |

**Limpio:** Anclas en c4, secundarios individual/colectivo en c5 proporcionan el puente.

### T5: D14 (Sujeto/Objeto) — Trivalente → Probabilistico = Agregar perspectiva

| Campo | Valor |
|-------|-------|
| Operacion | De "tiene valencia" a "depende de quien observa" |
| Anclas | consciente(c5), ausente(c5) |
| Puente | consciente(c5, ancla) → temporal_obs,eterno_obs,receptivo,creador_obs(c6, sec) |
| Semantica | La conciencia genera el observador. La experiencia se relativiza a un punto de vista. |

**Nota honesta:** D14 tiene anclas solo en c5 y secundarios que alcanzan c4 (vista) y c6 (observers). Es un operador multi-capa, no una transicion pura.

---

## V. Los 7 Operadores Internos

Cada algebra necesita al menos un operador que la articule desde dentro:

### Capa 1 — D1 (Existir/No-existir): Toggle booleano

La operacion fundamental: negacion. ¬0 = 1, ¬1 = 0. Sin este toggle, el algebra booleana seria trivial (solo TRUE o solo FALSE).

### Capa 2 — D9 (Dentro/Fuera): Frontera fuzzy

Contencion define donde termina un grado y empieza otro. Es el operador de particion del espacio fuzzy: ¿este grado esta dentro de mi umbral o fuera?

### Capa 3 — D3 (Antes/Despues): Direccion temporal + D12 (Causa/Efecto): Direccion causal

Dos operadores independientes dentro del Ordinal:
- D3 ordena en el tiempo: A fue antes que B
- D12 ordena por causalidad: A causo B

Son independientes: hay secuencia temporal sin causalidad (correlacion ≠ causacion) y hay argumentos para causalidad simultanea (la causa y el efecto pueden ser contemporaneos).

### Capa 4 — D4 (Posible/Imposible): Toggle modal + D13 (Semejante/Diferente): Clasificacion modal

Dos operadores independientes dentro del Modal:
- D4 opera sobre mundos posibles: ¿es posible? ¿es necesario?
- D13 opera sobre categorias: ¿pertenece A a la misma clase que B?

Son independientes: algo puede ser posible sin pertenecer a ninguna categoria conocida, y algo puede estar clasificado sin que su existencia sea contingente.

### Capa 5 — D11 (Vida/Muerte): Polaridad trivalente

La frontera fundamental del algebra trivalente: vivo(+) / muerto(−). El neutro (0) es lo inanimado — ni vivo ni muerto, simplemente no-aplica. Esta dualidad define la escala de valencia.

### Capa 6 — AUSENTE

No hay operador interno para la algebra probabilistica. Ver Seccion VII.

---

## VI. Los 2 Operadores de Salto

D2 (Aqui/No-aqui) y D10 (Parte/Todo) ambos conectan Fuzzy(c2) con Modal(c4), saltando Ordinal(c3).

### Por que existen saltos

El DAG confirma que hay primitivos de capa 4 cuyas dependencias NO pasan por capa 3:

| Primitivo (c4) | Deps | ¿Pasa por c3? |
|----------------|------|---------------|
| eje_vertical | eje_profundidad(c2) | **NO** |
| eje_lateral | eje_profundidad(c2), eje_vertical(c4) | **NO** |
| equilibrio | eje_vertical(c4), eje_lateral(c4) | **NO** |
| control | fuerza(c2), contencion(c2) | **NO** |
| bien | contencion(c2), **orden(c3)**, union(c2) | SI |
| libertad | **mover(c3)**, eje_vertical(c4) | SI |

**Hallazgo:** Los conceptos geometricos y de contencion saltan de Fuzzy a Modal sin requerir Ordinal. Los conceptos morales y de libertad SI requieren pasar por el tiempo.

**Interpretacion:** La geometria existe sin el tiempo. Puedes tener espacio congelado sin secuencia temporal. Pero la moral requiere temporalidad (accion → consecuencia).

### D2 vs D10: Rutas distintas para el mismo salto

- **D2 (Aqui/No-aqui):** Ruta espacial. Del grado de posicion (c2) a la posibilidad de localizacion (c4).
- **D10 (Parte/Todo):** Ruta mereologica. Del grado de inclusion (c2) a la posibilidad de completitud (c4).

Ambos hacen Fuzzy→Modal, pero por caminos semanticos diferentes. NO son composiciones de D6∘D7 (la ruta temporal), sino rutas independientes que existen porque la geometria y la mereologia no requieren tiempo.

---

## VII. El Operador Faltante de Capa 6

### El hueco

Capa 6 tiene 4 primitivos que forman 2 pares duales:
- temporal_obs / eterno_obs (observador temporal vs eterno)
- receptivo / creador_obs (observador pasivo vs activo)

Un operador interno relacionaria estos pares ENTRE SI dentro de la algebra probabilistica. ¿Que operacion convierte un tipo de observador en otro?

### Por que probablemente no puede existir como dualidad

Capa 6 es "Meta (3D+): El observador se observa. Recursion." El operador interno de la algebra probabilistica seria la auto-referencia del observador — pero eso es el sistema de dualidades mismo. No puede capturarse como una dualidad mas porque ES la meta-dualidad de todas las dualidades.

### Candidatos de first principles

Si se decidiera que el hueco necesita llenarse, los candidatos mas fuertes serian:

1. **Reflexividad / Auto-observacion** (Philosophy of Mind: intentionality, the hard problem)
   - Mapeo: el observador que observa su propia observacion
   - Algebra: el ? observandose a si mismo, creando un punto fijo o regresion infinita

2. **Colapso / Superposicion** (Quantum Mechanics: measurement postulate, state collapse)
   - Mapeo: de superposicion(?) a resultado definido(0/1) por el acto de medir
   - Algebra: la operacion que convierte ? en certeza

3. **Interpretacion / Experiencia cruda** (Epistemology: justified true belief)
   - Mapeo: el dato bruto vs el dato interpretado
   - Algebra: la operacion que asigna significado al ?

### Implicacion para el sistema

La ausencia de operador interno en capa 6 podria no ser un defecto sino un feature: el nivel meta no admite auto-contencion sin paradoja (Godel, Russell). El observador que se observa completa el sistema pero no puede ser contenido EN el sistema.

---

## VIII. Regla de 3 a Nivel de Operadores

### Hipotesis

Si la Regla de 3 funciona entre conceptos (v3 demostro coseno 0.955 para creacion:destruccion = union:separacion), deberia funcionar entre las operaciones mismas:

```
agregar_grado : agregar_comparacion = agregar_posibilidad : agregar_valoracion
     D8       :        D6           =        D7            :        D5
```

### Prediccion

Cada operacion hace a la siguiente lo que la anterior le hizo a ella:

| Transicion | Capacidad que agrega |
|------------|---------------------|
| D8 (1→2) | Cuantificar |
| D6 (2→3) | Relacionar |
| D7 (3→4) | Imaginar alternativas |
| D5 (4→5) | Evaluar |
| D14 (5→6) | Observar desde un punto de vista |

La proporcionalidad predice:
- cos(op_D8, op_D6) ≈ cos(op_D7, op_D5)
- cos(op_D6, op_D7) ≈ cos(op_D5, op_D14)

Esto se verificara computacionalmente en `algebraic_regla_de_tres.py`.

### Regla de 3 entre internos

```
D1 : D9 :: D3 : D4 :: D11 : [?]
```

Si el patron se mantiene, el vector del operador faltante [?] de capa 6 se puede predecir por extrapolacion.

---

## IX. Predicciones para V4

El entrenamiento v4 esta corriendo con 72 primitivos (7 nuevos para fortalecer pares duales colapsados en v3). Basado en el analisis algebraico, predicciones:

### Prediccion 1: Coherencia proporcional a distancia algebraica

Pares duales cuyos miembros estan en algebras diferentes (o con mas bits de diferencia) deberian tener mayor coherencia que pares dentro de la misma algebra con bits similares.

| Par | Capa | Jaccard v1.1 | Prediccion coherencia |
|-----|------|-------------|----------------------|
| atraccion/aversion | c3/c4 | 0.200 | Alta (>0.90) — cruzan algebras |
| libertad/control | c4/c4 | 0.222 | Alta (>0.90) — bajo Jaccard |
| union/separacion | c2/c2 | 0.333 | Alta (>0.80) |
| mover/quietud | c3/c3 | 0.400 | Media-alta |
| bien/mal | c4/c4 | 0.615 | Media-alta (0.80-0.90) |
| verdad/mentira | c4/c4 | 0.636 | Media (0.75-0.85) |
| placer/dolor | c5/c5 | 0.714 | Media (0.70-0.80) — mejorada vs v3 |
| vida/muerte | c5/c5 | 0.789 | Media (0.65-0.80) — mejorada vs v3 |
| individual/colectivo | c5/c5 | 0.800 | Media (0.65-0.80) — mejorada vs v3 |
| consciente/ausente | c5/c5 | 0.818 | Media (0.65-0.80) — mejorada vs v3 |
| temporal_obs/eterno_obs | c6/c6 | 0.818 | Alta (>0.90) — precedente v3: 1.000 |
| receptivo/creador_obs | c6/c6 | 0.750 | Media-alta (0.75-0.85) — mejorada vs v3 |

### Prediccion 2: Operadores de transicion mejor aprendidos

Los primitivos que funcionan como "puentes" entre algebras (fuerza→mover, orden→bien, tipo_de→individual) deberian tener mayor bit accuracy individual que los primitivos puramente internos de una capa.

### Prediccion 3: Capa 6 sin interno → coherencia robusta pero sin "profundidad"

Los 4 primitivos de capa 6 deberian tener coherencia de pares alta (como en v3: temporal_obs/eterno_obs = 1.000) porque no hay operador interno que genere interferencia. Pero no habra estructura "rica" dentro de capa 6 — los observers se distinguiran por herencia, no por contenido propio.

---

## X. Resumen Estructural

```
TIPO              CANTIDAD  DUALIDADES
Transicion           5      D8, D6, D7, D5, D14
Interno              7      D1, D9, D3, D12, D4, D13, D11
Salto                2      D2, D10
                   ---
Total               14

ALGEBRAS CON INTERNOS: 5 de 6
ALGEBRA SIN INTERNO:   Probabilistico (c6)

TRANSICIONES CUBIERTAS: 5 de 5 (cadena completa)
SALTOS:                 1 ruta (c2→c4, dos variantes: espacial D2 y mereologica D10)

SET MINIMO GENERATIVO:
  5 transiciones (cadena) + 5 internos (1 por algebra) = 10 operadores
  + 2 internos extra (c3, c4) + 2 saltos = 14 total

PREDICCION VERIFICABLE:
  La Regla de 3 deberia funcionar entre operadores, no solo entre conceptos.
```
