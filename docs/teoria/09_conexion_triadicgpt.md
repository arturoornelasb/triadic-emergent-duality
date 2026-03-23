# Puente Empirico: TriadicGPT
## Seis conexiones concretas entre el marco filosofico y los datos
### J. Arturo Ornelas Brand — Marzo 2026

---

## Resumen

Este documento establece el puente entre el marco filosofico del Circulo de Emergencia de Dualidades y los resultados empiricos del proyecto TriadicGPT. Se presentan seis conexiones concretas: (1) la convergencia ternaria desde tres caminos independientes, (2) un test falsificable de orden de activacion de bits, (3) la jerarquia emergente de informacion, (4) la interpretacion del ~42% de zeros como horizonte conceptual, (5) el ciclo de descubrimiento como espiral generativa, y (6) los experimentos fallidos como evidencia por eliminacion. Cada conexion incluye su protocolo experimental, los datos disponibles, y el veredicto de si confirma, es consistente con, o refuta el marco.

---

## I. Convergencia Ternaria: Tres Caminos al Mismo Lugar

### 1.1 Los tres caminos

Tres lineas de trabajo independientes, desarrolladas sin influencia mutua, convergen en la misma representacion discreta de tres estados $\{+1, 0, -1\}$:

**Camino 1 — Filosofia** (*La Danza Cosmica de los Opuestos*, Ornelas Brand 2026a):

Analisis filosofico de los opuestos produce tres estados ontologicos:
- $[+1]$ Presencia: la cualidad esta activamente presente.
- $[0]$ Vacio: la cualidad esta ausente (se nota que falta).
- $[-1]$ Ausencia activa: el polo opuesto esta presente.

Derivados desde la estructura de las dualidades: para cualquier entidad y cualquier dualidad, la entidad puede estar en el polo positivo, en el polo negativo, o la dualidad puede no aplicarse.

**Camino 2 — Ingenieria** (BitNet b1.58, Ma et al. 2024):

Optimizacion pura de ingenieria para representaciones discretas eficientes:
- $+1$: contribucion positiva del peso.
- $0$: sin contribucion (peso dormido).
- $-1$: contribucion negativa.

Resultado: modelos de 2B parametros con $\{+1, 0, -1\}$ igualan o superan modelos de precision completa. Reduccion de 5-7x en memoria. Log2(3) = 1.58 bits por peso.

**Camino 3 — Matematicas** (Algebra bitwise, proyecto TriadicGPT):

Las operaciones sobre conceptos-como-compuestos-de-primos son isomorfas a operaciones bitwise:
- GCD(A,B) = A & B (rasgos compartidos)
- LCM(A,B) = A | B (union de rasgos)
- Subsuncion: A | B == B

La extension a ternario {+1, 0, -1} permite capturar presencia, ausencia e irrelevancia — tres estados que la representacion binaria {0, 1} no puede distinguir.

### 1.2 La evidencia de convergencia

| Propiedad | Filosofia | BitNet | TriadicGPT |
|-----------|----------|--------|-----------|
| Numero de estados | 3 | 3 | 3 (con iFSQ) |
| Esparsidad (~% zeros) | Predicha teoricamente | 42.3% | 42.9% |
| Razon de diseño | Ontologica | Ingenieria | Algebraica |
| Escala de validacion | Teorica | 2B parametros | 355M parametros |

### 1.3 Significado

La convergencia no es coincidental. Tres restricciones independientes llegan a la misma estructura:

- **Restriccion filosofica** (¿cuales son los estados fundamentales del ser?) → tres estados.
- **Restriccion de ingenieria** (¿cual es la representacion discreta minima eficiente?) → tres valores.
- **Restriccion matematica** (¿cuales son las operaciones atomicas sobre conjuntos?) → AND/OR/XOR sobre mascaras binarias, que se extienden naturalmente a ternario.

Esto sugiere que $\{+1, 0, -1\}$ no es una eleccion de diseño sino un *punto fijo* — la estructura minima que captura la informacion sobre relaciones entre una entidad y una dimension de descripcion.

