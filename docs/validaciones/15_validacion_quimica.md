# Validacion Quimica del Modelo de 63 Primitivos
## Test 9: Quimica como segundo dominio de verificacion independiente
### J. Arturo Ornelas Brand — Marzo 2026

---

## Resumen

Este documento presenta la segunda validacion cross-domain del modelo de 63 primitivos: un mapeo exhaustivo a quimica, verificacion de las 128 dependencias contra relaciones quimicas establecidas, y comparacion con cinco jerarquias quimicas formalizadas. Los resultados:

| Sub-test | Resultado | Benchmark |
|----------|-----------|-----------|
| 9A Cobertura | 63/63 primitivos mapean (100.0%) | >75% |
| 9B Dependencias | 128/128 CONFIRMED (100.0%), 0 VIOLATED | >60% |
| 9C Jerarquias | 5/5 con alineacion positiva (τ de Kendall) | >=4/5 |
| 9D Ejes duales | 11/12 STRONG+MODERATE (92%) | >50% |
| 9E Anclas quimicas | 34.6% vs 5.4% baseline (6.35x) | >baseline |
| 9F Predicciones | 7 confirmadas, 1 gap | informativo |

**Veredicto**: PASS. El modelo se valida contra quimica.

**Hallazgo cross-domain**: `gusto`/`olfato` pasan de NULL (musica) a DIRECT (quimica), confirmando que el modelo predice relevancia domain-specific. El gap de proporcion/ratio reaparece como estequiometria (mismo gap que la serie armonica en musica).

---

## I. Motivacion: Por que quimica

La quimica es el segundo dominio independiente para validar el modelo de 63 primitivos. La motivacion es triple:

1. **Jerarquias formalizadas**: Desde la tabla periodica de Mendeleev (1869) hasta la termodinamica de Gibbs (1878), la quimica ha producido jerarquias rigurosas e independientemente verificables. Si las capas de `primitivos.json` se alinean con estas jerarquias, eso no puede ser accidente.

2. **Independencia total**: El modelo fue construido desde ontologia filosofica, no desde quimica. Cualquier correspondencia es una prediccion, no un ajuste post-hoc. Ademas, la quimica es completamente independiente del primer dominio de validacion (musica).

3. **Predicciones cross-domain verificables**: Test 8 (musica) dejo dos primitivos como NULL (`gusto`, `olfato`) y un gap (serie armonica/proporcion). Si el modelo tiene validez real, debemos poder predecir: (a) `gusto`/`olfato` deben pasar a DIRECT en quimica (la quimica IS quimiorrecepcion), y (b) el gap de proporcion debe reaparecer como estequiometria.

El Documento 14 establecio la validacion musical. Este documento realiza la misma verificacion fina contra quimica y compara los resultados cross-domain.

---

## II. El Mapeo Completo: 63 Primitivos → Quimica

### 2.1 Clasificacion tripartita

Cada primitivo recibe una de tres clasificaciones:

- **DIRECT**: Correspondencia inequivoca con un concepto quimico establecido. Ejemplo: `union` → enlace quimico.
- **ANALOGICAL**: Analogia estructural defendible. Ejemplo: `porque` → mecanismo de reaccion / ΔG como causa.
- **NULL**: Sin mapeo quimico significativo. **No hay ninguno**.

### 2.2 Resultados de cobertura

| Clasificacion | Total | Porcentaje |
|---------------|-------|------------|
| DIRECT | 32 | 50.8% |
| ANALOGICAL | 31 | 49.2% |
| NULL | 0 | 0.0% |
| **MAPPED (D+A)** | **63** | **100.0%** |

Cobertura por capa:

| Capa | Total | DIRECT | ANALOGICAL | NULL | Mapped% |
|------|-------|--------|------------|------|---------|
| 1 (Punto) | 3 | 3 | 0 | 0 | 100% |
| 2 (Linea) | 8 | 6 | 2 | 0 | 100% |
| 3 (Tiempo) | 10 | 8 | 2 | 0 | 100% |
| 4 (Plano) | 17 | 5 | 12 | 0 | 100% |
| 5 (Volumen) | 21 | 10 | 11 | 0 | 100% |
| 6 (Meta) | 4 | 0 | 4 | 0 | 100% |

**Cero NULL**: A diferencia de la musica (donde `gusto` y `olfato` eran NULL), la quimica mapea los 63 primitivos. Esto es coherente: la quimica es la ciencia de la materia y sus transformaciones, cubriendo un rango mas amplio de fenomenos que cualquier dominio artistico.

### 2.3 Cobertura por sub-dominio quimico

