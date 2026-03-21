# Definiciones Formales: Que es una Dualidad
## Fundamentos ontologicos del Circulo de Emergencia
### J. Arturo Ornelas Brand — Marzo 2026

---

## Resumen

Este documento establece las definiciones formales que sustentan el marco del Circulo de Emergencia de Dualidades. Se define con precision que es una dualidad, que la distingue de una mera oposicion binaria, como se formaliza la dependencia de emergencia entre dualidades, y como opera el mecanismo generativo de sintesis central y espiral. El objetivo es proveer un vocabulario riguroso que sirva de base para los nueve documentos subsecuentes del manuscrito.

---

## I. Motivacion: por que hacen falta definiciones

La nocion de "opuestos" es ubicua en la historia del pensamiento — desde el *apeiron* de Anaximandro hasta la dialectica de Hegel, desde el yin-yang hasta la complementariedad de Bohr. Sin embargo, la mayoria de los marcos filosoficos que emplean oposiciones lo hacen de manera informal: asumen que el lector comparte una intuicion sobre que significa que dos conceptos "se opongan" sin definir las condiciones que hacen a una oposicion genuinamente productiva.

El Circulo de Emergencia de Dualidades propone algo mas fuerte que una lista de opuestos: propone que existe un conjunto finito de dualidades fundamentales, que estas tienen un orden de emergencia necesario, y que la tension entre sus polos genera sintesis que a su vez abren nuevas dualidades. Para que estas proposiciones sean evaluables — y refutables — necesitamos definiciones precisas.

Este documento no argumenta a favor de la secuencia especifica de 7 dualidades (eso lo hace el Documento 02) ni justifica la extension a 14 (Documento 04). Su proposito es exclusivamente definicional: fijar los terminos que todo el manuscrito utilizara.

---

## II. Definicion de Dualidad

### 2.1 Definicion informal

Una dualidad es un par de conceptos que son polos opuestos de una misma dimension de la realidad, de tal forma que:
- No pueden ser verdaderos simultaneamente del mismo sujeto en el mismo respecto (*exclusion mutua*).
- Todo lo que existe en el dominio relevante se situa en alguna relacion con ambos polos (*exhaustividad conjunta*).
- La tension entre los polos produce algo nuevo que no estaba contenido en ninguno de los dos (*generatividad*).

### 2.2 Definicion formal

**Definicion 1** (Dualidad). Sea $U$ un dominio de discurso no vacio. Una *dualidad* es una tupla $d = (P^+, P^-, U_d, \sigma)$ donde:

1. **Polos**: $P^+$ y $P^-$ son propiedades sobre $U$ tales que para todo $x \in U_d$:
   - *Exclusion mutua*: $\neg(P^+(x) \wedge P^-(x))$ — ningun elemento satisface ambos polos simultaneamente.
   - *Exhaustividad conjunta*: $P^+(x) \vee P^-(x) \vee \text{null}(x)$ — todo elemento esta en uno de los polos o bien la dualidad no se le aplica.
2. **Dominio de aplicabilidad**: $U_d \subseteq U$ es el subconjunto del universo donde la dualidad tiene sentido (donde la dimension "ha emergido").
3. **Funcion de sintesis**: $\sigma: P^+ \times P^- \to C$ mapea la tension entre los polos a un concepto sintetico $c \in C$ que no es reducible a ninguno de los dos polos.

### 2.3 Tres estados, no dos

Una distincion critica separa este marco de la logica binaria clasica. Para cualquier entidad $x \in U$ y cualquier dualidad $d_i$, hay exactamente tres estados posibles:

| Estado | Notacion | Significado | Ejemplo |
|--------|----------|-------------|---------|
| Activo positivo | $+1$ | El polo positivo $P^+$ esta presente y operando | Un objeto caliente |
| Activo negativo | $-1$ | El polo negativo $P^-$ esta presente y operando | Un objeto frio |
| No aplica | $0$ (null) | La dimension no ha emergido para esta entidad; la pregunta carece de sentido | Una piedra respecto a consciente/ausente |