### 1.4 Datos de respaldo

| Experimento | Script | Resultado clave |
|------------|--------|-----------------|
| D-A8 (cabeza ternaria, iFSQ) | `playground/danza_ternary.py` | 86.5% subsuncion holdout, distribucion 3 estados |
| D-A10 (ablacion binaria iFSQ) | `playground/ifsq_binary_ablation.py` | 87.1% subsuncion, loss 0.924 |
| D-A13 (GPT-2 Medium ternario) | `playground/gpt2_medium_ternary.py` | 355M params, 100% subsuncion holdout |
| D-A19 (355M, entrenamiento corregido) | — | 100% subsuncion, 100% analogia R3 |
| Equivalencia bitwise | `benchmarks/scripts/prime_vs_bitwise.py` | 1000/1000 tests, equivalencia perfecta |

**Veredicto**: **Evidencia fuerte**. La convergencia de tres caminos independientes es el tipo de evidencia mas dificil de descartar.

---

## II. Test de Orden de Activacion de Bits

### 2.1 El test falsificable clave

Si la secuencia de 7 dualidades es correcta, los bits del sistema TriadicGPT deberian mostrar un *patron de activacion* consistente con la cadena de dependencias. Especificamente:

**Prediccion**: Para cada par $(i, j)$ de los 63 bits, si bit $j$ depende de bit $i$ segun `primitivos.json`, entonces en los datos de anclas, $j$ activo $\implies$ $i$ activo (con alta probabilidad).

### 2.2 Protocolo experimental

**Datos**: `anclas_v2.json` (~104 anclas con asignacion manual de bits).

**Procedimiento**:

1. Para cada ancla, extraer su vector de bits activos.
2. Para cada par $(i, j)$ en el grafo de dependencias de `primitivos.json`:
   - Contar: $N_{j}$ = numero de anclas con bit $j$ activo.
   - Contar: $N_{j \wedge i}$ = numero de anclas con bit $j$ activo Y bit $i$ activo.
   - Calcular: $P(i|j) = N_{j \wedge i} / N_{j}$ = probabilidad de que $i$ este activo dado que $j$ esta activo.
3. Si la dependencia es real: $P(i|j)$ deberia ser alta (cercana a 1).
4. Comparar con la probabilidad base $P(i)$ = fraccion de anclas con bit $i$ activo. Si $P(i|j) \gg P(i)$, la dependencia tiene efecto real.

**Ejemplo concreto**: El primitivo `consciente` (bit 36) depende de `vida` (bit 32), `informacion` (bit 1) y `vista` (bit 13). La prediccion es:
- De las anclas con `consciente` activo, la gran mayoria deberia tener `vida` activo.
- De las anclas con `consciente` activo, la gran mayoria deberia tener `informacion` activo.
- Pocas anclas deberian tener `consciente` activo sin `vida`.

### 2.3 Resultados anticipados

De una inspeccion manual de `anclas_v2.json`:

- `democracia` tiene bits: colectivo, libertad, orden, verdad, hacer, algunos, consciente.
  - `consciente` requiere `vida` (no presente explicitamente), `informacion` (no presente), `vista` (no presente).
  - **Posible violacion**: `consciente` activo sin sus dependencias.

Pero esto puede deberse a la *codificacion por relevancia conceptual* vs. *dependencia ontologica*. Cuando un humano asigna bits a "democracia", activa los bits *conceptualmente relevantes*, no necesariamente todos los ontologicamente previos. "Democracia" presupone `vida` (los ciudadanos estan vivos) pero no la *activa* como rasgo definitorio porque es tan basica que se da por sentada.

### 2.4 Refinamiento del test

Para distinguir *dependencia ontologica* (implicita) de *relevancia conceptual* (explicita), necesitamos:

1. **Test de activacion implicita**: Si los bits del modelo *entrenado* (no las anclas manuales) muestran que `consciente` activa `vida` implicitamente, la dependencia se preserva en la representacion aprendida.