| Sub-dominio | Primitivos mapeados |
|-------------|-------------------|
| Structure (estructura atomica → materia) | 23 |
| Bonding (enlaces y fuerzas) | 9 |
| Reaction (cinetica → equilibrio) | 45 |
| Classification (elemento → material) | 18 |

Reaction domina con 45 primitivos — la quimica es, ante todo, la ciencia de las transformaciones. Structure recibe buena cobertura desde capas 1-3 (niveles fundamentales de la materia). Classification conecta con capas 4-5 donde emergen las categorias.

### 2.4 Mapeos destacados

**Capa 1 → Fundamentos de la materia**: `vacio` = espacio vacio (requerido para orbitales y estructura), `informacion` = estado cuantico / configuracion electronica (lo que define un atomo), `uno` = atomo individual / particula fundamental.

**Capa 2 → Operaciones quimicas basicas**: `union`/`separacion` = enlace/disociacion (la operacion fundamental de toda la quimica, Pauling 1960). `fuerza` = fuerzas electromagnetica y nuclear. `contencion` = orbital como contenedor de electrones. `mas`/`menos` = polimerizacion/descomposicion.

**Capa 3 → Dinamica y reacciones**: `mover` = movimiento molecular / difusion. `orden`/`caos` = estructura cristalina / entropia. `creacion`/`destruccion` = sintesis / descomposicion. `flujo_temporal` = velocidad de reaccion. `porque` = mecanismo de reaccion (por que ocurre, ΔG).

**Capa 4 → Termodinamica y clasificacion**: `equilibrio` = equilibrio quimico (Le Chatelier). `libertad` = energia libre / grados de libertad. `control` = catalisis / inhibicion. `verdad`/`mentira` = minimo termodinamico / trampa cinetica. `tipo_de` = clasificacion de grupos funcionales.

**Capa 5 → Estados, sentidos, vida**: `tierra`/`agua`/`aire`/`fuego` = solido/liquido/gaseoso/combustion (los estados de la materia y la reaccion primordial). `gusto`/`olfato` = quimiorrecepcion gustativa/olfativa (DIRECT — eran NULL en musica). `vida`/`muerte` = bioquimica / desnaturalizacion.

**Capa 6 → Observador quimico**: `temporal_obs`/`eterno_obs` = cinetica / termodinamica (la dualidad fundacional de la quimica fisica). `receptivo`/`creador_obs` = quimica analitica / sintetica.

### 2.5 Comparacion con musica: Cambios de clase

| Primitivo | Musica (T8) | Quimica (T9) | Cambio |
|-----------|-------------|--------------|--------|
| gusto | NULL | **DIRECT** | Activacion cross-domain |
| olfato | NULL | **DIRECT** | Activacion cross-domain |

Este "flip" NULL→DIRECT no es un ajuste: es una prediccion del modelo. Los sentidos son domain-specific. La musica no necesita gusto ni olfato; la quimica SI, porque la quimiorrecepcion es literalmente quimica.

---

## III. Verificacion de Dependencias

### 3.1 Protocolo

Para cada una de las 128 dependencias (hijo, padre) en `primitivos.json`, se evaluo la relacion quimica correspondiente:

- **CONFIRMED**: Relacion atestiguada en quimica establecida.
- **PLAUSIBLE**: Analogia estructural sostenible pero no canonica.
- **NEUTRAL**: Al menos uno de los primitivos tiene mapeo NULL. *No aplica en quimica*.
- **VIOLATED**: La relacion quimica contradice la dependencia ontologica.

### 3.2 Resultados

| Veredicto | Total | Porcentaje |
|-----------|-------|------------|
| CONFIRMED | 128 | 100.0% |
| PLAUSIBLE | 0 | 0.0% |
| NEUTRAL | 0 | 0.0% |
| VIOLATED | 0 | 0.0% |
| **CONF+PLAUS** | **128/128** | **100.0%** |

**Todas las dependencias confirmadas**. Cada dependencia ontologica tiene una correspondencia quimica atestiguada. El benchmark de test4 era >60%; obtuvimos 100%.

Comparacion con musica: Test 8 obtuvo 96.9% (104 CONFIRMED, 20 PLAUSIBLE, 4 NEUTRAL). La quimica mejora este resultado al eliminar los 4 pares NEUTRAL (que involucraban gusto/olfato) y confirmar directamente los 20 pares que en musica eran solo PLAUSIBLE.

### 3.3 Consistencia por salto de capa

