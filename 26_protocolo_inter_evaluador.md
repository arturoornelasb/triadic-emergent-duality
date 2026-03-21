# Documento 26: Protocolo para Validación Inter-Evaluador

## I. Objetivo del Protocolo

Establecer un procedimiento estandarizado para que un evaluador independiente pueda:

1. Clasificar los 63 primitivos del Sistema 7×7 en un dominio dado como DIRECT, ANALOGICAL o NULL
2. Comparar su clasificación con la del autor original
3. Calcular métricas de acuerdo inter-evaluador (Cohen's κ, Krippendorff's α)
4. Determinar si el modelo tiene validez independiente del evaluador

## II. Materiales

### 2.1 Proporcionados al Evaluador

1. **primitivos.json** — Archivo con 63 primitivos, cada uno con:
   - nombre, definición, capa (1-6), dependencias, primo
   - El evaluador NO recibe los mapeos previos del autor
2. **Definiciones de las capas** — Descripción de las 6 capas dimensionales
3. **Instrucciones de clasificación** — Este documento (secciones III-IV)
4. **Formulario vacío** — Tabla de 63 filas × 4 columnas (§VII)
5. **Lista de dominios** — El dominio a evaluar con su descripción

### 2.2 NO Proporcionados

- Los mapeos previos del autor (DOMAIN_MAP)
- Los resultados de tests anteriores
- Las anclas definidas por el autor
- Este documento solo se comparte DESPUÉS de que el evaluador complete su clasificación independiente

## III. Instrucciones para el Evaluador

### 3.1 Preparación

1. Leer las definiciones de los 63 primitivos (primitivos.json)
2. Familiarizarse con las 6 capas dimensionales
3. Leer la descripción general del dominio a evaluar
4. **NO consultar** los documentos de validación previos (Docs 8-15)

### 3.2 Clasificación

Para cada uno de los 63 primitivos, el evaluador debe:

**Paso 1**: Leer la definición del primitivo y su capa.

**Paso 2**: Determinar si existe una correspondencia con un concepto del dominio:

| Clasificación | Criterio | Ejemplo |
|---------------|----------|---------|
| **DIRECT** | El primitivo tiene una correspondencia directa, unívoca y no metafórica con un concepto establecido del dominio | "fuerza" → Fuerza de Newton (física) |
| **ANALOGICAL** | El primitivo tiene una analogía estructural defendible pero que requiere extensión metafórica | "equilibrio" → Markedness equilibrium (lingüística) |
| **NULL** | El primitivo no tiene correspondencia significativa en el dominio, ni directa ni analógica | "olfato" → (ninguna en matemáticas) |

**Paso 3**: Para cada DIRECT o ANALOGICAL, escribir:
- El concepto específico del dominio
- Los sub-dominios donde aplica
- Una justificación breve (1-2 oraciones)

**Paso 4**: Para cada NULL, escribir:
- Por qué no existe correspondencia
- Si existe alguna correspondencia marginal que fue descartada

### 3.3 Criterios de Decisión

**¿DIRECT o ANALOGICAL?** Usar DIRECT solo cuando:
- El concepto del dominio usa el mismo término o un sinónimo técnico
- La correspondencia no requiere extensión metafórica
- Un especialista del dominio reconocería la correspondencia inmediatamente

**¿ANALOGICAL o NULL?** Usar NULL solo cuando:
- No se puede articular ninguna analogía estructural coherente
- La correspondencia sería arbitraria o forzada
- Un especialista del dominio NO reconocería la correspondencia

### 3.4 Tiempo Estimado

2-3 horas por dominio. Se recomienda:
- 30 min: lectura de materiales
- 90-120 min: clasificación de los 63 primitivos
- 30 min: revisión y ajustes

## IV. Métricas de Acuerdo Inter-Evaluador

### 4.1 Cohen's κ (kappa)

Para 2 evaluadores con 3 categorías (D, A, N):

κ = (pₒ - pₑ) / (1 - pₑ)

Donde:
- pₒ = proporción de acuerdo observado
- pₑ = proporción de acuerdo esperado por azar

### 4.2 Krippendorff's α (alpha)

Para ≥2 evaluadores, con tratamiento ordinal (D > A > N):

α = 1 - Dₒ / Dₑ

Donde:
- Dₒ = desacuerdo observado
- Dₑ = desacuerdo esperado por azar

### 4.3 Porcentaje de Acuerdo Exacto

Proporción de los 63 primitivos donde ambos evaluadores asignan la misma clase.

### 4.4 Matriz de Confusión D×A×N

|  | Evaluador 2: D | Evaluador 2: A | Evaluador 2: N |
|--|----------------|----------------|----------------|
| Evaluador 1: D | a | b | c |
| Evaluador 1: A | d | e | f |
| Evaluador 1: N | g | h | i |

## V. Criterios de Validez

| κ / α | Interpretación | Acción |
|-------|---------------|--------|
| ≥ 0.80 | Acuerdo casi perfecto | Modelo validado para este dominio |
| 0.60 – 0.79 | Acuerdo sustancial | Modelo probablemente válido; revisar desacuerdos |
| 0.40 – 0.59 | Acuerdo moderado | Dominio ambiguo o definiciones insuficientes |
| < 0.40 | Acuerdo pobre | Modelo necesita revisión o dominio no es apto |

**Umbral mínimo**: κ ≥ 0.60 para considerar un dominio validado por inter-evaluador.

## VI. Procedimiento de Resolución de Desacuerdos

### 6.1 Identificación

Después de calcular κ, identificar los primitivos específicos donde los evaluadores discrepan. Clasificar los desacuerdos:

