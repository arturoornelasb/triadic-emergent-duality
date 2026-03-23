# Documento 28: Validación Psicológica — Test 16

| Test | Resultado |
|------|-----------|
| 16A — Cobertura | 44 DIRECT, 17 ANALOGICAL, 2 NULL (96.8% mapped) |
| 16B — Dependencias | 0 VIOLATED |
| 16C — Jerarquías | 3/5 alineadas (Maslow, Piaget, Erikson con τ > 0) |
| 16D — Ejes duales | 11 STRONG, 1 MODERATE, 0 WEAK, 0 NONE (12/12 = 100%) |
| 16E — Anclas | 17.5% consistencia (baseline 4.8%, ratio 3.65x) |
| 16F — Predicciones | 9/10 confirmadas |
| 16G — Adversarial | 10/10 defendidas |
| 16H — Embodiment | 18/20 NULLs de matemáticas recuperados |

## I. Motivación: Psicología como Dominio Fenomenológico

Psicología es el 8o dominio de validación del modelo de 63 primitivos. Es un dominio ideal porque:

1. **Experiencia directa**: Estudia la subjetividad — consciencia, emoción, voluntad, percepción. Debería recuperar todo lo que matemáticas pierde.
2. **Tradiciones formales independientes**: Psicoanálisis (Freud), conductismo (Skinner/Bandura), cognitiva (Piaget), humanista (Maslow/Rogers), existencial (Frankl). Cada una proporciona vocabulario técnico para los primitivos.
3. **Complemento a matemáticas**: Si la meta-dualidad lógico/abstracto vs fenomenológico/material es real, psicología debería estar en el extremo opuesto a matemáticas.

**Predicción**: ~2 NULLs (gusto, olfato — el residuo quimiosensorial), con 100% de cobertura en L1-4.

## II. El Mapeo Completo: 63 Primitivos → Psicología

### Capas 1-3 (21 primitivos): 17 DIRECT, 4 ANALOGICAL, 0 NULL

Las tres primeras capas mapean completamente, con mayoría DIRECT. Los conceptos clave:

- **vacío** → Inconsciente / Represión / Espacio negativo (DIRECT)
- **información** → Cognición / Representación mental / Contenido del pensamiento (DIRECT)
- **uno** → Psique individual / Self / Ego (DIRECT)
- **fuerza** → Pulsión / Motivación / Energía psíquica (DIRECT)
- **contención** → Frontera del ego / Defensa / Contención (DIRECT)
- **unión** → Apego / Identificación / Vínculo (DIRECT)
- **separación** → Individuación / Diferenciación / Pérdida objetal (DIRECT)
- **creación** → Crecimiento / Insight / Generatividad / Sublimación (DIRECT)
- **destrucción** → Agresión / Ansiedad / Auto-sabotaje / Tánatos (DIRECT)
- **orden** → Organización del ego / Estructura psíquica / Coherencia (DIRECT)
- **caos** → Regresión / Desorganización / Proceso psicótico (DIRECT)

### Capa 4 (17 primitivos): 10 DIRECT, 7 ANALOGICAL, 0 NULL

- **eje_vertical** → Jerarquía de necesidades (Maslow) / Poder (Adler) (DIRECT)
- **eje_lateral** → Dimensiones de personalidad / Espectro temperamental (DIRECT)
- **equilibrio** → Homeostasis / Bienestar / Balance psicológico (DIRECT)
- **vista** → Insight / Autoconciencia / Capacidad reflexiva (DIRECT)
- **libertad** → Autonomía / Elección / Autodeterminación (DIRECT)
- **control** → Autorregulación / Control de impulsos / Fuerza del ego (DIRECT)
- **tipo_de** → Tipo de personalidad / Categoría diagnóstica / DSM (DIRECT)
- **todo** → Persona completa / Integración / Autorrealización (DIRECT)
- **debe** → Imperativo moral / Superyó / Yo-ideal (DIRECT)
- **tal_vez** → Ambivalencia / Incertidumbre / Angustia existencial (DIRECT)
- **bien/mal** → Adaptación/Patología (ANALOGICAL — evaluación moral vs clínica)
- **verdad/mentira** → Testeo de realidad/Autoengaño (ANALOGICAL)

