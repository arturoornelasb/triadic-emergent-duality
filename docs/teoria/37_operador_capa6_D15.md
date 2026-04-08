# Doc 37: D15 — El Operador Interno de la Capa 6 (Probabilística)

**Fecha**: 2026-04-05  
**Versión**: Propuesta formal  
**Prerequisito**: Docs 34 (14 dualidades), ALGEBRAIC_LAYERS.md  

---

## 1. El hueco

La distribución de operadores internos por capa es:

| Capa | Álgebra | Operadores internos | Operador(es) |
|------|---------|:-------------------:|--------------|
| 1 | Booleano {0,1} | 1 | D1: Existir/No-existir |
| 2 | Fuzzy {0,+} | 1 | D9: Dentro/Fuera |
| 3 | Ordinal {<,=,>} | 2 | D3: Antes/Después, D12: Causa/Efecto |
| 4 | Modal {◇,□} | 2 | D4: Posible/Imposible, D13: Semejante/Diferente |
| 5 | Trivalente {−,0,+} | 1 | D11: Vida/Muerte |
| 6 | Probabilístico {0,?} | **0** | **← HUECO** |

El patrón 1,1,2,2,1,0 es incompleto. Cada álgebra necesita al menos un operador que la articule desde dentro. El álgebra probabilística no tiene el suyo.

---

## 2. Análisis del álgebra probabilística

El álgebra {0,?} tiene dos estados:
- **0**: No hay superposición — el estado está colapsado (o la dimensión no aplica)
- **?**: Superposición genuina — el resultado depende de quién observa

Los 4 primitivos de Capa 6 forman 2 ejes duales:
- `temporal_obs` / `eterno_obs` (D14 — pero D14 es TRANSICIÓN c5→c6, no interno)
- `receptivo` / `creador_obs` (D14 — mismo problema)

Ambos ejes son manejados por D14 (Sujeto/Objeto), que es un operador de **transición** (Trivalente → Probabilístico), no un operador **interno**. D14 responde "¿para quién?" — lleva al observador. Pero una vez que el observador existe, ¿qué operación DENTRO de la perspectiva probabilística falta?

---

## 3. Propuesta: D15 = Colapso/Superposición

### Nombre: **D15 — Colapso/Superposición** (Determinar/Indeterminar)

| Campo | Valor |
|-------|-------|
| Nombre | Colapso / Superposición |
| Álgebra | Probabilístico {0,?} |
| Tipo | INTERNO (c6) |
| Operación | Toggle entre estado colapsado (determinado) y superpuesto (indeterminado) |
| Anclas | temporal_obs (colapso: perspectiva fija en el tiempo) + eterno_obs (superposición: perspectiva no colapsada) |
| Análogos | QM: medición colapsa la función de onda; Friston: atención activa colapsa posteriors; McGilchrist: LH colapsa, RH mantiene apertura |

### ¿Por qué Colapso/Superposición?

**El argumento algebraico:**

Cada operador interno realiza la operación fundamental de su álgebra:
- D1 en {0,1}: **negación** (0↔1)
- D9 en {0,+}: **partición** (dónde está el umbral)
- D3 en {<,=,>}: **inversión temporal** (antes↔después)
- D4 en {◇,□}: **alternancia modal** (posible↔necesario)
- D11 en {−,0,+}: **inversión de valencia** (vida↔muerte, placer↔dolor)

El álgebra {0,?} tiene una operación fundamental: el **colapso** de ? a 0 (observación determina el estado) y su inversa, la **superposición** (deshacer la determinación, reabrir la indeterminación).

D15 opera DENTRO de la capa probabilística:
- **Colapso**: ? → 0. El observador fija una perspectiva. El temporal_obs elige un punto en el tiempo; la superposición se resuelve.
- **Superposición**: 0 → ?. El observador reabre la indeterminación. El eterno_obs disuelve la perspectiva fija; el estado vuelve a ser genuinamente abierto.

### ¿Por qué no es redundante con D14?

D14 (Sujeto/Objeto) es la **transición** que genera al observador desde la conciencia. Responde: "¿existe un observador?"

D15 opera una vez que el observador ya existe. Responde: "¿el observador ha colapsado su perspectiva o la mantiene abierta?"

Análogamente:
- D14 es como encender el instrumento de medición (transición: no-observador → observador)
- D15 es la medición misma (interno: superposición → colapso)

### Conexión con k (selección recursiva)

D15 es la manifestación de k en Capa 6: la selección recursiva opera como colapso. Cuando k > 0, el sistema selecciona (colapsa). Cuando k = 0 pero r,i,j > 0 (estado de estancamiento, K2), el sistema permanece en superposición sin colapsar — tiene capacidad de observar pero no selecciona.

---

## 4. Impacto en el sistema

### Patrón actualizado: 1, 1, 2, 2, 1, **1**

El patrón simétrico 1,1,2,2,1,1 tiene mejor estructura que 1,1,2,2,1,0:
- Capas extremas (1,2 y 5,6): 1 operador interno cada una
- Capas intermedias (3,4): 2 operadores internos cada una
- Simetría: (1,1,2) | (2,1,1)

### Primitivos propuestos

No se requieren primitivos nuevos. D15 reutiliza los existentes de Capa 6 con un nuevo rol operacional:

| Polo | Primitivo | Bit | Primo | Interpretación en D15 |
|------|-----------|-----|-------|----------------------|
| Colapso | temporal_obs | 38 | 167 | Observador que fija perspectiva temporal → estado determinado |
| Superposición | eterno_obs | 39 | 173 | Observador sin perspectiva fija → estado indeterminado |

### Relación con los ejes duales existentes

- temporal_obs/eterno_obs ya están definidos como eje dual en primitivos.json
- Actualmente asignados a D14, pero D14 es operador de transición
- Propuesta: reasignar temporal_obs/eterno_obs como anclas de D15 (interno c6)
- D14 retiene consciente/ausente como anclas (transición c5→c6) y receptivo/creador_obs como secundarios

### Verificación algebraica

Para que D15 sea consistente:
1. **Ambas anclas en misma capa**: temporal_obs(c6), eterno_obs(c6) ✓
2. **Opera dentro del álgebra**: {0,?} toggle ✓
3. **Independiente de D14**: D14 genera al observador; D15 opera sobre su estado ✓
4. **No requiere primitivos nuevos**: Reutiliza existentes ✓
5. **Consistente con k**: Colapso = k activo; Superposición = k inactivo ✓

---

## 5. Verificación empírica propuesta

1. **Neural probe**: En modelo v6, verificar si temporal_obs y eterno_obs anti-correlacionan más fuerte que con receptivo/creador_obs (lo que indicaría que son eje dual propio, no parte de D14)
2. **DVS impact**: Recalcular DVS con 15 dualidades para los 9 dominios — ¿mejora la separación?
3. **DAG consistency**: Verificar que la reasignación no viola la triangularidad de la matriz 15×15

---

## 6. Implicaciones filosóficas

D15 cierra el ciclo de las 6 álgebras con el operador más profundo: el acto de observar que colapsa la realidad probabilística. 

El sistema completo entonces narra:
1. **Existir** (D1: algo existe)
2. **Medir** (D9: tiene grado, tiene límites)
3. **Ordenar** (D3: esto va antes, D12: esto causa aquello)
4. **Imaginar** (D4: podría ser diferente, D13: esto se parece a aquello)
5. **Vivir** (D11: esto vive/muere, siente placer/dolor)
6. **Observar** (D15: ¿el observador ha elegido una perspectiva, o mantiene todas abiertas?)

La última dualidad es la más recursiva: el observador que observa si ha colapsado su propia observación.
