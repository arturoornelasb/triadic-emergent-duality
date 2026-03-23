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

> **Para el log completo de experimentos con resultados, decisiones y hallazgos, ver:**
> **[../EXPERIMENT_LOG.md](../EXPERIMENT_LOG.md)**

| Run | Bits | Accuracy | Unique | Coherence | PPL | Key Change |
|-----|------|----------|--------|-----------|-----|------------|
| v1 | 65 | ~90%? | ? | ? | 2,777 | Baseline |
| v2 | 65 | 95.8% | 3.8% | ? | 6,735 | 262 domain anchors (bad targets) |
| v3 | 65 | 90.9% | 89.2% | 0.653 | 5,388 | 65 primitivos directos |
| v4 | 72 | 92.5% | 100% | 0.876 | 5,608 | Circle expanded +7 primitivos |
| v5_frozen | 72 | 90.8% | 100% | 0.818 | 31.95 | freeze_base (forgetting FIXED) |

### Checkpoints

| Run | Dir | Gold file |
|-----|-----|-----------|
| v1 | `checkpoints/gpt2_triadic_65/` | `gold_primitivos_65.json` |
| v2 | `checkpoints/gpt2_triadic_65_v2/` | `gold_primes_65.json` |
| v3 | `checkpoints/gpt2_triadic_65_v3/` | `gold_primitivos_65.json` |
| v4 | `checkpoints/gpt2_triadic_72_v4/` | `gold_primitivos_72.json` |
| v5_frozen | `checkpoints/gpt2_triadic_72_v5_frozen/` | `gold_primitivos_72.json` |

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
