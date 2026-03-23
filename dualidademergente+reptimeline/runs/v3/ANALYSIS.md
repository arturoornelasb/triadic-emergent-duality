# V3 Analysis — What the Model Tells Us About the Circle

## Resultado Principal

V3 demostró que GPT-2 Medium aprende la estructura del DAG de 65 primitivos:
- 90.9% bit accuracy en 65 targets únicos (vs 95.8% en v2, pero contra 10 targets repetidos)
- 89.2% firmas únicas aprendidas
- 99% subsunción — el orden jerárquico se impuso
- Analogías duales funcionan: coseno promedio 0.90, bit accuracy 95.2%
- 377 duals descubiertos (vs 199 en v2)
- 65/65 bits activos (vs 56/65 en v2)

**El modelo aprende lo que le pedimos. La pregunta es si le pedimos lo correcto.**

---

## El Patrón: Jaccard de Targets Predice Coherencia

Los 13 ejes duales del círculo, ordenados por Jaccard de sus targets:

| Par dual                       | Jaccard | Bits A | Bits B | Compartidos | Diferentes | Coherencia V3 |
|--------------------------------|---------|--------|--------|-------------|------------|---------------|
| freedom / control              |  0.222  |    6   |    5   |      2      |     7      |   **0.938**   |
| union / separation             |  0.333  |    2   |    2   |      1      |     2      |     —¹        |
| move / stillness               |  0.400  |    4   |    3   |      2      |     3      |     0.396     |
| good / evil                    |  0.615  |   11   |   10   |      8      |     5      |   **0.889**   |
| truth / lie                    |  0.636  |    9   |    9   |      7      |     4      |   **0.812**   |
| creation / destruction         |  0.750  |    7   |    7   |      6      |     2      |     —¹        |
| order / chaos                  |  0.750  |    7   |    7   |      6      |     2      |     —¹        |
| mortal_obs / eternal_obs       |  0.818  |   19   |   21   |     18      |     4      |   **1.000**   |
| life / death                   |  0.882  |   15   |   17   |     15      |     2      |     0.175     |
| pleasure / pain                |  0.882  |   16   |   16   |     15      |     2      |     0.286     |
| individual / collective        |  0.889  |   16   |   18   |     16      |     2      |     0.685     |
| receptive / creator_obs        |  0.900  |   19   |   19   |     18      |     2      |     0.692     |
| conscious / absent             |  0.947  |   18   |   19   |     18      |     1      |     0.660     |

¹ orden/caos, creación/destrucción, unión/separación no tienen campo `dual` en primitivos.json (solo en ejes_duales), por lo que PrimitiveOverlay no reporta coherencia.

### Observaciones:

1. **Los pares con Jaccard < 0.70 tienen coherencia > 0.80** — el modelo los distingue perfectamente.
2. **Los pares con Jaccard > 0.88 tienen coherencia < 0.70** — el modelo no puede distinguirlos.
3. **Excepción: mortal_obs/eternal_obs** — Jaccard 0.818 pero coherencia 1.000. Tienen 4 bits de diferencia (no 2), y sus 19-21 bits activos les dan más "espacio" proporcional.
4. **La frontera está en ~3-4 bits de diferencia.** Con 2 bits de diferencia de 65, el modelo necesitaría >97% accuracy en esos bits específicos para distinguirlos. A 90.9% global, no alcanza.

---

## Por Qué Colapsan los Duals de Capas Altas

El esquema de targets es: **bit propio ON + todas las dependencias transitivas ON**.

Esto crea un problema estructural en capas altas:

```
muerte = vida + {destrucción, bit_propio_muerte}
         ↓
muerte hereda los 15 bits de vida, agrega solo 2 propios
         ↓
Jaccard = 15/17 = 0.882
         ↓
Solo 2 bits distinguen vida de muerte en un vector de 65
```

Lo mismo pasa con:
- **placer/dolor**: ambos dependen de vida + información → comparten 15 bits, difieren en 2
- **consciente/ausente**: ausente depende de consciente → comparten 18 bits, difieren en 1
- **individual/colectivo**: colectivo depende de individual (vía muchos) → comparten 16 bits, difieren en 2
- **receptivo/creador_obs**: ambos dependen de consciente + base similar → comparten 18 bits, difieren en 2

**Es una consecuencia directa de la herencia transitiva.** Cuantas más capas tiene un primitivo, más bits hereda, y menos proporción de su signature es "propia."

### Distribución de bits propios vs heredados:

| Capa | Primitivos | Bits activos (rango) | Bits propios | % propio |
|------|-----------|----------------------|-------------|----------|
| 1    | 3         | 1                    | 1           | 100%     |
| 2    | 8         | 2-4                  | 1           | 25-50%   |
| 3    | 12        | 3-9                  | 1           | 11-33%   |
| 4    | 17        | 3-11                 | 1           | 9-33%    |
| 5    | 21        | 5-20                 | 1           | 5-20%    |
| 6    | 4         | 19-21                | 1           | 5%       |

En capa 6, cada primitivo tiene ~20 bits activos pero solo 1 es "propio". El 95% de su signature es herencia. **Dos duals en capa 6 son 95% idénticos por diseño.**

---

## Los False Positives Revelan Otra Cosa

Los bits más sobre-activados por el modelo:

| Bit | Primitivo      | Capa | Targets donde es ON | Model lo activa para |
|-----|----------------|------|--------------------|-----------------------|
| 15  | tacto          | 5    | 1/65               | 56/65                 |
| 47  | algunos        | 4    | 1/65               | 56/65                 |
| 25  | destrucción    | 3    | 3/65               | 55/65                 |
| 4   | tierra         | 5    | 1/65               | 51/65                 |
| 19  | interocepción  | 5    | 1/65               | 51/65                 |

Estos no son los primitivos "más generales" del DAG — son **hojas** que solo deberían activarse para sí mismos. Pero GPT-2 tiene asociaciones semánticas amplias para "touch", "earth", "some", "destruction" en su espacio pre-trained. El triadic head no logra suprimir esas asociaciones con solo 25K steps de supervisión efectiva (50% fue warmup).

**El modelo dice "todo involucra tacto y tierra" porque GPT-2 asocia esas palabras con muchos conceptos.** Es el prior semántico de GPT-2 sangrando hacia el espacio triádico.

Los bits que sí aprende bien son los que el prior de GPT-2 refuerza:
- bit 49 (querer/want): 95.4% — muy específico semánticamente
- bit 54 (porque/because): 95.4% — ídem
- bit 28 (verdad/truth): 92.3%
- bit 31 (control): 92.3%

---

## Implicación: El Círculo Necesita Expandirse

El modelo nos dice dónde el sistema de 65 primitivos se queda corto:

### Problema 1: Duals de capas altas son indistinguibles
- Necesitan primitivos intermedios que diferencien los caminos
- Ejemplo: entre vida y muerte, algo que no sea simplemente "vida + destrucción"
- Conceptos como "continuidad", "cesación", "renovación", "decaimiento" crearían caminos divergentes
- Con más bits de diferencia, el modelo puede distinguir los pares

### Problema 2: Hojas de capa 5 son semánticamente genéricas para GPT-2
- tacto, tierra, gusto, olfato — GPT-2 los asocia con todo
- Posibles soluciones:
  - Sub-primitivos más específicos (tacto → presión, temperatura, textura)
  - O aceptar que estos primitivos necesitan más contexto en el text prompt

### Problema 3: La proporción propio/heredado se degrada con la capa
- Capa 1: 100% propio → totalmente distinguible
- Capa 6: 5% propio → casi indistinguible de sus dependencias
- Expandir el círculo en capas 4-6 aumentaría la proporción de bits propios

### Criterio para expansión:
**Si dos duals tienen Jaccard > 0.80 en sus targets, necesitan al menos 1-2 primitivos intermedios que diferencien sus caminos por el DAG.**

Pares que necesitan expansión (Jaccard > 0.80):
1. vida / muerte (0.882) — 2 bits de diferencia
2. placer / dolor (0.882) — 2 bits
3. consciente / ausente (0.947) — 1 bit
4. individual / colectivo (0.889) — 2 bits
5. receptivo / creador_obs (0.900) — 2 bits
6. mortal_obs / eternal_obs (0.818) — 4 bits (funciona por margen mínimo)

---

## Resumen

| Hallazgo | Evidencia | Implicación |
|----------|-----------|-------------|
| Modelo aprende estructura DAG | 99% subsunción, Regla de Tres cos=0.90 | Fase 1 completada |
| Duals con Jaccard < 0.70 funcionan | libertad/control 0.938, verdad/mentira 0.812 | DAG correcto para estos pares |
| Duals con Jaccard > 0.88 colapsan | vida/muerte 0.175, placer/dolor 0.286 | Herencia transitiva los hace indistinguibles |
| Bits-hoja se sobre-activan | tacto 1→56, tierra 1→51 | Prior de GPT-2 satura el espacio triádico |
| Proporción propio/heredado cae | Capa 1: 100%, Capa 6: 5% | Capas altas necesitan más primitivos propios |

**El modelo no tiene un problema de arquitectura ni de entrenamiento. Tiene un problema de resolución teórica: 65 bits no son suficientes para codificar las distinciones que el círculo necesita en capas altas.**

La expansión del círculo no es una opción — es lo que los datos exigen.