Esta estructura ternaria $\{+1, 0, -1\}$ no es arbitraria. Fue derivada independientemente desde tres caminos:

1. **Filosofia** (*La Danza Cosmica de los Opuestos*): Presencia [+], vacio [0], ausencia activa [null] como los tres estados ontologicos fundamentales.
2. **Ingenieria** (BitNet b1.58, Ma et al. 2024): La cuantizacion ternaria de pesos $\{+1, 0, -1\}$ resulta ser la representacion discreta minima que preserva la calidad del modelo.
3. **Matematicas** (Algebra bitwise del proyecto TriadicGPT): Las operaciones sobre mascaras de bits con tres estados resultan isomorfas a la aritmetica de primos.

La convergencia de tres caminos independientes hacia la misma estructura ternaria es evidencia de que $\{+1, 0, -1\}$ captura algo genuino sobre la estructura de la informacion (ver Documento 09 para el analisis completo).

### 2.4 Diferencia con oposiciones binarias simples

No toda oposicion binaria es una dualidad en el sentido de este marco. Consideremos varios tipos de pares opuestos:

| Par | Exclusion mutua | Exhaustividad | Generatividad | Es dualidad? |
|-----|----------------|---------------|---------------|-------------|
| Existir / No existir | Si | Si (todo existe o no) | Si (la tension produce informacion) | Si |
| Par / Impar | Si | Si (para enteros) | No (su tension no genera nada nuevo) | No |
| Rojo / Azul | Si (como frecuencia pura) | No (hay otros colores) | No | No |
| Calor / Frio | Si (extremos) | Si (todo tiene temperatura) | Si (la sintesis es temperatura) | Si, pero derivada |
| Verdadero / Falso | Si | Si (bivalencia) | Debatible | Subsumed por Ser/No-ser |

La generatividad es el criterio que distingue una dualidad genuina de una mera clasificacion binaria. Una dualidad autentica produce un concepto sintetico que abre un espacio conceptual nuevo. Los numeros pares e impares no generan un tercer tipo de numero a partir de su tension; existir y no existir generan la informacion misma.

---

## III. Dependencia de Emergencia

### 3.1 Intuicion

Algunas dualidades no pueden existir sin que otras existan primero. No puede haber movimiento sin que haya algo que se mueva, un lugar donde moverse, y un tiempo en el cual moverse. La dualidad Movimiento/Quietud *depende* de las dualidades Existir/No-existir, Aqui/No-aqui, y Antes/Despues.

Esta relacion de dependencia no es empirica (no decimos que historicamente una aparecio primero), sino *logica*: en todo mundo posible donde existe la dualidad j, necesariamente existen todas las dualidades de las que depende.

### 3.2 Formalizacion via Fundierung husserliana

Husserl (1900-1901) desarrollo en la Tercera Investigacion Logica el concepto de *Fundierung* (fundacion): un contenido $\alpha$ funda un contenido $\beta$ si $\beta$ no puede existir sin $\alpha$. Adoptamos esta relacion:

**Definicion 2** (Dependencia de emergencia). Dadas dos dualidades $d_i$ y $d_j$, decimos que $d_i$ *funda* $d_j$ (notacion: $d_i \leq d_j$, o equivalentemente $d_i \preceq d_j$) si y solo si:

$$\Box(E(d_j) \to E(d_i))$$

donde $E(d)$ es el predicado "la dualidad $d$ existe (ha emergido)" y $\Box$ es el operador de necesidad modal (en todo mundo posible).

En lenguaje llano: *es necesario que, si la dualidad $j$ existe, la dualidad $i$ ya exista.* No puede haber un mundo posible donde exista el movimiento pero no exista el espacio.

### 3.3 Propiedades de la relacion de dependencia

