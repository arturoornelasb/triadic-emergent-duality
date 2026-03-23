# Documento 32: Algebra de Composicion de Conceptos

| Metrica | Resultado |
|---------|-----------|
| Operacion central | Producto de primos ancestrales = firma unica |
| Primitivos | 63, cada uno con un primo asignado |
| Propiedad clave | Teorema fundamental de la aritmetica: firma unica y reversible |
| MCD | Primitivos compartidos entre dos conceptos |
| MCM | Primitivos necesarios para que ambos conceptos existan |
| Dependencias | Solo stdlib Python (json, math, sys, os, collections) |

---

## I. La idea

Cada primitivo tiene un numero primo asignado (campo `primo` en `primitivos.json`). Cada primitivo tambien tiene dependencias transitivas — todos los primitivos que necesita para existir.

**Observacion:** El producto de los primos de todos los ancestros transitivos de un primitivo produce un numero unico que funciona como **firma algebraica** del concepto. Por el teorema fundamental de la aritmetica, esta firma es:

1. **Unica** — ningun otro conjunto de primitivos produce el mismo producto
2. **Reversible** — factorizar el numero recupera exactamente los primitivos componentes
3. **Composicional** — la firma codifica la definicion completa del concepto

## II. Definicion formal

Sea $P = \{p_1, p_2, ..., p_{63}\}$ el conjunto de primitivos, y sea $\pi(p_i)$ el primo asignado al primitivo $p_i$.

Sea $A(p_i) \subseteq P$ el conjunto de ancestros transitivos de $p_i$ en el DAG (todos los primitivos de los que depende, directa o indirectamente).

**Firma de composicion:**

$$\sigma(p_i) = \prod_{a \in A(p_i)} \pi(a)$$

Para las raices (vacio, informacion, uno), $A(p_i) = \emptyset$, por lo que $\sigma(p_i) = 1$ (producto vacio).

## III. Ejemplos

```
orden (primo=83, capa 3)
  Ancestros: uno, fuerza, eje_profundidad, mas, mover, posicion_temporal
  Firma: 197 x 5 x 23 x 293 x 233 x 37 = 57,225,465,215

puede (primo=269, capa 4)
  Ancestros: uno, fuerza, eje_profundidad, mover, hacer, eje_vertical, libertad
  Firma: 197 x 5 x 23 x 233 x 227 x 19 x 127 = 2,891,366,644,865

vida (primo=137, capa 5)
  Ancestros: 13 primitivos
  Firma: 42,669,307,913,327,123,333,505

consciente (primo=157, capa 5)
  Ancestros: 16 primitivos
  Firma: 4,775,932,965,430,791,587,595,881,145
```

A mayor capa, mayor firma. Esto es inevitable: mas ancestros = mas factores = numero mas grande. La **longitud en digitos** de la firma es una medida natural de la complejidad del concepto.

## IV. Operaciones entre conceptos

### MCD: lo que comparten

$$\text{MCD}(\sigma(p_i), \sigma(p_j)) = \prod_{a \in A(p_i) \cap A(p_j)} \pi(a)$$

El maximo comun divisor de dos firmas da exactamente los primitivos ancestrales que ambos conceptos comparten.

**Ejemplo:** Si `orden` y `flujo_temporal` comparten los ancestros {uno, fuerza, eje_profundidad, mover}, su MCD codifica esa interseccion.

### MCM: lo que necesitas para ambos

$$\text{MCM}(\sigma(p_i), \sigma(p_j)) = \prod_{a \in A(p_i) \cup A(p_j)} \pi(a)$$

El minimo comun multiplo da el conjunto completo de primitivos necesarios para que ambos conceptos existan simultaneamente.

### Division: lo que diferencia

$$\frac{\sigma(p_i)}{\text{MCD}(\sigma(p_i), \sigma(p_j))} = \prod_{a \in A(p_i) \setminus A(p_j)} \pi(a)$$

Los primitivos que $p_i$ necesita pero $p_j$ no. Esto da la **diferencia conceptual** entre dos conceptos.

## V. Conceptos compuestos de nivel superior

Los 63 primitivos son conceptos de nivel 1. Pero conceptos como "temperatura" o "amor" son compuestos que combinan multiples primitivos sin ser primitivos ellos mismos.

### Complementarios vs opuestos reales

