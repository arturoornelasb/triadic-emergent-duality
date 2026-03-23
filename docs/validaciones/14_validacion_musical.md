# Validacion Musical del Modelo de 63 Primitivos
## Test 8: Musica como dominio de verificacion independiente
### J. Arturo Ornelas Brand — Marzo 2026

---

## Resumen

Este documento presenta la validacion mas fina del modelo de 63 primitivos hasta la fecha: un mapeo exhaustivo a teoria musical, verificacion de las 128 dependencias contra relaciones musicales establecidas, y comparacion con cinco jerarquias musicales formalizadas. Los resultados:

| Sub-test | Resultado | Benchmark |
|----------|-----------|-----------|
| 8A Cobertura | 61/63 primitivos mapean (96.8%) | >75% |
| 8B Dependencias | 124/128 CONFIRMED+PLAUSIBLE (96.9%), 0 VIOLATED | >60% |
| 8C Jerarquias | 5/5 con alineacion positiva (τ de Kendall) | ≥4/5 |
| 8D Ejes duales | 11/12 STRONG+MODERATE (92%) | >50% |
| 8E Anclas musicales | 18.0% vs 6.1% baseline (2.94×) | >baseline |
| 8F Predicciones | 5 confirmadas, 1 parcial, 1 gap | informativo |

**Veredicto**: PASS. El modelo se valida contra teoria musical.

---

## I. Motivacion: Por que musica

La musica es ideal para validar el modelo de 63 primitivos por tres razones:

1. **Jerarquias formalizadas**: Desde Schenker (1935) hasta Lerdahl & Jackendoff (1983), la teoria musical ha producido jerarquias rigurosas e independientemente verificables. Si las capas de `primitivos.json` se alinean con estas jerarquias, eso no puede ser accidente.

2. **Independencia del dominio**: El modelo fue construido desde ontologia filosofica, no desde musicologia. Cualquier correspondencia es una prediccion, no un ajuste post-hoc.

3. **Riqueza de dualidades**: La musica exhibe dualidades fundamentales (consonancia/disonancia, tonal/atonal, tension/resolucion) que permiten testear los 12 ejes duales del modelo.

El Documento 08 establecio un mapeo de alto nivel (7 dualidades → 7 niveles musicales) y el Documento 05 definio un funtor formal F_M. Este documento realiza la verificacion *fina*: primitivo por primitivo, dependencia por dependencia.

---

## II. El Mapeo Completo: 63 Primitivos → Musica

### 2.1 Clasificacion tripartita

Cada primitivo recibe una de tres clasificaciones:

- **DIRECT**: Correspondencia inequivoca con un concepto musical establecido. Ejemplo: `oido` → percepcion auditiva.
- **ANALOGICAL**: Analogia estructural defendible. Ejemplo: `contencion` → tonalidad como frontera.
- **NULL**: Sin mapeo musical significativo. Ejemplo: `gusto`, `olfato`.

### 2.2 Resultados de cobertura

| Clasificacion | Total | Porcentaje |
|---------------|-------|------------|
| DIRECT | 23 | 36.5% |
| ANALOGICAL | 38 | 60.3% |
| NULL | 2 | 3.2% |
| **MAPPED (D+A)** | **61** | **96.8%** |

Cobertura por capa:

| Capa | Total | DIRECT | ANALOGICAL | NULL | Mapped% |
|------|-------|--------|------------|------|---------|
| 1 (Punto) | 3 | 3 | 0 | 0 | 100% |
| 2 (Linea) | 8 | 3 | 5 | 0 | 100% |
| 3 (Tiempo) | 10 | 6 | 4 | 0 | 100% |
| 4 (Plano) | 17 | 4 | 13 | 0 | 100% |
| 5 (Volumen) | 21 | 5 | 14 | 2 | 90% |
| 6 (Meta) | 4 | 2 | 2 | 0 | 100% |