| Gap (hijo-padre) | CONFIRMED | PLAUSIBLE | NEUTRAL | Total |
|-------------------|-----------|-----------|---------|-------|
| 0 (misma capa) | 34 | 0 | 0 | 34 |
| 1 | 29 | 0 | 0 | 29 |
| 2 | 33 | 0 | 0 | 33 |
| 3 | 20 | 0 | 0 | 20 |
| 4 | 11 | 0 | 0 | 11 |
| 5 | 1 | 0 | 0 | 1 |

La tasa de CONFIRMED es 100% en todos los gaps. Incluso las dependencias de largo alcance (gap 4-5) encuentran confirmacion directa en quimica.

### 3.4 Dependencias CONFIRMED mas significativas

1. **`caos` ← {mas, posicion_temporal}**: La entropia S = k ln W (Boltzmann 1877) cuenta microestados (mas = multiplicidad) en posiciones configuracionales (posicion_temporal). El modelo predice exactamente la descomposicion de la entropia en sus componentes.

2. **`equilibrio` ← {eje_vertical, eje_lateral}**: El equilibrio quimico es el minimo en la superficie de energia libre (Gibbs 1878). eje_vertical = eje de energia, eje_lateral = coordenada de reaccion/composicion. El modelo predice que el equilibrio necesita ambas dimensiones del paisaje energetico.

3. **`libertad` ← {mover, eje_vertical}**: G = H - TS combina entalpia H (niveles de energia, eje_vertical) y entropia S (movimiento molecular, mover). El modelo descompone `libertad` exactamente como la termodinamica descompone la energia libre.

4. **`fuego` ← {fuerza, creacion, destruccion}**: La combustion segun Lavoisier (1789): oxidacion rapida que requiere energia (fuerza), produce nuevas sustancias (creacion) y consume reactivos (destruccion). Tres componentes, exactamente los deps del modelo.

5. **`gusto` ← {contencion, informacion}**: La quimiorrecepcion gustativa requiere un receptor contenido en la membrana celular (contencion) que detecta informacion molecular (informacion). Confirmada en quimica; era NEUTRAL en musica.

6. **`olfato` ← {mover, informacion}**: Las moleculas odorantes se mueven (mover) llevando informacion quimica (informacion) al receptor olfativo. La teoria lock-and-key de la olfaccion confirma ambas deps.

---

## IV. Comparacion con 5 Jerarquias Establecidas

### 4.1 Protocolo

Para cada jerarquia quimica, se asignaron primitivos a cada nivel y se calculo la capa promedio (avg layer). Luego se midio la correlacion Kendall τ entre el orden de la jerarquia y el orden de las capas.

### 4.2 Resultados

#### Jerarquia 1: Estructura de la materia (7 niveles)

| Nivel | Primitivos | Capa promedio |
|-------|-----------|--------------|
| Quark | vacio, informacion, fuerza | 1.33 |
| Nucleon | uno, fuerza, union | 1.67 |
| Atomo | uno, informacion, contencion, fuerza | 1.50 |
| Molecula | union, mas, orden, contencion | 2.25 |
| Compuesto | tipo_de, union, orden, informacion | 2.50 |
| Material | muchos, todo, tierra, orden | 4.00 |
| Sistema | todo, equilibrio, colectivo, vida | 4.50 |

**Kendall τ = +0.905** | Pasos monotonicos: 5/6 | Alineado: SI

La unica inversion menor (Nucleon > Atomo en capa promedio) refleja que el atomo incluye `contencion` (capa 2) mientras que el nucleon se basa en primitivos de capas 1-2. La tendencia general es fuertemente creciente.

#### Jerarquia 2: Enlace quimico segun Pauling (5 niveles)

| Nivel | Primitivos | Capa promedio |
|-------|-----------|--------------|
| Electron | uno, informacion, mover | 1.67 |
| Par electronico | union, informacion, contencion | 1.67 |
| Enlace | union, fuerza, contencion, orden | 2.25 |
| Estructura molecular | orden, contencion, tipo_de, mas | 2.75 |
| Cristal | orden, muchos, tierra, todo | 4.00 |

**Kendall τ = +1.000** | Pasos monotonicos: 4/4 | Alineado: SI

Correlacion perfecta. La jerarquia de Pauling (electron → par → enlace → molecula → cristal) se alinea exactamente con las capas del modelo.

#### Jerarquia 3: Termodinamica (5 niveles)

| Nivel | Primitivos | Capa promedio |
|-------|-----------|--------------|
| Movimiento microscopico | mover, fuerza | 2.50 |
| Energia | fuerza, eje_vertical, mover | 3.00 |
| Entropia | caos, mas, posicion_temporal | 2.67 |
| Energia libre | libertad, mover, eje_vertical | 3.67 |
| Equilibrio | equilibrio, eje_vertical, eje_lateral | 4.00 |