Un par de primitivos complementarios (ej. bien/mal, orden/caos) comparte escala — se definen mutuamente. Su relacion:

- **Opuesto aparente:** el otro polo del mismo eje dual
- **Opuesto real:** la eliminacion del primitivo generador (trazar hacia atras en el DAG hasta encontrar la dependencia cuya ausencia anula ambos polos)

**Ejemplo:**
- bien y mal son complementarios (eje dual, capa 4)
- bien depende de: contencion, orden, union
- mal depende de: contencion, caos, separacion
- Comparten: contencion (y transitivamente: uno, separacion)
- Opuesto real de ambos: la ausencia de contencion — sin frontera interior/exterior, no hay moral

### Matiz del opuesto real

El opuesto real de cada polo llega al mismo lugar pero por caminos distintos:

- Opuesto real de bien: quitar orden → se pierde la estructura que define lo bueno
- Opuesto real de mal: quitar caos → se pierde el desorden que define lo malo
- Ambos convergen en: quitar contencion → sin frontera, no hay ni bien ni mal

Esto implica que el opuesto real no es un punto sino un **cono** — un conjunto de caminos que convergen en la eliminacion de las dependencias compartidas.

## VI. Gradiente de complejidad del opuesto

| Nivel | Ejemplo | Opuesto | Claridad |
|-------|---------|---------|----------|
| Primitivo | mover | no-mover | Total: un factor |
| Compuesto simple | temperatura (frio/calor) | inmovilidad | Alta: pocos factores |
| Compuesto medio | amor/odio | indiferencia (con matices) | Parcial: varios factores |
| Compuesto complejo | motor de combustion | ? | Difusa: muchos factores |

A mas factores primos en la firma, mas borroso se vuelve el opuesto aparente, pero el opuesto real (la factorizacion) siempre es preciso. La complejidad no esta en el sistema — esta en nuestra dificultad para percibir la factorizacion completa.

## VII. Perspectiva y definicion acumulativa

La clasificacion D/A/N por dominio en `reference_domains.json` es una **perspectiva** sobre cada primitivo. Un primitivo clasificado como D (directo) en fisica puede ser A (analogico) en filosofia.

Esto significa que el "opuesto real" de un concepto compuesto puede variar segun el dominio:

- En fisica: el opuesto real de temperatura es ausencia de energia cinetica (quitar mover en sentido fisico)
- En filosofia: el opuesto real de temperatura podria ser ausencia de cambio existencial (quitar mover en sentido metaforico)

**Definicion acumulativa:** La definicion "completa" de un concepto es la suma de todas sus definiciones por dominio. Formalmente:

$$\text{Def}(p) = \{(d, c_d(p)) : d \in \text{Domains}\}$$

donde $c_d(p) \in \{D, A, N\}$ es la clasificacion del primitivo $p$ en el dominio $d$.

La firma algebraica $\sigma(p)$ da la estructura (que primitivos lo componen), y el perfil de dominio $\text{Def}(p)$ da el significado (como opera en cada contexto). Juntos, definen completamente un concepto.

## VIII. Implicacion para el circulo de dualidades

Las 7 dualidades no son primitivos ni conceptos compuestos — son **categorias** que agrupan primitivos por el tipo de oposicion que encarnan. El circulo de emergencia ordena estas categorias, no los primitivos individuales.

La tension encontrada en el documento 31 (D6 aparece antes que D3 en el DAG pero despues en el circulo) se resuelve al distinguir niveles:

- **Nivel primitivo (DAG):** mover (capa 3) precede a posicion_temporal (capa 3) por dependencia directa
- **Nivel dualidad (circulo):** "Movimiento/Quietud" como categoria requiere que ya existan Espacio y Tiempo como marcos de referencia

El producto de primos opera en el nivel primitivo. El circulo opera en el nivel de categorias. Son algebras diferentes sobre el mismo conjunto base.

## IX. Preguntas abiertas

1. ¿Se puede definir una "firma de dualidad" como el producto de los primos de todas sus anclas? ¿Que relaciones emergen entre las 7 firmas?
2. ¿El MCD entre firmas de dualidades revela dependencias que el circulo no captura?
3. ¿Existe una operacion algebraica sobre firmas que reproduzca el orden del circulo?
4. ¿Los conceptos compuestos de nivel 2+ (temperatura, amor) necesitan primos propios, o basta con el producto de sus componentes?
