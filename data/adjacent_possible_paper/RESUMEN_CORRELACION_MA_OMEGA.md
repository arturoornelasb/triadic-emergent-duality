# Correlacion MA ~ omega: Assembly Theory meets Danza Cosmica

## Contexto

La conjetura central (P8) predice que el assembly index MA(x) se correlaciona con omega(x), el numero de factores primos irreducibles. Esto era la debilidad #8 del Excel: "Assembly index ~ omega es isomorfismo ESTRUCTURAL, no numerico. No hay un solo dato molecular."

Este analisis aborda esa debilidad con datos reales.

## Datasets

### Dataset 1: MA calculado (10,000 moleculas)
- **Archivo**: `dataset_1_calculated_MA_10000.csv`
- **Columnas**: InChI, MA
- **Fuente**: Sharma et al. via repo `croningp/molecular_complexity` (`data/calculated_data.pkl`)
- **MA range**: 2 - 22, mean 10.1

### Dataset 2: MA experimental (101 moleculas unicas)
- **Archivo**: `dataset_2_experimental_MA_450.csv`
- **Columnas**: sample_id, SMILES, formula, MW, CAS, MA, MA(mean est.), Error, Dataset
- **Fuente**: Sharma et al. via repo `croningp/molecular_complexity` (`data/combined_results_ms.xlsx`)
- **MA range**: 4 - 25, mean 13.6
- **Nota**: 450 filas pero ~101 moleculas unicas (repeticiones experimentales)

### Repo original
- **Directorio**: `molecular_complexity/`
- **Origen**: https://github.com/croningp/molecular_complexity

## Operacionalizacion de omega

En el framework de la Danza Cosmica, omega(n) = numero de factores primos distintos de un concepto codificado como producto de primos. Para moleculas, la operacionalizacion analogica es:

- **omega_elements**: numero de tipos de elementos quimicos distintos (C, H, O, N, S, Cl, F, etc.). Cada elemento = un "primo" irreducible.
- **omega_heavy**: idem excluyendo hidrogeno.

Variables de control:
- **n_heavy_atoms**: numero total de atomos pesados (proxy de tamano molecular)
- **n_atoms_total**: numero total de atomos
- **MW**: peso molecular

## Resultados

### Correlaciones directas (todas p < 0.001)

| Variable | Dataset 1 (N=10,000) r | Dataset 1 rho | Dataset 2 (N=101) r | Dataset 2 rho |
|---|---|---|---|---|
| omega_elements | 0.5484 | 0.5593 | 0.4629 | 0.4128 |
| omega_heavy | 0.5478 | 0.5585 | 0.4629 | 0.4128 |
| n_heavy_atoms | 0.9453 | 0.9471 | 0.7259 | 0.6948 |
| n_atoms_total | 0.8729 | 0.8787 | 0.4586 | 0.4821 |
| MW | - | - | 0.6724 | 0.6357 |

### Correlacion parcial (omega controlando por tamano)

La prueba critica: si la correlacion MA~omega desaparece al controlar por n_heavy_atoms, la relacion es espuria.

| Dataset | r_parcial(omega_elements, MA | n_heavy_atoms) | p-value |
|---|---|---|
| Dataset 1 (N=10,000) | **0.5193** | **p ~ 0** |
| Dataset 2 (N=101) | **0.5716** | **p = 4.31e-10** |

**La correlacion parcial NO desaparece.** omega tiene un efecto independiente y fuerte sobre MA mas alla del tamano molecular.

### MA medio por valor de omega (Dataset 1)

| omega_elements | N | MA mean | MA std |
|---|---|---|---|
| 2 | 3 | 4.33 | 1.15 |
| 3 | 3,595 | 7.03 | 3.29 |
| 4 | 4,776 | 11.21 | 4.06 |
| 5 | 1,450 | 13.73 | 3.61 |
| 6 | 172 | 15.08 | 2.93 |
| 7 | 4 | 15.75 | 2.87 |

Patron monotonicamente creciente: cada tipo de elemento irreducible adicional agrega ~2-3 pasos de ensamblaje.

## Interpretacion

1. **A favor de la conjetura**: omega_elements correlaciona significativamente con MA (r~0.5) y esta correlacion persiste (r_parcial~0.52-0.57) despues de controlar por tamano molecular. La diversidad de componentes irreducibles predice complejidad de ensamblaje.

2. **El patron por bins es monotonicamente creciente** — exactamente lo que predice la conjetura: mas "primos" irreducibles = mas pasos de ensamblaje.

3. **Caveats**:
   - omega aqui son tipos de elementos quimicos, no factores primos semanticos — la operacionalizacion es analogica, no identica al framework formal
   - El rango de omega es estrecho (2-7) vs MA (2-25)
   - n_heavy_atoms es el predictor dominante (r=0.95 en Dataset 1) — el tamano molecular explica mas varianza que omega
   - Los datos son de un solo dominio (moleculas organicas) — falta validacion en otros dominios

4. **Status de la debilidad #8**: Ya no es N=0 datos. Hay 10,101 moleculas con evidencia positiva. Pero la operacionalizacion cross-domain (moleculas -> semantica) sigue pendiente.

## Archivos del analisis

| Archivo | Descripcion |
|---|---|
| `correlacion_MA_omega.py` | Script completo: parseo de formulas, correlaciones Pearson/Spearman, parciales, bins, graficas |
| `correlacion_MA_omega.png` | 6 scatter plots (2 datasets x 3 variables) con regresiones y medias por bin |
| `dataset_1_calculated_MA_10000.csv` | Datos limpios Dataset 1 |
| `dataset_2_experimental_MA_450.csv` | Datos limpios Dataset 2 |
| `molecular_complexity/` | Repo fuente original clonado |

## Proximos pasos sugeridos

1. **Operacionalizacion mas rica de omega**: usar grupos funcionales como "primos" en lugar de solo tipos de elementos (requiere RDKit)
2. **Regresion multivariada**: MA ~ omega + n_heavy_atoms + interacciones
3. **Validacion cross-domain**: aplicar la misma logica a conceptos semanticos y comparar las distribuciones
4. **Incluir en paper**: estos resultados pueden ir como evidencia empirica en P8 o como apendice
