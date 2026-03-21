# Extension: Dualidades 8-14
## Propuesta y evaluacion de siete dualidades post-fundacionales
### J. Arturo Ornelas Brand — Marzo 2026

---

## Resumen

Los Documentos 01 y 02 establecieron siete dualidades fundamentales cuya secuencia de emergencia forma un poset casi-total: desde Existir/No-existir (d1) hasta Orden/Caos (d7). Estas siete constituyen las condiciones minimas de la realidad — el escenario, la bisagra y la dinamica sin los cuales nada puede ocurrir, moverse ni formar patron. Sin embargo, la espiral generativa (Documento 01, Seccion V) predice que las sintesis centrales de las siete fundamentales se externalizan como nuevas dualidades perifericas de orden superior. Este documento ejecuta esa prediccion: propone siete dualidades candidatas (d8-d14), las somete a los tres criterios de seleccion (dependencia, irreductibilidad, generatividad), evalua su estructura interna (cadena, arbol o reticula), presenta cuatro candidatas rechazadas con razonamiento explicito, y mapea el resultado al sistema de 63 bits de `primitivos.json`.

La tesis principal es que las dualidades 8-14 forman una cadena de emergencia que extiende la secuencia fundacional, abriendo dominios progresivamente mas ricos — desde la matematica (Uno/Muchos) hasta la consciencia (Sujeto/Objeto) — pero que esta cadena podria admitir al menos una bifurcacion interna, lo cual la convertiria en un lattice y no en un orden total.

---

## I. Principio de Seleccion

### 1.1 Motivacion

Las siete dualidades fundamentales no fueron elegidas arbitrariamente. El Documento 02 demostro que, de 21 pares ordenados evaluados, 20 satisfacen la relacion de dependencia con veredicto NECESARIO o FUERTE. Cualquier extension del conjunto debe someterse a un rigor comparable. La proliferacion de "dualidades" sin criterio conduce a una lista inflada sin poder explicativo — como las listas de opuestos de la tradicion pitagorica, que mezclaban niveles categoriales (par/impar junto a masculino/femenino, luz/oscuridad y finito/infinito en el mismo plano).

Para evitar esta inflacion, establecemos tres criterios conjuntos. Una candidata debe satisfacer los tres para ser admitida.

### 1.2 Los tres criterios

**Criterio 1 — Dependencia.** La dualidad candidata $d_k$ (con $k > 7$) debe requerir logicamente al menos una de las siete fundamentales, y no puede existir en un mundo posible donde esa fundamental este ausente. Formalmente:

$$\exists \, d_i \text{ con } i \leq 7 \text{ tal que } \Box(E(d_k) \to E(d_i))$$

Ademas, la candidata debe requerir al menos una dualidad que no sea d1 (Existir/No-existir), ya que d1 es requisito trivial de toda dualidad. El requisito interesante es la dependencia *critica*: la dualidad mas alta en la cadena sin la cual la candidata no puede concebirse.

**Criterio 2 — Irreductibilidad.** La candidata no puede ser expresable como combinacion booleana o sintesis de dos o mas de las siete fundamentales. Si la candidata resulta ser una sintesis central (en el sentido de la Definicion 3 del Documento 01), es un concepto compuesto, no una dualidad nueva. El test es: ¿tiene la candidata polos genuinamente opuestos que definan una dimension nueva, o son sus polos meras instanciaciones de polos ya existentes?

**Criterio 3 — Generatividad.** La candidata debe abrir un dominio de discurso que las siete fundamentales no cubren por si solas. "Abrir un dominio" significa que hay preguntas formulables en terminos de la candidata que no pueden siquiera enunciarse usando solo d1-d7. Si toda pregunta que la candidata permite ya es expresable con las siete, la candidata es redundante.

### 1.3 Procedimiento de evaluacion

Para cada candidata, el analisis sigue cuatro pasos:

1. **Identificacion**: nombre, polos, dominio que abre.
2. **Argumento de dependencia critica**: cual dualidad previa es el prerequisito mas exigente y por que.
3. **Conexion con primitivos.json**: si la candidata tiene representacion explicita en el sistema de 63 bits, y cual.
4. **Objecion y contraargumento**: la mejor objecion que encontramos contra la admision de la candidata, y nuestra respuesta.

---

## II. Las Siete Candidatas Evaluadas

### 2.1 Dualidad 8: Uno / Muchos — Nace la cantidad

**Polos**: Uno ($P^+$) y Muchos ($P^-$).
**Dominio que abre**: Matematicas, aritmetica, teoria de conjuntos, medida. Antes de Uno/Muchos, la realidad tiene existentes que se mueven formando patrones, pero no puede *contar*. La pregunta "¿cuantos?" carece de sentido sin esta dualidad.

**Argumento de dependencia critica — requiere Orden/Caos (d7).**
Contar presupone identificar unidades repetidas. Para reconocer que hay "muchos" de algo, se necesita detectar un patron de repeticion — que hay algo (d1), distinguible (d5), que aparece mas de una vez en una disposicion reconocible (d7). La dependencia de d7 no es trivial: en un universo puramente caotico, donde nada se repite ni forma patron, la nocion de "muchos del mismo tipo" colapsa. Uno/Muchos es la primera dualidad que surge cuando Orden/Caos ha establecido la posibilidad de regularidad.

Puede objetarse que la distincion uno/muchos es mas primitiva que el patron — que basta con la existencia (d1) y la identidad (d5) para distinguir "un objeto" de "dos objetos." Pero la identificacion de la multiplicidad *como tal* — no como mera coexistencia sino como *cantidad* — requiere que el observador (o el sistema) detecte la repeticion de una forma. Sin patron, hay existentes coexistentes; con patron, hay *n* instancias de algo.