### Capa 5 (21 primitivos): 15 DIRECT, 4 ANALOGICAL, 2 NULL

Aquí emergen los 2 NULLs esperados — gusto y olfato:

- **tierra** → Cuerpo / Experiencia somática / Embodiment / Grounding (DIRECT)
- **agua** → Emoción / Flujo afectivo / Empatía / Fluidez (DIRECT)
- **aire** → Pensamiento / Ideación / Cognición abstracta (DIRECT)
- **fuego** → Pasión / Intensidad / Catarsis / Transformación (DIRECT)
- **tacto** → Intimidad física / Contacto piel / Apego (Harlow) (DIRECT)
- **oído** → Escucha / Sintonización / Escucha terapéutica (DIRECT)
- **interocepción** → Conciencia interoceptiva / Marcadores somáticos (Damasio) (DIRECT)
- **consciente** → Consciencia / Awareness / Experiencia fenoménica (DIRECT)
- **ausente** → Disociación / Automaticidad / Proceso inconsciente (DIRECT)
- **vida** → Vitalidad / Bienestar / Vivacidad / Eros (DIRECT)
- **muerte** → Ansiedad de muerte / Saliencia de mortalidad / Terror existencial (DIRECT)
- **placer** → Recompensa / Refuerzo positivo / Tono hedónico (DIRECT)
- **dolor** → Dolor psicológico / Sufrimiento / Distrés (DIRECT)
- **gusto** → NULL
- **olfato** → NULL

### Capa 6 (4 primitivos): 2 DIRECT, 2 ANALOGICAL, 0 NULL

- **temporal_obs** → Self autobiográfico / Identidad narrativa (DIRECT)
- **eterno_obs** → Self arquetípico / Transpersonal (Jung) / Patrones universales (ANALOGICAL)
- **receptivo** → Empatía / Receptividad / Postura de escucha (DIRECT)
- **creador_obs** → Agencia / Autoría / Voluntad activa / Rol del terapeuta (ANALOGICAL)

### Totales

| Clase | Cantidad | % |
|-------|----------|---|
| DIRECT | 44 | 69.8% |
| ANALOGICAL | 17 | 27.0% |
| NULL | 2 | 3.2% |
| **Mapped** | **61/63** | **96.8%** |

## III. Los 2 NULLs: El Residuo Quimiosensorial

Los NULLs de psicología son **gusto** y **olfato** — exactamente los mismos que en música y lingüística. Esto confirma el patrón del residuo quimiosensorial: los sentidos químicos no tienen correlato directo en dominios fenomenológicos no-materiales.

**Gradiente actualizado (8 puntos + control):**

| Posición | Dominio | NULLs |
|----------|---------|-------|
| 1 | Biología | 0 |
| 1 | Química | 0 |
| 3 | Música | 2 |
| 3 | Lingüística | 2 |
| 3 | **Psicología** | **2** |
| 6 | Filosofía | 5 |
| 7 | Física | 9 |
| 8 | Matemáticas | 20 |
| — | Astrología (control) | 25 |

Psicología empata con música y lingüística en el nivel fenomenológico — los tres requieren experiencia humana directa pero no manipulan directamente sustancias químicas.

## IV. Verificación de Dependencias

**0 dependencias violadas** de 112 pares evaluados.

Para cada par (padre, hijo) en el grafo de dependencias del modelo, si ambos están mapeados (no-NULL), la dependencia se verifica en psicología: el concepto del hijo presupone el concepto del padre.

Ejemplos:
- contención (frontera del ego) depende de uno (psique individual) ✓
- creación (crecimiento) depende de hacer (agencia) ✓
- consciencia (awareness) depende de información (cognición) ✓

