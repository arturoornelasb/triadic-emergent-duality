# V4 Analysis — 72-bit Circle (Expansion v1.1)

**Fecha:** 2026-03-23
**Cambio único vs v3:** Círculo expandido de 65 → 72 primitivos (7 nuevos: atracción, decaimiento, aversión, cooperación, pérdida, atención, intención)

---

## 1. Métricas de entrenamiento

| Métrica | v3 (65 bits) | v4 (72 bits) | Delta |
|---------|-------------|-------------|-------|
| Best bit accuracy (test) | 90.89% | **92.46%** | +1.57% |
| Final bit accuracy (test) | 90.18% | **91.77%** | +1.59% |
| Subsumption (test) | **99.03%** | 96.67% | -2.36% |
| Dead bits | 47/65 (72%) | 52/72 (72%) | mismo ratio |
| Entropy | 0.322 | 0.324 | ~igual |
| Final loss | 4.566 | 4.570 | ~igual |
| Tiempo | 5.8h | 5.8h | igual |

## 2. Coherencia dual — LA GRAN MEJORA

| Par dual | v3 | v4 | Delta | Nota |
|----------|-----|-----|-------|------|
| placer/dolor | 0.286 | **0.971** | +0.685 | De colapsado a casi perfecto |
| vida/muerte | 0.175 | **0.667** | +0.491 | De colapsado a funcional |
| consciente/ausente | 0.660 | **1.000** | +0.340 | Perfecto |
| mover/quietud | 0.396 | **0.636** | +0.240 | Mejora significativa |
| individual/colectivo | 0.685 | **0.881** | +0.196 | Bien |
| bien/mal | 0.889 | **1.000** | +0.111 | Perfecto |
| verdad/mentira | 0.812 | **0.909** | +0.097 | Bien |
| receptivo/creador_obs | 0.692 | **0.773** | +0.080 | Mejora modesta |
| libertad/control | **0.938** | 0.921 | -0.016 | ~igual |
| temporal_obs/eterno_obs | **1.000** | 0.875 | -0.125 | Ligera regresión |
| atracción/aversión | - | **1.000** | nuevo | Par nuevo, perfecto |

**Media de coherencia:** v3=0.653 → v4=**0.876** (+0.223)

### Pares que estaban colapsados en v3 (coherencia < 0.5):
- placer/dolor: 0.286 → **0.971** ✓ RESUELTO
- vida/muerte: 0.175 → **0.667** ✓ MEJORADO (todavía no perfecto)
- mover/quietud: 0.396 → **0.636** ✓ MEJORADO

## 3. Análisis aprendido

| Métrica | v3 | v4 | Delta |
|---------|-----|-----|-------|
| Unique learned | 58/65 (89.2%) | **72/72 (100%)** | +10.8% |
| Active bits | 65 | 68 | +3 |
| Discovered duals | 377 | 313 | -64 |
| Discovered deps | 287 | **516** | +229 |
| Discovered triadic | 779 | 293 | -486 |

**100% firmas únicas** — el modelo diferencia los 72 conceptos perfectamente.

## 4. Per-domain accuracy (aprendido vs target)

| Capa | v3 | v4 | Delta |
|------|-----|-----|-------|
| 1 (Boolean) | 0.615 | 0.556 | -0.060 |
| 2 (Fuzzy) | 0.600 | 0.582 | -0.018 |
| 3 (Ordinal) | 0.664 | 0.620 | -0.044 |
| 4 (Modal) | 0.606 | 0.556 | -0.050 |
| 5 (Trivalent) | 0.603 | 0.583 | -0.020 |
| 6 (Probabilistic) | **0.885** | 0.688 | -0.197 |

**Todas las capas bajaron.** El modelo está aprendiendo firmas MÁS ÚNICAS (100% vs 89%) pero MENOS parecidas a los targets. Está encontrando su propia estructura en vez de replicar exactamente lo que le pedimos.

## 5. Separación por capa

