# Documento 29: Métrica Universal en Bits — IDVS

| Métrica | Resultado |
|---------|-----------|
| IDVS — 8 dominios positivos | Todos ≥ 0.859 (PASS) |
| IDVS — Control negativo | 0.469 (FAIL) |
| Separación mínima IDVS | 0.391 (Filosofía 0.859 vs Astrología 0.469) |
| Separación mínima DVS | 0.285 (referencia) |
| MI topológica | NO discrimina (Astrología 0.053 > Filosofía 0.006) |
| Monotonicity topológica | SÍ discrimina (gap 0.117) |
| Firmas primas | 9 únicas (63 trits → entero único por dominio) |

**Script:** `scripts/information_metric.py`
**Dependencias:** Solo stdlib Python (json, math, collections). Sin numpy, scipy ni networkx.

---

## I. Motivación: De Pesos Ad-Hoc a Teoría de Información

El DVS (Documento 27) discrimina perfectamente con 5 sub-métricas, pero depende de pesos ad-hoc:

```
DVS = 0.30×M1 + 0.25×M2 + 0.20×M3 + 0.15×M4 + 0.10×M5
```

¿Por qué 0.30 y no 0.35? ¿Por qué no una media geométrica? La pregunta no tiene respuesta empírica — los pesos fueron elegidos manualmente para maximizar la separación.

**Objetivo de Fase 5:** Construir una métrica fundamentada en teoría de información que:
1. No requiera pesos arbitrarios
2. Se mida en unidades universales (bits)
3. Mantenga o mejore la discriminación

**Hipótesis original:** La información mutua topológica (MI) entre clasificaciones padre/hijo en el DAG debería discriminar — los dominios genuinos tendrían mayor acoplamiento informacional.

**Resultado:** La hipótesis es FALSA. MI no discrimina. Lo que sí discrimina es la *dirección* del flujo de información: la monotonicity topológica.

---

## II. Codificación Ternaria y Firmas Primas

Cada dominio asigna a cada primitivo uno de tres estados: D (DIRECTO=2), A (ANALÓGICO=1), N (NULL=0). Esto produce un vector ternario de 63 posiciones.

**Firma prima:** Para cada dominio, se computa:

```
Σ = Π(primo_i ^ estado_i)
```

donde `primo_i` es el número primo asignado al i-ésimo primitivo y `estado_i ∈ {0, 1, 2}`. Python maneja enteros de precisión arbitraria.

| Dominio | log₂(Σ) (bits) | Dígitos decimales |
|---------|----------------|-------------------|
| Lingüística | 693.65 | 209 |
| Psicología | 667.28 | 201 |
| Filosofía | 659.55 | 199 |
| Biología | 633.12 | 191 |
| Química | 595.21 | 180 |
| Física | 567.51 | 171 |
| Música | 542.64 | 164 |
| Matemáticas | 426.09 | 129 |
| Astrología | 265.57 | 80 |

Las 9 firmas son **únicas**, garantizado por el teorema fundamental de la aritmética. Cada dominio es un punto distinto en un espacio de 3^63 ≈ 1.14×10³⁰ asignaciones posibles.

**Interpretación:** La firma prima codifica la identidad algebraica completa del dominio. Dos dominios con la misma firma tendrían clasificaciones idénticas para los 63 primitivos — son el mismo dominio. La unicidad confirma que los 9 dominios son genuinamente diferentes.

---

## III. Entropía de Distribución

La entropía de Shannon de la distribución D/A/N mide la diversidad de clasificación:

```
H_dist = -Σ p_k × log₂(p_k),  k ∈ {D, A, N}
```

| Dominio | n_D | n_A | n_N | H_dist | H/H_max |
|---------|-----|-----|-----|--------|---------|
| Matemáticas | 23 | 20 | 20 | 1.582 | 0.998 |
| Física | 37 | 17 | 9 | 1.362 | 0.859 |
| Astrología | 4 | 37 | 22 | 1.234 | 0.778 |
| Filosofía | 40 | 18 | 5 | 1.223 | 0.771 |
| Música | 24 | 37 | 2 | 1.139 | 0.719 |
| Lingüística | 44 | 17 | 2 | 1.030 | 0.650 |
| Psicología | 44 | 17 | 2 | 1.030 | 0.650 |
| Química | 32 | 31 | 0 | 1.000 | 0.631 |
| Biología | 37 | 26 | 0 | 0.978 | 0.617 |