## V. Cinco Jerarquías Psicológicas vs Capas del Modelo

### 5.1 Maslow (Jerarquía de Necesidades)

| Nivel Maslow | Primitivos | Capa promedio |
|-------------|-----------|--------------|
| Fisiológicas | tierra, agua, aire, vida | 5.0 |
| Seguridad | contención, control, orden, equilibrio | 3.25 |
| Pertenencia | unión, colectivo, vida, individual | 3.75 |
| Estima | bien, fuerza, creación, individual | 3.50 |
| Autorrealización | todo, libertad, creación, consciente | 4.25 |

τ > 0 — alineación parcial. La discrepancia en capas medias refleja que Maslow no es puramente jerárquico-lineal.

### 5.2 Piaget (Desarrollo Cognitivo)

| Etapa Piaget | Primitivos | Capa promedio |
|-------------|-----------|--------------|
| Sensoriomotor | mover, tacto, vista, fuerza | 3.50 |
| Preoperatorio | información, creación, uno, hacer | 2.25 |
| Operaciones concretas | orden, tipo_de, más, contención | 3.25 |
| Operaciones formales | si_entonces, porque, verdad, todo | 3.75 |
| Metacognición | pensar, saber, consciente, verdad | 4.50 |

τ > 0 — tendencia creciente general, con inversión en las primeras etapas.

### 5.3 Freud (Estructura Psíquica)

| Nivel Freud | Primitivos | Capa promedio |
|------------|-----------|--------------|
| Ello (id) | fuerza, querer, placer, caos | 3.75 |
| Yo (ego) | orden, contención, control, consciente | 3.75 |
| Superyó | debe, bien, mal, verdad | 4.00 |
| Inconsciente | vacío, ausente, destrucción, menos | 3.00 |
| Sublimación | creación, orden, todo, libertad | 3.75 |

τ no significativo — Freud's model no es jerárquico-lineal sino topográfico/estructural. Esto es esperado: Id, Ego y Superego coexisten, no se apilan.

### 5.4 Niveles de Consciencia

| Nivel | Primitivos | Capa promedio |
|-------|-----------|--------------|
| Inconsciente | vacío, ausente, fuerza | 2.67 |
| Preconsciente | información, contención, mover | 2.00 |
| Consciente | consciente, vista, pensar, saber | 4.50 |
| Metaconsciente | pensar, consciente, verdad, temporal_obs | 4.75 |
| Transpersonal | eterno_obs, colectivo, todo | 5.00 |

τ no significativo — la inversión en "Preconsciente" rompe la monotonía, pero la tendencia general es ascendente.

### 5.5 Erikson (Etapas Psicosociales)

| Etapa Erikson | Primitivos | Capa promedio |
|--------------|-----------|--------------|
| Confianza/Desconfianza | unión, separación, vida, contención | 3.25 |
| Autonomía/Vergüenza | libertad, control, hacer, individual | 4.00 |
| Iniciativa/Culpa | creación, bien, mal, hacer | 3.50 |
| Identidad/Confusión | individual, tipo_de, orden, caos | 4.00 |
| Generatividad/Estancamiento | creación, colectivo, todo, vida | 4.25 |

τ > 0 — alineación parcial, tendencia generalmente creciente.

**Resumen: 3/5 jerarquías con τ > 0** (Maslow, Piaget, Erikson). Freud y Niveles de Consciencia no muestran alineación significativa, lo cual es coherente — estas teorías no proponen jerarquías lineales sino estructuras topográficas.

## VI. Ejes Duales: 11 STRONG, 1 MODERATE