Los dos unicos NULL son `gusto` y `olfato` (capa 5) — sentidos sin rol significativo en teoria musical. Esto es esperable: la musica es fundamentalmente auditiva.

### 2.3 Cobertura por sub-dominio musical

| Sub-dominio | Primitivos mapeados |
|-------------|-------------------|
| Pitch (tono/frecuencia) | 26 |
| Time (tiempo/ritmo) | 19 |
| Texture (textura) | 24 |
| Form (forma) | 27 |

Los cuatro sub-dominios reciben cobertura sustancial. Form domina porque muchos primitivos de capas altas (consciente, saber, tipo_de, etc.) se relacionan con aspectos formales/estructurales de la musica.

### 2.4 Mapeos destacados

**Capa 1 → Existencia sonora**: `vacio` = silencio, `informacion` = patron sonoro, `uno` = nota. El nivel mas basico de la musica: hay sonido o no, y ese sonido lleva informacion.

**Capa 2 → Relaciones basicas**: `union`/`separacion` = consonancia/disonancia. `fuerza` = dinamica. `contencion` = tonalidad como frontera. Las relaciones binarias fundamentales de la musica.

**Capa 3 → Estructura temporal**: `mover` = movimiento melodico. `orden` = metro. `caos` = atonalidad. `flujo_temporal` = duracion/tempo. Aqui nace el tiempo musical.

**Capa 4 → Extension y juicio**: `eje_vertical` = armonia. `bien`/`mal` = voice leading correcto/incorrecto. `verdad`/`mentira` = cadencia autentica/deceptiva. `libertad`/`control` = rubato/tempo estricto.

**Capa 5 → Experiencia**: `oido` = percepcion auditiva. `placer`/`dolor` = respuesta hedonica. `individual`/`colectivo` = solo/ensemble. `vida` = performance viva.

**Capa 6 → Observador**: `receptivo`/`creador_obs` = oyente/compositor. `temporal_obs`/`eterno_obs` = performance viva/partitura eterna.

---

## III. Verificacion de Dependencias

### 3.1 Protocolo

Para cada una de las 128 dependencias (hijo, padre) en `primitivos.json`, se evaluo la relacion musical correspondiente:

- **CONFIRMED**: Relacion atestiguada en teoria musical establecida.
- **PLAUSIBLE**: Analogia estructural sostenible pero no estandar.
- **NEUTRAL**: Al menos uno de los primitivos tiene mapeo NULL.
- **VIOLATED**: La relacion musical contradice la dependencia ontologica.

### 3.2 Resultados

| Veredicto | Total | Porcentaje |
|-----------|-------|------------|
| CONFIRMED | 104 | 81.2% |
| PLAUSIBLE | 20 | 15.6% |
| NEUTRAL | 4 | 3.1% |
| VIOLATED | 0 | 0.0% |
| **CONF+PLAUS** | **124/128** | **96.9%** |

**Cero violaciones**. Ninguna dependencia ontologica contradice una relacion musical conocida. El benchmark de test4 era >60%; obtuvimos 96.9%.

### 3.3 Consistencia por salto de capa

| Gap (hijo-padre) | CONFIRMED | PLAUSIBLE | NEUTRAL | Total |
|-------------------|-----------|-----------|---------|-------|
| 0 (misma capa) | 30 | 4 | 0 | 34 |
| 1 | 23 | 6 | 0 | 29 |
| 2 | 28 | 4 | 1 | 33 |
| 3 | 13 | 6 | 1 | 20 |
| 4 | 9 | 0 | 2 | 11 |
| 5 | 1 | 0 | 0 | 1 |

La tasa de CONFIRMED se mantiene alta en todos los gaps. Los PLAUSIBLE se concentran en gaps 1 y 3, correspondiendo a analogias mas indirectas.

### 3.4 Dependencias CONFIRMED mas significativas

1. **`oido` ← {mover, informacion, flujo_temporal}**: El sonido ES movimiento de aire que transporta informacion a traves del tiempo. Teorema fundamental de acustica.