H_max = log₂(3) = 1.585 bits (distribución uniforme).

**NO discrimina.** Astrología (1.234 bits) cae dentro del rango de los dominios positivos. Matemáticas tiene la entropía máxima (casi uniforme: 23D/20A/20N), lo que refleja su naturaleza puramente abstracta — usa las tres categorías con frecuencias similares.

---

## IV. Ganancia de Información por Capas

La información mutua entre clase y capa mide cuánto la posición en la jerarquía predice la clasificación:

```
I(class; layer) = H(class) - H(class | layer)
```

| Dominio | H(class) | H(class\|layer) | I(class;layer) | I_norm |
|---------|----------|-----------------|----------------|--------|
| Matemáticas | 1.582 | 0.794 | 0.788 | 0.498 |
| Música | 1.139 | 0.727 | 0.412 | 0.362 |
| Física | 1.362 | 1.043 | 0.319 | 0.234 |
| Filosofía | 1.223 | 0.923 | 0.300 | 0.245 |
| Biología | 0.978 | 0.694 | 0.284 | 0.290 |
| Química | 1.000 | 0.786 | 0.214 | 0.214 |
| Astrología | 1.234 | 1.042 | 0.191 | 0.155 |
| Psicología | 1.030 | 0.920 | 0.110 | 0.106 |
| Lingüística | 1.030 | 0.943 | 0.087 | 0.085 |

Matemáticas tiene la mayor ganancia de información porque sus NULLs se concentran masivamente en L5–L6 (sentidos, vida, conciencia), mientras L1–L4 son D/A. Las capas predicen la clasificación. Pero Astrología (0.191) supera a Lingüística (0.087), así que **tampoco discrimina perfectamente**.

---

## V. Información Mutua Topológica: Por Qué NO Discrimina

**Esta es la sección clave del documento.**

Para cada dominio, se construye la tabla de contingencia 3×3 sobre las 128 aristas del DAG:

```
P(parent_class, child_class) sobre las 128 dependencias
```

| Dominio | D→D | D→A | D→N | A→D | A→A | A→N | N→D | N→A | N→N | MI | NMI |
|---------|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|------|
| Física | 62 | 29 | 13 | 9 | 3 | 3 | 0 | 5 | 4 | 0.094 | 0.107 |
| Matemáticas | 29 | 27 | 27 | 7 | 11 | 11 | 0 | 4 | 12 | 0.091 | 0.072 |
| Química | 55 | 51 | 0 | 4 | 18 | 0 | 0 | 0 | 0 | 0.051 | 0.077 |
| **Astrología** | **0** | **0** | **0** | **11** | **50** | **35** | **0** | **22** | **10** | **0.043** | **0.053** |
| Música | 33 | 57 | 4 | 7 | 27 | 0 | 0 | 0 | 0 | 0.032 | 0.038 |
| Lingüística | 80 | 32 | 4 | 6 | 6 | 0 | 0 | 0 | 0 | 0.017 | 0.037 |
| Biología | 66 | 45 | 0 | 7 | 10 | 0 | 0 | 0 | 0 | 0.011 | 0.020 |
| Psicología | 80 | 35 | 4 | 7 | 2 | 0 | 0 | 0 | 0 | 0.005 | 0.013 |
| Filosofía | 61 | 26 | 11 | 18 | 10 | 2 | 0 | 0 | 0 | 0.005 | 0.006 |

**Astrología NMI (0.053) > Filosofía NMI (0.006).**

### ¿Por qué MI falla?

MI mide *cualquier* dependencia estadística entre la clasificación del padre y la del hijo. No distingue entre:

1. **Acoplamiento genuino:** En Física, padre=D implica hijo≈D/A (nunca N en L1-4). La clasificación se propaga coherentemente por el DAG.

2. **Coherencia trivial:** En Astrología, 37/63 primitivos son A. La probabilidad base de A→A es alta simplemente por frecuencia. Astrología no tiene *ningún* padre D (los 4 DIRECTs son hojas sin hijos). Su MI viene de la asociación A→A y A→N, que es trivial.