La relacion $\leq$ satisface las propiedades de un *orden parcial*:

1. **Reflexividad**: $d_i \leq d_i$ — toda dualidad depende trivialmente de si misma (no puede existir sin existir).
2. **Antisimetria**: Si $d_i \leq d_j$ y $d_j \leq d_i$, entonces $d_i = d_j$ — dos dualidades no pueden fundarse mutuamente (eso seria circularidad, y la circularidad en la Fundierung colapsa las dos dualidades en una sola).
3. **Transitividad**: Si $d_i \leq d_j$ y $d_j \leq d_k$, entonces $d_i \leq d_k$ — si el movimiento requiere el espacio y el patron requiere el movimiento, entonces el patron requiere el espacio.

Un conjunto equipado con un orden parcial es un *poset* (conjunto parcialmente ordenado). El conjunto de dualidades $D = \{d_1, ..., d_n\}$ con la relacion de dependencia $\leq$ forma el **poset de emergencia** $(D, \leq)$.

### 3.4 Orden total vs. orden parcial

Una pregunta central es si las 7 dualidades fundamentales forman un *orden total* (cadena) — donde para cualesquiera $d_i, d_j$ se cumple que $d_i \leq d_j$ o $d_j \leq d_i$ — o un *orden parcial* (lattice) donde algunas dualidades podrian ser incomparables.

La propuesta inicial es que las 7 forman un orden total:

$$d_1 < d_2 < d_3 < d_4 < d_5 < d_6 < d_7$$

donde $d_1$ = Existir/No-existir, $d_2$ = Aqui/No-aqui, ..., $d_7$ = Orden/Caos.

El Documento 02 evalua esta hipotesis rigurosamente. El Documento 05 formaliza la estructura resultante con herramientas de teoria de lattices y teoria de categorias.

### 3.5 Notacion

A lo largo del manuscrito usaremos la siguiente notacion consistente:

| Simbolo | Significado |
|---------|-------------|
| $d_i$ | La $i$-esima dualidad en la secuencia de emergencia |
| $P^+_i, P^-_i$ | Los polos positivo y negativo de $d_i$ |
| $d_i \leq d_j$ | $d_i$ funda $d_j$ (es requisito de emergencia) |
| $d_i < d_j$ | $d_i$ funda $d_j$ estrictamente ($i \neq j$) |
| $\sigma(d_i, d_j)$ | El concepto sintetico generado por la interseccion de los ejes de $d_i$ y $d_j$ |
| $E(d)$ | Predicado: la dualidad $d$ ha emergido (existe) |
| $\Box \varphi$ | Necesariamente $\varphi$ (en todo mundo posible accesible) |
| $U_d$ | Dominio de aplicabilidad de la dualidad $d$ |
| $(D, \leq)$ | El poset de emergencia |

---

## IV. Sintesis Central

### 4.1 Definicion

**Definicion 3** (Sintesis central). Dadas dos o mas dualidades $d_i, d_j, ..., d_k$ cuyos ejes se intersectan en el espacio conceptual, la *sintesis central* es el concepto compuesto $c = \sigma(d_i, d_j, ..., d_k)$ que:

1. Presupone la existencia de todas las dualidades involucradas.
2. No es reducible a ninguno de los polos individuales.
3. Se situa en el "centro" del espacio definido por las dualidades participantes.

### 4.2 Ejemplos

| Sintesis central | Dualidades involucradas | Justificacion |
|-----------------|------------------------|---------------|
| Temperatura | Movimiento/Quietud + Orden/Caos | Temperatura = energia cinetica media; requiere movimiento (moleculas moviéndose) y orden (medida estadistica) |
| Velocidad | Aqui/No-aqui + Antes/Despues + Movimiento/Quietud | Velocidad = cambio de posicion en el tiempo; requiere espacio, tiempo y movimiento |
| Frecuencia | Antes/Despues + Orden/Caos | Frecuencia = patron temporal; requiere tiempo y repeticion |
| Identidad quimica | Ser/No-ser + Orden/Caos + Posible/Imposible | Una especie quimica tiene identidad definida, patron de enlace estable, y se actualiza entre posibilidades de configuracion |