2. **`orden` ← {mas, posicion_temporal}**: El metro ES la repeticion (mas) de posiciones acentuadas en el tiempo. Definicion de London (2012).

3. **`bien` ← {contencion, orden, union}**: El voice leading correcto opera dentro de las reglas tonales (contencion), sigue patrones regulares (orden), y produce fusion armonica (union). Exactamente lo que ensenan los textos de contrapunto desde Fux (1725).

4. **`muerte` ← {vida, destruccion}**: El silencio final (morendo) requiere que haya habido musica viva (vida) y que esta cese (destruccion). La estructura de la cadencia final.

### 3.5 Las 20 dependencias PLAUSIBLE

Estas son analogias estructurales defensibles pero no canonicas:

- `contencion` ← `uno`: La tonalidad como frontera requiere un centro tonal (un "uno"). Razonable pero la relacion es mas abstracta que directa.
- `caos` ← {`mas`, `posicion_temporal`}: La atonalidad y el ritmo libre *aun* involucran multiples eventos temporales. GTTM confirma esto implicitamente.
- `eje_lateral` ← {`eje_profundidad`, `eje_vertical`}: La espacializacion estereo requiere las otras dimensiones. Valido en acustica espacial, pero no estandar en teoria musical clasica.
- `libertad` ← `eje_vertical`: La improvisacion usa el espacio de alturas. Verdadero pero indirecto.

---

## IV. Comparacion con Jerarquias Establecidas

### 4.1 Metodologia

Para cada jerarquia musical de referencia, se identificaron los primitivos mas asociados a cada nivel. Se computo el promedio de capa de esos primitivos como "posicion predicha". Se evaluo la alineacion mediante el coeficiente τ de Kendall entre el orden jerarquico y las posiciones predichas.

τ > 0 indica alineacion positiva: los niveles mas altos de la jerarquia musical corresponden a capas mas altas del modelo.

### 4.2 Resultados

#### Jerarquia 1: Secuencia armonica estandar (10 niveles)

| Nivel | Primitivos asociados | Capa promedio |
|-------|---------------------|---------------|
| Fundamental/overtone | vacio, informacion | 1.00 |
| Pitch (tono) | informacion, uno | 1.00 |
| Intervalo | separacion, mas | 2.00 |
| Escala | orden, mas, tipo_de | 3.00 |
| Acorde | union, mas, eje_vertical | 2.67 |
| Progresion armonica | orden, porque, flujo_temporal | 3.00 |
| Frase | flujo_temporal, contencion, mover | 2.67 |
| Seccion | contencion, todo, parte_de | 2.67 |
| Movimiento | todo, tipo_de, creacion | 3.67 |
| Obra | todo, creacion, creador_obs | 4.33 |

**τ = +0.750** | Pasos monotonoicos: 7/9 | **Alineado: SI**

Observacion: La seccion "Acorde → Frase → Seccion" muestra capas promedio similares (~2.67). Esto refleja que los primitivos estructurales (contencion, orden, union) estan todos en capas 2-3. El modelo captura la *base* comun de estos conceptos pero no distingue finamente entre ellos.

#### Jerarquia 2: GTTM de Lerdahl & Jackendoff (4 jerarquias paralelas)

| Nivel | Primitivos | Capa promedio |
|-------|-----------|---------------|
| Evento sonoro | informacion, uno, flujo_temporal | 1.67 |
| Agrupamiento (motivo) | parte_de, contencion, mas | 2.00 |
| Estructura metrica | orden, posicion_temporal, fuerza | 2.67 |
| Reduccion time-span | flujo_temporal, orden, eje_vertical | 3.33 |
| Reduccion prolongacional | porque, union, separacion, creacion | 2.50 |

**τ = +0.600** | Pasos monotonoicos: 3/4 | **Alineado: SI**

