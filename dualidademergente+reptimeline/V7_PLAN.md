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

## V9: GPT-Neo 125M / OpenWebText — Segundo modelo (N>1)

### Motivacion

Debilidad #5 (N=1): toda la evidencia neural venia de un solo modelo (GPT-2 Medium).
V9 entrena un modelo completamente diferente (arquitectura, dataset, escala) para
verificar replicabilidad de los hallazgos.

### Cambios V8 → V9

| Parametro | V8 | V9 | Razon |
|-----------|----|----|-------|
| Modelo base | GPT-2 Medium (345M) | **GPT-Neo 125M** | Arquitectura diferente (N>1) |
| Dataset | TinyStories | **OpenWebText 100K docs** | Dataset diferente (N>1) |
| Steps | 250,000 | **50,000** | Suficiente para convergencia |
| save-every | 5,000 | **5,000** | Mismo |
| head_mode | deep | deep | Mismo |
| activation | ifsq | ifsq | Mismo |
| bits | 72 | 72 | Mismo |

### Resultados V9 (2026-04-07) — COMPLETADO

**Duracion:** ~6h (50K steps en RTX 4060 Ti 16GB)

#### Metricas finales

| Metrica | V8 (250K) | V9 (50K) |
|---------|-----------|----------|
| Bit accuracy (test) | 85.3% | **83.2%** |
| Subsumption (test) | 95.7% | **93.1%** |
| Dead bits | 25 | **30** |
| Entropy | 0.554 | **0.545** |

#### Neural probes Q1-Q9

| Probe | V8 resultado | V9 resultado | Replicado? |
|-------|-------------|-------------|------------|
| Q1 Layer order | NULL (p=0.71) | NULL (rho=-0.072, p=0.55) | Si (ambos NULL) |
| Q2 Dual anti-corr | 5/13 sig | NULL (1/14) | No (diverge) |
| Q3 DAG recovery | Above random | NULL (F1=0.152, p=0.001 vs random) | Parcial |
| Q4 Triadic S/C/E/A | NULL | MIXED (66% C, 0.6% E) | — |
| Q5 Phase transition | POSITIVE (p=0.0004) | **POSITIVE (p=0.018)** | **SI** |
| Q6 Unsupervised | NULL | MIXED (77.8% agreement) | — |
| Q7 Causal | NULL | NULL (40/72 sig, no layer effect) | Si (ambos NULL) |
| Q8 Cross-arch identity | — | NULL (Jaccard=0, SHD=147) | N/A (nuevo) |
| Q9 Structural conservation | — | MIXED (topologia >90% sim, S/C/E/A diverge) | N/A (nuevo) |

#### reptimeline — Diagnostico temporal V9 (10 checkpoints)

```
Fases detectadas:
  [1] Step 5K:         PRIMER SNAPSHOT
      entropy=0.412, churn=0.0, utilization=0.323

  [2] Step 10K:        PHASE TRANSITION
      entropy 0.412→0.506, churn 0→1.0, utilization 0.323→0.296

  [3] Steps 10K-50K:   CRISTALIZACION GRADUAL
      entropy 0.506→0.545, churn 1.0→0.458
```

**Patron "pulpo" confirmado:** Misma dinamica que V8:
- Explosion (churn=1.0) seguida de cristalizacion gradual
- V8: explosion step 35K, V9: explosion step 10K
- Ambos cristalizan a churn ~0.46-0.49
- Layer emergence: L1 y L6 estabilizan rapido, L2-L5 graduales

#### FEP wave fit

| Parametro | V8 | V9 |
|-----------|----|----|
| R² wave | — | **0.734** |
| f (frecuencia) | ~0 | **1.45** |
| dAIC (wave vs exp) | ~-4 | **+44.5** (wave gana) |
| Regimen | overdamped | **underdamped** (d/w=0.703) |
| Bootstrap | — | **1000/1000 exitoso** |

V9 muestra oscilacion genuina. V8 era compatible con exponencial puro.

#### Hallazgo clave: Emergencia simultanea

La transicion de fase es una EXPLOSION donde todas las capas se activan
al mismo tiempo, no secuencialmente (L1→L6). Esto invalida Q1 como estaba
formulado — no hay secuencia porque no hay orden, hay un evento unico.

**Implicacion:** La estructura emerge como un todo coherente (transicion
de fase / criticidad), no pieza por pieza. Consistente con FEP y Q5.

### Archivos generados V9