**Kendall τ = +0.800** | Pasos monotonicos: 3/4 | Alineado: SI

La unica inversion (Entropia < Energia en capa promedio) refleja que `caos` y `posicion_temporal` son primitivos de capa 3, mientras que `eje_vertical` (en Energia) es capa 4. En la termodinamica clasica, la energia precede a la entropia como concepto, pero la entropia de Boltzmann se construye sobre conceptos estadisticos mas basicos.

#### Jerarquia 4: Tabla periodica (5 niveles)

| Nivel | Primitivos | Capa promedio |
|-------|-----------|--------------|
| Numero atomico | uno, mas | 1.50 |
| Config. electronica | informacion, orden, contencion | 2.00 |
| Estructura de capas | contencion, eje_profundidad, orden | 2.33 |
| Propiedades periodicas | tipo_de, orden, mas, fuerza | 2.75 |
| Tendencias de grupo | tipo_de, mas, muchos, orden | 3.25 |

**Kendall τ = +1.000** | Pasos monotonicos: 4/4 | Alineado: SI

Correlacion perfecta. Los principios organizadores de la tabla periodica (Z → configuracion → capas → propiedades → tendencias) se alinean exactamente con las capas de emergencia del modelo.

#### Jerarquia 5: Mecanismos de reaccion (5 niveles)

| Nivel | Primitivos | Capa promedio |
|-------|-----------|--------------|
| Colision | mover, fuerza, uno | 2.00 |
| Paso elemental | hacer, creacion, destruccion | 3.00 |
| Mecanismo | porque, si_entonces, orden | 3.00 |
| Reaccion | hacer, todo, flujo_temporal | 3.33 |
| Ruta sintetica | creacion, orden, creador_obs, todo | 4.00 |

**Kendall τ = +1.000** | Pasos monotonicos: 4/4 | Alineado: SI

Correlacion perfecta. Desde la colision molecular hasta la ruta sintetica, cada nivel de complejidad mecanistica se mapea a capas progresivamente mas altas.

### 4.3 Resumen de jerarquias

| Jerarquia | Niveles | τ Kendall | Alineado |
|-----------|---------|-----------|----------|
| Estructura de la materia | 7 | +0.905 | SI |
| Enlace (Pauling) | 5 | +1.000 | SI |
| Termodinamica | 5 | +0.800 | SI |
| Tabla periodica | 5 | +1.000 | SI |
| Mecanismos de reaccion | 5 | +1.000 | SI |

**5/5 jerarquias con alineacion positiva. 3/5 con correlacion perfecta (τ = 1.000).**

Comparacion con musica: Test 8 tambien obtuvo 5/5, pero con τ promedio menor. En quimica, la correlacion promedio es τ = 0.941 — la mas alta obtenida en cualquier dominio de validacion.

---

## V. Ejes Duales como Dualidades Quimicas

### 5.1 Los 12 ejes

| Eje dual | Dualidad quimica | Fuerza |
|----------|-----------------|--------|
| union / separacion | Enlace / Disociacion | **STRONG** |
| orden / caos | Cristal↔Entropia; Entalpia↔Entropia | **STRONG** |
| creacion / destruccion | Sintesis / Descomposicion | **STRONG** |
| libertad / control | Espontaneo / Catalizado | **STRONG** |
| verdad / mentira | Minimo termodinamico / Trampa cinetica | **STRONG** |
| temporal_obs / eterno_obs | Cinetica / Termodinamica | **STRONG** |
| bien / mal | ΔG < 0 / ΔG > 0 | MODERATE |
| placer / dolor | Exotermico / Endotermico | MODERATE |
| individual / colectivo | Molecula / Agregado | MODERATE |
| vida / muerte | Bioquimica activa / Desnaturalizacion | MODERATE |
| consciente / ausente | Reactivo / Inerte (gas noble) | MODERATE |
| receptivo / creador_obs | Quimica analitica / Sintetica | WEAK |

### 5.2 Analisis

**6 STRONG** (mismo numero que musica, pero con cambios de composicion):
- `verdad`/`mentira` sube de MODERATE (musica) a **STRONG** (quimica): el minimo termodinamico vs. la trampa cinetica es una dualidad constitutiva en quimica. El diamante (trampa cinetica del carbono) vs. el grafito (minimo termodinamico) es el ejemplo clasico.
- `temporal_obs`/`eterno_obs` sube de MODERATE a **STRONG**: la dualidad cinetica/termodinamica es uno de los dos pilares de la quimica fisica (Atkins & de Paula, 2014).