| Tipo | Descripción | Gravedad |
|------|-------------|----------|
| D↔A | Discrepancia sobre si la correspondencia es directa o analógica | Baja |
| D↔N | Discrepancia sobre si existe correspondencia | Alta |
| A↔N | Discrepancia sobre si la analogía es defendible | Media |

### 6.2 Discusión

Los evaluadores discuten cada desacuerdo presentando:
- Su razonamiento original
- Referencias bibliográficas que respaldan su clasificación
- Contra-argumentos específicos

### 6.3 Clasificación Consensuada

Después de la discusión, se produce un mapeo consensuado. Se reportan:
- El mapeo pre-discusión de cada evaluador
- El mapeo consensuado
- Los primitivos que permanecen en desacuerdo (sin consenso)

## VII. Template de Formulario

### Formulario de Evaluación Inter-Evaluador

**Evaluador**: ________________
**Dominio**: ________________
**Fecha**: ________________

| # | Primitivo | Capa | Clase (D/A/N) | Concepto del dominio | Sub-dominios | Justificación |
|---|-----------|------|---------------|---------------------|-------------|---------------|
| 1 | vacío | 1 | | | | |
| 2 | información | 1 | | | | |
| 3 | uno | 1 | | | | |
| 4 | fuerza | 2 | | | | |
| 5 | eje_profundidad | 2 | | | | |
| 6 | contención | 2 | | | | |
| 7 | más | 2 | | | | |
| 8 | menos | 2 | | | | |
| 9 | unión | 2 | | | | |
| 10 | separación | 2 | | | | |
| 11 | parte_de | 2 | | | | |
| 12 | mover | 3 | | | | |
| 13 | posición_temporal | 3 | | | | |
| 14 | flujo_temporal | 3 | | | | |
| 15 | hacer | 3 | | | | |
| 16 | creación | 3 | | | | |
| 17 | destrucción | 3 | | | | |
| 18 | orden | 3 | | | | |
| 19 | caos | 3 | | | | |
| 20 | porque | 3 | | | | |
| 21 | si_entonces | 3 | | | | |
| 22 | eje_vertical | 4 | | | | |
| 23 | eje_lateral | 4 | | | | |
| 24 | equilibrio | 4 | | | | |
| 25 | vista | 4 | | | | |
| 26 | bien | 4 | | | | |
| 27 | mal | 4 | | | | |
| 28 | verdad | 4 | | | | |
| 29 | mentira | 4 | | | | |
| 30 | libertad | 4 | | | | |
| 31 | control | 4 | | | | |
| 32 | tipo_de | 4 | | | | |
| 33 | algunos | 4 | | | | |
| 34 | muchos | 4 | | | | |
| 35 | todo | 4 | | | | |
| 36 | puede | 4 | | | | |
| 37 | debe | 4 | | | | |
| 38 | tal_vez | 4 | | | | |
| 39 | tierra | 5 | | | | |
| 40 | agua | 5 | | | | |
| 41 | aire | 5 | | | | |
| 42 | fuego | 5 | | | | |
| 43 | tacto | 5 | | | | |
| 44 | oído | 5 | | | | |
| 45 | gusto | 5 | | | | |
| 46 | olfato | 5 | | | | |
| 47 | interocepción | 5 | | | | |
| 48 | vida | 5 | | | | |
| 49 | muerte | 5 | | | | |
| 50 | placer | 5 | | | | |
| 51 | dolor | 5 | | | | |
| 52 | consciente | 5 | | | | |
| 53 | ausente | 5 | | | | |
| 54 | individual | 5 | | | | |
| 55 | colectivo | 5 | | | | |
| 56 | querer | 5 | | | | |
| 57 | saber | 5 | | | | |
| 58 | pensar | 5 | | | | |
| 59 | decir | 5 | | | | |
| 60 | temporal_obs | 6 | | | | |
| 61 | eterno_obs | 6 | | | | |
| 62 | receptivo | 6 | | | | |
| 63 | creador_obs | 6 | | | | |

**Totales**: D: ___ | A: ___ | N: ___

**Notas del evaluador**:

## VIII. Script de Cálculo

Las funciones `cohens_kappa()`, `krippendorffs_alpha()`, y `confusion_matrix_dan()` están implementadas en `scripts/statistical_rigor.py` (sección 2). Uso:

```python
from statistical_rigor import cohens_kappa, krippendorffs_alpha, confusion_matrix_dan

# Ejemplo con dos evaluadores
rater1 = {'vacío': 'D', 'información': 'D', 'uno': 'D', ...}  # 63 entries
rater2 = {'vacío': 'D', 'información': 'D', 'uno': 'A', ...}  # 63 entries

# Cohen's kappa
result = cohens_kappa(rater1, rater2)
print(f"κ = {result['kappa']:.3f}")
print(f"Observed agreement: {result['po']:.3f}")
print(f"Expected agreement: {result['pe']:.3f}")

# Confusion matrix
cm = confusion_matrix_dan(rater1, rater2)
print(f"Exact agreement: {cm['pct_agreement']:.1f}%")

# Krippendorff's alpha (for 2+ raters)
alpha_result = krippendorffs_alpha([rater1, rater2], level='ordinal')
print(f"α = {alpha_result['alpha']:.3f}")
```

---

**Script asociado**: `scripts/statistical_rigor.py` (funciones inter-evaluador)
**Documento previo**: Doc 25 (Validación Lingüística)
**Aplicación**: evaluar cada dominio (T8-T15) con ≥1 evaluador independiente