MI no puede distinguir "el DAG predice la clasificación porque la estructura ontológica es real" de "la clasificación es tan uniforme que cualquier par tiende a coincidir".

---

## VI. Predictibilidad Topológica y Monotonicity

La monotonicity captura algo que MI no puede: la *dirección* del flujo de clasificación.

```
Monotonicity = fracción de aristas donde child_state ≤ parent_state
```

Con D=2, A=1, N=0, las transiciones monótonas son aquellas donde la clasificación "fluye hacia abajo" o se mantiene: D→D, D→A, D→N, A→A, A→N, N→N. Las violaciones son transiciones ascendentes: A→D, N→A, N→D.

| Dominio | P(D\|D) | P(A\|D) | P(D\|A) | P(A\|A) | Mono | Violaciones |
|---------|---------|---------|---------|---------|------|-------------|
| Química | 0.519 | 0.481 | 0.182 | 0.818 | 0.969 | 4 |
| Lingüística | 0.690 | 0.276 | 0.500 | 0.500 | 0.953 | 6 |
| Música | 0.351 | 0.606 | 0.206 | 0.794 | 0.945 | 7 |
| Biología | 0.595 | 0.405 | 0.412 | 0.588 | 0.945 | 7 |
| Psicología | 0.672 | 0.294 | 0.778 | 0.222 | 0.945 | 7 |
| Matemáticas | 0.349 | 0.325 | 0.241 | 0.379 | 0.914 | 11 |
| Física | 0.596 | 0.279 | 0.600 | 0.200 | 0.891 | 14 |
| Filosofía | 0.622 | 0.265 | 0.600 | 0.333 | 0.859 | 18 |
| **Astrología** | **—** | **—** | **0.115** | **0.521** | **0.742** | **33** |

Gap monotonicidad: 0.117 (Filosofía 0.859 → Astrología 0.742).

### ¿Por qué monotonicity SÍ funciona?

En un dominio válido, si un padre es DIRECTO (el dominio lo "usa" directamente), sus hijos tienden a ser DIRECTOS o ANALÓGICOS — nunca "más directos" que el padre. La estructura ontológica fluye coherentemente por las capas.

En Astrología, las 4 únicas clasificaciones DIRECTAS son los elementos (tierra, agua, aire, fuego) en L5. Sus padres (fuerza, contención, orden, mover, creación, destrucción) están en L2–L3 y son ANALÓGICOS. Esto invierte el flujo: hijos D con padres A. 11 violaciones vienen solo de los 4 elementos.

Además, los 22 NULLs de Astrología en L2–L4 (porque, si_entonces, caos, hacer, verdad, mentira, etc.) son padres de primitivos A en L3–L5, generando 22 violaciones más (A>N: child=1, parent=0).

Total: 33 violaciones de monotonicity (vs 4–18 en dominios positivos).

---

## VII. Redundancia: Bits Ahorrados por Estructura

| Medida | Fórmula | Significado |
|--------|---------|-------------|
| H_max | 63 × log₂(3) = 99.85 bits | Asignación aleatoria |
| H_marginal | 63 × H(class) | Asumiendo independencia entre posiciones |
| H_structured | 63 × H(class\|layer) | Conociendo la capa |
| R_layer | H_marginal − H_structured | Bits ahorrados por las capas |
| R_topo | 128 × MI | Bits ahorrados por la topología |

| Dominio | H_marg | H_struct | R_layer | R_topo | R_total |
|---------|--------|----------|---------|--------|---------|
| Matemáticas | 99.65 | 50.03 | 49.61 | 11.63 | 61.24 |
| Física | 85.80 | 65.69 | 20.11 | 12.00 | 32.11 |
| Música | 71.78 | 45.82 | 25.96 | 4.04 | 30.00 |
| Química | 62.99 | 49.53 | 13.46 | 6.50 | 19.95 |
| Filosofía | 77.02 | 58.15 | 18.87 | 0.65 | 19.52 |
| Biología | 61.61 | 43.72 | 17.89 | 1.44 | 19.32 |
| Astrología | 77.71 | 65.67 | 12.04 | 5.52 | 17.56 |
| Lingüística | 64.87 | 59.38 | 5.49 | 2.15 | 7.64 |
| Psicología | 64.87 | 57.96 | 6.91 | 0.63 | 7.54 |