| Archivo | Que es |
|---------|--------|
| `model/train_v9_neo.bat` | Bat de entrenamiento V9 |
| `model/save_v9_timeline.py` | Extraccion reptimeline V9 |
| `model/fit_wave_fep_v9.py` | Fit onda amortiguada vs exponencial |
| `model/update_excel_v9.py` | Actualizacion programatica del Excel |
| `model/update_excel_q8.py` | Actualizacion Q8 en Excel |
| `model/update_excel_q9.py` | Actualizacion Q9 en Excel |
| `model/update_excel_octopus.py` | Actualizacion cristalizacion cross-model |
| `model/checkpoints/v9_neo_openwebtext/` | 11 checkpoints (5K-50K) + best.pt |
| `neural/q9_probe_structural_conservation.py` | Nuevo probe Q9 |
| `neural/results/q*` | Resultados Q1-Q9 |
| `neural/results/v9_*.json/.csv` | Timeline, fases, estabilidad V9 |
| `runs/v9_neo/plots/` | 5 graficas (dashboard, churn, swimlane, layers, FEP) |

---

## V9_xray: Radiografia de la transicion de fase

### Motivacion

Con checkpoints cada 5K steps, la transicion de fase aparece como instantanea
(churn 0→1.0 en un step). Necesitamos resolucion temporal fina para determinar
si la explosion es realmente simultanea o si hay una micro-secuencia oculta.

### Enfoque telescopico

1. **Paso 1:** Reentrenar V9 desde step 5K hasta 15K con `--save-every 1000` (10 ckpts, ~5GB)
2. **Paso 2:** Analizar reptimeline, identificar rango exacto de la explosion
3. **Paso 3:** Reentrenar solo ese rango (ej. 8K→9K) con `--save-every 100` (10 ckpts, ~5GB)

### Resultado parcial Paso 1 (2026-04-07)

Training log revela que la explosion ocurre entre **step 5001 y 5501**:

| Step | bit_acc_test | sub_test | dead_bits | Observacion |
|------|-------------|----------|-----------|-------------|
| 5001 | 52% | 0.7% | 29 | Pre-explosion |
| 5501 | 78% | 96.7% | 32 | **POST-EXPLOSION** |
| 6001 | 79% | 97.8% | 33 | Estabilizandose |
| 7001 | 80% | 97.3% | 35 | Estable |
| 8001 | 80% | 97.6% | 35 | Estable |

La explosion NO es entre step 5K y 10K como se veia con resolucion 5K.
Es entre **5001 y 5501** — un rango de solo 500 steps.

### Paso 2: Zoom (v9_xray_zoom) — COMPLETADO 2026-04-07

Basado en hallazgo del paso 1: reentrenar de step 5K a 6K con checkpoint
cada 50 steps. 20 snapshots dentro del rango de la explosion.

- Resume desde: `v9_neo_openwebtext/step_5000.pt` (mismo que paso 1)
- --save-every 50, --eval-every 50
- Checkpoints: `v9_xray_zoom/` (NO sobreescribe v9_xray/)

#### Resultado Paso 2

La explosion tiene una micro-secuencia clara:

| Step | bit_acc_test | sub_test | churn | Fase |
|------|-------------|----------|-------|------|
| 5050 | — | — | 0.000 | Pre-explosion |
| 5100 | 60.2% | 17.2% | **1.000** | Churn explosion (instantanea) |
| 5150 | 63.6% | **71.8%** | 0.995 | Sub explosion (sigmoide) |
| 5200 | 65.6% | 86.9% | 0.946 | Consolidando |
| 5300 | 67.7% | 93.4% | 0.733 | Estabilizando |
| 5500 | 69.6% | 96.9% | 0.524 | Plateau |
| 6000 | 72.2% | 96.7% | 0.336 | Cristalizado |

**Secuencia descubierta:**
1. Steps 5050-5100: TODOS los codigos cambian (churn 0→1.0) — evento instantaneo
2. Steps 5100-5200: Subsumption explota (1%→87%) — sigmoide de 100 steps
3. Steps 5200-6000: Refinamiento gradual, churn desciende logaritmicamente

**Churn heatmap** revela que NO todos los bits cambian al mismo ritmo:
- Bits 0-8: cambian fuerte al inicio, estabilizan rapido
- Bits 28-36, 40-56: los mas activos, churn alto hasta el final
- Bits 56-68: relativamente estables

**Hallazgo:** La explosion del churn es instantanea (50 steps), pero la
organizacion relacional (subsumption) tarda ~150 steps mas. Primero los bits
se "sueltan", despues se reorganizan en estructura.

