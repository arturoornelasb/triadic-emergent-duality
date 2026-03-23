# Propuesta del Primitivo `proporcion` (64o Primitivo)
## Evidencia Cross-Domain, Definicion Formal y Validacion Retroactiva
### J. Arturo Ornelas Brand — Marzo 2026

---

## Resumen

Tres dominios independientes (musica T8, quimica T9, biologia T10) identificaron el MISMO gap estructural: el modelo de 63 primitivos carece de un primitivo para **proporcion/ratio**. Este documento formaliza la propuesta, la valida retroactivamente en los tres dominios, y pre-registra una prediccion falsificable para Test 11 (matematicas).

| Metrica | Resultado |
|---------|-----------|
| Dominios que confirman el gap | 3/3 (musica, quimica, biologia) |
| Nucleo comun de workarounds | mas, orden |
| Complejidad promedio de workaround | 3.3 primitivos → 1 |
| Mejora anclas musica | +12.6pp |
| Mejora anclas quimica | +27.0pp |
| Mejora anclas biologia | +14.5pp |
| Patron cross-domain predicho | D/D/D (se une a 20 primitivos D/D/D) |
| Prediccion T11 | DIRECT (falsificable) |

**Status**: PROPUESTA — `primitivos.json` NO se modifica.

---

## I. Evidencia del Gap (3 Dominios)

### 1.1 El patron recurrente

En cada dominio validado, ciertos conceptos fundamentales requirieron workarounds de 3-4 primitivos para expresar lo que deberia ser un solo primitivo:

| Dominio | Manifestacion | Workaround | Referencia |
|---------|--------------|------------|------------|
| Musica (T8) | Serie armonica (1:2, 2:3, 3:4...) | informacion + orden + union | Helmholtz (1863) |
| Quimica (T9) | Estequiometria (2H2 + O2 → 2H2O) | debe + orden + mas + todo | Lavoisier (1789) |
| Biologia (T10) | Ratios mendelianos (3:1, 9:3:3:1) | debe + orden + mas | Mendel (1866) |

### 1.2 Nucleo comun

El analisis de los tres workarounds revela un nucleo compartido:

- **orden** aparece en 3/3 workarounds (regularidad de la relacion)
- **mas** aparece en 2/3 workarounds explicitamente (cantidades comparadas)
- **informacion** aparece en 1/3 pero es presupuesto por los otros (patron del ratio)

Este nucleo comun {mas, informacion, orden} se convierte en las dependencias propuestas.

### 1.3 Conceptos especificos que requieren proporcion

**Musica**: Serie armonica, consonancia (ratios enteros simples), compas (divisiones proporcionales 3/4, 4/4, 6/8), temperamento igual (raiz 12a de 2), rango dinamico.

**Quimica**: Coeficientes estequiometricos, concentracion (pH = -log[H+]), constantes de equilibrio (Keq = [productos]/[reactivos]), electronegatividad (escala Pauling), ley de proporciones definidas (Proust 1799).

**Biologia**: Ratios mendelianos (3:1 monohibrido, 9:3:3:1 dihibrido), escalamiento alometrico (Kleiber: M^0.75), equilibrio Hardy-Weinberg (p2 + 2pq + q2 = 1), sex ratio 1:1 (Fisher).

---

## II. Propuesta Formal

### 2.1 Definicion

```json
{
  "bit": 63,
  "primo": 311,
  "nombre": "proporcion",
  "capa": 3,
  "deps": ["mas", "informacion", "orden"],
  "def": "Relacion cuantitativa entre cantidades, ratio, medida relativa"
}
```

### 2.2 Verificaciones

- **311 es primo**: Verificado
- **311 no esta en uso**: Verificado (ningun primitivo existente usa 311)
- **Bit 63 no esta en uso**: Verificado
- **Deps en capas inferiores/iguales**: mas (capa 2), informacion (capa 1), orden (capa 3) — todas <= capa 3

### 2.3 Decisiones de diseno

**1. Primitivo singular (sin par dual)**

Los ejes duales del modelo son fenomenologicos: bien/mal, vida/muerte, verdad/mentira. Proporcion es *estructural*, no fenomenologico. "Desproporcion" no es un opuesto constitutivo — ya se cubre con caos + separacion. Precedente: `porque` y `si_entonces` son primitivos singulares en capa 3 sin par dual.

**2. Capa 3 (Tiempo)**

Los tres workarounds utilizan primitivos de capas 2-3. El nucleo comun (orden + mas) vive en capas 2-3. Proporcion se necesita ANTES de equilibrio (capa 4): no se puede tener ecuacion sin proporcion. Es mas fundamental que los cuantificadores de capa 4 (algunos, muchos, todo).

**3. Dependencias: mas + informacion + orden**

- `mas` = cantidades que se comparan (la materia prima del ratio)
- `informacion` = el patron/estructura del ratio
- `orden` = la regularidad de la relacion

Nota: estas son las mismas dependencias que `tipo_de` (capa 4). Clasificar y medir son dos emergencias distintas de los mismos ingredientes — un patron que refuerza la coherencia de la propuesta.

---

## III. Validacion Retroactiva

### 3.1 Musica (Test 8)

Entrada propuesta: DIRECT — Serie armonica / Intervalo / Ratio de frecuencia / Compas