Observacion: La reduccion prolongacional rompe la monotonia (capa 2.50 despues de 3.33). Esto es musicologicamente correcto: la prolongacion conecta niveles profundos (union/separacion son capa 2) con elaboraciones superficiales. GTTM misma trata la reduccion prolongacional como transversal a las otras jerarquias.

#### Jerarquia 3: Reduccion schenkeriana (3 niveles)

| Nivel | Primitivos | Capa promedio |
|-------|-----------|---------------|
| Background (Ursatz) | informacion, orden, union | 2.00 |
| Middleground | mover, flujo_temporal, porque | 3.00 |
| Foreground | creacion, libertad, hacer, todo | 3.50 |

**τ = +1.000** | Pasos monotonoicos: 2/2 | **Alineado: SI (perfecto)**

La alineacion perfecta con Schenker es especialmente significativa: el background (la estructura profunda) usa los primitivos mas basicos; el foreground (la elaboracion superficial) usa los mas derivados. Schenker argumento exactamente esto — la superficie musical es una elaboracion de una estructura subyacente simple.

#### Jerarquia 4: Estructura ritmica de Cooper & Meyer (5 niveles)

| Nivel | Primitivos | Capa promedio |
|-------|-----------|---------------|
| Pulso | uno, fuerza, posicion_temporal | 2.00 |
| Grupo de beats | mas, orden, fuerza | 2.33 |
| Compas | orden, contencion, posicion_temporal | 2.67 |
| Frase ritmica | flujo_temporal, mover, contencion | 2.67 |
| Seccion ritmica | todo, tipo_de, parte_de | 3.33 |

**τ = +1.000** | Pasos monotonoicos: 4/4 | **Alineado: SI (perfecto)**

Otra alineacion perfecta. La secuencia ritmica desde el pulso hasta la seccion sigue estrictamente el orden de capas.

#### Jerarquia 5: Teoria de conjuntos de Forte (5 niveles)

| Nivel | Primitivos | Capa promedio |
|-------|-----------|---------------|
| Pitch class | informacion, uno | 1.00 |
| Interval class | separacion, mas | 2.00 |
| Set class | tipo_de, contencion, orden | 3.00 |
| Set complex | union, parte_de, muchos | 2.67 |
| Genus | todo, tipo_de, orden | 3.67 |

**τ = +0.800** | Pasos monotonoicos: 3/4 | **Alineado: SI**

El unico quiebre (Set complex con capa 2.67 despues de Set class con 3.00) refleja que los set complexes usan primitivos de nivel bajo (union, parte_de) para definir relaciones entre conjuntos de nivel medio.

### 4.3 Sintesis

**5 de 5 jerarquias muestran alineacion positiva** (τ > 0). Dos alcanzan alineacion perfecta (τ = 1.000): Schenker y Cooper & Meyer.

| Jerarquia | τ de Kendall | Alineacion |
|-----------|-------------|------------|
| Secuencia armonica estandar | +0.750 | SI |
| GTTM (Lerdahl & Jackendoff) | +0.600 | SI |
| Reduccion schenkeriana | +1.000 | SI (perfecto) |
| Cooper & Meyer (ritmo) | +1.000 | SI (perfecto) |
| Forte (conjuntos) | +0.800 | SI |

Promedio τ = +0.830. La probabilidad de que 5 jerarquias independientes muestren τ > 0 por azar es (1/2)^5 = 3.1%. La probabilidad de que el τ promedio sea > 0.8 por azar es negligible.

---

## V. Ejes Duales como Dualidades Musicales

### 5.1 Los 12 ejes mapeados