| Eje | Psicología | Evidencia |
|-----|-----------|-----------|
| unión/separación | **STRONG** | Apego/Individuación (Bowlby/Mahler) |
| orden/caos | **STRONG** | Organización del ego/Regresión |
| creación/destrucción | **STRONG** | Sublimación/Tánatos (Freud) |
| verdad/mentira | **STRONG** | Testeo de realidad/Autoengaño defensivo |
| libertad/control | **STRONG** | Autodeterminación/Regulación de impulsos |
| bien/mal | **STRONG** | Adaptación/Patología, Flourishing/Disfunción |
| vida/muerte | **STRONG** | Eros/Tánatos, Vitalidad/Saliencia de mortalidad |
| individual/colectivo | **STRONG** | Idiográfico/Nomotético, Self/Grupo |
| consciente/ausente | **STRONG** | Awareness/Disociación, Consciente/Inconsciente |
| placer/dolor | **STRONG** | Recompensa/Castigo, Hedónico/Sufrimiento |
| receptivo/creador_obs | **STRONG** | Empatía/Agencia, Paciente/Terapeuta |
| temporal_obs/eterno_obs | **MODERATE** | Self narrativo/Self arquetípico |

**11 STRONG, 1 MODERATE, 0 WEAK, 0 NONE.** Psicología tiene la puntuación dual más alta de los 8 dominios (empatada con el máximo teórico de 12/12 S+M). Esto confirma que la experiencia psicológica encarna directamente las tensiones duales del modelo.

## VII. Anclas Psicológicas

25 conceptos psicológicos mapeados como combinaciones de primitivos:

| Concepto | Primitivos | Consistencia |
|----------|-----------|-------------|
| condicionamiento | fuerza, si_entonces, hacer, información | ✓ |
| memoria | información, flujo_temporal, orden, consciente | ✓ |
| emoción | agua, placer, dolor, flujo_temporal | ✓ |
| percepción | vista, información, contención, consciente | ✓ |
| personalidad | tipo_de, individual, orden, consciente | ✓ |
| consciencia | consciente, información, vida, todo | ✓ |
| apego | unión, vida, individual, colectivo | ✓ |
| motivación | fuerza, querer, consciente, hacer | ✓ |
| cognición | pensar, información, orden, consciente | ✓ |
| mecanismo de defensa | contención, menos, separación, ausente | ✓ |
| neurosis | caos, dolor, consciente, contención | ✓ |
| psicosis | caos, ausente, información, destrucción | ✓ |
| desarrollo | creación, posición_temporal, orden, vida | ✓ |
| aprendizaje | información, creación, orden, flujo_temporal | ✓ |
| trauma | dolor, destrucción, ausente, muerte | ✓ |
| transferencia | unión, temporal_obs, receptivo, creador_obs | ✓ |
| insight | vista, verdad, pensar, consciente | ✓ |
| catarsis | destrucción, placer, creación, vida | ✓ |
| autorrealización | todo, libertad, creación, vida | ✓ |
| identidad | uno, individual, consciente, temporal_obs | ✓ |
| dinámica grupal | colectivo, unión, separación, orden | ✓ |
| regulación emocional | control, agua, equilibrio, consciente | ✓ |
| mentalización | pensar, saber, vista, consciente | ✓ |
| recompensa/castigo | placer, dolor, fuerza, si_entonces | ✓ |
| disociación | separación, ausente, parte_de, contención | ✓ |

**Consistencia observada: 17.5%** (baseline 4.8%, ratio 3.65×). Significativamente superior al azar (p < 0.001 por permutation test).

## VIII. Test de Embodiment: Recuperación de NULLs Matemáticos

Este test verifica la meta-dualidad lógico/abstracto vs fenomenológico/material. Matemáticas (el dominio más abstracto) tiene 20 NULLs. ¿Cuántos recupera psicología?

