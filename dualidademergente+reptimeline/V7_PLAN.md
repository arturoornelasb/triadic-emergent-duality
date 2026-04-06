# V7: Plan de Entrenamiento y Flujo Iterativo

## Estado actual: COMPLETADO — NO CONVERGIO (2026-03-31)

- **GPU:** RTX 4060 Ti 16GB
- **Steps:** 200,000 (~24h estimado)
- **Checkpoint:** `model/checkpoints/v7_contrastive/`
- **Monitor:** doble click `model/monitor_v7.bat`

---

## Que cambio de V6 a V7

### Problema principal: 529 conceptos colisionados en V6

V6 tenia 2,166 conceptos pero solo 1,801 firmas unicas (83.1%). 164 grupos
de conceptos compartian la misma firma gold. El grupo mas grande: 36 conceptos
de astrofisica con identica firma de 19 bits.

**Causa raiz:** El generador de gold (`generate_gold_extended.py`) usaba 3 capas:
1. Domain fingerprint (mismo para todo el dominio)
2. Keyword matching (substring — demasiado generico)
3. Dependency expansion (mismos deps para conceptos similares)

Resultado: conceptos del mismo subdominio → mismos bits → el modelo NO PUEDE distinguirlos.

### Solucion V7: 3 capas nuevas

| Capa | V6 | V7 |
|------|----|----|
| 1. Domain fingerprint | Si | Si |
| 2. Keyword matching | Substring | Substring + stem matching |
| 3. Dependency expansion | Si | Si |
| 4. **Subdomain fingerprint** | No | **Max 5 bits discriminativos por subdominio** |
| 5. **Word-level matching** | No | **Stem-like, keywords ≥4 chars** |
| 6. **Collision breaker** | No | **Hash de texto → flip 1-2 bits underused** |

**Resultado:** 2,166/2,166 firmas unicas (100%).

### Cambios en entrenamiento

| Parametro | V6 | V7 | Razon |
|-----------|----|----|-------|
| Gold file | v6 (83.1% unique) | v7 (100% unique) | Eliminar colisiones en targets |
| Steps | 100,000 | 200,000 | 46 triadic steps/concepto vs 24 |
| entropy_weight | 1.0 | 2.0 | V6 tenia 24 dead bits (33%) |
| contrast_weight | 0 (no existia) | 1.0 | Anti-colision en firmas aprendidas |
| triadic_warmup | 50% | 35% | Mas tiempo de aprendizaje triadico |
| n_sample | 128 | 128 | Mismo (seguro para 16GB VRAM) |

### Nuevo: Anti-collision loss

```python
concept_contrastive_loss(model, concepts, targets, n_sample=64, margin=0.3)
```

Samplea pares de conceptos. Para cada par:
- Calcula similaridad gold (Jaccard de bit patterns)
- Calcula similaridad aprendida (cosine de proyecciones)
- Penaliza cuando learned_sim > gold_sim + margin

Esto FUERZA al modelo a diferenciar conceptos que tienen targets diferentes.

---

## Flujo Iterativo del Programa

