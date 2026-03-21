# Doc 35: Firmas Algebraicas de Dualidad

**Script:** `scripts/duality_signatures.py`
**Alcance:** 14 dualidades, 3 tipos de firma (ancla, dependencia, extendida)
**Prerequisito:** Doc 32 (álgebra de composición — preguntas abiertas)

---

## 1. Tres tipos de firma

| Tipo | Definición | Uso |
|------|-----------|-----|
| σ_ancla(Dk) | ∏ primo(a) para a ∈ anclas | Identidad mínima de la dualidad |
| σ_dep(Dk) | ∏ primo(a) para a ∈ ancestors(anclas) | Fundamento completo (transitive closure) |
| σ_ext(Dk) | ∏ primo(a) para a ∈ anclas ∪ secundarios | Identidad operativa |

### Valores por dualidad

| Dualidad | log₂(σ_ancla) | log₂(σ_dep) | log₂(σ_ext) | #Ancestros |
|----------|---------------|-------------|-------------|------------|
| D1_existir | 10.21 | 0.00 | 10.21 | 0 |
| D2_espacio | 13.63 | 16.39 | 24.65 | 3 |
| D3_tiempo | 10.57 | 27.54 | 34.89 | 5 |
| D4_posibilidad | 24.27 | 69.78 | 38.29 | 12 |
| D5_identidad | 31.30 | 71.16 | 46.29 | 12 |
| D6_movimiento | 23.98 | 22.33 | 39.56 | 4 |
| D7_orden | 12.85 | 35.74 | 38.93 | 6 |
| D8_uno_muchos | 15.26 | 15.82 | 31.72 | 2 |
| D9_dentro_fuera | 4.95 | 14.36 | 18.38 | 2 |
| D10_parte_todo | 15.86 | 35.15 | 23.66 | 5 |
| D11_vida_muerte | 14.22 | 88.93 | 48.88 | 15 |
| D12_causa_efecto | 16.04 | 37.13 | 16.04 | 7 |
| D13_semejante_diferente | 8.14 | 43.70 | 8.14 | 8 |
| D14_sujeto_objeto | 14.64 | 99.24 | 119.76 | 17 |

**D1 tiene σ_dep = 1** (producto vacío, raíces sin ancestros). **D14 tiene σ_dep máximo** (99.24 bits, 17 ancestros), coherente con su posición terminal.

---

## 2. Verificaciones algebraicas

- σ_dep(D1) = 1 (raíces sin ancestros) ✓
- GCD(cualquiera, D1) = 1 ✓
- LCM(Di,Dj) ≥ max(σ_dep(Di), σ_dep(Dj)) ✓
- **14/14 firmas σ_dep son únicas** — cada dualidad tiene una identidad algebraica distinta

---

## 3. Distancia conceptual

dist(Di, Dj) = log₂(LCM/GCD) — cuántos primos hay que "añadir" para cubrir ambas dualidades.

### Pares más cercanos y lejanos

| Dualidad | Más cercano | dist | Más lejano | dist |
|----------|-------------|------|------------|------|
| D1_existir | D9_dentro_fuera | 14.4 | D14_sujeto_objeto | 99.2 |
| D3_tiempo | D6_movimiento | 5.2 | D14_sujeto_objeto | 71.7 |
| D5_identidad | D13_semejante | 27.5 | D1_existir | 71.2 |
| D7_orden | D13_semejante | 8.0 | D14_sujeto_objeto | 63.5 |
| D11_vida_muerte | D14_sujeto_objeto | 23.6 | D1_existir | 88.9 |

La distancia D3↔D6 = 5.2 bits es la mínima del sistema: Tiempo y Movimiento comparten casi todos sus ancestros. La distancia D1↔D14 = 99.2 bits es la máxima: la ontología pura (Existir) y la fenomenología (Sujeto/Objeto) están algebraicamente tan lejos como es posible.

---

## 4. Orden de divisibilidad

σ_dep(Di) | σ_dep(Dj) iff todo ancestro de Di-anclas es también ancestro de Dj-anclas.

