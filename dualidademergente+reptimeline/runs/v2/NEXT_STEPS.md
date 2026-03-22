# V3 Training Plan — Primitivos Directos

## Decisión Clave (2026-03-22)

V2 demostró que el modelo aprende lo que le pedimos (95.8% bit accuracy).
El problema era lo que le pedimos: 262 anchors con solo 10 firmas únicas (3.8%).

**V3 entrena directo con los 65 primitivos del círculo, sin anchors intermedios.**

## Diagnóstico V2

- 262 anchors de 8 dominios, generados por anchors.py + reference_domains.json
- reference_domains.json marca ~30-50 primitivos como "D" por dominio
- Resultado: todos los conceptos de un dominio tienen firma casi idéntica
- El modelo logró 95.8% accuracy contra targets que solo tenían 10 firmas únicas
- El "colapso" de firmas (70.6% uniqueness) era el RESULTADO CORRECTO

## V3: 65 Primitivos como Targets

Cada primitivo tiene target = su propio bit ON + dependencias transitivas ON + resto OFF.

Comparación:
| Métrica            | V2 (262 anchors) | V3 (65 primitivos) |
|--------------------|-------------------|--------------------|
| Targets únicos     | 10/262 (3.8%)     | 65/65 (100%)       |
| Bits always ON     | 21/65             | 1/65 (solo "uno")  |
| Jaccard mediana    | 0.667             | 0.261              |
| Pares idénticos    | 3,620             | 0                  |

## Pasos de Implementación

### Paso 1: gold_primitivos_65.json
Generar nuevo archivo de targets con los 65 primitivos.
Cada entrada tiene:
- nombre (español): "vacío", "fuerza", "mover"...
- english: traducción al inglés para GPT-2
- definition: definición en inglés (del campo "def" de primitivos.json)
- binary_signature: 65 bits (propio bit + deps transitivas)
- capa, deps, dual

### Paso 2: Adaptar train.py
- Cambiar gold_primes_65.json → gold_primitivos_65.json
- Adaptar la lógica de carga (no hay "domain", hay "capa")
- Ajustar train/test split (65 es poco — usar leave-one-out o 80/20)
- Considerar: presentar al modelo la definición en inglés como contexto
- Ajustar Regla de Tres quads con primitivos que estén en los targets

### Paso 3: Adaptar explore.py y audits
- Exploración con 65 conceptos en vez de 262
- Comparar estructura aprendida vs DAG teórico
- Verificar dual coherence con los 13 pares duales reales

### Paso 4: Entrenar v3
- Mismos hiperparámetros (50K steps, lr=1e-4, alpha=0.05, batch=4x2)
- GPU: RTX 4060 Ti 16GB, ~5 horas estimadas
- Guardar en checkpoints/gpt2_triadic_65_v3/

### Paso 5: Audit v3
- Correr audit_targets, audit_learned_vs_target, explore, deep_analysis
- Archivar en runs/v3/
- Comparar con v2: python compare_runs.py v2 v3

## Consideración: Contexto para GPT-2

Los 65 primitivos son palabras en español. GPT-2 fue entrenado en inglés.
Opciones para presentar los conceptos:
- A) Español directo: "vacío" → GPT-2 puede tener poco contexto
- B) Inglés traducido: "void", "force", "move"
- C) Definición en inglés: "Absence as substance, potential space"
- D) Combinación: "void: absence as substance, potential space"

Decisión pendiente del usuario.

## Archivos Relevantes

- `data/primitivos.json` — Los 65 primitivos con DAG, capas, duals
- `model/anchors.py` — Generador de targets (a adaptar para primitivos)
- `model/train.py` — Script de entrenamiento (a adaptar)
- `model/explore.py` — Exploración post-training
- `model/audit_primitivos_as_targets.py` — Análisis de diversidad de targets v3
- `neural/results/audit_primitivos_targets.json` — Resultados del análisis
- `runs/v2/` — Archivo completo del run v2 para comparación