**Conexion con primitivos.json**: El bit 44 (`uno`) y el bit 45 (`muchos`) representan explicitamente estos polos. Ambos estan en la capa 4 (Plano, 2D) del sistema, bajo la subcategoria `cantidad`. Sus dependencias en el grafo incluyen bits de capas anteriores vinculados a orden y repeticion.

**Objecion**: Frege (1884) argumento que el numero es un concepto puramente logico, derivable de la nocion de conjunto y de identidad. Si Uno/Muchos es derivable de Ser/No-ser (d5, identidad) y de la logica de conjuntos, no satisface el criterio de irreductibilidad.

**Respuesta**: La objecion fregeana funciona en el plano de la logica formal pero no en el plano ontologico. La pregunta no es si el numero puede *definirse* a partir de la identidad, sino si el *dominio de la cantidad* es reducible al dominio de la identidad. Un universo con identidad pero sin patron (d7) podria tener existentes distinguibles pero sin capacidad de *agruparlos y contarlos*. La agrupacion requiere deteccion de semejanza repetida, que es funcion del patron. Uno/Muchos no es la definicion logica de numero; es la apertura ontologica del dominio cuantitativo.

**Veredicto**: ADMITIDA.

---

### 2.2 Dualidad 9: Continuo / Discreto — Nace la topologia

**Polos**: Continuo ($P^+$) y Discreto ($P^-$).
**Dominio que abre**: Topologia, calculo infinitesimal, la pregunta de si la realidad es digital o analogica, la estructura del continuo matematico.

**Argumento de dependencia critica — requiere Uno/Muchos (d8).**
La distincion entre continuo y discreto solo tiene sentido una vez que se puede distinguir uno de muchos. Lo discreto *es* lo que se presenta como unidades separadas (muchos). Lo continuo *es* lo que resiste esa separacion — lo que permanece uno incluso cuando se intenta dividir. Sin la dualidad Uno/Muchos, la pregunta "¿es esto un conjunto de partes separadas o un todo indivisible?" no puede formularse.

La dependencia es genuinamente critica y no trivial. En un universo donde no existe la cantidad (pre-d8), no puede haber diferencia entre una linea (continua) y una coleccion de puntos (discreta). La topologia — la rama de las matematicas que estudia la continuidad y la conectividad — presupone la posibilidad de dividir (ir hacia "muchos") y de resistir la division (permanecer "uno").

**Conexion con primitivos.json**: Continuo/Discreto no tiene representacion explicita como eje dual en `primitivos.json`. Sin embargo, la tension entre lo continuo y lo discreto esta codificada implicitamente en la arquitectura misma del sistema TriadicGPT: los embeddings continuos se cuantizan a representaciones ternarias discretas {+1, 0, -1}. El paso de continuo a discreto es la operacion de cuantizacion; el paso de discreto a continuo es la operacion de embedding. La ausencia de un par explicito en primitivos.json sugiere que esta dualidad opera a nivel *meta* — es una propiedad de la representacion, no de un concepto representado.

**Objecion**: La distincion continuo/discreto podria ser una instanciacion de Uno/Muchos (si algo es "uno" es continuo, si es "muchos" es discreto). En tal caso, no satisface irreductibilidad.

**Respuesta**: La reduccion es superficial. Lo continuo no es simplemente "uno" y lo discreto no es simplemente "muchos." Una linea es continua *y* tiene muchos puntos. Un conjunto finito es discreto *y* puede tener un solo elemento. La dualidad Continuo/Discreto opera sobre una dimension distinta: no la *cantidad* de elementos sino la *estructura de conexion* entre ellos. Lo topologico es irreducible a lo aritmetico.

**Veredicto**: ADMITIDA.

---

### 2.3 Dualidad 10: Dentro / Fuera — Nace el limite y la autonomia

**Polos**: Dentro ($P^+$) y Fuera ($P^-$).
**Dominio que abre**: Biologia (membrana celular como condicion de la vida), termodinamica (distincion sistema/entorno), teoria de sistemas (Luhmann), topologia de conjuntos (interior, exterior, frontera).

**Argumento de dependencia critica — requiere Continuo/Discreto (d9).**
Un limite — una membrana, una frontera, un horizonte — es el punto donde lo continuo se vuelve discreto. La frontera de una celula es la superficie donde el medio continuo del citoplasma se interrumpe y comienza el medio externo. Sin la posibilidad de que algo sea continuo (conectado internamente) *y* discreto (separado de su entorno), la nocion de dentro/fuera no tiene contenido.

La dependencia tambien se sostiene desde la topologia: en un espacio topologico, la distincion entre interior y exterior de un conjunto requiere que el espacio tenga la estructura suficiente para definir conjuntos abiertos y cerrados — lo cual presupone nociones de continuidad y separacion.

**Conexion con primitivos.json**: El bit 10 (`contencion`) en la capa 2 (Linea, 1D) captura este concepto. Las dependencias de `contencion` en el grafo incluyen `fuerza` y primitivos de capa 1, lo cual es consistente con la idea de que contener algo requiere una fuerza que mantenga la separacion entre dentro y fuera. Ademas, los pares `union/separacion` (bits 11-12) en la misma capa codifican operaciones que presuponen la existencia de un limite que pueda cruzarse o mantenerse.

**Objecion**: La distincion dentro/fuera podria reducirse a Aqui/No-aqui (d2, espacio). Si "dentro" es un tipo de "aqui" y "fuera" es un tipo de "no-aqui," la candidata no es irreducible.