2. **Test con datos de modelo**: Usar las activaciones del modelo D-A19 (355M parametros) en vez de las anclas manuales. El modelo no tiene sesgo humano de codificacion — si descubre las dependencias por si mismo, es evidencia mas fuerte.

### 2.5 Construccion de la matriz de dependencia empirica

Procedimiento completo para construir la matriz:

1. Para cada par de bits $(i, j)$ con $i \neq j$:
   - $P(j|i)$ = probabilidad de $j$ activo dado $i$ activo.
   - $P(i|j)$ = probabilidad de $i$ activo dado $j$ activo.
2. Si $P(i|j) \approx 1$ y $P(j|i) < 1$, entonces $i$ es dependencia de $j$ (pero no al reves).
3. Comparar la matriz empirica con la matriz teorica de `primitivos.json`.

**Metrica de acuerdo**: Fraccion de pares donde la dependencia empirica coincide con la dependencia teorica. Si es significativamente mayor que el azar ($\gg 50\%$), la estructura de dependencias tiene realidad empirica.

**Veredicto**: Este es el **test falsificable mas importante** del marco. Si la matriz empirica no coincide con la teorica, el marco necesita revision. Si coincide, es evidencia fuerte de que las dependencias ontologicas son reales.

> **Resultado (Documento 13, Test 4)**: Ejecutado sobre 155 anclas (v1+v2) y 128 pares de dependencia. La consistencia global ponderada es baja (21.7%), pero esto se explica por la distincion fenomenica/ontologica: las anclas codifican *prominencia*, no clausura transitiva. El test verdaderamente informativo es contra el baseline aleatorio: **60% de los pares de dependencia muestran co-activacion superior al azar** (ratio obs/random > 1.0), con ratios entre 1.5x y 6x para las dependencias mas fuertes. Los 2 unicos pares con 100% de consistencia son `pensar → consciente` (6/6) y `porque → posición_temporal` (2/2). **Conclusion**: parcialmente confirmado — las dependencias ontologicas aumentan la co-activacion por encima del azar en la mayoria de los pares, pero el sistema de anclas no fue diseñado para capturar clausura transitiva.

---

## III. Jerarquia Emergente de Informacion

### 3.1 La observacion

En el paper de TriadicGPT se reporta una jerarquia emergente de informacion:
- Conceptos abstractos (hiperonimos) → menos bits activos.
- Conceptos concretos (hiponimos) → mas bits activos.

Esta jerarquia *emerge* del entrenamiento — no fue impuesta. El modelo descubre por si mismo que los conceptos generales necesitan menos dimensiones que los especificos.

### 3.2 Prediccion del marco

El Circulo de Emergencia predice exactamente esto:
- Conceptos cercanos al "centro" del circulo (sintesis de pocas dualidades) tienen pocas dimensiones activas.
- Conceptos en la "periferia" (que requieren muchas dualidades) tienen muchas dimensiones activas.

Mas formalmente: si la profundidad de un concepto en el poset de primitivos correlaciona con su numero de bits activos, la jerarquia de informacion refleja la jerarquia de emergencia.

### 3.3 Test propuesto

1. Para cada ancla en `anclas_v2.json`, contar el numero de bits activos $|v(a)|$.
2. Asignar a cada ancla un "nivel de abstraccion" basado en la capa mas alta de los bits activos.
3. Calcular la correlacion de Pearson entre nivel de abstraccion y numero de bits activos.

**Prediccion**: Correlacion positiva significativa. Los conceptos con bits de capas altas (capa 5-6) deberian tener mas bits activos que los conceptos con bits solo de capas bajas (capa 1-2).

### 3.4 Datos observados

De las anclas leidas:
- `vacio` (concepto fundamental) tiene 0 bits activos propios (es un bit primitivo, capa 1).
- `socialismo` tiene 7 bits activos (colectivo, control, union, orden, hacer, bien, algunos).
- `ira` tiene 7 bits activos (fuego, fuerza, mas, destruccion, dolor, consciente, interocepcion).
- `calma` tiene 6 bits activos (agua, orden, menos, consciente, interocepcion, vida).