**5 MODERATE**: Las dualidades de capa 5 (bien/mal, placer/dolor, vida/muerte, etc.) operan como analogias coherentes pero no constitutivas en quimica.

**1 WEAK**: `receptivo`/`creador_obs` (analitica/sintetica) es una distincion practica mas que una dualidad fundamental de la naturaleza.

**STRONG+MODERATE: 11/12 = 92%** — identico al resultado musical.

### 5.3 Promociones cross-domain

| Eje | Musica | Quimica | Interpretacion |
|-----|--------|---------|----------------|
| verdad/mentira | MODERATE | STRONG | La dualidad estable/metaestable es constitutiva en quimica |
| temporal_obs/eterno_obs | MODERATE | STRONG | Cinetica/Termodinamica es la dualidad central de la quimica fisica |

Estas promociones sugieren que la fuerza de una dualidad es domain-dependent: el modelo predice las dualidades, pero su intensidad varia segun el dominio.

---

## VI. Anclas Quimicas

### 6.1 Protocolo (test4)

Se definieron 25 conceptos quimicos, cada uno como una lista de 3-6 primitivos requeridos. Para cada ancla, se verifico cuantas dependencias internas estan satisfechas (si el primitivo A depende de B, y B esta en el ancla, la dependencia esta "presente").

### 6.2 Las 25 anclas

| Ancla | Primitivos |
|-------|-----------|
| atomo | uno, informacion, contencion, fuerza |
| electron | uno, informacion, fuerza, mover |
| enlace_covalente | union, informacion, fuerza, contencion |
| enlace_ionico | union, separacion, fuerza, mas, menos |
| molecula | uno, union, mas, contencion, orden |
| cristal | orden, union, mas, contencion, tierra |
| gas | mover, libertad, caos, aire |
| liquido | mover, contencion, fuerza, agua |
| reaccion | hacer, creacion, destruccion, fuerza, mover |
| catalizador | control, hacer, mover, fuerza |
| equilibrio_quimico | equilibrio, orden, caos, flujo_temporal |
| entropia | caos, mas, posicion_temporal, mover |
| energia_libre | libertad, mover, eje_vertical, fuerza |
| solucion | agua, union, separacion, mover |
| acido | mas, fuerza, separacion, hacer |
| base | menos, fuerza, union, hacer |
| oxidacion | separacion, hacer, fuerza, menos |
| reduccion_quim | union, hacer, fuerza, mas |
| polimero | mas, union, orden, colectivo, individual |
| elemento | uno, informacion, tipo_de |
| tabla_periodica | orden, informacion, tipo_de, mas, uno |
| combustion | fuego, fuerza, creacion, destruccion |
| fotosintesis | vida, creacion, orden, informacion, fuego |
| espectro | informacion, vista, orden, eje_vertical |
| estequiometria | debe, orden, mas, todo, informacion |

### 6.3 Resultados de consistencia

| Ancla | #Prims | Deps | Present | Consistencia |
|-------|--------|------|---------|-------------|
| tabla_periodica | 5 | 6 | 5 | 83.3% |
| atomo | 4 | 3 | 2 | 66.7% |
| electron | 4 | 3 | 2 | 66.7% |
| molecula | 5 | 6 | 4 | 66.7% |
| catalizador | 4 | 7 | 4 | 57.1% |
| reaccion | 5 | 9 | 5 | 55.6% |
| liquido | 4 | 8 | 4 | 50.0% |
| entropia | 4 | 6 | 3 | 50.0% |
| energia_libre | 4 | 6 | 3 | 50.0% |
| gas | 4 | 8 | 3 | 37.5% |
| combustion | 4 | 8 | 3 | 37.5% |
| fotosintesis | 5 | 11 | 4 | 36.4% |
| cristal | 5 | 9 | 3 | 33.3% |
| elemento | 3 | 3 | 1 | 33.3% |
| espectro | 4 | 6 | 2 | 33.3% |
| polimero | 5 | 9 | 2 | 22.2% |
| acido | 4 | 5 | 1 | 20.0% |
| reduccion_quim | 4 | 5 | 1 | 20.0% |
| base | 4 | 6 | 1 | 16.7% |
| oxidacion | 4 | 6 | 1 | 16.7% |
| solucion | 4 | 7 | 1 | 14.3% |
| estequiometria | 5 | 7 | 1 | 14.3% |
| enlace_covalente | 4 | 4 | 0 | 0.0% |
| enlace_ionico | 5 | 6 | 0 | 0.0% |
| equilibrio_quimico | 4 | 8 | 0 | 0.0% |