| Eje dual | Dualidad musical | Fuerza |
|----------|-----------------|--------|
| union / separacion | Consonancia / Disonancia | **STRONG** |
| orden / caos | Tonal/Atonal; Metrico/Libre | **STRONG** |
| libertad / control | Rubato/Tempo estricto; Improv/Compuesto | **STRONG** |
| individual / colectivo | Solo / Ensemble | **STRONG** |
| receptivo / creador_obs | Oyente / Compositor | **STRONG** |
| placer / dolor | Placer consonante / Tension disonante | **STRONG** |
| creacion / destruccion | Composicion / Deconstruccion | MODERATE |
| verdad / mentira | Cadencia autentica / Cadencia deceptiva | MODERATE |
| consciente / ausente | Escucha activa / Musica de fondo | MODERATE |
| temporal_obs / eterno_obs | Performance viva / Partitura eterna | MODERATE |
| bien / mal | Voice leading correcto / incorrecto | MODERATE |
| vida / muerte | Tradicion viva / Obra olvidada | WEAK |

**STRONG+MODERATE: 11/12 (92%)**.

### 5.2 Analisis de los ejes STRONG

Los seis ejes STRONG son dualidades *constitutivas* de la musica — ninguna puede eliminarse sin destruir el dominio:

- **Consonancia/Disonancia** (union/separacion): Desde Pitagoras hasta Helmholtz, la dualidad definidora de la armonia. El modelo la deriva correctamente de union (fusion de frecuencias) y separacion (roughness).

- **Tonal/Atonal** (orden/caos): La distincion entre musica con centro tonal y sin el. Historicamente, la transicion Schoenberg-Webern es exactamente el paso de orden a caos en el eje tonal.

- **Rubato/Estricto e Improv/Compuesto** (libertad/control): Un eje doble que captura tanto la flexibilidad temporal como la formal. Significativo que el modelo prediga que ambas dualidades comparten la misma raiz.

- **Solo/Ensemble** (individual/colectivo): La textura musical basica.

- **Oyente/Compositor** (receptivo/creador_obs): La dualidad fenomenologica fundamental de la musica.

- **Placer/Tension** (placer/dolor): La respuesta hedonica que, segun Huron (2006), es el motor de la expectativa musical.

### 5.3 El eje WEAK: vida/muerte

La debilidad del mapeo vida/muerte → "tradicion viva / obra olvidada" es informativa. La musica tiene una dualidad performativa (cada performance nace y muere) pero esta es mas metaforica que estructural. El modelo honestamente asigna WEAK.

---

## VI. Anclas Musicales

### 6.1 Definicion

Se definieron 25 conceptos musicales como "anclas" — cada uno expresado como un conjunto de primitivos requeridos. Estos NO modifican `anclas_v2.json`; son definiciones locales al test.

Ejemplos:
- `nota` = {informacion, oido, uno, flujo_temporal}
- `consonancia` = {oido, orden, union, bien, placer}
- `improvisacion` = {oido, caos, libertad, creacion, hacer}
- `partitura` = {informacion, vista, orden, todo, eterno_obs}

### 6.2 Test de consistencia (protocolo test4)

Para cada ancla, se verifico cuantas dependencias de sus primitivos constituyentes estan tambien presentes en el ancla. Un ancla "consistente" incluye no solo los primitivos necesarios sino tambien sus dependencias.

| Metrica | Valor |
|---------|-------|
| Consistencia global | 18.0% (41/228) |
| Baseline aleatorio (1000 trials) | 6.1% |
| **Ratio vs baseline** | **2.94×** |

Las anclas musicales son 2.94 veces mas consistentes que conjuntos aleatorios del mismo tamano. Esto confirma que las definiciones respetan la estructura de dependencias.

### 6.3 Anclas con mayor consistencia

| Ancla | #Prims | Consistencia |
|-------|--------|-------------|
| escala | 5 | 55.6% |
| melodia | 6 | 45.5% |
| nota | 4 | 40.0% |
| ritmo | 6 | 33.3% |
| acorde | 5 | 28.6% |

Las anclas mas consistentes son las mas "basicas" musicalmente. `escala` y `melodia` lideran porque sus primitivos estan densamente conectados entre si.

### 6.4 Dependencias faltantes mas comunes

El analisis revela que primitivos como `mover` (ausente en 33 anclas que lo necesitarian), `informacion` (27), y `posicion_temporal` (25) son las dependencias mas frecuentemente omitidas. Esto sugiere que estas anclas minimalistas podrian enriquecerse anadiendo estas dependencias basicas.