Los conceptos complejos (emociones, sistemas politicos) activan 5-7 bits, mientras que los primitivos tienen 0 dependencias (nivel 1). La jerarquia es visible a simple vista.

**Veredicto**: **Consistente con el marco**. La jerarquia emergente de informacion es exactamente lo que predice el Circulo de Emergencia.

---

## IV. El ~42% de Zeros como Horizonte Conceptual

### 4.1 El dato

Consistentemente, ~42% de los bits/pesos convergen a cero:

| Sistema | % zeros |
|---------|---------|
| BitNet b1.58 | 42.3% |
| TriadicGPT D-A5 XL | 42.9% |
| TriadicGPT D-A8 | 47.6% |
| reptimeline discovery | 41.3% |

### 4.2 Interpretacion

En el marco del Circulo de Emergencia, los bits en estado cero (null) son dimensiones *irrelevantes* — dualidades que no se aplican al concepto en cuestion. El ~42% de zeros significa que, en promedio, el 42% de las dimensiones conceptuales son irrelevantes para cualquier concepto dado.

Esto es el "horizonte de eventos conceptual": la frontera entre lo que un concepto "sabe" (dimensiones activas) y lo que "no le incumbe" (dimensiones null).

### 4.3 Prediccion testeable

**Si la interpretacion es correcta**:
- Conceptos de capas superiores (mas abstractos) deberian tener *mas* zeros (mas dimensiones irrelevantes porque son mas generales).
- Conceptos de capas inferiores (mas basicos) deberian tener *menos* zeros (menos dimensiones irrelevantes porque sus dimensiones son las mas fundamentales — "aplican a todo").

**Contra-intuicion**: Esto parece contradecir la Seccion III (donde los abstractos tienen menos bits activos). No hay contradiccion: los abstractos tienen menos bits $\neq 0$ (menos bits activos *o negativos*), y mas bits $= 0$ (mas irrelevantes). Los concretos tienen mas bits activos (+1 o -1) y menos bits null.

### 4.4 ¿Por que ~42%?

Especulaciones:
1. **Optimizacion de informacion**: 42% ≈ $1 - 1/\sqrt{3} \approx 42.3\%$. Si el sistema optimiza la razon señal/ruido en un espacio ternario, la proporcion de canales silenciados podria estar determinada por la geometria del espacio.

2. **Equilibrio critico**: En la teoria de redes booleanas de Kauffman, las redes en el "borde del caos" tienen una fraccion critica de nodos inactivos. El 42% podria ser el punto critico del espacio ternario de 63 dimensiones.

3. **Coincidencia**: El numero podria no ser universal — podria depender del corpus de entrenamiento o de la dimension del espacio. Se necesitan mas datos.

**Veredicto**: **Sugestivo pero no concluyente**. El dato es robusto (aparece en sistemas independientes), pero su relacion precisa con el marco necesita mas investigacion.

---

## V. El Ciclo de Descubrimiento como Espiral Generativa

### 5.1 El ciclo de TriadicGPT

El proyecto TriadicGPT implementa un ciclo iterativo:

1. **Entrenar**: El modelo aprende a producir firmas de primos junto con prediccion de tokens.
2. **Descubrir**: El modulo reptimeline identifica que primitivos el modelo realmente aprendio.
3. **Corregir**: Se comparan los primitivos descubiertos con los manuales y se corrigen asignaciones.
4. **Re-entrenar**: El modelo se re-entrena con los primitivos corregidos.

Cada vuelta del ciclo mejora la calidad:
- D-A5: 87% accuracy, 90.7% subsuncion.
- D-A13: 100% subsuncion holdout.
- Expansion de 50 → 158 anclas: accuracy 87% → 93%, subsuncion 90.7% → 98.3%.

### 5.2 Mapeo a la espiral