Anclas mejoradas al incluir proporcion:

| Ancla | Antes | Despues | Razon |
|-------|-------|---------|-------|
| serie_armonica | 4 prims | 5 prims | La serie armonica ES un conjunto de proporciones enteras |
| consonancia | 4 prims | 5 prims | Consonancia = ratios enteros simples (Helmholtz 1863) |
| compas | 3 prims | 4 prims | Compases son divisiones proporcionales |
| intervalo | 3 prims | 4 prims | Intervalos musicales SON ratios de frecuencia |

**Consistencia de anclas**: 23.8% → 36.4% (+12.6 puntos porcentuales)

### 3.2 Quimica (Test 9)

Entrada propuesta: DIRECT — Estequiometria / Concentracion / Constante de equilibrio

Anclas mejoradas:

| Ancla | Antes | Despues | Razon |
|-------|-------|---------|-------|
| estequiometria | 5 prims | 6 prims | Estequiometria ES relaciones proporcionales |
| constante_equilibrio | 4 prims | 5 prims | Keq = [productos]/[reactivos] es un ratio |
| pH | 4 prims | 5 prims | pH es una proporcion logaritmica de concentracion |
| ley_proporciones_definidas | 4 prims | 5 prims | Proust (1799): LA ley de las proporciones |

**Consistencia de anclas**: 13.0% → 40.0% (+27.0 puntos porcentuales)

### 3.3 Biologia (Test 10)

Entrada propuesta: DIRECT — Ratios mendelianos / Leyes alometricas / Hardy-Weinberg

Anclas mejoradas:

| Ancla | Antes | Despues | Razon |
|-------|-------|---------|-------|
| herencia_mendeliana | 5 prims | 6 prims | Mendel (1866): ratios 3:1 y 9:3:3:1 |
| escalamiento_alometrico | 4 prims | 5 prims | Kleiber: tasa metabolica ∝ M^(3/4) |
| Hardy_Weinberg | 4 prims | 5 prims | p2 + 2pq + q2 = 1 define proporciones alelicas |
| sex_ratio | 4 prims | 5 prims | Ratio 1:1 de Fisher mantenido por seleccion |

**Consistencia de anclas**: 12.1% → 26.7% (+14.5 puntos porcentuales)

### 3.4 Resumen retroactivo

La adicion de proporcion mejora la consistencia de anclas en los tres dominios:

| Dominio | Antes | Despues | Mejora |
|---------|-------|---------|--------|
| Musica | 23.8% | 36.4% | +12.6pp |
| Quimica | 13.0% | 40.0% | +27.0pp |
| Biologia | 12.1% | 26.7% | +14.5pp |

---

## IV. Prediccion para Test 11 (Matematicas)

### 4.1 Pre-registro

**Prediccion**: proporcion seria el primitivo MAS DIRECT en matematicas.

**Evidencia**:
- Euclides, Elementos Libro V: libro ENTERO dedicado a proporcion/ratio
- Numeros racionales Q = {p/q : p,q ∈ Z, q ≠ 0} SON proporciones
- Teoria de Eudoxo de la proporcion = precursor de los numeros reales
- Trigonometria: seno, coseno, tangente son TODOS ratios
- Probabilidad: P(A) = favorables/total es un ratio
- Algebra lineal: eigenvalores expresan relaciones proporcionales

### 4.2 Falsificabilidad

Si Test 11 mapea proporcion como ANALOGICAL o NULL, la propuesta pierde su evidencia mas fuerte. La prediccion es genuinamente falsificable.

---

## V. Impacto en el Modelo

### 5.1 Reduccion de complejidad

La complejidad promedio de los workarounds se reduce de 3.3 primitivos a 1:

| Dominio | Workaround actual | Con proporcion | Reduccion |
|---------|------------------|----------------|-----------|
| Musica | informacion + orden + union (3) | proporcion (1) | 3x |
| Quimica | debe + orden + mas + todo (4) | proporcion (1) | 4x |
| Biologia | debe + orden + mas (3) | proporcion (1) | 3x |

### 5.2 Patron cross-domain

proporcion seria D/D/D (DIRECT en los 3 dominios validados), uniendose a 20 primitivos existentes con ese patron. Todos pertenecen a capas 1-4, excepto individual y colectivo (capa 5).

### 5.3 Verificacion de dependencias

Las tres dependencias propuestas (mas, informacion, orden) son CONFIRMED en los 3 dominios. No hay ninguna dependencia que no haya sido validada independientemente.

---

## VI. Conclusion

La propuesta de proporcion como 64o primitivo se sostiene sobre:

1. **Evidencia convergente**: 3 dominios independientes identificaron el mismo gap
2. **Nucleo comun**: los workarounds comparten las mismas dependencias
3. **Mejora retroactiva**: la consistencia de anclas mejora en 3/3 dominios
4. **Prediccion falsificable**: Test 11 (matematicas) deberia producir la confirmacion mas fuerte
5. **Coherencia interna**: mismas deps que tipo_de, capa correcta, primo verificado

**Status**: PROPUESTA. No se modifica primitivos.json hasta completar Test 11 y evaluar la prediccion.

---

*Parte del manuscrito "Expansion del Circulo de Emergencia de Dualidades."*