Matemáticas tiene la mayor redundancia total (61 bits) porque sus NULLs en L5–L6 crean un gradiente predecible: conociendo la capa, se puede adivinar la clasificación con alta confianza. Esto es redundancia "genuina" — refleja que las matemáticas puras *realmente* no usan sentidos ni conciencia.

---

## VIII. Distancia de Hamming y Geometría de Dominios

**Hamming simple** (posiciones diferentes, de 63 posibles):

| | Mus | Chem | Bio | Math | Phil | Phys | Ling | Psy | Astr |
|---|-----|------|-----|------|------|------|------|-----|------|
| Mus | 0 | 16 | 13 | 32 | 29 | 24 | 30 | 20 | **42** |
| Chem | 16 | 0 | 11 | 33 | 26 | 18 | 28 | 16 | **44** |
| Bio | 13 | 11 | 0 | 35 | 28 | 22 | 27 | 11 | **46** |
| Math | 32 | 33 | 35 | 0 | 36 | 25 | 36 | 33 | **44** |
| Phil | 29 | 26 | 28 | 36 | 0 | 26 | 22 | 27 | **54** |
| Phys | 24 | 18 | 22 | 25 | 26 | 0 | 26 | 14 | **49** |
| Ling | 30 | 28 | 27 | 36 | 22 | 26 | 0 | 22 | **51** |
| Psy | 20 | 16 | 11 | 33 | 27 | 14 | 22 | 0 | **49** |
| Astr | **42** | **44** | **46** | **44** | **54** | **49** | **51** | **49** | 0 |

**Clusters identificados:**
- **Cluster material:** Química–Biología (d=11). Los dominios que estudian materia comparten el mayor número de clasificaciones.
- **Cluster fenomenológico:** Biología–Psicología (d=11), Música–Biología (d=13). Dominios del cuerpo y la experiencia.
- **Outlier abstracto:** Matemáticas. Distancia alta a todos (25–36) porque es el único dominio con 20 NULLs.
- **Outlier control:** Astrología. Distancia mínima 42, máxima 54. Aislada de todos.

**MDS 2D** (68.7% de varianza explicada):

Astrología se proyecta a (-38.7, 3.1), masivamente separada del cluster positivo. Los 8 dominios positivos forman un grupo cohesivo en x ∈ [-7, 13], y ∈ [-22, 11].

---

## IX. IDVS: Coverage × Monotonicity

```
IDVS = Coverage_L14 × Monotonicity_topo
```

| Componente | Definición | Qué mide |
|------------|-----------|----------|
| Coverage_L14 | 1 − (NULLs en L1–4 / total L1–4) | ¿El dominio cubre la estructura abstracta? |
| Monotonicity | Fracción de aristas con child_state ≤ parent_state | ¿La clasificación respeta el DAG? |

**Propiedades:**
- Sin pesos arbitrarios — producto multiplicativo
- Ambos factores están en [0, 1]
- Un solo factor bajo basta para penalizar (multiplicativo > aditivo)
- Fundamentado en teoría de información: Coverage es un constraint entrópico, Monotonicity es un constraint topológico

| Dominio | Cov_L14 | Mono | IDVS | DVS_orig | Resultado |
|---------|---------|------|------|----------|-----------|
| Química | 1.000 | 0.969 | **0.969** | 0.777 | ✓ PASS |
| Lingüística | 1.000 | 0.953 | **0.953** | 0.853 | ✓ PASS |
| Música | 1.000 | 0.945 | **0.945** | 0.741 | ✓ PASS |
| Biología | 1.000 | 0.945 | **0.945** | 0.813 | ✓ PASS |
| Psicología | 1.000 | 0.945 | **0.945** | 0.903 | ✓ PASS |
| Matemáticas | 1.000 | 0.914 | **0.914** | 0.645 | ✓ PASS |
| Física | 1.000 | 0.891 | **0.891** | 0.751 | ✓ PASS |
| Filosofía | 1.000 | 0.859 | **0.859** | 0.843 | ✓ PASS |
| **Astrología** | **0.632** | **0.742** | **0.469** | 0.360 | ✗ FAIL |

---

## X. Comparación con DVS Original