```
                    ┌──────────────────────────────────┐
                    │                                  │
                    ▼                                  │
    ┌─────────────────────────────┐                    │
    │  [1] DEFINIR ANCLAS         │                    │
    │  72 primitivos + conceptos  │                    │
    │  gold_extended_v7.json      │                    │
    └──────────┬──────────────────┘                    │
               │                                       │
               ▼                                       │
    ┌─────────────────────────────┐                    │
    │  [2] ENTRENAR               │                    │
    │  GPT-2 frozen + triadic head│                    │
    │  L = L_lang + α(L_tri +    │                    │
    │    L_sup + L_sub + L_ctr)   │                    │
    │  200K steps, ~24h           │                    │
    └──────────┬──────────────────┘                    │
               │                                       │
               ▼                                       │
    ┌─────────────────────────────┐                    │
    │  [3] EVALUAR ALGEBRAICAMENTE│                    │
    │  (sin evaluadores humanos)  │                    │
    │                             │                    │
    │  • Bit accuracy vs gold     │                    │
    │  • Subsumcion (A ⊇ B)      │                    │
    │  • Regla de Tres (A:B=C:D)  │                    │
    │  • Dead bits / entropy      │                    │
    │  • Colisiones aprendidas    │                    │
    └──────────┬──────────────────┘                    │
               │                                       │
               ▼                                       │
    ┌─────────────────────────────┐                    │
    │  [4] AUDITAR EN CONCEPTFLOW │  ← otro agente    │
    │                             │    integrando      │
    │  • Jaccard similarity       │                    │
    │  • MCD/MCM (bits comunes)   │                    │
    │  • Clasificacion oposicion  │                    │
    │    (Aristoteles, computada) │                    │
    │  • Algebra por capas (6)    │                    │
    │  • 10 vistas de visualizacion                    │
    └──────────┬──────────────────┘                    │
               │                                       │
               ▼                                       │
    ┌─────────────────────────────┐                    │
    │  [5] DIAGNOSTICAR           │                    │
    │  reptimeline (P3)           │                    │
    │                             │                    │
    │  • Cristalizacion temporal  │                    │
    │  • Nacimiento/muerte de bits│                    │
    │  • Dependencias entre bits  │                    │
    │  • Reconciler vs ontologia  │                    │
    └──────────┬──────────────────┘                    │
               │                                       │
               ▼                                       │
    ┌─────────────────────────────┐                    │
    │  [6] REFINAR                │────────────────────┘
    │                             │
    │  • Ajustar gold para        │
    │    conceptos debiles        │
    │  • Modificar hiperparametros│
    ��  • Agregar/quitar conceptos │
    │  → V8, V9, ...             │
    └─────────────────────────────┘
```

### La validacion es algebraica, no humana

El sistema se valida a si mismo:

| Operacion | Que verifica | Como |
|-----------|-------------|------|
| Subsumcion | A contiene todos los bits de B | `(A & B) == B` |
| Regla de Tres | A:B = C:D proporcionalmente | `D_pred = C + (B - A)`, cosine vs D_real |
| Jaccard | Similaridad entre conceptos | `\|A ∩ B\| / \|A ∪ B\|` |
| MCD | Bits compartidos | `A AND B` |
| MCM | Union de conceptos | `A OR B` |
| Oposicion | Tipo aristotelico | Patron de bits compartidos/exclusivos |

Si estas operaciones producen resultados semanticamente coherentes, las firmas son validas.
Los evaluadores humanos (K2) agregan credibilidad al paper pero NO son bloqueadores del sistema.

---

## Resultados V7 (2026-03-31)

**Duracion:** 76.5 horas (200K steps en RTX 5060 Ti 16GB)

### Metricas finales vs V6

| Metrica | V6 | Target V7 | **V7 real** | Resultado |
|---------|----|----|----|----|
| Bit accuracy (test) | 80.9% | >83% | **79.3%** | FAIL (-1.6%) |
| Colisiones aprendidas | 1,703 | <100 | **~1,580** | FAIL (337 groups) |
| Dead bits | 24 | <15 | **32** | FAIL (peor) |
| Primitivo accuracy | 0.63 | >0.70 | **0.907** | PASS (+0.277) |
| Subsumption rate | 95.2% | >95% | **91.0%** | FAIL (-4.2%) |
| Unique signatures | 463 (21.4%) | >90% | **586 (27.1%)** | PARCIAL (+5.7%) |
| Dual coherence mean | - | >0.60 | **0.731** | PASS |
| verdad/mentira dual | 0.33 | >0.60 | **0.335** | FAIL |
| orden/caos dual | 0.23 | >0.50 | **0.138** | FAIL |

**Resumen:** Primitivos mejoraron dramaticamente (0.63→0.91), pero el modelo NO convergio
para los ~2,100 conceptos extendidos. Colisiones y dead bits empeoraron.

### reptimeline — Diagnostico temporal (20 checkpoints)

```
Fases detectadas:
  [1] Steps 5K-65K:  FROZEN (warmup, triadic loss = 0)
      entropy=0.077, churn=0.0, utilization=0.03

  [2] Step 75K:      PHASE TRANSITION (triadic loss arranca)
      entropy 0.077→0.479, churn 0→1.0, utilization 0.03→0.40

  [3] Steps 75K-200K: REFINAMIENTO LENTO (no converge)
      entropy 0.479→0.518, churn 1.0→0.711, utilization 0.40→0.43
```

