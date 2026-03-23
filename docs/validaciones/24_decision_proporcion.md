# Documento 24: Decisión Formal de Proporción — Simulación 63→64

| Métrica | Antes (63) | Después (64) |
|---------|------------|--------------|
| Primitivos | 63 | 64 |
| Bits | 63 (no alineado) | 64 (2⁶, word completo) |
| Espacio de estados | 3⁶³ ≈ 1.14×10³⁰ | 3⁶⁴ ≈ 3.42×10³⁰ |
| Primo del 64o | — | 311 |
| Núcleo universal | 13 (D/D/D/D/D/D) | 14 (D/D/D/D/D/D) |
| VIOLATED deps | 0 | 0 |
| Dependencias circulares | No | No |
| **Decisión** | — | **DEFER** |

## I. Recapitulación de la Evidencia

El Doc 17 identificó por primera vez el gap de *proporción* en 3 dominios (música, química, biología). El Doc 22 expandió la evidencia a 6/6 dominios con clase DIRECT universalmente:

| Dominio | Manifestación | Workaround actual |
|---------|--------------|-------------------|
| Música (T8) | Series armónica (1:2, 2:3) | información + orden + unión |
| Química (T9) | Estequiometría, Keq | debe + orden + más + todo |
| Biología (T10) | Ratios mendelianos (3:1) | debe + orden + más |
| Matemáticas (T11) | Números racionales Q, Euclides V | más + información + orden + todo |
| Filosofía (T12) | Línea Dividida, mesotes | equilibrio + orden + más + verdad |
| Física (T13) | Constante α ≈ 1/137, Planck | debe + orden + información + más |

El primitivo común a todos los workarounds: **orden** (6/6) y **más** (5/6).

## II. Implicaciones Algebraicas de 63→64

### 2.1 Word Size

63 bits NO es una potencia de 2 ni está alineado a byte (7.875 bytes). 64 bits = 2⁶ es un word completo: el tamaño estándar de registro en arquitecturas x86-64 y ARM64. Cada primitivo mapea exactamente a un bit en un `uint64`.

### 2.2 Espacio de Estados

Con 3 estados por primitivo (+, 0, null):
- 3⁶³ ≈ 1.14 × 10³⁰ estados
- 3⁶⁴ ≈ 3.42 × 10³⁰ estados (factor ×3, +200%)

### 2.3 Producto Primo Total

Cada primitivo tiene un número primo asociado (identidad algebraica). El producto total ∏(p₁..p₆₃) es un entero de ~80 dígitos. Multiplicar por 311 (el 64o primo) extiende este producto a ~83 dígitos. El producto primo codifica la identidad algebraica del modelo completo.

### 2.4 Compatibilidad con TriadicGPT

TriadicGPT codifica estados como vectores base-3 de dimensión N. 63 → 64 dimensiones añade una dimensión al vector de estado. 64 dimensiones es computacionalmente más limpio (byte-aligned) que 63.

## III. Simulación Computacional

### 3.1 Dependency Check

Se verificó con `simulate_proportion_64.py`:
- `proporcion` definido con capa=3, deps=[más, información, orden]
- Todas las dependencias apuntan a capas inferiores (✓)
- 0 VIOLATED con 64 primitivos
- 0 dependencias circulares (verificación topológica)
- 3 nuevos pares de dependencia (proporcion→más, proporcion→información, proporcion→orden)

### 3.2 Consistencia de Anclas por Dominio

Se re-evaluaron las anclas sensibles a proporción en los 6 dominios. Resultado: mejora positiva en todos los dominios. La mejora promedio ponderada es consistente con los +16.5pp reportados en Doc 22.

### 3.3 Núcleo Universal: 13 → 14

Proporción sería DIRECT en los 6 dominios → entra al núcleo universal. El núcleo crece de 13 a 14 primitivos sin desplazar ningún primitivo existente.

## IV. Matriz de Decisión

### 4.1 Argumentos a Favor

1. **Word completo**: 64 = 2⁶, byte-aligned
2. **Espacio de estados**: expansión algebraica limpia (×3)
3. **Identidad prima**: 311 es primo, sin colisión
4. **Evidencia universal**: D/D/D/D/D/D en 6/6 dominios
5. **Mejora métrica**: +16.5pp promedio en consistencia de anclas
6. **Cierra el gap**: el único gap estructural identificado
7. **Falsificable**: testeable en nuevos dominios inmediatamente
8. **Sin violaciones**: 0 VIOLATED, 0 circulares

### 4.2 Argumentos en Contra

1. **Rompe estabilidad**: el modelo ha sido 63 durante 6 validaciones
2. **Re-validación**: todos los tests existentes necesitarían re-ejecución
3. **Evaluador único**: toda la evidencia proviene de un solo evaluador
4. **Riesgo incremental**: si se acepta 64, ¿qué impide 65?
5. **Impacto computacional**: TriadicGPT necesita actualización

### 4.3 Condiciones para Aceptación Futura

1. Validación inter-evaluador (κ ≥ 0.6) confirma el mapeo de proporción en ≥ 3 dominios
2. Al menos 1 dominio adicional (7o) confirma proporción como DIRECT
3. Implementación de TriadicGPT actualizada y testeada con 64 dimensiones
4. Permutation tests confirman significancia estadística de la mejora
5. Sin efectos adversos en validaciones existentes tras re-ejecución

## V. Decisión: DEFER

**El modelo permanece en 63 primitivos.**

La evidencia justifica fuertemente la adición de proporción. Sin embargo, la decisión se difiere hasta que:

(a) Se aplique el protocolo inter-evaluador (Doc 26) por un evaluador independiente
(b) Se complete la validación de lingüística (Doc 25 / Test 15)
(c) Se actualice la implementación computacional en TriadicGPT

Proporción se documenta como una **predicción estructural** del modelo — el primer primitivo cuya existencia fue PREDICHA por análisis cross-dominio en lugar de derivada de primeros principios filosóficos.

## VI. Predicciones Falsificables

| ID | Predicción | Criterio |
|----|-----------|----------|
| F1 | Lingüística confirmará proporción como DIRECT | Test 15 |
| F2 | Mejora ≥5pp en consistencia de anclas lingüísticas | Conservador (avg=16.5pp) |
| F3 | 0 nuevas VIOLATED con 64 primitivos en cualquier dominio | Topológico |
| F4 | El 65o candidato, si existe, emergará de un 8o dominio | Principio de parsimonia |
| F5 | κ inter-evaluador ≥ 0.7 para clasificación de proporción | Doc 26 |

## VII. Conclusión

Proporción es, hasta la fecha, la predicción más fuerte del modelo 7×7: un concepto cuya ausencia se detectó independientemente en 6 dominios, con un candidato formal completamente especificado (bit=63, primo=311, capa=3, deps=[más, información, orden]) y 0 violaciones verificadas. La decisión DEFER es prudente, no escéptica — el modelo espera validación independiente antes de crecer.

---

**Script asociado**: `scripts/simulate_proportion_64.py`
**Documento previo**: Doc 22 (Proporción: Evidencia Universal en 6 Dominios)
**Siguiente paso**: Doc 25 (Validación Lingüística) → Doc 26 (Protocolo Inter-Evaluador)