**Respuesta**: La objecion confunde posicion con contencion. Aqui/No-aqui es la dualidad de la posicion: un existente esta en un lugar o no. Dentro/Fuera es la dualidad de la *relacion entre un existente y un limite que lo envuelve*. Un objeto puede estar "aqui" sin estar "dentro" de nada — flota en el espacio abierto. La nocion de interioridad requiere una frontera, y la frontera requiere topologia (d9), que requiere cantidad (d8), que requiere patron (d7). La cadena de dependencias es genuina.

**Veredicto**: ADMITIDA.

---

### 2.4 Dualidad 11: Causa / Efecto — Nace la causalidad

**Polos**: Causa ($P^+$) y Efecto ($P^-$).
**Dominio que abre**: Ciencia experimental (el metodo cientifico presupone causalidad), logica (implicacion material como sombra de la causalidad), etica (responsabilidad presupone que las acciones causan efectos), medicina (etiologia).

**Argumento de dependencia critica — requiere Dentro/Fuera (d10).**
La causalidad robusta — la que permite decir "A causo B" y no solo "A precedio a B" — requiere la capacidad de distinguir un sistema de su entorno. La nocion de causa como *intervencion* (Pearl, 2000; Woodward, 2003) lo explicita: A causa B si intervenir sobre A (desde fuera del sistema que contiene a B) cambia B. Sin la distincion sistema/entorno (dentro/fuera), la causalidad se reduce a mera correlacion temporal — lo que Hume (1739) ya denuncio como el limite del concepto.

El argumento es mas fuerte de lo que parece. Consideremos un universo sin limites, donde todo esta conectado con todo sin frontera. En tal universo, toda correlacion seria "causal" (o ninguna lo seria, que es lo mismo). La causalidad selectiva — que *esto* causo *aquello* pero no lo otro — requiere poder aislar subsistemas, lo cual requiere fronteras.

Ademas, la causalidad requiere secuencia temporal (d3, antes/despues), identidad de los relata (d5, la causa y el efecto deben ser identificables), y patron (d7, la causalidad es una regularidad: las mismas causas producen los mismos efectos). Pero la dependencia *critica* — la mas alta en la cadena que no es trivialmente heredada — es Dentro/Fuera.

**Conexion con primitivos.json**: El bit 54 (`porque`) en la capa 3 (Tiempo, 1D+t) codifica explicitamente la causalidad. El bit 55 (`si_entonces`) codifica la condicionalidad logica, que es la version proposicional de la causalidad. Ambos dependen de primitivos temporales (posicion_temporal, flujo_temporal) y de primitivos de accion (hacer, mover), confirmando que la causalidad en el sistema de 63 bits requiere tanto temporalidad como agencia.

**Objecion**: La causalidad podria no requerir Dentro/Fuera. Muchas formulaciones de causalidad (Hume, Lewis, la semantica contrafactica) solo requieren regularidad temporal y no mencionan limites ni sistemas. La dependencia de d10 podria ser un artefacto de la tradicion intervencionista de Pearl.

**Respuesta**: La objecion es seria. Las formulaciones humeanas de causalidad (regularidad + contigüidad + prioridad temporal) no requieren explicitamente Dentro/Fuera — requieren solo d3 (tiempo), d5 (identidad de eventos) y d7 (regularidad). Si aceptamos una formulacion humeana, Causa/Efecto dependeria de d7 directamente, no de d10. Esto abre la posibilidad de que Causa/Efecto y Dentro/Fuera sean ramas paralelas que emergen de Uno/Muchos o incluso de Orden/Caos, en vez de formar una cadena. Volveremos a esta cuestion crucial en la Seccion III.

**Veredicto**: ADMITIDA, pero con reserva sobre la posicion exacta en la cadena. La dependencia de d10 es defendible en el marco intervencionista; la dependencia de d7 directamente es defendible en el marco humeano. Ambas posiciones se analizan en la Seccion III.

---

### 2.5 Dualidad 12: Semejante / Diferente — Nace la relacion y la analogia

**Polos**: Semejante ($P^+$) y Diferente ($P^-$).
**Dominio que abre**: Logica relacional, matematicas (isomorfismo, homomorfismo, equivalencia), conocimiento cientifico por analogia, clasificacion taxonomica, metafora.

**Argumento de dependencia critica — requiere Causa/Efecto (d11).**
La semejanza profunda entre dos entidades no se reduce a compartir propiedades superficiales. Dos entidades son genuinamente semejantes cuando producen los *mismos efectos* bajo las *mismas causas*. La semejanza funcional — que es la que importa para la ciencia y para la analogia — es semejanza causal. Dos farmacos son "semejantes" si producen los mismos efectos; dos estructuras arquitectonicas son "semejantes" si resisten las mismas fuerzas.

Sin causalidad, la semejanza se reduce a coincidencia de apariencia — lo que Goodman (1972) llamo "semejanza de familia" sin fuerza explicativa. Con causalidad, la semejanza se convierte en *isomorfismo funcional*: A es semejante a B si hay un mapeo que preserva las relaciones causales.

**Conexion con primitivos.json**: El bit 60 (`tipo_de`) en la capa 4 (Plano, 2D) codifica la relacion de clasificacion, que es la cristalizacion de la semejanza en taxonomia. "X es tipo_de Y" significa que X comparte con Y las propiedades relevantes — es decir, que X es *semejante* a Y en los aspectos que definen la categoria Y. Las dependencias de `tipo_de` en el grafo incluyen bits de identidad y de estructura, confirmando que la clasificacion requiere tanto identidad (d5) como estructura relacional.

**Objecion**: La semejanza podria ser mas primitiva que la causalidad. Los bebes reconocen semejanzas (caras, formas) antes de entender la causalidad. La psicologia del desarrollo (Piaget, 1952) sugiere que la comparacion es una operacion cognitiva mas temprana que la inferencia causal.

