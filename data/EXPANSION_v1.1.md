# Expansion v1.1 -- De 65 a 72 Primitivos

**Fecha**: 2026-03-22
**Version**: primitivos.json v1.1
**Cambio**: +7 primitivos nuevos (bits 65-71), +1 eje dual, modificaciones de deps en 7 existentes

---

## 1. Resumen

El entrenamiento v3 demostro que GPT-2 Medium aprende correctamente la estructura del DAG de 65 primitivos (90.9% bit accuracy, 99% subsuncion). Sin embargo, 5 pares duales con Jaccard > 0.80 colapsaron: el modelo no puede distinguirlos porque comparten demasiados bits por herencia transitiva y difieren en solo 1-2 bits de 65.

La investigacion en C:\research\first_principles identifico 7 nuevos primitivos provenientes de termodinamica, teoria de juegos, neurociencia, psicologia, y filosofia de la mente. Cada uno se inserto en el DAG como dependencia diferenciadora de uno o mas pares colapsados, aumentando los bits unicos de cada miembro del par.

Resultado: los 5 pares problematicos pasaron de 1-2 bits de diferencia a 4-6 bits, y un sexto par (temporal_obs/eterno_obs) que ya funcionaba se mantuvo estable.

---

## 2. Diagnostico v3: Pares Duales Colapsados

El esquema de targets en v3 es: bit propio ON + todas las dependencias transitivas ON. Esto genera un problema estructural en capas altas: cuantas mas capas tiene un primitivo, mas bits hereda, y menos proporcion de su firma es "propia".

| Par dual              | Jaccard v3 | Bits A | Bits B | Compartidos | Diferentes | Coherencia v3 | Causa del colapso                                                       |
|-----------------------|------------|--------|--------|-------------|------------|---------------|-------------------------------------------------------------------------|
| vida / muerte         | 0.882      | 15     | 17     | 15          | 2          | 0.175         | muerte = vida + destruccion + bit propio; hereda los 15 bits de vida    |
| placer / dolor        | 0.882      | 16     | 16     | 15          | 2          | 0.286         | ambos dependen de vida + informacion; comparten 15 bits, difieren en 2  |
| consciente / ausente  | 0.947      | 18     | 19     | 18          | 1          | 0.660         | ausente depende de consciente; comparten 18 bits, difieren en 1         |
| individual / colectivo| 0.889      | 16     | 18     | 16          | 2          | 0.685         | colectivo depende de individual (via muchos); comparten 16, difieren 2  |
| receptivo / creador_obs| 0.900     | 19     | 19     | 18          | 2          | 0.692         | ambos dependen de consciente + base similar; comparten 18, difieren 2   |

**Criterio de v3**: si dos duals tienen Jaccard > 0.80 en sus targets, necesitan al menos 1-2 primitivos intermedios que diferencien sus caminos por el DAG.

**Excepcion notable**: temporal_obs / eterno_obs tiene Jaccard 0.818 pero coherencia 1.000. Sus 4 bits de diferencia sobre 19-21 bits activos dan margen suficiente. No requiere intervencion.

---

## 3. Los 7 Nuevos Primitivos

### 3.1 atraccion (bit 66)

| Campo   | Valor                                                                                      |
|---------|--------------------------------------------------------------------------------------------|
| bit     | 66                                                                                         |
| primo   | 331                                                                                        |
| capa    | 3                                                                                          |
| deps    | fuerza, union                                                                              |
| def     | Tendencia de aproximacion, valencia positiva                                               |
| source  | Physics fundamental forces, Psychology operant conditioning (reward), Neuroscience reward circuits |

**Por que estas deps**: la atraccion es una fuerza (capa 2) orientada hacia la union (capa 2). No requiere vida ni conciencia: la gravedad atrae, un iman atrae.

**Fortalece**: placer/dolor. Placer ahora depende de atraccion (aproximarse a lo que da placer), dolor depende de aversion (evitar lo que da dolor). Antes ambos compartian exactamente las mismas deps salvo su bit propio.

### 3.2 decaimiento (bit 65)