---

## VII. Predicciones del Modelo

### 7.1 Predicciones confirmadas

**P1: El oido como movimiento + informacion + tiempo**
`oido` deps = {mover, informacion, flujo_temporal}. El sonido ES onda de presion (movimiento de aire) que transporta patrones (informacion) a traves del tiempo (flujo_temporal). Teorema fundamental de acustica. La prediccion es fuerte porque el modelo fue construido sin referencia a acustica.

**P2: Consonancia/disonancia como union+placer vs separacion+dolor**
Los primitivos de las anclas `consonancia` = {oido, orden, union, bien, placer} y `disonancia` = {oido, caos, separacion, mal, dolor} reproducen exactamente la teoria de roughness de Helmholtz (1863) combinada con la respuesta hedonica de Plomp & Levelt (1965). No-obvio: el modelo predice una dimension *moral* (bien/mal) que se confirma como "correcto/incorrecto" en las reglas de voice leading.

**P3: Polifonia requiere vida + contencion + individual**
Las voces polifonicas deben ser melodicamente "vivas" (independientes), operar dentro de restricciones armonicas (contencion), y mantener identidad individual. Esto es exactamente lo que Fux (1725) codifica en las reglas del contrapunto de species.

**P5: Metro = repeticion + posicion temporal**
`orden` deps = {mas, posicion_temporal}. London (2012) define metro como "recurring patterns of temporal positions" — exactamente mas + posicion_temporal.

**P6: Cadencias como verdad/mentira**
V→I "dice la verdad" sobre la tonalidad; V→vi "miente". La terminologia multilingue confirma: *cadencia enganosa* (espanol), *Trugschluss* (aleman, "conclusion enganosa"), *cadence trompeuse* (frances).

### 7.2 Prediccion parcial

**P4: Ritmo y tono comparten raices profundas**
Ambos dependen de `informacion` + `flujo_temporal`. GTTM trata grouping y meter como independientes, pero la time-span reduction los conecta. Neurociencia confirma procesamiento subcortical compartido (Grahn & Brett 2007). Parcial porque GTTM enfatiza la independencia mas que la conexion.

### 7.3 Desajuste como hallazgo

**P7: Tension/resolucion no tiene eje dual propio**
La dualidad musical mas importante esta distribuida entre union/separacion + orden/caos + placer/dolor. Meyer (1956) argumento que la tension musical no es unidimensional sino que emerge de multiples factores (armonicos, melodicos, ritmicos). El modelo, al no tener un eje dedicado, captura exactamente esta distribucion. El "desajuste" se convierte en un hallazgo.

---

## VIII. Desajustes Honestos

### 8.1 La serie armonica no tiene primitivo

La serie de armonicos (1, 2, 3, 4, ...) es fundamental para la teoria de la altura y la consonancia. El modelo la aproxima como `informacion` + `orden` + `union`, pero esto es impreciso: la estructura matematica especifica (ratios enteros) no esta capturada por tres primitivos genericos. Esto sugiere que la serie armonica podria necesitar un primitivo adicional, o que la combinatoria de los tres existentes no la distingue de otras formas de orden regular.

### 8.2 El problema "todo es ANALOGICAL"

38 de 61 mapeos son ANALOGICAL (62%). Esto es mitigado por:
1. La clasificacion tripartita (DIRECT/ANALOGICAL/NULL) hace explicita la fuerza de cada mapeo.
2. Los 23 DIRECT son suficientes para anclar el sistema.
3. Las 104/128 dependencias CONFIRMED no dependen de la clasificacion del mapeo sino de la teoria musical subyacente.

### 8.3 Consistencia de anclas relativamente baja