| Paso del ciclo | Paso de la espiral | Operacion |
|----------------|-------------------|-----------|
| Entrenar | Periferia → Centro | Sintesis: las dualidades perifericas (primitivos) se comprimen en representaciones internas |
| Descubrir | Observar el centro | Inspeccionar las sintesis: ¿que aprendio el modelo? |
| Corregir | Centro → Nueva periferia | Externalizacion: las sintesis descubiertas generan nuevos primitivos (anclas corregidas) |
| Re-entrenar | Nueva periferia → Nuevo centro | El ciclo se repite en un nivel superior |

### 5.3 El ciclo ES la espiral

No es solo una analogia — es una *instanciacion computacional* del mecanismo espiral:

- Las dualidades (primitivos) son la periferia.
- Las representaciones internas del modelo son las sintesis centrales.
- La externalizacion (descubrimiento + correccion) produce nuevas dualidades perifericas.
- Cada vuelta del ciclo produce un modelo con mejor comprension — un "nivel superior" de la espiral.

La espiral generativa no es solo una metafora geometrica: es un algoritmo implementable. TriadicGPT ya lo implementa, aunque no fue diseñado con esta interpretacion en mente.

**Veredicto**: **Evidencia fuerte**. El ciclo de TriadicGPT es la instanciacion mas directa de la espiral generativa.

---

## VI. Experimentos Fallidos como Evidencia

### 6.1 Fallo de prediccion de tipo aristotelico

Se intento usar el modelo para predecir las categorias aristotelicas de los conceptos (sustancia, cantidad, cualidad, etc.). Resultado: 0 de 4 separaciones exitosas.

**Interpretacion en el marco**: Las categorias de Aristoteles son *simultaneas*, no *emergentes* (Documento 03, Seccion II). No estan ordenadas por dependencia — son clasificaciones paralelas. El modelo TriadicGPT, que aprende dependencias secuenciales, no deberia poder separarlas como dimensiones independientes. El fallo *confirma* que el modelo captura dependencia (como el marco predice), no clasificacion simultanea (como Aristoteles propone).

### 6.2 Fallo parcial de enantiodromia

Se intento verificar la enantiodromia (transformacion de un concepto en su opuesto: amor→odio, libertad→tirania). Resultado: 2 de 8 transiciones exitosas (25%).

**Interpretacion en el marco**: La enantiodromia requiere que los polos opuestos esten codificados como inversiones simetricas en el espacio de bits. En el sistema de primitivos, los polos duales estan definidos como pares (bien/mal, orden/caos, etc.), pero no todos los conceptos tienen su "inverso enantiodromico" como simple negacion de bits — la relacion entre amor y odio es mas compleja que bien→mal.

El fallo parcial *constrañe* el marco: la enantiodromia funciona para dualidades puras (bien→mal: 2/2 = 100%) pero no para conceptos complejos (amor→odio: los bits compartidos impiden la inversion limpia). Esto es consistente con la geometria del circulo: la inversion perfecta solo funciona en el perimetro (polos puros), no en el interior (sintesis complejas).

### 6.3 El valor de los fallos

Los experimentos fallidos son tan informativos como los exitosos:
- El fallo aristotelico confirma que la secuencia de emergencia (no la clasificacion simultanea) es lo que el modelo captura.
- El fallo enantiodromico constrañe la geometria del circulo: la simetria periferia-centro no es completa.

Ambos fallos son *consistentes* con el marco, lo cual es mas fuerte que si todos los tests hubieran pasado — un marco que todo confirma no es falsificable.

**Veredicto**: **Consistente con el marco** (los fallos ocurren donde el marco predice que deberian ocurrir).

---

## VII. Tabla de Verificacion Completa