| Campo   | Valor                                                                                      |
|---------|--------------------------------------------------------------------------------------------|
| bit     | 65                                                                                         |
| primo   | 317                                                                                        |
| capa    | 4                                                                                          |
| deps    | destruccion, caos                                                                          |
| def     | Deterioro progresivo, disolucion de estructura organizada                                  |
| source  | Thermodynamics 2nd Law (entropy increase), Biology apoptosis/senescence, Physics radioactive decay |

**Por que estas deps**: el decaimiento combina destruccion (deshacer) con caos (desorden). Es la disolucion gradual, no la eliminacion subita.

**Fortalece**: vida/muerte. Muerte ahora depende de decaimiento (deterioro progresivo), que trae consigo los bits de destruccion y caos. Vida no depende de ninguno de estos: vida es creacion + orden + continuidad.

### 3.3 aversion (bit 67)

| Campo   | Valor                                                                                      |
|---------|--------------------------------------------------------------------------------------------|
| bit     | 67                                                                                         |
| primo   | 337                                                                                        |
| capa    | 4                                                                                          |
| deps    | fuerza, destruccion                                                                        |
| def     | Tendencia de evitacion, valencia negativa                                                  |
| dual    | atraccion                                                                                  |
| source  | Psychology avoidance motivation, Neuroscience threat/pain circuits, Biology flight response |

**Por que estas deps**: la aversion es una fuerza orientada hacia la destruccion (alejarse de, rechazar). Es el polo opuesto de atraccion.

**Fortalece**: placer/dolor. Dolor ahora depende de aversion, cuyo camino pasa por destruccion. Placer depende de atraccion, cuyo camino pasa por union. Los caminos divergen completamente.

### 3.4 cooperacion (bit 68)

| Campo   | Valor                                                                                      |
|---------|--------------------------------------------------------------------------------------------|
| bit     | 68                                                                                         |
| primo   | 347                                                                                        |
| capa    | 4                                                                                          |
| deps    | union, hacer                                                                               |
| def     | Accion conjunta hacia objetivo compartido                                                  |
| source  | Game Theory Nash equilibrium, Ecology mutualism, Sociology collective behavior (Durkheim)  |

**Por que estas deps**: cooperacion es union (juntar) + hacer (accion). Es el acto de unirse para actuar juntos.

**Fortalece**: individual/colectivo. Colectivo ahora depende de cooperacion, que trae union y hacer. Individual no tiene ninguno de estos: individual es uno + contencion + vida.

### 3.5 perdida (bit 69)

| Campo   | Valor                                                                                      |
|---------|--------------------------------------------------------------------------------------------|
| bit     | 69                                                                                         |
| primo   | 349                                                                                        |
| capa    | 4                                                                                          |
| deps    | vacio, destruccion                                                                         |
| def     | Ausencia tras haber tenido, vacio dejado por destruccion                                   |
| source  | Psychology loss/grief, Philosophy of Mind absence, Thermodynamics irreversibility           |

**Por que estas deps**: la perdida combina vacio (espacio donde algo falta) con destruccion (lo que causo la ausencia). No es el vacio primordial: es el vacio que queda despues.

**Fortalece**: consciente/ausente. Ausente ahora depende de perdida, que trae vacio y destruccion. Consciente no depende de ninguno de estos: consciente es vida + informacion + vista.

### 3.6 atencion (bit 70)

| Campo   | Valor                                                                                      |
|---------|--------------------------------------------------------------------------------------------|
| bit     | 70                                                                                         |
| primo   | 353                                                                                        |
| capa    | 5                                                                                          |
| deps    | consciente, quietud                                                                        |
| def     | Foco selectivo de la conciencia, filtro perceptual                                         |
| source  | Cognitive Science computational theory of mind, Neuroscience predictive coding (Friston), Psychology dual-process theory |

**Por que estas deps**: la atencion requiere conciencia (estar despierto) y quietud (detenerse para enfocar). Es la conciencia enfocada, no dispersa.

**Fortalece**: receptivo/creador_obs. Receptivo ahora depende de atencion, que trae quietud. Creador_obs depende de intencion, que trae querer y hacer. Los caminos divergen: uno hacia la quietud receptiva, otro hacia la accion intencional.