### Diagrama de Hasse (σ_dep)

```
D1 ─┬─ D2 ─┬─ D4
    │       └─ D14
    ├─ D6 ─┬─ D3 ─┬─ D7 ── D13 ─┬─ D5
    │       │      └─ D12         ├─ D11
    │       └─ D4                 └─ D14
    ├─ D8 ─┬─ D7
    │      └─ D10 ── D5
    └─ D9 ─┬─ D4
           ├─ D10
           ├─ D11
           └─ D14
```

**Aciclicidad:** PASS (es un DAG)

**Consistencia con ordenamiento:** 14/21 aristas Hasse = 0.667

7 aristas inconsistentes (dualidad "posterior" divide a una "anterior"):
- D6 → D3, D4 (Movimiento precede a Tiempo y Posibilidad algebraicamente)
- D8 → D7 (Uno/Muchos precede a Orden)
- D9 → D4, D10 → D5, D13 → D5, D11 (espirales preceden a sus "mayores")

Estas inconsistencias reflejan que el orden algebraico (quién tiene ancestros más fundamentales) no coincide exactamente con el orden filosófico postulado.

---

## 5. Spearman algebraico

Rank por log₂(σ_dep) vs posición en la secuencia.

| Grupo | ρ (σ_dep) | p | ρ (σ_ext) | Mejor |
|-------|-----------|---|-----------|-------|
| Círculo D1-D7 | +0.607 | ~0.20 | +0.857 | σ_ext |
| Espiral D8-D14 | +0.857 | ~0.05 | +0.000 | σ_dep |
| Combinado D1-D14 | +0.521 | ~0.10 | +0.055 | σ_dep |

La **espiral muestra ρ = 0.857 con p ~ 0.05** usando σ_dep — la correlación más fuerte de todo el análisis. Esto significa que el "peso algebraico" (acumulación de ancestros) predice el orden de la espiral con alta fidelidad.

Para el círculo, σ_ext (que incluye secundarios) obtiene mejor correlación (0.857) que σ_dep (0.607), sugiriendo que los secundarios codifican información posicional relevante en la secuencia del círculo.

---

## 6. Respuestas a las 4 preguntas del Doc 32

### P1: ¿Las firmas distinguen las dualidades?

**SÍ.** Las 14 σ_dep son únicas. Cada dualidad tiene una identidad algebraica distinta determinada por su conjunto de ancestros transitivos.

### P2: ¿La divisibilidad refleja el orden de emergencia?

**PARCIALMENTE.** Consistencia 0.667: 14/21 aristas Hasse respetan el orden. Las 7 inconsistencias se concentran en D6 (Movimiento tiene pocos ancestros pese a ser posición 6) y las espirales (D8-D10 tienen ancestros más fundamentales que D4-D5).

### P3: ¿El Spearman algebraico mejora el análisis?

**SÍ para la espiral.** ρ = 0.857 (p ~ 0.05) para D8-D14 con σ_dep es la mejor correlación observada, superior al ρ depth = 0.643 del doc 34. Para el círculo, ρ = 0.607 mejora el depth-based (0.321) pero no alcanza significancia.

### P4: ¿σ_ext mejora sobre σ_dep?

**Depende del contexto.** σ_dep gana 2/3 comparaciones globales y es mejor para la espiral y el combinado. σ_ext gana decisivamente para el círculo (0.857 vs 0.607) porque los secundarios del círculo codifican orden posicional. Recomendación: usar σ_dep como métrica principal y σ_ext como complemento para el círculo.

---

## 7. Conclusión

Las firmas algebraicas confirman que las 14 dualidades tienen identidades únicas codificadas en el DAG de primitivos. La espiral D8-D14 es algebraicamente más "limpia" que el círculo D1-D7: su orden emerge naturalmente del peso de ancestros acumulados. La distancia conceptual D1↔D14 = 99.2 bits cuantifica el gradiente ontología → fenomenología que recorre el sistema completo.