**Falta zoom:** El salto churn 0→1.0 ocurre en 50 steps (5050→5100).
Necesitamos paso 3 para ver si es verdaderamente instantaneo.

### Paso 3: Zoom2 (v9_xray_zoom2) — COMPLETADO 2026-04-07

Basado en hallazgo del paso 2: el churn salta de 0.0 a 1.0 entre step
5050 y 5100. Reentrenar ese rango con checkpoint cada 5 steps.

- Resume desde: `v9_xray_zoom/step_5050.pt`
- --save-every 5, --eval-every 5
- Checkpoints: `v9_xray_zoom2/` (NO sobreescribe v9_xray_zoom/)

#### Resultado Paso 3 — HALLAZGO CLAVE

**El salto churn 0→1.0 era un artefacto de baja resolucion.** A resolucion
de 5 steps, el churn sube gradualmente (~0.17-0.21) y NUNCA llega a 1.0
dentro de esta ventana. La "explosion" es en realidad una **onda de activacion**
que se propaga bit por bit en ~45 steps.

Churn a 5-step resolution:

| Step | Churn | dChurn |
|------|-------|--------|
| 5055 | 0.000 | — |
| 5060 | 0.173 | +0.173 (onset) |
| 5065 | 0.191 | +0.018 |
| 5070 | 0.188 | -0.003 |
| 5075 | 0.212 | +0.024 |
| 5080 | 0.187 | -0.025 |
| 5085 | 0.184 | -0.004 |
| 5090 | 0.176 | -0.007 |
| 5095 | 0.190 | +0.013 |
| 5100 | 0.172 | -0.018 |

**Cascada de activacion por bit:**

| Step | N bits | Bits que cambian por primera vez |
|------|--------|---------------------------------|
| 5060 | 6 | 12, 41, 23, 47, 31, 35 |
| 5065 | 8 | 11, 3, 33, 69, 58, 8, 7, 59 |
| 5070 | 5 | 67, 30, 5, 28, 61 |
| 5075 | 4 | 18, 17, 43, 14 |
| 5080 | 1 | 4 |
| 5085 | 4 | 52, 57, 42, 66 |
| 5100 | 3 | 0, 44, 39 |

Total: 31 bits cambian en oleadas de 1-8 bits a lo largo de ~45 steps.
Los primeros 6 bits (step 5060) podrian ser los "semilla" que desencadenan
la reorganizacion de los demas.

**Implicacion para Q1:** No es una transicion de fase instantanea sino
una cascada con orden temporal. Analizar si los bits semilla corresponden
a capas especificas de la ontologia.

**Bits mas estables (no cambian):** 60, 63, 68, 70, 71
**Bits menos estables:** 39, 18, 44, 57, 32

#### Mapeo de la cascada a la ontologia

Los bits semilla y oleadas mapeados a primitivos y capas revelan un patron:
**la cascada va del MEDIO hacia los EXTREMOS.**

| Oleada | Step | N | Primitivos | Capas |
|--------|------|---|------------|-------|
| Semilla | 5060 | 6 | flujo_temporal, colectivo, caos, algunos, control, dolor | L3(2) L4(2) L5(2) |
| Oleada 2 | 5065 | 8 | posicion_temporal, fuego, muerte, perdida, tal_vez, eje_profundidad, eje_vertical, parte_de | L2(2) L3(1) L4(3) L5(2) |
| Oleada 3 | 5070 | 5 | aversion, libertad, agua, verdad, mas | L2(1) L4(3) L5(1) |
| Oleada 4 | 5075 | 4 | equilibrio, olfato, creador_obs, oido | L4(1) L5(2) L6(1) |
| Oleada 5 | 5080 | 1 | tierra | L5(1) |
| Oleada 6 | 5085 | 4 | pensar, debe, receptivo, atraccion | L3(1) L4(1) L5(1) L6(1) |
| Oleada 7 | 5100 | 3 | **vacio, uno**, eterno_obs | **L1(2)** L6(1) |
| Estables | — | 5 | tipo_de, proporcion, cooperacion, atencion, intencion | L3(1) L4(2) L5(2) |

**Interpretacion:**

1. **Semilla (L3-L5):** Los conceptos de tiempo, moral y cuerpo inician la cascada.
   Son los mas "estadisticamente discriminativos" en el espacio del LM.
2. **Expansion (L2-L5):** Las oleadas 2-3 reclutan ejes espaciales y conceptos morales.
3. **Observador (L6):** creador_obs y receptivo llegan en oleada 4-6.
4. **Extremos al final (L1, L6):** vacio y uno (fundamentos ontologicos) son los
   ULTIMOS en cambiar (step 5100). La base abstracta se adapta al final.