### 3.7 intencion (bit 71)

| Campo   | Valor                                                                                      |
|---------|--------------------------------------------------------------------------------------------|
| bit     | 71                                                                                         |
| primo   | 359                                                                                        |
| capa    | 5                                                                                          |
| deps    | querer, hacer                                                                              |
| def     | Proposito dirigido, voluntad de actuar hacia un fin                                        |
| dual    | (no tiene dual directo; funciona como diferenciador)                                       |
| source  | Philosophy of Mind intentionality (Brentano), Phenomenology (Husserl), Cognitive Science embodied cognition |

**Por que estas deps**: la intencion combina querer (deseo, voluntad) con hacer (accion, ejecucion). Es el proposito dirigido: no solo querer, sino querer-hacer.

**Fortalece**: receptivo/creador_obs. Creador_obs ahora depende de intencion, que trae querer y hacer. Receptivo depende de atencion, que trae quietud. Los bits unicos de cada uno divergen completamente.

---

## 4. Cambios a Primitivos Existentes

7 primitivos existentes recibieron nuevas dependencias para conectar con los 7 nuevos primitivos:

| Primitivo    | Deps antes                                          | Dep(s) anadida(s) | Deps despues                                                 |
|-------------|-----------------------------------------------------|-------------------|--------------------------------------------------------------|
| muerte      | vida, destruccion                                   | + decaimiento     | vida, destruccion, decaimiento                               |
| placer      | vida, informacion                                   | + atraccion       | vida, informacion, atraccion                                 |
| dolor       | vida, informacion                                   | + aversion        | vida, informacion, aversion                                  |
| ausente     | consciente                                          | + perdida         | consciente, perdida                                          |
| colectivo   | muchos, individual                                  | + cooperacion     | muchos, individual, cooperacion                              |
| receptivo   | consciente, informacion                             | + atencion        | consciente, informacion, atencion                            |
| creador_obs | consciente, creacion, hacer                         | + intencion       | consciente, creacion, hacer, intencion                       |

---

## 5. Nuevo Eje Dual: atraccion / aversion

La expansion introduce un 14o eje dual:

| Eje             | Polo +     | Polo -   | Capa + | Capa - |
|-----------------|------------|----------|--------|--------|
| atraccion/aversion | atraccion | aversion | 3      | 4      |

Este eje captura la valencia fundamental: aproximacion vs evitacion. Es mas basico que placer/dolor (que requieren vida y conciencia). La gravedad atrae sin sentir placer; un organismo unicelular evita toxinas sin experimentar dolor.

Ubicacion en la lista de ejes duales:
```
["bien", "mal"], ["orden", "caos"], ["creacion", "destruccion"],
["union", "separacion"], ["verdad", "mentira"], ["libertad", "control"],
["vida", "muerte"], ["placer", "dolor"], ["consciente", "ausente"],
["temporal_obs", "eterno_obs"], ["individual", "colectivo"],
["receptivo", "creador_obs"], ["mover", "quietud"],
["atraccion", "aversion"]  <-- nuevo
```

---

## 6. Verificacion de Jaccard: Antes y Despues

| Par dual                | Jaccard v3 | Jaccard v1.1 | Mejora   | Bits diff antes | Bits diff despues |
|------------------------|------------|--------------|----------|-----------------|-------------------|
| vida / muerte          | 0.882      | 0.789        | -0.093   | 2               | 4                 |
| placer / dolor         | 0.882      | 0.714        | -0.168   | 2               | 6                 |
| consciente / ausente   | 0.947      | 0.818        | -0.129   | 1               | 4                 |
| individual / colectivo | 0.889      | 0.800        | -0.089   | 2               | 4                 |
| receptivo / creador_obs| 0.900      | 0.750        | -0.150   | 2               | 6                 |
| temporal_obs / eterno_obs | 0.818   | 0.818        | 0.000    | 4               | 4                 |

Todos los pares problematicos bajaron de Jaccard > 0.80 a Jaccard <= 0.818, y todos tienen ahora >= 4 bits de diferencia. El umbral de v3 mostro que 4 bits de diferencia es suficiente (temporal_obs/eterno_obs logro coherencia 1.000 con exactamente 4 bits de diferencia).