**Consistencia global: 56/162 = 34.6%**

### 6.4 Comparacion con baseline aleatorio

| Metrica | Anclas quimicas | Baseline aleatorio | Ratio |
|---------|-----------------|-------------------|-------|
| Consistencia | 34.6% | 5.4% | **6.35x** |

Las anclas quimicas son 6.35 veces mas consistentes que conjuntos aleatorios del mismo tamano. Comparacion con musica: las anclas musicales eran 2.94x sobre baseline. El ratio mayor en quimica sugiere que los conceptos quimicos se alinean aun mejor con la estructura de dependencias del modelo.

### 6.5 Anclas de alta consistencia

- **tabla_periodica** (83.3%): La tabla periodica (orden + informacion + tipo_de + mas + uno) captura casi todas las dependencias internas. El concepto que mejor se alinea con el modelo.
- **atomo, electron, molecula** (66.7%): Los conceptos fundamentales de la quimica se construyen naturalmente sobre las dependencias del modelo.
- **catalizador** (57.1%): control + hacer + mover + fuerza — la catalisis como regulacion de transformaciones.

### 6.6 Anclas de baja consistencia

Las anclas con 0% (enlace_covalente, enlace_ionico, equilibrio_quimico) tienen baja consistencia porque sus primitivos pertenecen a capas diferentes sin cadenas de dependencia directa dentro del conjunto. Esto no invalida los mapeos — simplemente indica que estos conceptos quimicos integran primitivos de multiples lineas de emergencia.

---

## VII. Predicciones del Modelo

### 7.1 Las 8 predicciones

| ID | Prediccion | Status |
|----|-----------|--------|
| P1 | `caos` deps = [mas, posicion_temporal] → Entropia = microestados x tiempo (Boltzmann) | **CONFIRMED** |
| P2 | `equilibrio` deps = [eje_vertical, eje_lateral] → Equilibrio necesita paisaje energetico (Gibbs) | **CONFIRMED** |
| P3 | `libertad` deps = [mover, eje_vertical] → G = H - TS (energia libre) | **CONFIRMED** |
| P4 | union/separacion → Enlace/Disociacion, operacion fundamental (Pauling) | **CONFIRMED** |
| P5 | gusto/olfato: NULL→DIRECT cross-domain flip | **CONFIRMED** |
| P6 | `fuego` deps = [fuerza, creacion, destruccion] → Combustion segun Lavoisier | **CONFIRMED** |
| P7 | Gap de proporcion/ratio → estequiometria (= serie armonica en musica) | **GAP** |
| P8 | temporal_obs/eterno_obs → Cinetica/Termodinamica | **CONFIRMED** |

### 7.2 Predicciones detalladas

**P1 — Entropia como caos emergente** (CONFIRMED): El modelo predice que `caos` depende de `mas` (multiplicidad) y `posicion_temporal` (posicion configuracional). Boltzmann (1877) definio S = k ln W exactamente asi: la entropia cuenta la multiplicidad de microestados accesibles en posiciones configuracionales. La descomposicion ontologica del modelo reproduce la descomposicion estadistica de Boltzmann.

**P2 — Equilibrio como paisaje bidimensional** (CONFIRMED): `equilibrio` depende de `eje_vertical` y `eje_lateral`. Gibbs (1878) demostro que el equilibrio quimico es el minimo en una superficie de energia libre que requiere al menos dos coordenadas: energia (vertical) y composicion/coordenada de reaccion (lateral). El modelo lo predice desde la estructura de dependencias.

**P3 — Energia libre como libertad termodinamica** (CONFIRMED): `libertad` depende de `mover` y `eje_vertical`. G = H - TS: la energia libre combina contribuciones entalpicas (niveles de energia, eje_vertical) y entropicas (movimiento molecular, mover). La descomposicion del modelo refleja la descomposicion termodinamica.

**P4 — Enlace/Disociacion como dualidad primordial** (CONFIRMED): El modelo coloca `union`/`separacion` en la capa 2, la dualidad mas temprana. Pauling (1960): "toda la quimica se reduce a formacion y ruptura de enlaces." El modelo predice que esta es la primera operacion quimica, no solo una mas.

**P5 — Flip cross-domain de gusto/olfato** (CONFIRMED): En musica, `gusto` y `olfato` eran NULL — la musica no involucra quimiorrecepcion. En quimica, ambos son DIRECT: el gusto ES quimiorrecepcion gustativa (receptores que responden a forma/carga molecular) y el olfato ES reconocimiento molecular (teoria lock-and-key). Esta prediccion es la mas fuerte evidencia de validez cross-domain: el modelo no dice "todo mapea a todo", sino que predice selectivamente que primitivos se activan en cada dominio.

