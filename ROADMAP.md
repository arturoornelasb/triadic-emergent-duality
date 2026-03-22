# Roadmap: Production-Ready & Comercializable

Estado actual: framework de investigacion con 37 documentos, 32 scripts de validacion,
modelo neural funcional y resultados parciales. Falta empaquetado, reproducibilidad y producto.

---

## Tecnico

### Empaquetado y reproducibilidad

- [ ] Crear `pyproject.toml` o `requirements.txt` con versiones pinneadas (torch, numpy, transformers, reptimeline)
- [ ] Agregar `LICENSE` file (definir modelo: MIT, Apache-2.0, o licencia comercial dual)
- [ ] Publicar model weights pre-entrenados (HuggingFace Hub o GitHub Releases) — sin ellos nadie puede reproducir resultados
- [ ] Dockerizar el entorno de entrenamiento (GPU + dependencias exactas)
- [ ] Agregar versionado semantico y tags de release (`v0.1.0-beta` existe solo en commit message)

### Testing y CI/CD

- [ ] Agregar test suite con pytest: unit tests para `stats/`, `triadic.py`, `anchors.py`
- [ ] Los 32 scripts de `scripts/` no tienen asserts — convertirlos en tests ejecutables con exit codes
- [ ] GitHub Actions: lint (ruff/flake8), tests, validacion de JSONs en `data/`
- [ ] Pre-commit hooks (formatting, type checking)

### Datos y validacion

- [ ] Completar interrater data — solo existe `Mathematics_rater2.csv`, faltan los otros 8 dominios
- [ ] 3/8 dominios dentro de la distribucion null (Philosophy, Physics, Mathematics) — necesitan reclasificacion D-A-N o justificacion formal
- [ ] Correlaciones de rango sin poder estadistico (n=7/14) — necesitan corpus mas grande o test alternativo
- [ ] Sensibilidad D-A-N fragil (28.4% de perturbaciones causan >5% cambio IDVS) — estabilizar clasificaciones
- [ ] Directorio `figures/` vacio — generar visualizaciones del DAG, spiral, resultados por dominio

### Modelo neural

- [ ] Resolver tradeoff escala-algebra: GPT-2 355M logra 76.9% subsumption vs 98.3% en 40M — investigar causa
- [ ] Integrar bits 63-64 (proporcion, quietud) formalmente o eliminarlos del pipeline
- [ ] Principio holografico solo parcial (3.13x vs random, no determinista) — formalizar o descartar claim
- [ ] Script `download_corpus.py` existe pero el corpus no se distribuye — documentar fuente o incluir script funcional

### API y accesibilidad

- [ ] API REST o CLI para consultar primitivos de un concepto dado (input: texto, output: vector 65-bit)
- [ ] SDK/libreria Python instalable via pip: `pip install dualidad-emergente`
- [ ] Documentacion tecnica (Sphinx o MkDocs) — actualmente solo existen los 37 .md de teoria

---

## Comercial

### Propiedad intelectual

- [ ] Definir estrategia de licenciamiento: open-core (stdlib gratis, modelo/API de pago) o SaaS
- [ ] Registrar propiedad intelectual del framework (patente de metodo o copyright formal)
- [ ] Los 37 documentos teoricos son el asset principal — protegerlos antes de publicar

### Publicacion academica

- [ ] Ejecutar plan de 4 articulos definido en Doc 10 (prioridad: empirico → filosofico → breadth → formal)
- [ ] Target journals: Synthese, Foundations of Science, Minds and Machines, Artificial Intelligence
- [ ] Peer review externo antes de submit — actualmente todo es auto-evaluado
- [ ] Las refutaciones honestas (abstraction-zeros, holographic parcial) son fortaleza editorial — mantenerlas

### Producto

- [ ] Definir que se vende: framework teorico (consultoria), API de clasificacion semantica, o herramienta de investigacion
- [ ] Landing page / sitio web con demo interactiva (input concepto → output vector + dualidades activas)
- [ ] Caso de uso concreto demostrable: NLP, ontology engineering, knowledge graphs, curriculum design
- [ ] Benchmarks contra alternativas existentes (ConceptNet, FrameNet, WordNet) — sin comparativa no hay pitch

### Comunidad

- [ ] README bilingue (espanol/ingles) o traduccion completa a ingles para audiencia internacional
- [ ] Los documentos 01-37 estan en espanol — traducir al menos el abstract/resumen de cada uno
- [ ] Contributing guide si se abre el codigo
- [ ] Canal de discusion (GitHub Discussions o Discord)

---

## Bloqueos

| Bloqueo | Severidad | Impacto |
|---------|-----------|---------|
| Sin LICENSE file | **Critica** | Nadie puede usar, modificar ni contribuir legalmente |
| Sin model weights publicados | **Critica** | Resultados no reproducibles por terceros |
| Sin requirements.txt/pyproject.toml | **Alta** | Instalacion no reproducible |
| Interrater data incompleta (1/9 dominios) | **Alta** | IDVS metric no verificable externamente para 8 dominios |
| Estadisticas underpowered (n=7/14) | **Alta** | Peer reviewers rechazaran claims de orden sin mas evidencia |
| 3 dominios dentro de null | **Media** | Debilita el claim de validacion universal |
| Sin peer review externo | **Media** | Todo resultado es auto-reportado |
| Codebase monolingue (espanol) | **Media** | Limita audiencia y contribuciones internacionales |
| Sin CI/CD | **Baja** | No bloquea uso pero impide desarrollo colaborativo |
| Sin API/CLI | **Baja** | No bloquea investigacion pero impide comercializacion |