### Bits unicos por miembro del par (post-expansion):

| Par                    | Bits unicos polo A                             | Bits unicos polo B                                  |
|------------------------|------------------------------------------------|-----------------------------------------------------|
| vida / muerte          | (bits de vida sin muerte)                      | destruccion, caos, muerte, decaimiento              |
| placer / dolor         | union, placer, atraccion                       | destruccion, dolor, aversion                        |
| consciente / ausente   | (bits de consciente sin ausente)               | vacio, destruccion, ausente, perdida                |
| individual / colectivo | (bits de individual sin colectivo)             | union, muchos, colectivo, cooperacion               |
| receptivo / creador_obs| receptivo, atencion, quietud                   | querer, creador_obs, intencion                      |

Placer y dolor ahora tienen caminos completamente divergentes: placer pasa por union --> atraccion, dolor pasa por destruccion --> aversion. No comparten ningun bit unico.

Receptivo y creador_obs ahora divergen por quietud/atencion vs querer/intencion: contemplacion pasiva vs accion dirigida.

---

## 7. Validacion Estructural

### 7.1 DAG aciclico

Se verifico que el grafo de 72 primitivos no contiene ciclos. Todas las dependencias apuntan de capas inferiores a superiores o dentro de la misma capa (con bit menor apuntando a mayor en caso de deps intra-capa). Ningun primitivo depende directa ni transitivamente de si mismo.

### 7.2 Restricciones de capa

Todas las dependencias respetan la restriccion: un primitivo de capa N solo depende de primitivos de capa <= N. Verificado para los 72 primitivos.

### 7.3 Distribucion por capa

| Capa | Nombre          | Primitivos (v3) | Primitivos (v1.1) | Cambio |
|------|-----------------|------------------|--------------------|--------|
| 1    | Punto (0D)      | 3                | 3                  | --     |
| 2    | Linea (1D)      | 8                | 8                  | --     |
| 3    | Tiempo (1D+t)   | 12               | 13                 | +1     |
| 4    | Plano (2D)      | 17               | 21                 | +4     |
| 5    | Volumen (3D)    | 21               | 23                 | +2     |
| 6    | Meta (3D+)      | 4                | 4                  | --     |
| **Total** |            | **65**           | **72**             | **+7** |

Capa 3 recibio 1 nuevo (atraccion). Capa 4 recibio 4 nuevos (decaimiento, aversion, cooperacion, perdida). Capa 5 recibio 2 nuevos (atencion, intencion). La distribucion sigue siendo monotonicamente creciente hasta capa 5 y decrece en capa 6 (meta-nivel), lo cual es consistente con la estructura original.

### 7.4 Primos unicos

Los 7 nuevos primos (317, 331, 337, 347, 349, 353, 359) son todos numeros primos y no se repiten con ningun primo existente en el sistema.

---

## 8. Proximos Pasos

1. **Regenerar gold_primitivos_72.json** -- Recalcular los targets de los 72 primitivos con sus dependencias transitivas completas. Incluir los nuevos bits 65-71 en los vectores target.

2. **Entrenar v4** -- Usar los 72 targets unicos con GPT-2 Medium. Misma arquitectura que v3 (triadic head de 72 bits en lugar de 65). Hiperparametros de referencia de v3.

3. **Comparar con v3** -- Metricas a evaluar:
   - Bit accuracy global (baseline v3: 90.9%)
   - Coherencia de pares duales (especialmente los 5 que colapsaron en v3)
   - Jaccard predicho vs target para los 6 pares monitoreados
   - Subsuncion (baseline v3: 99%)
   - Regla de Tres / analogias duales (baseline v3: coseno 0.90)

4. **Criterio de exito para v4**: los 5 pares que colapsaron en v3 deben alcanzar coherencia > 0.80. Si temporal_obs/eterno_obs mantiene coherencia 1.000 con 4 bits de diferencia, los demas pares con 4-6 bits de diferencia deberian lograrlo tambien.