**Respuesta**: La objecion confunde el orden de emergencia *cognitiva* (en el desarrollo individual) con el orden de emergencia *ontologica* (en la estructura de la realidad). Un bebe puede detectar semejanzas perceptuales sin entender la causalidad, pero la *dualidad* Semejante/Diferente como dimension ontologica — la que permite que dos cosas sean genuinamente del mismo tipo y no solo visualmente parecidas — requiere un criterio de agrupacion mas fuerte que la percepcion. Ese criterio es la equivalencia funcional, que presupone causalidad. La semejanza perceptual temprana del bebe es un uso *debil* de la dualidad, que se fortalece cuando la causalidad emerge.

Con todo, la objecion tiene fuerza suficiente para considerar que Semejante/Diferente podria depender directamente de Identidad (d5) en vez de Causalidad (d11), formando otra posible bifurcacion. Este punto se retoma en la Seccion III.

**Veredicto**: ADMITIDA.

---

### 2.6 Dualidad 13: Parte / Todo — Nace la composicion y la emergencia

**Polos**: Parte ($P^+$) y Todo ($P^-$).
**Dominio que abre**: Mereologia (la logica formal de las partes y los todos), emergencia (la propiedad del todo que no esta en las partes), holismo vs. reduccionismo, composicion musical, arquitectura, biologia de sistemas.

**Argumento de dependencia critica — requiere Semejante/Diferente (d12).**
Para entender que algo es *parte* de un todo, se necesita poder comparar la parte con el todo y detectar tanto la semejanza (la parte comparte algo con el todo) como la diferencia (la parte no es el todo). Un ladrillo es parte de un muro: es *semejante* al muro en material, pero *diferente* en escala y funcion. Sin la capacidad de comparar, la relacion parte-todo se reduce a mera contencion espacial (Dentro/Fuera, d10), lo cual es mas pobre. La mereologia autentica requiere que la parte *contribuya* al todo — que la relacion sea funcional, no solo geometrica.

La mereologia ha sido formalizada extensamente (Lesniewski, 1916; Simons, 1987; Varzi, 2016), y todas las formulaciones presuponen una relacion de comparacion entre la parte y el todo. La relacion mereologica "x es parte de y" no es una mera relacion de inclusion conjuntista; es una relacion ontologica que requiere que x y y compartan un tipo de existencia (sean *semejantes* en algun respecto) pero difieran en completitud.

**Conexion con primitivos.json**: El bit 59 (`parte_de`) y el bit 46 (`todo`) representan explicitamente estos polos. `parte_de` esta en la capa 4 (Plano, 2D), consistente con su caracter relacional. `todo` esta en la capa 4 tambien. Sus dependencias incluyen bits de estructura y de cantidad, confirmando que la composicion requiere tanto la capacidad de contar (d8) como la de relacionar (d12).

**Objecion**: La relacion parte/todo podria ser mas primitiva que la semejanza. No necesito comparar un atomo con una molecula para saber que el atomo es parte de la molecula — basta con la contencion (d10). La mereologia extensional clasica (Goodman, Leonard, 1940) define la parthood sin referencia a semejanza.

**Respuesta**: La mereologia extensional clasica es deliberadamente minimalista — define la relacion parte-todo solo en terminos de overlap (compartir partes). Pero incluso el overlap presupone identidad de partes compartidas, lo cual es una forma de semejanza. Ademas, la mereologia extensional no captura la emergencia — la propiedad de que el todo sea mas que la suma de las partes — que es precisamente el fenomeno que motiva esta dualidad en el marco. La emergencia genuina requiere que el todo tenga propiedades *diferentes* de las partes, lo cual presupone la dualidad Semejante/Diferente.

**Veredicto**: ADMITIDA.

---

### 2.7 Dualidad 14: Sujeto / Objeto — Nace la consciencia

**Polos**: Sujeto ($P^+$) y Objeto ($P^-$).
**Dominio que abre**: Epistemologia (el conocimiento es relacion sujeto-objeto), fenomenologia (la consciencia es siempre consciencia *de* algo — intencionalidad husserliana), filosofia de la mente (el problema dificil de la consciencia), etica (el sujeto moral).

**Argumento de dependencia critica — requiere Parte/Todo (d13).**
El sujeto es un todo que se reconoce como distinto de su entorno. La auto-consciencia requiere que una entidad sea un *todo* organizado (no una mera coleccion de partes) que se distingue del *todo* mas amplio que lo contiene. Sin la relacion parte/todo, un existente no puede distinguir lo que *es* (su totalidad como organismo, como mente) de lo que lo *rodea* (el resto del universo). El sujeto nace cuando un todo dice "yo" — cuando la relacion parte/todo se vuelve reflexiva.

La fenomenologia de Husserl lo confirma: la consciencia es *intencional* — siempre esta dirigida a un objeto. Pero para que haya intencionalidad, debe haber un sujeto que dirige y un objeto al que se dirige, y ambos deben ser *todos* distinguibles dentro de un todo mayor. El sujeto es la parte del universo que se experimenta a si misma como todo; el objeto es la parte que el sujeto experimenta como otro todo.

**Conexion con primitivos.json**: Los bits 36-37 (`consciente/ausente`) en la capa 5 (Volumen, 3D) codifican explicitamente el eje de la consciencia como par dual. Su posicion en la capa mas alta de primitivos concretos (antes de la capa meta) es consistente con la posicion terminal de Sujeto/Objeto en la cadena extendida. Las dependencias de estos bits incluyen primitivos de vida/muerte, placer/dolor, querer, saber y pensar — todos en la misma capa 5 — confirmando que la consciencia presupone un organismo vivo con sensaciones, deseos y cognicion, es decir, un *todo* complejo.