**Hallazgos clave:**
- Churn rate **71% al final** — los bits siguen cambiando, el modelo no encontro optimo
- Solo tuvo **130K effective triadic steps** (70K desperdiciados en warmup)
- Bit accuracy plateau en 79.3% desde step 100K — sin mejora en ultimos 100K steps
- Subsumption BAJO de 0.95 (step 72K) a 0.91 (200K) — regresion
- 3 bits colapsados a "siempre on" (bits 2, 10, 11 con >97% activation rate)
- Bits mas inestables: 8, 27, 68, 49, 23 (stability <0.90)
- Bits mas estables: 45, 64, 41, 42, 11 (stability >0.997)

**Dual coherence por par:**

| Par | Score | Estado |
|-----|-------|--------|
| union/separacion | 0.935 | OK |
| mover/quietud | 0.991 | OK |
| creacion/destruccion | 0.806 | OK |
| bien/mal | 0.903 | OK |
| libertad/control | 0.679 | OK |
| placer/dolor | 0.714 | OK |
| consciente/ausente | 0.999 | OK |
| individual/colectivo | 0.999 | OK |
| temporal/eterno | 0.999 | OK |
| receptivo/creador | 0.996 | OK |
| **orden/caos** | **0.138** | **LOW** |
| **verdad/mentira** | **0.335** | **LOW** |
| **vida/muerte** | **0.488** | **LOW** |
| **atraccion/aversion** | **0.248** | **LOW** |

**Layer emergence:**

| Capa | Primitivos | Median activation step |
|------|-----------|----------------------|
| 1 | 3/3 | 75,000 (ultimo — mas abstracto) |
| 2 | 8/8 | 5,000 |
| 3 | 13/13 | 5,000 |
| 4 | 21/21 | 5,000 |
| 5 | 23/23 | 5,000 |
| 6 | 4/4 | 85,000 |

### Causas raiz identificadas

1. **Warmup demasiado largo (35% = 70K steps)** — solo 130K effective triadic steps
2. **contrast_weight=1.0 pelea con supervision** — gradientes opuestos
3. **LR floor demasiado alto** — cosine decay a lr*0.1 = 3e-5, churn 71% sugiere aun alto
4. **Linear head sin capacidad** — 74K params para distinguir 2,166 conceptos con 72 bits
5. **entropy_weight=2.0 insuficiente** — 32 dead bits persisten (peor que V6)

### Archivos generados

| Archivo | Que es |
|---------|--------|
| `neural/results/timeline_v7.json` | Timeline completo (1.9GB, 20 snapshots × 2166 conceptos) |
| `neural/results/v7_curves.csv` | Entropy, churn, utilization por step |
| `neural/results/v7_phase_transitions.json` | 3 transiciones detectadas |
| `neural/results/v7_bit_stability.json` | Estabilidad por bit (72 scores) |
| `runs/v7_contrastive/plots/phase_dashboard.png` | Dashboard de fases |
| `runs/v7_contrastive/plots/churn_heatmap.png` | Heatmap de churn por bit |
| `runs/v7_contrastive/plots/swimlane_primitivos.png` | Swimlane (7 primitivos) |
| `runs/v7_contrastive/plots/layer_emergence.png` | Orden de emergencia por capa |

---

## V8: Plan basado en diagnostico reptimeline

### Cambios V7 → V8

| Parametro | V7 | V8 | Razon (reptimeline) |
|-----------|----|----|------|
| warmup | 35% (70K wasted) | **10%** (25K) | 225K effective vs 130K |
| contrast_weight | 1.0 | **0.3** | Gradientes opuestos con supervision |
| entropy_weight | 2.0 | **3.0** | 32 dead bits persisten |
| lr_min_ratio | 0.1 (3e-5 floor) | **0.03** (1e-5 floor) | Churn 71% = LR alto al final |
| head_mode | simple (74K params) | **deep** (561K params) | Mas capacidad para 2,166 conceptos |
| steps | 200K | **250K** | Con 10% warmup = 225K effective |

### Hipotesis V8

1. **Deep head** da la capacidad que falta para distinguir 2,166 conceptos
2. **Menos warmup** duplica los triadic steps efectivos
3. **LR decay mas agresivo** permite convergencia (churn → 0)
4. **Contrast_weight reducido** deja que supervision domine
5. **Mas entropy weight** ataca los dead bits directamente

### Resultados V8 (2026-04-05) — COMPLETADO

**Duracion:** ~100h (250K steps en RTX 5060 Ti 16GB)

#### Metricas finales V8 vs V7