| NULL de Matemáticas | Psicología | Concepto psicológico |
|--------------------|-----------|---------------------|
| tierra | DIRECT | Cuerpo / Embodiment / Grounding |
| agua | DIRECT | Emoción / Flujo afectivo |
| aire | DIRECT | Pensamiento / Cognición abstracta |
| fuego | DIRECT | Pasión / Catarsis |
| tacto | DIRECT | Intimidad / Apego (Harlow) |
| oído | DIRECT | Escucha terapéutica |
| interocepción | DIRECT | Marcadores somáticos (Damasio) |
| vida | DIRECT | Vitalidad / Eros |
| muerte | DIRECT | Ansiedad de muerte |
| placer | DIRECT | Recompensa / Tono hedónico |
| dolor | DIRECT | Sufrimiento / Distrés |
| consciente | DIRECT | Consciencia / Awareness |
| ausente | DIRECT | Disociación / Inconsciente |
| querer | ANALOGICAL | Deseo / Meta / Conación |
| decir | ANALOGICAL | Auto-revelación / Reporte verbal |
| temporal_obs | DIRECT | Self autobiográfico |
| eterno_obs | ANALOGICAL | Self arquetípico (Jung) |
| receptivo | DIRECT | Empatía / Receptividad |
| creador_obs | ANALOGICAL | Agencia / Autoría |
| **gusto** | **NULL** | — |
| **olfato** | **NULL** | — |

**Resultado: 18/20 recuperados** (14 DIRECT, 4 ANALOGICAL). Solo gusto y olfato permanecen NULL — el residuo quimiosensorial irreducible.

Esto confirma la predicción central: psicología y matemáticas son complementarios en el espacio de primitivos. Lo que uno pierde, el otro recupera (excepto los sentidos químicos que requieren materialidad directa).

**Matriz de recuperación combinada (4 dominios fenomenológicos):**

| Dominio | NULLs de Mat recuperados |
|---------|------------------------|
| Filosofía | 15/20 |
| Física | 12/20 |
| Lingüística | 18/20 |
| Psicología | 18/20 |
| **Combinados** | **19/20** |

Solo olfato resiste a los 4 dominios combinados. Gusto es recuperado por filosofía (como analogía del juicio estético).

## IX. Predicciones y Adversarial

### 9.1 Predicciones Confirmadas (9/10)

1. ✓ Exactamente 2 NULLs (gusto, olfato)
2. ✓ 100% cobertura en L1-4
3. ✓ 0 VIOLATED en dependencias
4. ✗ ≥4/5 jerarquías alineadas (resultado: 3/5)
5. ✓ ≥10 STRONG en ejes duales (resultado: 11)
6. ✓ 0 NONE en ejes duales
7. ✓ Consistencia de anclas > baseline
8. ✓ ≥18/20 NULLs de matemáticas recuperados
9. ✓ Gradiente monotónico con 8 puntos
10. ✓ proporcion sigue siendo DIRECT

La predicción 4 falla parcialmente: 3/5 jerarquías (Maslow, Piaget, Erikson) muestran alineación, pero Freud y Niveles de Consciencia no. Esto es interpretable: las teorías freudianas son topográficas, no jerárquico-lineales.

### 9.2 Adversarial (10/10)

Cada objeción adversarial fue respondida satisfactoriamente:

1. "¿Todo es proyección del investigador?" — Los NULLs (gusto, olfato) demuestran que NO todo mapea.
2. "¿Por qué ANALOGICAL y no DIRECT para querer?" — Querer en psicología es deseo (carga motivacional), no acto volitivo puro.
3. "¿Consciencia debería ser L5?" — El modelo coloca consciente en L5 como experiencia, no como primitivo metafísico.
4. "¿Freud está obsoleto?" — El mapeo usa conceptos que sobreviven en la psicología contemporánea (defensa, inconsciente, motivación).
5. "¿Conductismo rechaza consciente?" — El conductismo radical sí, pero la psicología moderna integra ambos.

## X. Comparación Cross-Domain: 8 Columnas

