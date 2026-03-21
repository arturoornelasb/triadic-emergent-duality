# Documento 30: Validador Automatico de Dominios

| Metrica | Resultado |
|---------|-----------|
| Herramienta | `scripts/validate_domain.py` |
| Dominios de referencia | 9 (8 positivos + 1 control negativo) |
| Metrica central | IDVS = Coverage_L14 x Monotonicity |
| Umbral PASS | IDVS >= 0.85 |
| Umbral FAIL | IDVS < 0.50 |
| Gap referencia | 0.391 (Filosofia 0.859 vs Astrologia 0.469) |
| Dependencias | Solo stdlib Python (json, math, sys, os) |

**Script:** `scripts/validate_domain.py`
**Datos:** `data/primitivos.json`, `data/reference_domains.json`

---

## I. Como usar el validador

### Paso 1: Generar plantilla

```bash
python scripts/validate_domain.py --template mi_dominio.json
```

Esto genera un JSON con los 63 primitivos, cada uno marcado con `"?"`. Incluye una guia `_guide` con capa, definicion y dependencias de cada primitivo.

### Paso 2: Clasificar los 63 primitivos

Abrir el JSON generado y reemplazar cada `"?"` con:

| Valor | Significado | Ejemplo (Musica) |
|-------|-------------|-------------------|
| `D` | **Directo** — el primitivo opera directamente en el dominio | `"oido": "D"` |
| `A` | **Analogico** — aplica por metafora o analogia | `"libertad": "A"` |
| `N` | **Nulo** — no aplica en absoluto | `"gusto": "N"` |

### Paso 3: Ejecutar validacion

```bash
python scripts/validate_domain.py mi_dominio.json
```

### Formato de entrada

```json
{
  "domain": "Economia",
  "classes": {
    "vacio": "D",
    "informacion": "D",
    "uno": "D",
    ...
  }
}
```

El campo `_guide` (si existe) se ignora durante la validacion.

---

## II. Que mide el IDVS

El IDVS (Informational Domain Validity Score) es el producto de dos metricas independientes:

```
IDVS = Coverage_L14 x Monotonicity
```

### Coverage L1-4

Mide que proporcion de los 38 primitivos fundacionales (capas 1-4) no son NULL:

```
Coverage = 1 - NULLs_L14 / 38
```

**Intuicion:** Un dominio genuino deberia involucrar los primitivos basicos (existencia, fuerza, tiempo, espacio, logica). Si muchos son NULL, el dominio probablemente opera solo por analogia superficial.

### Monotonicity

Mide que proporcion de las 128 aristas del DAG de dependencias respeta la jerarquia:

```
Monotonicity = edges_monotone / 128
```

Una arista es monotona si `estado_hijo <= estado_padre` (D=2, A=1, N=0). Un hijo no deberia ser mas "directo" que su padre — si la causa es analogica, el efecto no puede ser directo.

**Intuicion:** Los dominios genuinos clasifican primitivos de forma coherente con la estructura de dependencias. Los pseudo-dominios violan esta coherencia sistematicamente.

### Por que multiplicacion

El producto es la eleccion mas simple sin pesos arbitrarios:
- Si ambas metricas son altas, IDVS es alto
- Si cualquiera es baja, IDVS se penaliza
- No hay pesos que ajustar (a diferencia del DVS original: 0.30/0.25/0.20/0.15/0.10)

---

## III. Interpretacion del reporte

El reporte de validacion contiene las siguientes secciones:

### Input Validation
Confirma que los 63 primitivos estan presentes y todos tienen valores D, A, o N. Muestra distribucion por capa.

### Coverage L1-4
Reporta el coverage y lista los NULLs en capas 1-4 con su definicion, para que el usuario pueda reconsiderar si realmente son NULL.

### Monotonicity
Reporta la fraccion de aristas monotomas y lista las violaciones agrupadas por tipo (D<-A, A<-N, D<-N). Cada violacion indica hijo y padre con su capa y estado.

### IDVS + Veredicto
Calcula el producto y emite el veredicto (PASS / UNCERTAIN / FAIL).

### Prime Signature
Firma algebraica unica del dominio: `Sigma = Pi(primo_i ^ estado_i)`. Verifica que no coincida con ningun dominio de referencia.

### Comparison with Reference Domains
Tabla ordenada por IDVS con distancias Hamming simple y ponderada a los 9 dominios de referencia. Identifica el dominio mas cercano y mas lejano.

### MDS 2D
Proyeccion bidimensional via MDS clasico (Jacobi). Muestra donde se ubica el nuevo dominio en el espacio de los 9 de referencia. Reporta varianza explicada.

### Summary
Tabla consolidada de todas las metricas y re-enunciacion del veredicto.

---

## IV. Las tres zonas del veredicto

| Zona | IDVS | Significado |
|------|------|-------------|
| **PASS** | >= 0.85 | Consistente con los 8 dominios validos conocidos. El minimo positivo es Filosofia (0.859). |
| **UNCERTAIN** | 0.50 -- 0.85 | Entre valido e invalido. Ningun dominio de referencia cae aqui — es una zona de separacion natural. |
| **FAIL** | < 0.50 | Consistente con pseudo-ciencia. Astrologia obtiene 0.469. |

### Referencia: IDVS de los 9 dominios

| Dominio | Coverage | Mono | IDVS | Tipo |
|---------|----------|------|------|------|
| Quimica | 1.000 | 0.969 | 0.969 | positivo |
| Linguistica | 1.000 | 0.953 | 0.953 | positivo |
| Musica | 1.000 | 0.945 | 0.945 | positivo |
| Biologia | 1.000 | 0.945 | 0.945 | positivo |
| Psicologia | 1.000 | 0.945 | 0.945 | positivo |
| Matematicas | 1.000 | 0.914 | 0.914 | positivo |
| Fisica | 1.000 | 0.891 | 0.891 | positivo |
| Filosofia | 1.000 | 0.859 | 0.859 | positivo |
| Astrologia | 0.632 | 0.742 | 0.469 | control negativo |

**Gap minimo:** 0.391 (Filosofia 0.859 vs Astrologia 0.469)

---

## V. Limitaciones

1. **Clasificacion subjetiva:** La asignacion D/A/N depende del criterio del clasificador. Dos personas pueden clasificar el mismo dominio de forma diferente.

2. **Muestra de referencia:** Solo 9 dominios de referencia (8 positivos + 1 control). Mas dominios validados fortalecerian los umbrales.

3. **Umbrales empiricos:** Los umbrales 0.85 y 0.50 se derivan del gap observado, no de un argumento teorico. Un dominio en la zona UNCERTAIN requiere analisis caso por caso.

4. **Un solo control negativo:** Solo Astrologia como pseudo-ciencia. Mas controles negativos (homeopatia, numerologia) confirmarian la robustez del umbral inferior.

5. **Sin ponderacion por capa:** IDVS trata todas las aristas por igual en monotonicity. Una version futura podria ponderar las violaciones en capas fundamentales mas que en capas altas.