**Objecion**: La consciencia podria no ser una dualidad sino una propiedad emergente (monista) que no tiene un polo opuesto genuino. "Ausente" no es el polo opuesto de "consciente" de la misma manera que "aqui" es polo opuesto de "no-aqui." La ausencia de consciencia no es una fuerza activa; es simplemente la falta de la propiedad. Si Sujeto/Objeto no tiene exclusion mutua genuina (en el sentido de la Definicion 1 del Documento 01), no es una dualidad propiamente dicha.

**Respuesta**: La objecion toca un punto profundo. El polo "Objeto" no es la mera ausencia de subjetividad, sino la *posicion de lo que es experimentado* en contraste con *lo que experimenta*. En la relacion sujeto-objeto, ambos polos son activos: el sujeto actua (percibe, juzga, desea) y el objeto resiste (tiene propiedades que el sujeto no puede alterar a voluntad). La piedra que observo no es "inconsciente" de la misma manera en que una habitacion esta "vacia": la piedra es *activamente objeto* — se presenta ante mi con propiedades que yo descubro pero no invento. La fenomenologia de Husserl, Heidegger y Merleau-Ponty insiste en que la objetividad es una modalidad de ser, no una carencia.

**Veredicto**: ADMITIDA.

---

## III. Estructura de las Dualidades Extendidas

### 3.1 ¿Cadena, arbol o lattice?

La presentacion lineal de las siete candidatas (d8 → d9 → d10 → d11 → d12 → d13 → d14) sugiere una cadena — un orden total donde cada dualidad depende estrictamente de la inmediata anterior. Pero el analisis detallado de la Seccion II revelo dos puntos donde la dependencia estricta es cuestionable:

1. **Causa/Efecto (d11) podria no requerir Dentro/Fuera (d10).** En una formulacion humeana de la causalidad (regularidad + secuencia temporal), d11 dependeria directamente de d7 (Orden/Caos) sin pasar por d8-d10.

2. **Semejante/Diferente (d12) podria no requerir Causa/Efecto (d11).** Si la semejanza se entiende perceptualmente (coincidencia de propiedades), d12 dependeria de d5 (Identidad) o de d8 (Uno/Muchos), sin necesitar causalidad.

Si ambas bifurcaciones son reales, la estructura de d8-d14 no es una cadena sino un lattice con al menos dos ramas.

### 3.2 Hipotesis de la cadena (orden total)

Bajo la hipotesis de la cadena, la secuencia completa de 14 dualidades es:

$$d_1 < d_2 < d_3 < d_4 < d_5 < d_6 < d_7 < d_8 < d_9 < d_10 < d_{11} < d_{12} < d_{13} < d_{14}$$

con la posible bifurcacion temprana d2/d3 ya identificada en el Documento 02. Los argumentos a favor:

- Cada paso de la cadena tiene una justificacion de dependencia (Seccion II).
- La cadena tiene una logica narrativa coherente: de la existencia al espacio, al tiempo, a la posibilidad, a la identidad, al movimiento, al patron, a la cantidad, a la topologia, al limite, a la causalidad, a la comparacion, a la composicion, a la consciencia.
- La cadena es parsimononiosa: no introduce estructura que no sea estrictamente necesaria.

### 3.3 Hipotesis del lattice (orden parcial con bifurcaciones)

Si las dos objeciones de la Seccion 3.1 se aceptan, la estructura seria un lattice con la siguiente forma:

```
d1 — d2 — d3 — d4 — d5 — d6 — d7
                                  |
                            d8 (Uno/Muchos)
                           /              \
                   d9 (Cont/Disc)    d11 (Causa/Efecto)
                          |                |
                   d10 (Dentro/Fuera) d12 (Semejante/Diferente)
                          \              /
                         d13 (Parte/Todo)
                               |
                        d14 (Sujeto/Objeto)
```

En esta estructura:
- d8 depende de d7.
- d9 y d11 dependen ambas de d8 pero son *incomparables* entre si (no se requieren mutuamente).
- d10 depende de d9; d12 depende de d11.
- d13 es el *join* (supremo) de d10 y d12: depende de ambas ramas, porque la composicion mereologica requiere tanto topologia (limites que definan las partes) como semejanza (criterio para saber que es parte de que).
- d14 depende de d13.

### 3.4 Descripcion del diagrama de Hasse

El diagrama de Hasse del poset completo (14 dualidades) bajo la hipotesis del lattice tendria las siguientes relaciones de cubierta (dependencia inmediata, sin intermediarios):

- $d_1 \lessdot d_2$
- $d_1 \lessdot d_3$ (o $d_2 \lessdot d_3$ si se sostiene el orden total temprano)
- $d_2 \lessdot d_4$ y $d_3 \lessdot d_4$ (d4 es el join de d2 y d3)
- $d_4 \lessdot d_5$
- $d_5 \lessdot d_6$
- $d_6 \lessdot d_7$
- $d_7 \lessdot d_8$
- $d_8 \lessdot d_9$ y $d_8 \lessdot d_{11}$ (bifurcacion)
- $d_9 \lessdot d_{10}$
- $d_{11} \lessdot d_{12}$
- $d_{10} \lessdot d_{13}$ y $d_{12} \lessdot d_{13}$ (d13 es el join)
- $d_{13} \lessdot d_{14}$

Este lattice tiene una propiedad estetica notable: la bifurcacion temprana (d2/d3 hacia d4) se replica en la bifurcacion tardia (d9/d11 hacia d13), sugiriendo una *auto-similitud* en la estructura de emergencia. La espiral generativa predice exactamente esto: el patron de nivel inferior se replica en niveles superiores.

### 3.5 Evaluacion: ¿cadena o lattice?