| Capa | Within sim | Between sim | Separation ratio |
|------|-----------|-------------|-----------------|
| 1 (Boolean) | 0.634 | 0.618 | 1.025 |
| 2 (Fuzzy) | 0.430 | 0.510 | 0.843 |
| 3 (Ordinal) | 0.506 | 0.537 | 0.942 |
| 4 (Modal) | 0.577 | 0.584 | 0.986 |
| 5 (Trivalent) | 0.718 | 0.531 | **1.353** |
| 6 (Probabilistic) | 0.653 | 0.436 | **1.496** |

**Capas 5 y 6 muestran la mejor separación** — los primitivos de vida/conciencia y meta-observación forman clusters distintos.

## 6. Perplejidad (degradación de lenguaje)

| Modelo | PPL | Status |
|--------|-----|--------|
| Base GPT-2 Medium | 31.95 | REF |
| v1 | 2,777 | DEGRADADO |
| v2 | 6,735 | DEGRADADO |
| v3 | 5,388 | DEGRADADO |
| v4 | 5,608 | DEGRADADO |

**Catastrophic forgetting en todas las runs.** El modelo olvida el lenguaje general porque el training data es demasiado pequeño (72 definiciones cortas x 50K pasos). Esto NO afecta la cabeza triádica pero el modelo ya no puede generar texto coherente.

## 7. Regla de tres (v4)

```
good:evil=truth:lie                           cos=+0.898  bits=95.8%
creation:destruction=life:death               cos=+0.898  bits=94.4%
freedom:control=individual:collective         cos=+0.872  bits=94.4%
pleasure:pain=conscious:absent                cos=+0.960  bits=98.6%
union:separation=order:chaos                  cos=+0.931  bits=97.2%
move:stillness=mortal_observer:eternal_observer cos=+0.836  bits=91.7%
receptive:creator_observer=truth:lie          cos=+0.785  bits=90.3%
creation:destruction=union:separation         cos=+0.907  bits=94.4%
Media: cosine=+0.886  bit_accuracy=94.6%
```

## 8. Validación de predicciones algebraicas

| Predicción | Resultado |
|------------|-----------|
| P1: Distancia algebraica → coherencia | PARCIAL — los pares inter-capa mejoraron más |
| P2: 72-bit no arregla Jaccard colapsados | **REFUTADA** — la coherencia mejoró masivamente |
| P3: Transiciones > internos | INCONCLUSO — per-domain bajó uniformemente |
| P4: Capa 6 coherencia más baja | **REFUTADA** — capa 6 tiene separation ratio más alto (1.496) |
| P5: D14 alta varianza | PENDIENTE |

### Por qué P2 fue refutada (hallazgo clave)

Los 7 nuevos primitivos NO cambian las firmas de los pares existentes (están ARRIBA en el DAG). Sin embargo, dan al modelo más CONTEXTO de entrenamiento:
- atracción/aversión (Jaccard=0.200) enseñan al modelo qué es un par dual bien diferenciado
- decaimiento depende de muerte pero no de vida → señal implícita de diferenciación
- El modelo generalizó esta señal a los pares colapsados existentes

**Conclusión: más diversidad en el training set > targets más distintos.**

## 9. Diagnóstico para v5

### Problemas resueltos
- ✅ Pares colapsados: 3 de 3 resueltos o mejorados significativamente
- ✅ Uniqueness: 100% (era 89% en v3)
- ✅ Coherencia dual media: 0.876 (era 0.653)

### Problemas pendientes
- ❌ Catastrophic forgetting (PPL 5608 vs baseline 31.95)
- ❌ Per-domain accuracy bajó (~0.59 vs ~0.66 en v3)
- ❌ 52/72 dead bits (72% del espacio no discrimina)
- ❌ Bits con alta tasa de false positives (si_entonces, proporción, olfato: <10% accuracy)
- ⚠️ vida/muerte todavía no perfecto (0.667)

### Prioridad para v5
1. **CRÍTICO: Resolver catastrophic forgetting** — sin esto el modelo no sirve para nada práctico
2. Reducir dead bits (¿normalización por capa? ¿loss ponderado?)
3. Mejorar per-bit accuracy de los peores bits (false positives masivos)