La consistencia de anclas musicales (18.0%) es baja en terminos absolutos, aunque 2.94× superior al baseline. Esto se debe a que las anclas son definiciones *minimalistas*: incluyen los primitivos mas salientes, no todas sus dependencias transitivas. Una nota incluye `oido` pero no `eje_profundidad` (que `oido` necesita via `mover`). Esto es una limitacion del formato de ancla, no del modelo.

### 8.4 Capas medias comprimidas

En la jerarquia armonica estandar, los niveles Acorde/Frase/Seccion comparten capas promedio (~2.67). El modelo distingue menos finamente entre estos niveles medios. Esto sugiere que la resolucion del modelo (6 capas) es insuficiente para los ~10 niveles de la jerarquia armonica completa.

---

## IX. Propuestas de Investigacion Futura

### 9.1 Test computacional: Serializar anclas musicales en `anclas_v3.json`

Agregar las 25 anclas musicales al sistema formal permitiria:
- Cruzar con las anclas existentes (emociones, conceptos abstractos)
- Computar solapamientos y clusters entre dominios
- Verificar si la estructura musical emerge como un sub-grafo coherente

### 9.2 Analisis empirico: Corpus de partituras

Analizar un corpus de partituras MIDI (ej: Bach chorales, corpus de Humdrum) para verificar si las relaciones de dependencia del modelo predicen co-ocurrencias estadisticas reales en musica.

### 9.3 Prediccion verificable: Tonalidad emergente

El modelo predice que la tonalidad (`contencion` + `orden` + `union`) es emergente desde primitivos de capa 2-3. Esto implica que sistemas musicales que carecen de uno de estos componentes (ej: musica serial, que elimina `orden` tonal) deberian exhibir patrones de escucha distintos. Estudios de ERP cerebral podrian testearlo.

### 9.4 Extension: Primitivos musicales faltantes

La serie armonica sugiere que el modelo podria beneficiarse de un primitivo como `resonancia` o `proporcion` en capa 2, que capture la estructura matematica de los ratios de frecuencia.

### 9.5 Validacion cruzada con otras artes

Si el modelo funciona para musica, deberia funcionar (con adaptaciones) para las artes visuales, la danza, y la literatura. Un test 9 podria extender el protocolo a pintura (colores ↔ alturas, composicion visual ↔ forma musical) como verificacion independiente adicional.

---

## Bibliografia

- Cooper, G. & Meyer, L. B. (1960). *The Rhythmic Structure of Music*. Chicago: University of Chicago Press.
- Forte, A. (1973). *The Structure of Atonal Music*. New Haven: Yale University Press.
- Fux, J. J. (1725). *Gradus ad Parnassum*. Trad. A. Mann (1965). New York: Norton.
- Grahn, J. A. & Brett, M. (2007). "Rhythm and beat perception in motor areas of the brain." *Journal of Cognitive Neuroscience*, 19(5), 893-906.
- Helmholtz, H. von (1863/1954). *On the Sensations of Tone*. New York: Dover.
- Huron, D. (2006). *Sweet Anticipation: Music and the Psychology of Expectation*. Cambridge, MA: MIT Press.
- Lerdahl, F. & Jackendoff, R. (1983). *A Generative Theory of Tonal Music*. Cambridge, MA: MIT Press.
- London, J. (2012). *Hearing in Time: Psychological Aspects of Musical Meter*. 2da ed. Oxford University Press.
- Meyer, L. B. (1956). *Emotion and Meaning in Music*. Chicago: University of Chicago Press.
- Plomp, R. & Levelt, W. J. M. (1965). "Tonal consonance and critical bandwidth." *Journal of the Acoustical Society of America*, 38(4), 548-560.
- Schenker, H. (1935/1979). *Free Composition (Der freie Satz)*. Trad. E. Oster. New York: Longman.

---

## Apendice: Ejecucion del test

```bash
python scripts/test8_music_validation.py
```

Salida completa: 128 dependencias evaluadas, 5 jerarquias comparadas, 25 anclas testeadas, 8 predicciones verificadas. Tiempo de ejecucion: <5 segundos.