No podemos resolver esta cuestion solo con argumentacion a priori. La estructura correcta depende de hechos sobre las dependencias que son, en ultima instancia, empiricamente evaluables (ver Seccion V). Sin embargo, ofrecemos dos observaciones:

1. La hipotesis del lattice es *mas conservadora* epistemicamente: afirma menos (no todos los pares estan ordenados) y por lo tanto tiene menor riesgo de error.

2. La hipotesis del lattice es *mas consistente* con la estructura de primitivos.json, que muestra multiples ramas paralelas dentro de cada capa, no un orden total.

**Recomendacion**: Adoptar la hipotesis del lattice como hipotesis de trabajo, con la cadena como caso especial (si las bifurcaciones resultan ser dependencias genuinas que no detectamos).

---

## IV. Candidatas Rechazadas

Para cada candidata rechazada, indicamos cual de los tres criterios falla.

### 4.1 Caliente / Frio — Rechazada por reducibilidad

**Dominio aparente**: Termodinamica, temperatura, transferencia de calor.

**Razon del rechazo**: Caliente/Frio no satisface el criterio de irreductibilidad (Criterio 2). La temperatura es una *sintesis central* de Movimiento/Quietud (d6) y Uno/Muchos (d8, a traves de la cantidad): la temperatura es la energia cinetica *media* de un conjunto de particulas en movimiento. "Caliente" significa mucho movimiento promedio; "frio" significa poco movimiento promedio.

Como el Documento 01 establece en la Seccion IV (Sintesis Central), la temperatura es un concepto compuesto que se situa en el interior del circulo, en la interseccion de los ejes de movimiento y cantidad. No es una dimension nueva, sino una combinacion de dimensiones existentes.

**Test de irreductibilidad**: ¿Hay preguntas formulables en terminos de caliente/frio que no se puedan formular en terminos de movimiento + cantidad? La respuesta es no: "¿esta caliente este objeto?" equivale a "¿tiene este objeto mucha energia cinetica media?" La reformulacion es completa.

### 4.2 Verdadero / Falso — Rechazada por subsuncion

**Dominio aparente**: Logica, epistemologia, verdad como correspondencia o coherencia.

**Razon del rechazo**: Verdadero/Falso no satisface el criterio de irreductibilidad. La verdad proposicional — "es verdad que P" — es la aplicacion de Ser/No-ser (d5, Determinado/Indeterminado) al dominio de las proposiciones. Una proposicion verdadera es una que *es* (el caso); una proposicion falsa es una que *no es* (el caso). La dualidad Verdadero/Falso es d5 restringida al dominio linguistico.

Esto ya fue observado en el Documento 01, Seccion 2.4, donde se clasifico Verdadero/Falso como "subsumed por Ser/No-ser en el dominio proposicional." La clasificacion se mantiene.

**Test de irreductibilidad**: ¿Hay preguntas formulables en terminos de verdadero/falso que no se puedan formular en terminos de ser/no-ser? La respuesta requiere cuidado. "¿Es verdadera esta oracion?" parece requerir un concepto de verdad propio. Pero "¿es verdadera esta oracion?" puede reformularse como "¿es el caso lo que esta oracion dice?" — que es una pregunta sobre si el estado de cosas descrito por la oracion *es* o *no es*. La verdad es la *mediacion* entre lenguaje y ser, no una dimension independiente.

### 4.3 Mas / Menos — Rechazada por derivabilidad

**Dominio aparente**: Comparacion cuantitativa, magnitud, medida.

**Razon del rechazo**: Mas/Menos no satisface el criterio de irreductibilidad. La comparacion cuantitativa es una operacion *derivada* de Uno/Muchos (d8): "A tiene mas que B" presupone que se puede contar lo que A tiene y lo que B tiene, y luego comparar las cantidades. Mas/Menos es a Uno/Muchos lo que la velocidad es a espacio y tiempo — un concepto compuesto, no una dimension primaria.

El propio plan de investigacion (seccion III del plan) ya identifico esta relacion: "Mas primitivo que 'mas/menos' — primero necesitas distinguir 'uno' de 'muchos' antes de comparar cantidades." Uno/Muchos subsume a Mas/Menos.

**Test de generatividad**: ¿Abre Mas/Menos un dominio que Uno/Muchos no cubra? La respuesta es no. Todo lo que puede formularse en terminos de mas/menos puede formularse en terminos de cantidad (cuantos hay aqui vs. cuantos hay alli).

### 4.4 Repeticion / Variacion — Rechazada por equivalencia

**Dominio aparente**: Ritmo, patron, composicion musical, genetica (mutacion vs. copia fiel).

**Razon del rechazo**: Repeticion/Variacion no satisface el criterio de irreductibilidad porque es una *reformulacion* de Orden/Caos (d7). El orden *es* la repeticion de lo reconocible. El caos *es* la variacion de lo esperado. Los polos de Repeticion/Variacion son los mismos polos de Orden/Caos con distintos nombres.

**Test de irreductibilidad**: ¿Son "repeticion" y "orden" conceptos genuinamente distintos? El orden admite formas no repetitivas (un cristal quasi-periodico, la secuencia de Fibonacci), por lo que "orden" es mas general que "repeticion." Pero esto no salva a Repeticion/Variacion como dualidad independiente — solo muestra que es un caso especial de Orden/Caos, no una dimension nueva.

---

## V. Conexion Empirica

### 5.1 Mapeo al sistema de 63 bits

El sistema TriadicGPT utiliza 63 primitivos conceptuales organizados en 6 capas de dimensionalidad creciente (0D → 1D → 1D+t → 2D → 3D → 3D+). Cada primitivo puede estar en estado +1, 0 o -1 para cualquier concepto. La pregunta clave es: ¿como se mapean las dualidades extendidas (d8-d14) a este sistema?