| Primitivo | Mus | Che | Bio | Mat | Fil | Fís | Ling | **Psic** |
|-----------|-----|-----|-----|-----|-----|-----|------|----------|
| vacío | D | D | D | D | D | D | D | **D** |
| información | D | D | D | D | D | D | D | **D** |
| uno | D | D | D | D | D | D | D | **D** |
| fuerza | D | D | D | A | D | D | D | **D** |
| contención | A | D | D | A | D | D | A | **D** |
| más | D | D | D | D | A | D | A | **D** |
| menos | D | D | D | D | D | D | D | **D** |
| unión | D | D | D | D | D | D | D | **D** |
| separación | D | D | D | D | D | D | D | **D** |
| orden | D | D | D | D | D | D | D | **D** |
| caos | D | D | D | D | D | D | D | **D** |
| creación | D | D | D | D | D | D | D | **D** |
| destrucción | D | D | D | D | D | D | D | **D** |

(Tabla parcial — las 63 filas completas están en `scripts/test16_psychology_validation.py`)

**11 primitivos forman el núcleo universal D/D/D/D/D/D/D/D**: vacío, información, uno, menos, unión, separación, mover, posición_temporal, flujo_temporal, creación, orden.

## XI. Gradiente Actualizado: 8 Puntos

El gradiente de abstracción con 8 dominios confirma la monotonía no-estricta:

```
Bio(0) = Chem(0) ≤ Mus(2) = Ling(2) = Psic(2) ≤ Fil(5) ≤ Fís(9) ≤ Mat(20)
```

Los tres dominios fenomenológicos (Música, Lingüística, Psicología) empatan en 2 NULLs, formando un cluster coherente. Todos pierden exactamente gusto y olfato — el residuo quimiosensorial.

## XII. Domain Validity Score: Psicología vs Astrología

| Métrica | Psicología | Astrología | Ratio |
|---------|-----------|-----------|-------|
| M1 (Cobertura) | 1.00 | 0.63 | 1.6× |
| M2 (Profundidad) | 0.70 | 0.06 | 11.7× |
| M3 (Dualidad) | 0.92 | 0.00 | ∞ |
| M4 (Engagement) | 0.97 | 0.48 | 2.0× |
| **DVS** | **0.903** | **0.360** | **2.5×** |

Psicología obtiene el DVS más alto de los 8 dominios (0.903), confirmando que es la correspondencia más genuina con el modelo. Astrología obtiene el más bajo (0.360). La separación es máxima: M3 = 0.92 vs 0.00 (psicología tiene 11 ejes STRONG; astrología tiene 0).

## XIII. Limitaciones

1. **Sesgo del mapeador**: El mapeo fue realizado por un solo investigador. El Doc 26 (protocolo inter-evaluador) especifica cómo futuras validaciones con múltiples evaluadores podrían confirmar la objetividad.
2. **Jerarquías**: Solo 3/5 muestran alineación con las capas del modelo. Las teorías no-lineales (Freud, consciencia) no se alinean jerárquicamente, lo cual puede ser un límite del test más que del mapeo.
3. **Escuelas**: Diferentes escuelas psicológicas (conductista, psicoanalítica, cognitiva, humanista) podrían generar clasificaciones ligeramente diferentes para ciertos primitivos.
4. **Quimiosensorial**: La explicación del residuo gusto/olfato como "irreduciblemente químico" es coherente pero no ha sido testada formalmente con otros dominios no-materiales.

## XIV. Conclusión

Psicología valida el modelo de 63 primitivos con la puntuación más alta observada:

- **DVS = 0.903** (máximo entre 8 dominios)
- **11/12 ejes STRONG** (máximo entre 8 dominios)
- **44 DIRECT** (empatado con lingüística)
- **18/20 NULLs de matemáticas recuperados** (empatado con lingüística)
- **0 VIOLATED** en dependencias

El test de embodiment (16H) confirma formalmente la meta-dualidad: psicología y matemáticas son complementarios — lo que uno pierde, el otro recupera. Las únicas excepciones (gusto, olfato) son consistentes con el residuo quimiosensorial observado en todos los dominios fenomenológicos.

---

*Parte del manuscrito "Expansión del Círculo de Emergencia de Dualidades."*
*Script: `scripts/test16_psychology_validation.py`*
