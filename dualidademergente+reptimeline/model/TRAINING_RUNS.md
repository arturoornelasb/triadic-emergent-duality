# Training Runs — GPT-2 Triadic Head

## Estructura de Archivos

```
model/
├── train.py                    ← Script de entrenamiento (actualmente v3)
├── generate_gold_primitivos.py ← Genera gold_primitivos_65.json desde primitivos.json
├── gold_primitivos_65.json     ← Targets v3: 65 primitivos directos
├── gold_primes_65.json         ← Targets v2: 262 anchors de dominio (deprecated)
├── archive_run.py              ← Archiva cualquier run a runs/{version}/
├── compare_runs.py             ← Compara dos runs: python compare_runs.py v2 v3
├── explore.py                  ← Exploración post-training
├── deep_analysis.py            ← Análisis profundo (clusters, triadic, deps)
├── audit_targets.py            ← Auditoría de targets (diversidad de firmas)
├── audit_learned_vs_target.py  ← Comparación learned vs gold
├── audit_primitivos_as_targets.py ← Análisis de primitivos como targets
├── audit_v2.py                 ← Auditoría específica v2 (deprecated, usar archive_run.py)
│
├── checkpoints/
│   ├── gpt2_triadic_65/        ← v1 (run original)
│   │   └── *.pt
│   ├── gpt2_triadic_65_v2/     ← v2 (262 anchors)
│   │   ├── run_config.json     ← NO tiene (v2 pre-dates this)
│   │   ├── results.json
│   │   ├── training_log.csv
│   │   ├── best.pt
│   │   └── step_*.pt           ← 21 checkpoints cada 2500 steps
│   └── gpt2_triadic_65_v3/     ← v3 (65 primitivos) — SE CREA AL ENTRENAR
│       ├── run_config.json     ← Config completa + args + fecha
│       ├── gold_primitivos_65.json  ← Snapshot de targets usados
│       ├── results.json        ← Métricas finales + metadata
│       ├── training_log.csv    ← Log paso a paso
│       ├── best.pt             ← Mejor modelo por test accuracy
│       └── step_*.pt           ← Checkpoints periódicos
│
runs/
├── v2/                         ← Archivo completo v2
│   ├── manifest.json           ← Metadata consolidada
│   ├── audit_report.txt        ← Reporte humano
│   ├── NEXT_STEPS.md           ← Plan v3 (referencia histórica)
│   ├── results.json
│   ├── training_log.csv
│   ├── exploration.json
│   ├── deep_analysis.json
│   ├── audit_targets.json
│   ├── audit_learned_vs_target.json
│   └── checkpoints_path.txt    ← Puntero a model/checkpoints/gpt2_triadic_65_v2/
└── v3/                         ← SE CREA POST-TRAINING con archive_run.py v3
```

## Runs Completados

### v1 — Run Original
- **Modelo:** GPT-2 + 65-bit head
- **Checkpoints:** `model/checkpoints/gpt2_triadic_65/`
- **Status:** Completado, no archivado formalmente

### v2 — 262 Domain Anchors (2026-03-22)
- **Modelo:** GPT-2 Medium (355M) + 65-bit triadic head (simple, iFSQ)
- **Targets:** 262 anchors de 8 dominios via `gold_primes_65.json`
- **Steps:** 50,000 | **Batch:** 4×2=8 | **LR:** 3e-4 | **Alpha:** 0.05
- **GPU:** RTX 4060 Ti 16GB | **Tiempo:** ~4.9 horas
- **Resultado:** 95.8% bit accuracy — modelo correcto, TARGETS incorrectos
- **Root cause:** Solo 10 firmas únicas en 262 targets (3.8%)
- **Checkpoints:** `model/checkpoints/gpt2_triadic_65_v2/` (21 .pt)
- **Archivo:** `runs/v2/` (10 archivos + manifest)

### v3 — 65 Primitivos Directos (PENDIENTE)
- **Modelo:** GPT-2 Medium (355M) + 65-bit triadic head (simple, iFSQ)
- **Targets:** 65 primitivos directos via `gold_primitivos_65.json`
- **Cambios clave vs v2:**
  - 65 conceptos (no 262) — cada uno con firma única (100%, 0 colisiones)
  - Texto inglés "word: definition" para GPT-2 (Option D, max 20 tokens)
  - Regla de Tres usa pares duales del círculo
  - 515 pares de subsunción (del DAG transitivo)
  - Jaccard mediana 0.261 (vs 0.667 en v2) — mucho más diverso
- **Hyperparams:** Mismos que v2 (50K steps, 3e-4 lr, 0.05 alpha)
- **Checkpoints:** `model/checkpoints/gpt2_triadic_65_v3/`

## Cómo Lanzar un Entrenamiento

```bash
conda activate triadic-microgpt
cd C:\Github\dualidad_emergente\dualidademergente+reptimeline\model
python train.py
```

Argumentos opcionales:
```
--lr 1e-4                    # Cambiar learning rate
--steps 75000                # Más pasos
--run-name gpt2_triadic_65_v3b  # Nombre distinto para variante
--resume checkpoints/gpt2_triadic_65_v3/step_25000.pt  # Continuar
```

## Pipeline Post-Training

```bash
# 1. Exploración (requiere GPU)
python explore.py --device cuda

# 2. Análisis profundo
python deep_analysis.py --device cuda --recompute

# 3. Auditorías
python audit_targets.py
python audit_learned_vs_target.py

# 4. Archivar
python archive_run.py v3

# 5. Comparar con v2
python compare_runs.py v2 v3
```

## Qué Guarda Cada Checkpoint .pt

Cada archivo `.pt` contiene:
```python
{
    'model_state_dict': ...,        # Pesos del modelo
    'optimizer_state_dict': ...,    # Estado del optimizer (para resume)
    'config': {
        'run_name': 'gpt2_triadic_65_v3',
        'gold_file': 'gold_primitivos_65.json',
        'model_name': 'gpt2-medium',
        'n_triadic_bits': 65,
        'freeze_base': False,
        'head_mode': 'simple',
        'activation': 'ifsq',
        'lr': 3e-4,
        'alpha': 0.05,
    },
    'step': N,
    'loss': float,                  # En step checkpoints
    'bit_accuracy_test': float,     # En best.pt
    'sub_rate_test': float,         # En best.pt
}
```

## Qué Guarda run_config.json (nuevo en v3)

Se genera al inicio del entrenamiento:
```python
{
    'run_name': 'gpt2_triadic_65_v3',
    'date': '2026-03-22 ...',
    'gold_file': 'gold_primitivos_65.json',
    'n_concepts': 65,
    'n_train': 52,
    'n_test': 13,
    'has_supervision': True,
    'has_subsumption': True,
    'args': { ... todos los argumentos de CLI ... }
}
```