La tabla siguiente resume el mapeo:

| Dualidad | Bits explicitamente asociados | Capa | ¿Representacion directa? |
|----------|------------------------------|------|--------------------------|
| d8 Uno/Muchos | bit 44 (`uno`), bit 45 (`muchos`) | 4 (2D) | Si — par explicito |
| d9 Continuo/Discreto | — | — | No — ausente del sistema |
| d10 Dentro/Fuera | bit 10 (`contencion`) | 2 (1D) | Parcial — solo un polo |
| d11 Causa/Efecto | bit 54 (`porque`), bit 55 (`si_entonces`) | 3 (1D+t) | Si — par explicito |
| d12 Semejante/Diferente | bit 60 (`tipo_de`) | 4 (2D) | Parcial — solo clasificacion |
| d13 Parte/Todo | bit 59 (`parte_de`), bit 46 (`todo`) | 4 (2D) | Si — par explicito |
| d14 Sujeto/Objeto | bits 36-37 (`consciente/ausente`) | 5 (3D) | Si — eje dual explicito |

### 5.2 Observaciones

**1. Tres dualidades extendidas tienen representacion dual completa** (d8, d13, d14): ambos polos estan codificados como primitivos distintos. Esto sugiere que el diseño original de primitivos.json ya anticipaba estas dualidades, probablemente por intuicion, antes de que el marco formal las justificara.

**2. Dos dualidades tienen representacion parcial** (d10, d12): solo uno de los dos polos esta codificado. `contencion` captura "dentro" pero no "fuera"; `tipo_de` captura la semejanza taxonomica pero no la diferencia explicita. Esto sugiere que la representacion actual es *incompleta* y que agregar los polos faltantes podria enriquecer el sistema.

**3. Una dualidad esta completamente ausente** (d9, Continuo/Discreto): no hay ningun primitivo que capture explicitamente la distincion entre lo continuo y lo discreto. Esto es notable porque la distincion opera a nivel meta en el sistema (la tension entre embeddings continuos y cuantizacion ternaria), pero no esta reificada como primitivo. Esta ausencia es coherente con la observacion de la Seccion 2.2: Continuo/Discreto podria ser una propiedad de la *representacion* y no del *contenido representado*.

**4. Una dualidad tiene representacion dual pero en un contexto parcial** (d11): `porque` y `si_entonces` codifican causalidad y condicionalidad, pero estan en la capa temporal (1D+t), no en una capa relacional superior. Esto sugiere que primitivos.json trata la causalidad como fenomeno temporal, lo cual es consistente con una lectura humeana y refuerza la objecion de la Seccion 2.4 sobre la posicion de d11 en la cadena.

### 5.3 Prediccion falsificable

Si la cadena de emergencia d7 → d8 → ... → d14 es correcta, deberia cumplirse la siguiente prediccion en los datos de anclas (`anclas_v2.json`):

**Prediccion**: Para cada par (d_i, d_j) con i < j en la cadena extendida, la frecuencia de conceptos en `anclas_v2.json` que activan bits de d_j sin activar bits de d_i deberia ser significativamente menor que lo esperado por azar.

Formalmente: si $B_i$ es el conjunto de bits correspondientes a $d_i$ y $B_j$ el conjunto correspondiente a $d_j$, entonces:

$$P(\text{algun bit de } B_j \text{ activo} \mid \text{ningun bit de } B_i \text{ activo}) \ll P(\text{algun bit de } B_j \text{ activo})$$

Este test es ejecutable computacionalmente sobre los datos existentes.

### 5.4 Dualidades extendidas como guia para primitivos v3

Los resultados del mapeo sugieren que una version futura de `primitivos.json` (v3) podria beneficiarse de:

1. Agregar un par dual explicito para Continuo/Discreto (bits nuevos en capa 2 o 3).
2. Completar los pares parciales: agregar un polo `exterior` junto a `contencion`, y un polo `diferente_de` junto a `tipo_de`.
3. Reorganizar la posicion de `porque` y `si_entonces` si se confirma que la causalidad depende de Dentro/Fuera y no solo de temporalidad.

---

## VI. Preguntas Abiertas

1. **¿Es la bifurcacion d9/d11 real o aparente?** Si Causa/Efecto depende genuinamente solo de Orden/Caos (y no de Dentro/Fuera ni de Continuo/Discreto), la rama topologica (d9-d10) y la rama causal (d11-d12) son independientes, y el lattice tiene la forma descrita en la Seccion 3.3. Si Causa/Efecto requiere Dentro/Fuera, la estructura es una cadena. El test empirico de la Seccion 5.3 podria resolver esta cuestion.

2. **¿Hay dualidades 15+?** La espiral generativa predice que no hay limite superior al numero de dualidades. Candidatas posibles para d15+ incluyen: Finito/Infinito (¿requiere Continuo/Discreto?), Necesario/Contingente (¿requiere Causa/Efecto?), Significante/Significado (¿requiere Sujeto/Objeto?). El criterio es el mismo: dependencia, irreductibilidad, generatividad. Un documento futuro podria explorar estas extensiones.

3. **¿Coincide la secuencia con el orden de emergencia cosmologica?** Las 7 fundamentales siguen una logica de emergencia ontologica (logica, no historica). Pero ¿corresponden las extendidas a etapas del universo fisico? La cantidad (d8) emerge con las particulas; la topologia (d9) con el espacio-tiempo continuo; el limite (d10) con las primeras estructuras; la causalidad (d11) con las leyes fisicas; la semejanza (d12) con la formacion de especies quimicas; la composicion (d13) con la materia compleja; la consciencia (d14) con la vida neuronal. La correspondencia es sugestiva pero no constituye argumento — el orden ontologico podria diferir del cosmologico.