### 4.3 Geometria de la sintesis

En la representacion geometrica del circulo de dualidades:

- Los **polos** de cada dualidad se situan en posiciones diametralmente opuestas del perimetro.
- Los **ejes** son las lineas que conectan los polos de cada dualidad.
- Las **sintesis** se situan en el interior del circulo, en la interseccion de dos o mas ejes.
- El **centro absoluto** del circulo es el punto donde convergirian todos los ejes — el concepto que sintetiza todas las dualidades, el "Todo" indiferenciado.

Esta geometria no es meramente ilustrativa. El Documento 05 demuestra que admite formalizacion via complejos CW (cada dualidad agrega una dimension) y via la teoria de lattices (el infimo del lattice corresponde a la existencia pura, el supremo al concepto total).

### 4.4 Propiedad holografica

Una propiedad fundamental de la sintesis central es su posible *determinacion por la periferia*: si se conocen todas las dualidades perifericas y las posiciones de una entidad en cada eje, la sintesis central podria estar univocamente determinada.

**Conjetura 1** (Determinacion holografica). Para toda entidad $x \in U$, dado su vector de estados $v(x) = (s_1(x), s_2(x), ..., s_n(x))$ donde $s_i(x) \in \{+1, 0, -1\}$ es el estado de $x$ respecto a la dualidad $d_i$, las sintesis centrales de $x$ estan univocamente determinadas.

Si esta conjetura es verdadera, toda la informacion "interior" (sintesis) esta codificada en la "superficie" (dualidades perifericas), en analogia directa con el principio holografico de 't Hooft y Susskind. El Documento 06 analiza esta conjetura en profundidad y el Documento 09 propone un test empirico con datos de TriadicGPT.

---

## V. La Espiral Generativa

### 5.1 Definicion

**Definicion 4** (Espiral generativa). Sea $\mathcal{C}$ el circulo de dualidades con periferia $P$ (conjunto de polos duales) y centro $C$ (conjunto de sintesis). La *espiral generativa* es un operador $F: C \to P'$ que:

1. Toma una sintesis central $c \in C$.
2. La *externaliza* como un nuevo par de polos duales en una periferia de orden superior $P'$.
3. El nuevo par de polos forma una dualidad de orden $n+1$ que no existia en el circulo original.

### 5.2 Mecanismo

El mecanismo de la espiral opera en tres pasos:

**Paso 1 — Sintesis**: Los polos de dualidades existentes generan un concepto sintetico central.
$$P^+_i, P^-_i, P^+_j, P^-_j \xrightarrow{\sigma} c_{ij}$$

**Paso 2 — Diferenciacion**: La sintesis $c_{ij}$ se revela como un nuevo eje con sus propios polos opuestos.
$$c_{ij} \to (Q^+, Q^-)$$