| Metrica | V7 (200K) | V8 (250K) | Resultado |
|---------|-----------|-----------|-----------|
| Bit accuracy (test) | 79.3% | **85.3%** | **+6.0pp** |
| Subsumption (test) | 91.0% | **95.7%** | **+4.7pp** |
| Dead bits | 32 | **25** | **-7 bits** |
| Entropy | ~0.48 | **0.554** | **+15%** |
| Sup loss | 0.384 | **0.311** | **-19%** |

#### Kill criteria V8

| Criterio | Umbral | Resultado | Estado |
|----------|--------|-----------|--------|
| bit_acc_test | > 80% | 85.3% | **PASS** |
| churn final | < 50% | 48.9% | **PASS (barely)** |
| dead_bits | < 25 | 25 | **BORDERLINE** |

#### reptimeline — Diagnostico temporal V8 (25 checkpoints)

```
Fases detectadas:
  [1] Steps 5K-25K:   WARMUP (triadic loss = 0)
      entropy=0.058, churn=0.0, utilization=0.027

  [2] Step 35K:        PHASE TRANSITION (triadic loss arranca)
      entropy 0.058→0.500, churn 0→1.0, utilization 0.03→0.33

  [3] Steps 35K-250K:  REFINAMIENTO (convergencia parcial)
      entropy 0.500→0.554, churn 1.0→0.489, utilization 0.33→0.341
```

**Comparacion de fases V7 vs V8:**
- Phase transition: **35K** (V8) vs 75K (V7) — 2× mas temprano gracias a warmup 10%
- Churn final: **48.9%** (V8) vs 71% (V7) — LR decay 0.03 funciono parcialmente
- Entropy final: **0.554** (V8) vs ~0.48 (V7) — entropy_weight 3.0 activo mas bits
- Births: 133K, Deaths: 75K — crecimiento neto positivo (mas estructura)

**Bits mas estables:** 1, 55, 22, 70, 39
**Bits menos estables:** 6, 12, 51, 14, 26

**Conexiones null model:** O/E = 1.000 (consistente con V7, MNIST, Pythia)

### Que funciono en V8

1. **Deep head (+6pp bit accuracy)** — la capacidad extra fue el cambio mas impactante
2. **Warmup 10% (phase transition 2× antes)** — 225K effective triadic steps vs 130K
3. **Entropy weight 3.0 (-7 dead bits)** — de 32 a 25
4. **LR decay 0.03 (-22pp churn)** — de 71% a 48.9%

### Que NO se resolvio

- Churn 48.9% — aun alto, conceptos extendidos no convergieron del todo
- Dead bits 25 — borderline en el kill criterion
- Extended concepts siguen siendo el reto principal (primitivos a 90.7%+, extended lag)

### Archivos generados V8

| Archivo | Que es |
|---------|--------|
| `neural/results/timeline_v8.json` | Timeline completo (25 snapshots × 2166 conceptos) |
| `neural/results/v8_curves.csv` | Entropy, churn, utilization por step |
| `neural/results/v8_phase_transitions.json` | 3 transiciones detectadas (step 35K) |
| `neural/results/v8_bit_stability.json` | Estabilidad por bit (72 scores) |
| `neural/results/v8_connections_null.json` | Null model O/E = 1.000 |
| `runs/v8_deep/plots/phase_dashboard.png` | Dashboard de fases |
| `runs/v8_deep/plots/churn_heatmap.png` | Heatmap de churn por bit |
| `runs/v8_deep/plots/swimlane_primitivos.png` | Swimlane (7 primitivos) |
| `runs/v8_deep/plots/layer_emergence.png` | Orden de emergencia por capa |

---

## Archivos clave (todo el programa)

| Archivo | Que es |
|---------|--------|
| `model/train.py` | Script de entrenamiento (+concept_contrastive_loss, +lr-min-ratio) |
| `model/gpt2_triadic.py` | Arquitectura del modelo (simple + deep head) |
| `model/generate_gold_extended_v7.py` | Generador de gold V7 (6 capas) |
| `model/gold_extended_v7.json` | 2,166 conceptos, 100% unique |
| `model/run_v7.bat` | Lanzar V7 (completado) |
| `model/run_v8.bat` | Lanzar V8 (preparado) |
| `model/monitor_v7.bat` | Monitorear progreso |
| `model/save_v7_timeline.py` | Extraer timeline + plots V7 |
| `model/checkpoints/v7_contrastive/` | V7 checkpoints (40) + training_log.csv |