4. **¿Es d14 el techo o solo el techo *actual*?** Si Sujeto/Objeto es la ultima dualidad, el marco tiene una clausura natural — termina en la consciencia, que es donde comienza la filosofia. Pero la espiral no tiene clausura formal. Las sintesis de d14 (intersubjetividad, cultura, lenguaje, historia) podrian externalizarse como dualidades de tercer orden. La pregunta de si hay un techo absoluto es equivalente a preguntar si la espiral converge o diverge — una cuestion que el Documento 05 deberia abordar formalmente.

5. **¿Puede el sistema de 63 bits extenderse a 128 bits para capturar las dualidades 8-14 completas?** El sistema actual tiene 63 primitivos; una version con 128 bits (2^7 - 1 → 2^7) podria asignar bits explicitos a todos los polos de las 14 dualidades. La cuestion practica es si la extension mantiene la parsimonia del sistema o lo infla innecesariamente.

6. **¿Es la auto-similitud del lattice (bifurcacion temprana d2/d3 replicada en bifurcacion tardia d9/d11) una propiedad profunda o una coincidencia?** Si es profunda, sugiere que la espiral generativa produce *fractales categoriales* — cada ciclo de emergencia replica la estructura del ciclo anterior a mayor escala. Este seria un resultado notable que conectaria el marco con la geometria fractal y con la auto-similitud observada en sistemas complejos.

---

## Referencias

- Aristoteles (c. 350 a.C.). *Categorias*. En *Organon*.
- Aristoteles (c. 350 a.C.). *Metafisica*, Libro Theta.
- Frege, G. (1884). *Die Grundlagen der Arithmetik*.
- Goodman, N. (1972). "Seven Strictures on Similarity." En *Problems and Projects*, pp. 437-447. Indianapolis: Bobbs-Merrill.
- Goodman, N. & Leonard, H. S. (1940). "The Calculus of Individuals and Its Uses." *Journal of Symbolic Logic*, 5(2), 45-55.
- Hegel, G. W. F. (1812-1816). *Wissenschaft der Logik*.
- Hume, D. (1739). *A Treatise of Human Nature*, Book I, Part III.
- Husserl, E. (1900-1901). *Logische Untersuchungen*, Tercera Investigacion.
- Kant, I. (1781/1787). *Kritik der reinen Vernunft*.
- Lesniewski, S. (1916). *Podstawy ogolnej teoryi mnogosci* [Fundamentos de la teoria general de conjuntos].
- Luhmann, N. (1984). *Soziale Systeme*.
- Ornelas Brand, A. (2026a). *La Danza Cosmica de los Opuestos*.
- Ornelas Brand, A. (2026b). "End-to-End Prime Factorization in a Generative Language Model." Manuscrito.
- Pearl, J. (2000). *Causality: Models, Reasoning, and Inference*. Cambridge University Press.
- Piaget, J. (1952). *The Origins of Intelligence in Children*. New York: International Universities Press.
- Simons, P. (1987). *Parts: A Study in Ontology*. Oxford: Clarendon Press.
- Varzi, A. C. (2016). "Mereology." En E. N. Zalta (Ed.), *Stanford Encyclopedia of Philosophy*.
- Wheeler, J. A. (1990). "Information, Physics, Quantum." En *Complexity, Entropy, and the Physics of Information*.
- Woodward, J. (2003). *Making Things Happen: A Theory of Causal Explanation*. Oxford University Press.

---

## Addenda — Revision Empirica (Documentos 11-12)

Los Documentos 11 y 12 someten la estructura propuesta en este documento a verificacion computacional contra el grafo de dependencias de `primitivos.json` y los datos de `anclas_v2.json`. Los hallazgos principales que modifican las conclusiones de este documento son:

### A.1 La cadena d8→d14 no se sostiene

La estructura empirica no es una cadena ni un lattice simetrico, sino un **arbol asimetrico con tronco dominante**:

```
d8 (Uno/Muchos)
├── TRONCO: contención (d10→d9') → parte_de (d13→d10') → vida (→d11') → consciente (d14)
├── RAMAL: porque (d11) → si_entonces [1 descendente, FIN]
└── RAMAL: tipo_de (d12) [0 descendentes, FIN]
```

### A.2 d9 (Continuo/Discreto) eliminada

No tiene representacion en primitivos.json. Se reclasifica como meta-propiedad del marco de representacion. Dentro/Fuera asciende a la posicion d9'.

### A.3 Causa/Efecto y Semejante/Diferente son ramales terminales

- `porque`: betweenness #15, flujo DAG = 3, 1 descendente
- `tipo_de`: betweenness #22, flujo DAG = 5, 0 descendentes
- Cero co-activacion con la rama topologica en 104 anclas

Se propone una taxonomia: **dualidades constitutivas** (abren dominios) vs. **dualidades operativas** (codifican relaciones).

### A.4 Vida/Muerte como dualidad formal

vida es la bisagra de segundo orden: flujo DAG = 182 (rank #2), betweenness 0.126 (#5), unico nodo que cruza las tres ramas. Se propone numerarla como d11'.

### A.5 Auto-similitud confirmada al 80%

La bifurcacion d8→{contención, porque}→vida replica la bifurcacion d1→{d2, d3}→d4 con deformacion: mas ramas, mas asimetria, reunificacion parcial. Fractal natural, no matematico.

Ver Documentos 11 y 12 para los detalles completos, resultados cuantitativos, y scripts reproducibles.

---

*Parte del manuscrito "Expansion del Circulo de Emergencia de Dualidades."*