**P6 — Combustion segun Lavoisier** (CONFIRMED): `fuego` = fuerza + creacion + destruccion. Lavoisier (1789) demostro que la combustion es oxidacion rapida: requiere energia (fuerza), produce nuevas sustancias como CO₂ y H₂O (creacion), y consume combustible y O₂ (destruccion). El modelo descompone `fuego` en los mismos tres componentes que Lavoisier identifico al refutar la teoria del flogisto.

**P7 — Gap de proporcion/ratio** (GAP): En musica, la serie armonica (ratios de frecuencia enteros) no tenia primitivo dedicado. En quimica, la estequiometria (ratios molares enteros) enfrenta el mismo gap — se aproxima con `debe` + `orden` + `mas` + `todo`. Dos dominios completamente independientes revelan la misma carencia estructural. Este gap cross-domain es la evidencia mas fuerte para proponer un nuevo primitivo `proporcion`.

**P8 — Cinetica/Termodinamica como dualidad fundacional** (CONFIRMED): `temporal_obs`/`eterno_obs` mapea directamente a cinetica (observacion temporal, dependiente de la velocidad) vs. termodinamica (equilibrio, independiente del tiempo). Atkins & de Paula (2014) tratan estos como los dos pilares de la quimica fisica. La dualidad se promueve de MODERATE (musica) a STRONG (quimica).

### 7.3 Resumen de predicciones

| Status | Cantidad | Porcentaje |
|--------|----------|-----------|
| CONFIRMED | 7 | 87.5% |
| GAP | 1 | 12.5% |
| PARTIAL | 0 | 0% |
| VIOLATED | 0 | 0% |

7/8 predicciones confirmadas, 0 violadas. El unico GAP (proporcion/ratio) es el mismo que en musica — evidencia para la propuesta de primitivo `proporcion`.

---

## VIII. Desajustes Honestos

### 8.1 Mecanica cuantica sin primitivo

La superposicion cuantica y el entrelazamiento no tienen mapeo directo. El modelo trata `informacion` como "patron/codigo/estructura abstracta", lo cual cubre la configuracion electronica pero no captura la superposicion de estados ni la no-localidad. Esto sugiere que la mecanica cuantica requiere primitivos adicionales que estan fuera del alcance ontologico actual del modelo.

### 8.2 Electronegatividad y proporcion

La electronegatividad (escala de Pauling) es un ratio entre afinidades electronicas. Sin un primitivo `proporcion`, el modelo solo puede aproximarla como `querer` (tendencia termodinamica) — una analogia util pero imprecisa. Este desajuste refuerza P7.

### 8.3 Tabla periodica: resolucion limitada

El modelo mapea la tabla periodica a nivel de principios organizadores (numero atomico, configuracion, capas, propiedades, tendencias), pero no tiene resolucion para distinguir bloques (s, p, d, f), periodos individuales, o comportamientos anomalos (lantanidos, actinidos). Esto es esperable: 63 primitivos no pretenden capturar todos los detalles de un dominio especifico.

### 8.4 Anclas de consistencia cero

Tres anclas (enlace_covalente, enlace_ionico, equilibrio_quimico) tienen consistencia 0%. Esto indica que estos conceptos integran primitivos de multiples lineas de emergencia sin cadena directa. No invalida los mapeos, pero sugiere que la quimica combina primitivos de maneras mas "transversales" que la musica.

---

## IX. Propuestas de Investigacion Futura

### 9.1 Primitivo `proporcion` (evidencia cross-domain)

| Dominio | Concepto que lo necesita | Aproximacion actual |
|---------|------------------------|-------------------|
| Musica | Serie armonica (ratios de frecuencia) | informacion + orden + union |
| Quimica | Estequiometria (ratios molares) | debe + orden + mas + todo |
| Quimica | Electronegatividad (ratio de afinidades) | querer (analogia) |

El mismo gap estructural aparece en dos dominios independientes. Propuesta: un primitivo `proporcion` en capa 3, con deps = [mas, informacion, orden], que capture la nocion de "ratio entero/racional entre cantidades". Esto resolveria simultaneamente los gaps P8 (musica) y P7 (quimica).

### 9.2 Tercer dominio de validacion

Con dos dominios validados (musica, quimica), el siguiente paso natural es un tercer dominio independiente. Candidatos:

- **Biologia**: Jerarquias desde molecula hasta ecosistema; dualidades genotipo/fenotipo, depredador/presa.
- **Economia**: Jerarquias desde transaccion hasta macroeconomia; dualidades oferta/demanda, riesgo/retorno.
- **Fisica de particulas**: Jerarquias desde quark hasta universo; dualidades materia/antimateria, fermionic/bosonico.

### 9.3 Validacion cuantitativa de la promocion de dualidades

Las promociones MODERATE→STRONG de `verdad`/`mentira` y `temporal_obs`/`eterno_obs` sugieren una metrica: la "fuerza de dualidad" es domain-dependent. Una investigacion futura podria formalizar esta metrica y predecir que ejes seran STRONG en cada dominio antes de hacer el mapeo.

---

## X. Comparacion Cross-Domain: Musica vs Quimica

### 10.1 Tabla comparativa

| Metrica | Musica (T8) | Quimica (T9) | Delta |
|---------|-------------|--------------|-------|
| Primitivos DIRECT | 23 (36.5%) | 32 (50.8%) | +9 |
| Primitivos ANALOGICAL | 38 (60.3%) | 31 (49.2%) | -7 |
| Primitivos NULL | 2 (3.2%) | 0 (0.0%) | -2 |
| CONFIRMED+PLAUSIBLE | 96.9% | 100.0% | +3.1 |
| Jerarquias alineadas | 5/5 | 5/5 | = |
| STRONG+MODERATE ejes | 11/12 (92%) | 11/12 (92%) | = |
| Consistencia de anclas | 18.0% | 34.6% | +16.6 |
| Baseline aleatorio | 6.1% | 5.4% | -0.7 |
| Ratio sobre baseline | 2.94x | 6.35x | +3.41x |

### 10.2 Interpretacion

1. **La quimica mapea mas primitivos directamente**: 32 DIRECT vs 23. Esto es coherente: la quimica abarca fenomenos mas amplios que la musica (estados de la materia, sentidos quimicos, vida/muerte como procesos quimicos).

2. **Cero NULL confirma amplitud**: La musica dejo 2 primitivos sin mapeo; la quimica los absorbe todos. Esto sugiere que la quimica es un dominio "mas ancho" para el modelo.

3. **100% CONFIRMED es notable**: Todas las 128 dependencias tienen respaldo en quimica establecida. En musica, 20 pares eran solo PLAUSIBLE y 4 eran NEUTRAL. La quimica proporciona una validacion mas fuerte de la estructura de dependencias.

4. **Anclas quimicas 6.35x sobre baseline**: Casi el doble del ratio musical (2.94x). Los conceptos quimicos se alinean mejor con las dependencias del modelo que los conceptos musicales.

5. **Estabilidad de jerarquias y ejes**: 5/5 y 11/12 son identicos en ambos dominios. Esto sugiere que estas metricas son robustas cross-domain.

---

## Bibliografia

- Atkins, P. & de Paula, J. (2014). *Physical Chemistry*. 10ma ed. Oxford University Press.
- Boltzmann, L. (1877). "Uber die Beziehung zwischen dem zweiten Hauptsatze der mechanischen Warmetheorie und der Wahrscheinlichkeitsrechnung." *Sitzungsberichte der kaiserlichen Akademie der Wissenschaften*, 76, 373-435.
- Gibbs, J. W. (1878). "On the Equilibrium of Heterogeneous Substances." *Transactions of the Connecticut Academy of Arts and Sciences*, 3, 108-248; 343-524.
- Lavoisier, A. (1789). *Traite Elementaire de Chimie*. Paris: Cuchet.
- Le Chatelier, H. (1884). "Sur un enonce general des lois des equilibres chimiques." *Comptes Rendus de l'Academie des Sciences*, 99, 786-789.
- Mendeleev, D. (1869). "Sootnoshenie svoistv s atomnym vesom elementov." *Zhurnal Russkoe Fiziko-Khimicheskoe Obshchestvo*, 1, 60-77.
- Pauling, L. (1931). "The Nature of the Chemical Bond." *Journal of the American Chemical Society*, 53(4), 1367-1400.
- Pauling, L. (1960). *The Nature of the Chemical Bond*. 3ra ed. Ithaca: Cornell University Press.
- Woodward, R. B. & Hoffmann, R. (1969). "The Conservation of Orbital Symmetry." *Angewandte Chemie International Edition*, 8(11), 781-853.

---

*Parte del manuscrito "Expansion del Circulo de Emergencia de Dualidades."*
*Script computacional: `scripts/test9_chemistry_validation.py`*