5. **Andamios estables:** tipo_de, proporcion, cooperacion, atencion, intencion
   nunca cambian — son relaciones estructurales que sirven de "esqueleto".

**Esto contradice:**
- Q1 (predecia L1 primero → NULL)
- Paper linea 385 (reportaba L6 primero → era artefacto de baja resolucion)

**La realidad:** Las capas medias (3-5) contienen los conceptos que el LM
distingue primero, los extremos ontologicos (L1: existencia, L6: recursion)
son los ultimos en cristalizar. Los "andamios" relacionales nunca se mueven.

### Archivos

| Archivo | Que es |
|---------|--------|
| `model/train_v9_xray.bat` | Paso 1: 5K→15K cada 1000 steps |
| `model/train_v9_xray_zoom.bat` | Paso 2: 5K→6K cada 50 steps |
| `model/save_v9_xray_timeline.py` | Extraccion reptimeline para paso 1 |
| `model/save_v9_xray_zoom_timeline.py` | Extraccion reptimeline para paso 2 (incluye analisis per-layer) |
| `model/checkpoints/v9_xray/` | Checkpoints paso 1 (cada 1000 steps) |
| `model/checkpoints/v9_xray_zoom/` | Checkpoints paso 2 (cada 50 steps) |
| `model/checkpoints/v9_xray_zoom2/` | Checkpoints paso 3 (cada 5 steps) |
| `model/train_v9_xray_zoom2.bat` | Paso 3: 5050→5100 cada 5 steps |
| `model/save_v9_xray_zoom2_timeline.py` | Extraccion reptimeline para paso 3 |
| `runs/v9_xray/plots/` | Graficas paso 1 |
| `runs/v9_xray_zoom/plots/` | Graficas paso 2 |
| `runs/v9_xray_zoom2/plots/` | Graficas paso 3 |

---

## V8_xray: Radiografia de la transicion de fase en v8 (GPT-2 Medium)

**Objetivo:** Replicar el X-ray telescopico de v9 en v8 para confirmar que el
patron de cascada (centro→extremos) es independiente de la arquitectura/dataset.

- **Modelo:** GPT-2 Medium (345M params)
- **Dataset:** wikitext-103 (default)
- **Explosion original:** step 35K (churn 0→1.0 reportado a baja res en timeline_v8.json)
- **Explosion real (paso 1):** step 31K-32K (churn 0→0.81)
- **Estrategia:** mismo telescopio de 3 pasos que v9

### Paso 1: Resolucion 1000 steps (30K→45K) — COMPLETADO

- **Resume:** `checkpoints/v8_deep/step_30000.pt`
- **Rango:** 30K → 45K
- **Save-every:** 1000 (15 checkpoints)
- **Directorio:** `checkpoints/v8_xray/`
- **Script:** `model/train_v8_xray.bat`
- **Timeline:** `model/save_v8_xray_timeline.py`
- **Tiempo:** 695 min (~11.5h)
- **Estado:** COMPLETADO (2026-04-07)

**Resultado paso 1:**

| Step | Churn | dChurn |
|------|-------|--------|
| 31000 | 0.000 | — |
| 32000 | 0.814 | +0.814 (EXPLOSION) |
| 33000 | 0.869 | +0.056 |
| 34000 | 0.752 | -0.117 |
| 35000 | 0.868 | +0.116 |
| 36000 | 0.802 | -0.067 |
| 37000 | 0.777 | -0.025 |
| 38000 | 0.658 | -0.119 |
| 39000 | 0.609 | -0.049 |
| 40000 | 0.694 | +0.085 |
| 41000 | 0.552 | -0.142 |
| 42000 | 0.520 | -0.032 |
| 43000 | 0.603 | +0.083 |
| 44000 | 0.555 | -0.048 |
| 45000 | 0.487 | -0.068 |

Explosion entre step 31000 y 32000, NO en 35K como reportado a baja resolucion.
Churn nunca llega a 1.0 (max 0.87). Despues oscila y baja gradualmente (cristalizacion).
Patron identico al v9 pero a diferente escala temporal.

### Paso 2: Resolucion 50 steps (30K→32K) — COMPLETADO

- **Resume:** `checkpoints/v8_deep/step_30000.pt`
- **Rango:** 30K → 32K
- **Save-every:** 50 (40 checkpoints)
- **Directorio:** `checkpoints/v8_xray_zoom/`
- **Script:** `model/train_v8_xray_zoom.bat`
- **Timeline:** `model/save_v8_xray_zoom_timeline.py`
- **Tiempo:** 93 min
- **Estado:** COMPLETADO (2026-04-07)