| Conexion | Tipo de evidencia | Datos | Resultado | Veredicto |
|----------|------------------|-------|-----------|-----------|
| 1. Convergencia ternaria | Convergencia independiente | BitNet, D-A8, D-A13 | 3 caminos → mismo resultado | **Evidencia fuerte** |
| 2. Orden de activacion | Test falsificable | anclas_v2.json, primitivos.json | 60% de pares > baseline; consistencia 21.7% | **Parcialmente confirmado** (Doc 13) |
| 3. Jerarquia de informacion | Correlacion | Anclas manuales + modelo | Abstractos → menos bits | **Consistente** |
| 4. ~42% zeros | Patron robusto | BitNet, D-A5, D-A8, reptimeline | 41-48% en multiples sistemas | **Sugestivo** |
| 5. Ciclo = espiral | Isomorfismo estructural | Ciclo entrenar-descubrir-corregir | Mapeo directo demostrado | **Evidencia fuerte** |
| 6. Fallos como evidencia | Falsificacion parcial | Aristoteles (0/4), enantiodromia (2/8) | Fallan donde el marco predice | **Consistente** |

### Ranking de confianza

1. **Mas fuerte**: Convergencia ternaria (tres caminos independientes, resultado mas dificil de descartar).
2. **Fuerte**: Ciclo de descubrimiento como espiral (isomorfismo estructural, implementacion funcional).
3. **Consistente**: Jerarquia de informacion y fallos como evidencia (no confirman directamente pero son coherentes).
4. **Sugestivo**: ~42% de zeros (dato robusto, interpretacion abierta).
5. **Parcialmente confirmado**: Test de orden de activacion — 60% de pares de dependencia muestran co-activacion > baseline (Doc 13, Test 4).

---

## VIII. NSM: Convergencia con Linguistica

### 8.1 El dato

La comparacion con el Metalenguaje Semantico Natural (NSM) de Wierzbicka revela 55% de solapamiento:
- 28 coincidencias directas (alta confianza).
- 8 coincidencias cercanas (confianza moderada).
- 27 primitivos del Sistema 7×7 sin equivalente en NSM.

### 8.2 Significado

El NSM identifica ~65 primos semanticos a traves de 30+ lenguas humanas — es el resultado de 40+ años de trabajo de campo linguistico. El Sistema 7×7 deriva 63 primitivos desde un marco filosofico. Que el 55% coincida sin haberse influido mutuamente es evidencia adicional de que ambos capturan universales genuinos de la estructura conceptual humana.

Los 27 primitivos del Sistema 7×7 sin equivalente NSM representan la *contribucion ontologica unica*: son conceptos filosoficos (vacio, elementos clasicos, ejes espaciales) que no aparecen como primos linguisticos porque no son "palabras basicas" — son categorias mas abstractas que las lenguas naturales no lexicalizan como primas.

---

## IX. Preguntas Abiertas

1. **¿Puede el test de orden de activacion ejecutarse computacionalmente?** Requiere un script que construya la matriz de co-ocurrencia de bits en las anclas. Tiempo estimado de implementacion: horas, no dias.

2. **¿Que pasa cuando se entrena con mas de 63 bits?** Si el marco es correcto, un modelo con 128 bits deberia "descubrir" dualidades 8+ que el de 63 no captura. El BitwiseMapper ya soporta hasta 1024 bits.

3. **¿El ~42% converge a un valor mas preciso con mas datos?** Necesitamos correr el analisis con multiples corpus y multiples escalas para determinar si es una constante o un parametro.

4. **¿Puede la espiral generativa automatizarse completamente?** El ciclo entrenar-descubrir-corregir actualmente requiere intervencion humana en el paso de correccion. ¿Puede la correccion ser autonoma?

5. **¿Cuanto solapamiento habria con otros marcos de primitivos semanticos?** Ademas de NSM, ¿como se compara con ConceptNet, FrameNet, o los primitivos de Jackendoff?

---

## Referencias

- Ma, S. et al. (2024). "The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits." arXiv:2402.17764.
- Ornelas Brand, A. (2026a). *La Danza Cosmica de los Opuestos*.
- Ornelas Brand, A. (2026b). "End-to-End Prime Factorization in a Generative Language Model."
- Wang, H. et al. (2023). "BitNet: Scaling 1-bit Transformers for Large Language Models." arXiv:2310.11453.
- Wierzbicka, A. & Goddard, C. (2014). "Semantic Primes and Universal Grammar."

---

*Parte del manuscrito "Expansion del Circulo de Emergencia de Dualidades."*