**Paso 3 — Externalizacion**: Los nuevos polos $(Q^+, Q^-)$ se situan en la periferia de un circulo de orden superior, constituyendo una nueva dualidad $d_{n+1}$.
$$d_{n+1} = (Q^+, Q^-, U_{d_{n+1}}, \sigma')$$

### 5.3 Ejemplo concreto

1. Las dualidades Movimiento/Quietud y Orden/Caos generan la sintesis *temperatura* (energia cinetica media).
2. La temperatura se revela como un eje con polos propios: Frio / Calor.
3. Frio/Calor es ahora una nueva dualidad que se opone a otros conceptos sinteticos (como presion), formando dualidades de orden superior.
4. La tension Frio/Calor + presion genera *estados de la materia* — una sintesis de segundo orden.

Cada vuelta de la espiral corresponde a un "ciclo de emergencia" completo: de la periferia al centro (sintesis) y del centro a una nueva periferia (externalizacion).

### 5.4 Formalizacion como endofuntor

En terminos de teoria de categorias (desarrollados en el Documento 05), la espiral es un *endofuntor* $F: \mathbf{C} \to \mathbf{C}$ sobre la categoria de dualidades $\mathbf{C}$, donde:

- Los objetos de $\mathbf{C}$ son dualidades.
- Los morfismos son relaciones de dependencia.
- $F$ toma el colimite (sintesis de todas las dualidades) y lo devuelve como nuevo objeto periferico.

La espiral no se cierra en un plano — es topologicamente una *cubriente* (covering space) del circulo $S^1$. El grupo fundamental $\pi_1(S^1) = \mathbb{Z}$ captura que se pueden dar infinitas vueltas, cada una en un nivel superior. Cada vuelta completa es un ciclo de emergencia.

---

## VI. El Indice de Fertilidad

### 6.1 Definicion

No todas las sintesis son igualmente productivas. Una sintesis es *fertil* si al externalizarse como nueva dualidad genera tensiones adicionales que producen mas sintesis. Una sintesis es *esteril* si no abre ningun espacio conceptual nuevo.

**Definicion 5** (Indice de fertilidad). Sea $c$ una sintesis central y sea $\mathcal{T}(c)$ el conjunto de tensiones nuevas que $c$ genera al externalizarse como dualidad. El *indice de fertilidad* de $c$ es:

$$\phi(c) = |\mathcal{T}(c)| - 1$$

donde $|\mathcal{T}(c)|$ es el numero de tensiones nuevas. Si $\phi(c) > 0$, la sintesis es fertil (genera mas tensiones de las que resuelve). Si $\phi(c) = 0$, es neutra. Si $\phi(c) < 0$, es esteril.

### 6.2 Relacion con la analogia del agujero negro

El indice de fertilidad conecta con la "radiacion de Hawking conceptual" de la analogia del agujero negro informacional (Documento 06): un sistema cuyo centro sintetico tiene alta fertilidad "emite" mas dualidades al perimetro — su horizonte de eventos se expande, su frontera de conocimiento crece. Un sistema con fertilidad cero o negativa esta "muerto" — ya no genera preguntas nuevas.

### 6.3 Conexion con la temperatura conceptual

Se puede definir una "temperatura conceptual" como la densidad de tensiones no resueltas por unidad de sintesis:

$$T_c = \frac{\text{Numero de tensiones no resueltas}}{\text{Numero de sintesis existentes}}$$

Un sistema con alta temperatura conceptual tiene muchas preguntas abiertas relativas a su complejidad — esta "caliente", generativo, en crecimiento. Un sistema con baja temperatura conceptual ha resuelto la mayoria de sus tensiones — esta "frio", estable, potencialmente dogmatico.

---

## VII. Las 7 Dualidades Fundamentales: Presentacion Formal

Aplicando las definiciones anteriores, presentamos la secuencia propuesta de 7 dualidades fundamentales. Este apartado solo enuncia la secuencia; la justificacion de cada dependencia se desarrolla en el Documento 02.

| $i$ | Dualidad $d_i$ | Polo $P^+$ | Polo $P^-$ | Dominio que abre | Rol estructural |
|-----|---------------|------------|------------|-----------------|-----------------|
| 1 | Existir / No-existir | Existir | No-existir | Ontologia + Informacion | ESCENARIO |
| 2 | Aqui / No-aqui | Aqui | No-aqui | Espacio (Geometria) | ESCENARIO |
| 3 | Antes / Despues | Antes | Despues | Tiempo (Cronologia) | ESCENARIO |
| 4 | Posible / Imposible | Posible | Imposible | Logica modal (Bifurcacion) | BISAGRA |
| 5 | Ser / No-ser | Ser | No-ser | Identidad (Metafisica) | DINAMICO |
| 6 | Movimiento / Quietud | Movimiento | Quietud | Fisica | DINAMICO |
| 7 | Orden / Caos | Orden | Caos | Patron / Informacion funcional | DINAMICO |

### 7.1 Estructura tripartita

Las 7 dualidades exhiben una triparticion natural:

- **Escenario** (d1-d3): Establecen las condiciones minimas de la realidad — que haya algo, que este en algun lugar, que transcurra el tiempo. Sin las tres, nada puede ocurrir.
- **Bisagra** (d4): La posibilidad es el punto de inflexion. Divide lo estatico de lo dinamico. Sin posibilidad, la existencia esta congelada; con posibilidad, se abre la bifurcacion.
- **Dinamico** (d5-d7): Lo que ocurre una vez que la posibilidad permite el cambio — cosas adquieren identidad, se mueven, y su movimiento forma patrones.

### 7.2 La informacion como sustrato

Un descubrimiento clave de la sesion exploratoria original: la informacion no es una dualidad separada ni un concepto sintetico central. La primera dualidad — Existir/No-existir — *ya es* un bit de informacion. La informacion es el material del que esta hecho el circulo entero, no algo que emerge dentro de el.

$$\text{Existir} = \text{Informar}$$

Esto conecta con Wheeler (1990): "It from bit" — la realidad emerge de la informacion. Pero aqui se llega a la misma conclusion desde una ruta independiente: no postulamos que la informacion es fundamental; *demostramos* que la primera dualidad concebible ya es informacion por necesidad logica.

---

## VIII. Verificacion: Conexion con primitivos.json

Las definiciones formales no existen en el vacio. El archivo `primitivos.json` del proyecto TriadicGPT contiene 63 primitivos conceptuales con dependencias explicitas, organizados en 6 capas dimensionales. Este archivo proporciona una *instanciacion empirica* del poset de emergencia.

### 8.1 Correspondencia entre capas y dualidades

| Capa | Nombre | Primitivos | Dualidades principales |
|------|--------|------------|----------------------|
| 1 | Punto (0D) | vacio, informacion, uno | d1 (Existir/No-existir) |
| 2 | Linea (1D) | fuerza, contencion, union, separacion, mas, menos, parte_de | d2 (Aqui/No-aqui), d8-d10 |
| 3 | Tiempo (1D+t) | mover, posicion_temporal, flujo_temporal, hacer, creacion, destruccion, orden, caos, porque, si_entonces | d3 (Antes/Despues), d6-d7, d11 |
| 4 | Plano (2D) | ejes, moral, verdad, libertad, tipo_de, cantidad, modalidad | d4 (Posible/Imposible), d8, d12 |
| 5 | Volumen (3D) | elementos, sentidos, vida/muerte, placer/dolor, consciente/ausente, individual/colectivo, querer, saber, pensar, decir | d5 (Ser/No-ser), d13-d14 |
| 6 | Meta (3D+) | temporal_obs/eterno_obs, receptivo/creador_obs | Dualidades recursivas |

### 8.2 Ejes duales en primitivos.json

El archivo define 12 ejes duales explicitos:

$$\text{Ejes} = \{(\text{bien, mal}), (\text{orden, caos}), (\text{creacion, destruccion}), ...$$
$$(\text{union, separacion}), (\text{verdad, mentira}), (\text{libertad, control}), ...$$
$$(\text{vida, muerte}), (\text{placer, dolor}), (\text{consciente, ausente}), ...$$
$$(\text{temporal\_obs, eterno\_obs}), (\text{individual, colectivo}), (\text{receptivo, creador\_obs})\}$$

Cada eje dual es una instanciacion concreta de una dualidad en el sentido de la Definicion 1. Los tres estados $\{+1, 0, -1\}$ del sistema TriadicGPT corresponden exactamente a los tres estados de la Definicion 2.3.

### 8.3 Mapeo no trivial

Es importante senalar que las capas de `primitivos.json` organizan por *dimensionalidad geometrica* (0D → 1D → 2D → 3D) mientras que las dualidades organizan por *dependencia ontologica*. Son dos cortes distintos a traves del mismo espacio conceptual:

- Las capas responden a: ¿cuantas dimensiones espaciales necesita este concepto?
- Las dualidades responden a: ¿que otros conceptos necesitan existir antes para que este sea concebible?

El Documento 08 analiza esta tension en profundidad y muestra que ambos ordenamientos son *facetas complementarias* de una estructura unica.

---

## IX. Conexion Empirica

Las definiciones de este documento admiten tests empiricos concretos a traves del sistema TriadicGPT:

1. **Test de tres estados**: Verificar que el modelo entrenado produce distribucion ternaria $\{+1, 0, -1\}$ espontaneamente — ya confirmado en D-A8 (1.3% negativo, 73.3% cero, 25.3% positivo) y D-A13 (100% subsuncion holdout a 355M parametros).

2. **Test de dependencia**: Verificar que en los datos de anclas (`anclas_v2.json`), si un bit $j$ esta activo, los bits de los que depende en `primitivos.json` tienden a estar activos tambien. Este es el test falsificable clave (Documento 09, Seccion 2).

3. **Test de fertilidad**: Medir cuantas tensiones nuevas genera cada sintesis central en el espacio de 63 bits — cuantificacion directa del indice de fertilidad.

---

## X. Preguntas Abiertas

1. **¿Es la generatividad formalizable como propiedad algebraica?** La Definicion 1 la incluye como condicion, pero ¿puede verificarse algoritmicamente si un par de conceptos es genuinamente generativo?

2. **¿Deberia la exclusion mutua ser estricta o admitir grados?** En la fisica cuantica, la complementariedad (onda/particula) no es estrictamente binaria — un foton exhibe ambos aspectos segun el experimento. ¿Necesitamos una nocion mas debil de exclusion?

3. **¿Es el tercer estado ($0$, null, irrelevante) una propiedad de la entidad o de la dualidad?** Cuando decimos que una piedra tiene estado $0$ respecto a consciente/ausente, ¿es la piedra la que carece de la dimension, o es la dimension la que no se aplica a la piedra? La diferencia es ontologica: la primera posicion es realista (la consciencia es una propiedad real que la piedra no tiene), la segunda es perspectivista (la consciencia es una lente que no tiene sentido aplicar a la piedra).

4. **¿Cuantas dualidades fundamentales hay realmente?** Las definiciones de este documento son compatibles con 7, 14, o cualquier otro numero. La cuestion empirica es si existe un conjunto minimo que genere, via la espiral, todas las demas. El Documento 04 aborda esta cuestion.

---

## Referencias

- Aristoteles (c. 350 a.C.). *Categorias*.
- Bekenstein, J. D. (1973). "Black Holes and Entropy." *Physical Review D*, 7(8), 2333-2346.
- Hegel, G. W. F. (1812-1816). *Wissenschaft der Logik*.
- Husserl, E. (1900-1901). *Logische Untersuchungen*, Tercera Investigacion.
- Ma, S. et al. (2024). "The Era of 1-bit LLMs." arXiv:2402.17764.
- Ornelas Brand, A. (2026a). *La Danza Cosmica de los Opuestos*.
- Ornelas Brand, A. (2026b). "End-to-End Prime Factorization in a Generative Language Model." Manuscrito.
- Spencer-Brown, G. (1969). *Laws of Form*.
- 't Hooft, G. (1993). "Dimensional Reduction in Quantum Gravity." arXiv:gr-qc/9310026.
- Wheeler, J. A. (1990). "Information, Physics, Quantum." En *Complexity, Entropy, and the Physics of Information*.
- Wierzbicka, A. & Goddard, C. (2014). "Semantic Primes and Universal Grammar."

---

*Parte del manuscrito "Expansion del Circulo de Emergencia de Dualidades."*