**Resultado paso 2:**
- Explosion entre step 30050 y 30100 (churn 0→0.53)
- Despues oscila entre 0.25-0.45, nunca sube a 1.0
- Patron: explosion abrupta seguida de oscilaciones que decaen

### Paso 3: Resolucion 5 steps (30K→30150) — COMPLETADO

- **Resume:** `checkpoints/v8_deep/step_30000.pt`
- **Rango:** 30K → 30150
- **Save-every:** 5 (30 checkpoints)
- **Directorio:** `checkpoints/v8_xray_zoom2/`
- **Script:** `model/train_v8_xray_zoom2.bat`
- **Timeline:** `model/save_v8_xray_zoom2_timeline.py`
- **Tiempo:** 25 min training + 22 min extraction
- **Estado:** COMPLETADO (2026-04-08)

**Resultado paso 3: CASCADA CONFIRMADA EN V8**

65/72 bits cambian en oleadas de 1-7 bits a lo largo de ~145 steps.
7 bits estables (scaffold): eje_profundidad, eje_lateral, gusto, creacion,
creador_obs, hacer, si_entonces.

| Step | N bits | Bits (primeros que cambian) | Capas |
|------|--------|-----------------------------|-------|
| 30010 | 5 | vacío, tal_vez, puede, muchos, interocepción | L1(1) L4(3) L5(1) |
| 30015 | 2 | proporción, porque | L3(2) |
| 30020 | 4 | intención, uno, tipo_de, agua | L1(1) L4(1) L5(2) |
| 30025 | 2 | temporal_obs, vista | L4(1) L6(1) |
| 30030 | 4 | aire, aversión, tierra, eterno_obs | L4(1) L5(2) L6(1) |
| 30040 | 7 | verdad, libertad, individual, orden, ... | L3(2) L4(3) L5(1) L6(1) |
| 30080 | 6 | algunos, atención, tacto, querer, control, ausente | L4(2) L5(4) |
| 30140 | 5 | equilibrio, dolor, mover, fuego, mal | L3(1) L4(2) L5(2) |
| 30150 | 1 | más | L2(1) |

**Comparacion v8 vs v9:**

| Metrica | v9 (GPT-Neo 125M) | v8 (GPT-2 Medium) |
|---------|--------------------|--------------------|
| Bits que cambian | 31/72 (43%) | 65/72 (90%) |
| Bits estables | 5 | 7 |
| Duracion cascada | ~45 steps | ~145 steps |
| Churn max | 0.21 | 0.17 |
| Primer bit | flujo_temporal(L3) | vacío(L1) |
| Ultimo bit | vacío(L1), eterno_obs(L6) | más(L2) |

**Interpretacion:**
1. La cascada se confirma cross-arquitectura — NO es artefacto de un modelo.
2. v8 (modelo mas grande) tiene cascada mas larga y distribuida (90% bits vs 43%).
3. El churn real es ~0.17 en ambos modelos, nunca 1.0.
4. Los bits "scaffold" son diferentes en cada modelo pero el patron es el mismo.
5. v8 empieza con L1 (vacio) y v9 con L3-L5 — el orden de capas no es
   universal, pero el patron de cascada si lo es.

### Archivos V8_xray

| Archivo | Que es |
|---------|--------|
| `model/train_v8_xray.bat` | Paso 1: 30K→45K cada 1000 steps |
| `model/train_v8_xray_zoom.bat` | Paso 2: 30K→32K cada 50 steps |
| `model/save_v8_xray_timeline.py` | Extraccion reptimeline para paso 1 |
| `model/save_v8_xray_zoom_timeline.py` | Extraccion reptimeline para paso 2 |
| `model/train_v8_xray_zoom2.bat` | Paso 3: 30K→30150 cada 5 steps |
| `model/save_v8_xray_zoom2_timeline.py` | Extraccion reptimeline para paso 3 |
| `model/checkpoints/v8_xray/` | Checkpoints paso 1 (15 ckpts) |
| `model/checkpoints/v8_xray_zoom/` | Checkpoints paso 2 (40 ckpts) |
| `model/checkpoints/v8_xray_zoom2/` | Checkpoints paso 3 |
| `model/update_excel_v8_xray.py` | Excel update: paso 1 results |
| `runs/v8_xray/plots/` | Graficas paso 1 |
| `runs/v8_xray_zoom/plots/` | Graficas paso 2 |

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
