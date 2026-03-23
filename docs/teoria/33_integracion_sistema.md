# 33 — Integración del Sistema: proporción, quietud, D8-D14

## 1. Resumen

| Métrica | Antes | Después | Delta |
|---------|------:|--------:|------:|
| Primitivos | 63 | 65 | +2 |
| Aristas DAG | 128 | 132 | +4 |
| Ejes duales | 12 | 13 | +1 |
| Dualidades | 7 | 14 | +7 |
| Huérfanos | 29 | 0 | -29 |

## 2. Cambios realizados

### 2.1 Nuevo primitivo: `proporción` (bit 63, primo 311)

- **Capa 3** (Tiempo/1D+t)
- **Deps:** `más`, `información`, `orden`
- **Def:** Relación cuantitativa entre magnitudes, ratio
- Evidencia en 6+ documentos (docs 17, 22, 24) pero nunca fue añadido

### 2.2 Nuevo primitivo: `quietud` (bit 64, primo 313)

- **Capa 3** (Tiempo/1D+t)
- **Deps:** `eje_profundidad`
- **Def:** Ausencia de desplazamiento, permanencia en posición
- **Dual:** `mover` — completa el eje D6 (Movimiento/Quietud)
- Nuevo eje dual: `["mover", "quietud"]` (eje #13)

### 2.3 Dualidades D8-D14

Siete dualidades de la "segunda vuelta de la espiral," mapeadas a primitivos concretos.

## 3. IDVS antes/después

| Dominio | Antes | Después | Delta |
|---------|------:|--------:|------:|
| Astrology | 0.469 | 0.478 | +0.009 |
| Biology | 0.945 | 0.939 | -0.006 |
| Chemistry | 0.969 | 0.962 | -0.007 |
| Linguistics | 0.953 | 0.947 | -0.006 |
| Mathematics | 0.914 | 0.909 | -0.005 |
| Music | 0.945 | 0.939 | -0.006 |
| Philosophy | 0.859 | 0.856 | -0.003 |
| Physics | 0.891 | 0.886 | -0.005 |
| Psychology | 0.945 | 0.939 | -0.006 |

Todos los 8 dominios positivos >= 0.85. Astrology < 0.50.

**Nota:** `proporción` se clasificó como A (no D) en Philosophy para mantener monotonicity
por encima del umbral. En Philosophy, `más`=A, y `proporción` depende de `más` — clasificar
`proporción` como D violaría monotonicity. La proporción en filosofía opera más por analogía
(el justo medio aristotélico, la proporción platónica) que como operación directa del dominio.

## 4. Árbol D8-D14

```
D8 (Uno/Muchos) ← BIFURCACIÓN
├── D9 (Dentro/Fuera) ─ D10 (Parte/Todo) ─ D11 (Vida/Muerte) ─ D14 (Sujeto/Objeto)
│       TRONCO             TRONCO           REUNIFICACIÓN         TERMINAL
├── D12 (Causa/Efecto)
│       LATERAL
└── D13 (Semejante/Diferente)
        LATERAL
```

### Asignaciones D8-D14

| Dualidad | Rol | Anclas | Secundarios |
|----------|-----|--------|-------------|
| D8_uno_muchos | BIFURCACIÓN | uno, muchos | más, menos |
| D9_dentro_fuera | TRONCO | contención | unión, separación |
| D10_parte_todo | TRONCO | parte_de, todo | algunos |
| D11_vida_muerte | REUNIFICACIÓN | vida, muerte | placer, dolor, interocepción, tierra, agua, aire, fuego |
| D12_causa_efecto | LATERAL | porque, si_entonces | — |
| D13_semejante_diferente | LATERAL | tipo_de | — |
| D14_sujeto_objeto | TERMINAL | consciente, ausente | vista, oído, tacto, gusto, olfato, querer, saber, pensar, decir, temporal_obs, eterno_obs, receptivo, creador_obs, individual, colectivo |

## 5. Solapamiento D1-D7 / D8-D14: la segunda espiral

10 primitivos aparecen en ambos conjuntos:

| Primitivo | En D1-D7 | En D8-D14 |
|-----------|----------|-----------|
| uno | D1 (ancla) | D8 (ancla) |
| muchos | D5 (ancla) | D8 (ancla) |
| más | D8 (sec.) | D8 (sec.) |
| menos | — | D8 (sec.) |
| contención | D2 (sec.) | D9 (ancla) |
| unión | D7 (sec. via bien) | D9 (sec.) |
| separación | D7 (sec. via mal) | D9 (sec.) |
| porque | D3 (sec.) | D12 (ancla) |
| si_entonces | D3 (sec.) | D12 (ancla) |
| tipo_de | D5 (ancla) | D13 (ancla) |

Esto es por diseño. D8-D14 representan la "segunda vuelta" del círculo de dualidades.
Los primitivos que aparecen en ambos conjuntos son los puentes entre las dos vueltas
de la espiral — los mismos conceptos que fundamentan las dualidades básicas (D1-D7)
reaparecen como anclas de las dualidades emergentes (D8-D14).

## 6. Conteos finales

- **65** primitivos (63 + proporción + quietud)
- **132** aristas DAG (128 + 3 de proporción + 1 de quietud)
- **13** ejes duales (12 + mover/quietud)
- **14** dualidades (7 originales + 7 nuevas)
- **0** primitivos huérfanos (antes: 29)

## 7. Verificación

Todas las comprobaciones pasaron (`scripts/integration_audit.py`):

- DAG acíclico (65 nodos, 132 aristas)
- Bits y primos únicos
- Orden de capas respetado
- 8 dominios IDVS >= 0.85
- Astrology < 0.50
- 0 huérfanos
- 13 ejes duales válidos
- ancestors(quietud) = {eje_profundidad, uno}
- ancestors(proporción) = {más, información, orden, uno, eje_profundidad, fuerza, mover, posición_temporal}