| Propiedad | DVS | IDVS |
|-----------|-----|------|
| Fórmula | 0.30M1 + 0.25M2 + 0.20M3 + 0.15M4 + 0.10M5 | Coverage × Monotonicity |
| Pesos | 5 pesos ad-hoc | Ninguno |
| Sub-métricas | 5 (coverage, depth, authenticity, engagement, anchor quality) | 2 (coverage, monotonicity) |
| Gap | 0.285 (Matemáticas 0.645 → Astrología 0.360) | 0.391 (Filosofía 0.859 → Astrología 0.469) |
| Dominio más bajo (positivo) | Matemáticas (0.645) | Filosofía (0.859) |
| Unidades | Adimensional | Adimensional (derivable de bits) |
| Sensibilidad a pesos | Alta — cambiar pesos cambia el gap | Ninguna — no hay pesos |

**Ventaja clave:** IDVS no penaliza a Matemáticas por tener NULLs en L5–L6. Los NULLs de Matemáticas son *correctos* (las matemáticas puras genuinamente no involucran sentidos ni conciencia). DVS los penaliza a través de M2 (Mapping Depth = DIRECT/63) y M4 (Dependency Engagement). IDVS solo penaliza NULLs en L1–L4, que indican falta de cobertura de la estructura abstracta fundamental.

### Análisis de sensibilidad

| Variante | Fórmula | Gap | ¿Discrimina? |
|----------|---------|-----|---------------|
| IDVS (producto) | Cov × Mono | 0.391 | ✓ SÍ |
| IDVS (raíz) | √(Cov × Mono) | 0.242 | ✓ SÍ |
| IDVS (harmónica) | 2CovMono/(Cov+Mono) | 0.242 | ✓ SÍ |
| Solo Monotonicity | Mono | 0.117 | ✓ SÍ |

IDVS es robusto bajo todas las variantes. El producto maximiza el gap porque Coverage y Monotonicity penalizan a Astrología de forma independiente y multiplicativa.

---

## XI. Predicciones Falsificables

1. **Nuevo dominio genuino (ej. Economía, Sociología):**
   - IDVS ≥ 0.85 (Coverage_L14 = 1.0, Monotonicity ≥ 0.85)
   - Hamming a Astrología ≥ 40
   - Firma prima única

2. **Nuevo pseudo-dominio (ej. Numerología, Feng Shui):**
   - IDVS < 0.60
   - Coverage_L14 < 0.80 (NULLs en estructura abstracta)
   - Monotonicity < 0.80 (violaciones D→A en el DAG)

3. **MI nunca discriminará:**
   - Para cualquier pseudo-dominio con coherencia interna (mayoría A→A), MI será comparable a dominios genuinos como Filosofía

4. **El gap IDVS es falsificable:**
   - Si existe un pseudo-dominio con Coverage_L14 = 1.0 y Monotonicity ≥ 0.859, IDVS fallaría
   - Esto requeriría un dominio que cubra toda la estructura abstracta Y respete el flujo del DAG, lo cual es la definición operacional de un dominio genuino

---

## XII. Conclusión

La información mutua topológica — la hipótesis original — no discrimina entre dominios genuinos y pseudo-científicos. MI captura cualquier dependencia estadística, incluyendo la coherencia trivial A→A de Astrología.

Lo que sí discrimina es la **monotonicity topológica**: la fracción de aristas del DAG donde la clasificación del hijo no excede la del padre. En dominios genuinos, la clasificación fluye coherentemente por la jerarquía. En Astrología, los 4 DIRECTs (elementos en L5) violan la monotonicity con sus padres ANALÓGICOS en L2–L3, y los 22 NULLs en L2–L4 crean violaciones adicionales cuando son padres de nodos ANALÓGICOS.

**IDVS = Coverage_L14 × Monotonicity** captura dos constraints independientes:
- **Coverage:** ¿El dominio cubre la estructura abstracta? (capas 1–4)
- **Monotonicity:** ¿La clasificación respeta la dirección del DAG?

Con gap = 0.391 (37% más amplio que DVS), sin pesos arbitrarios, y robusto bajo variantes algebraicas, IDVS reemplaza al DVS como la métrica principal de validez de dominio.

La firma prima demuestra que cada dominio es algebraicamente único. La geometría de Hamming revela clusters naturales (material, fenomenológico, abstracto) y el aislamiento geométrico de Astrología. Todo medible en bits, todo falsificable, todo sin parámetros libres.
