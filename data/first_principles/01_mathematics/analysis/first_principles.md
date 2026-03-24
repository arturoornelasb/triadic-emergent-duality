# First Principles of Analysis

## Overview

Analysis is the rigorous study of **limits, continuity, differentiation, integration, and infinite processes**. It is the mathematical framework that formalizes calculus and extends it to higher dimensions, function spaces, and abstract settings. Analysis provides the precise language for describing change, approximation, and convergence — concepts that are central to physics, engineering, and probability theory.

The first principles of analysis are the axioms that define the real number system and the foundational theorems that flow from them.

## Prerequisites

- Logic & Set Theory (foundational language)
- Algebra (ordered field axioms)
- Mathematical Foundations (axiomatic method)

---

## First Principles

### AXIOM SYSTEM 1: The Complete Ordered Field (Axioms for ℝ)

The real numbers ℝ are characterized as the **unique complete ordered field**. This means ℝ satisfies:

#### AXIOM 1.1: Field Axioms
- (ℝ, +, ·) is a field (see Algebra: Field Axioms).

#### AXIOM 1.2: Total Order Axioms
- **Formal Statement:** There exists a relation ≤ on ℝ that is reflexive, antisymmetric, transitive, and total (∀a,b: a ≤ b or b ≤ a). Furthermore:
  - If a ≤ b, then a + c ≤ b + c (translation invariance)
  - If 0 ≤ a and 0 ≤ b, then 0 ≤ a · b (multiplication preserves positivity)
- **Plain Language:** The real numbers are lined up in order, and this order is compatible with arithmetic.

#### AXIOM 1.3: Completeness (Least Upper Bound Property) — THE KEY AXIOM

- **Formal Statement:** Every non-empty subset of ℝ that is bounded above has a least upper bound (supremum) in ℝ.
- **Plain Language:** There are no "gaps" in the real number line. If a set of real numbers has an upper bound, there is a smallest such bound, and it is a real number.
- **Historical Context:** This axiom is what distinguishes ℝ from ℚ. The rationals have gaps (e.g., {x ∈ ℚ : x² < 2} has no rational supremum). Dedekind (1872) formulated completeness via "cuts"; Cantor (1872) via Cauchy sequences. Hilbert (1900) gave the axiomatic characterization.
- **Depends On:** Field axioms, order axioms.
- **Implications:** Completeness is the single most important axiom in analysis. From it flow: convergence of bounded monotone sequences, the Bolzano-Weierstrass theorem, the Intermediate Value Theorem, the Extreme Value Theorem, and the entire edifice of calculus. Without completeness, limits would not always exist and integration would fail.

**Uniqueness:** There is exactly one complete ordered field up to isomorphism. Any two are isomorphic. This is why we can speak of "the" real numbers.

---

### PRINCIPLE 1: The ε-δ Definition of Limit

- **Formal Statement:** lim(x→a) f(x) = L if and only if: ∀ε > 0, ∃δ > 0: 0 < |x - a| < δ → |f(x) - L| < ε
- **Plain Language:** f(x) approaches L as x approaches a if we can make f(x) as close to L as we want by making x sufficiently close to a.
- **Historical Context:** Cauchy (1821) gave the intuitive version; Weierstrass (~1860s) provided the rigorous ε-δ formulation. This definition replaced centuries of vague notions of "infinitely small" with precise quantitative reasoning.
- **Depends On:** The real numbers (completeness, distance via absolute value).
- **Implications:** The ε-δ definition is the foundation of *all* of analysis. Continuity, differentiability, integrability, and convergence are all defined in terms of limits. It transforms vague intuition into checkable conditions.

---

### PRINCIPLE 2: Continuity

- **Formal Statement:** f: ℝ → ℝ is continuous at a if lim(x→a) f(x) = f(a). Equivalently: ∀ε > 0, ∃δ > 0: |x - a| < δ → |f(x) - f(a)| < ε
- **Plain Language:** A function is continuous if small changes in input produce small changes in output. No sudden jumps.
- **Historical Context:** Cauchy and Weierstrass. The modern topological definition (preimage of open sets is open) generalizes this to any topological space.
- **Depends On:** Limits (ε-δ definition).
- **Implications:** Continuity is the bridge between local and global behavior. The Intermediate Value Theorem (continuous functions on intervals take all intermediate values) and the Extreme Value Theorem (continuous functions on closed bounded intervals attain their bounds) both depend on continuity + completeness.

---

### PRINCIPLE 3: The Derivative (Definition of Differentiation)

- **Formal Statement:** f'(a) = lim(h→0) [f(a+h) - f(a)] / h, provided this limit exists.
- **Plain Language:** The derivative is the instantaneous rate of change — the slope of the tangent line at a point.
- **Historical Context:** Newton (~1666) and Leibniz (~1675), independently. Rigorized by Cauchy and Weierstrass using the ε-δ limit. Newton called it "fluxion"; Leibniz introduced the dy/dx notation.
- **Depends On:** Limits.
- **Implications:** Differentiation is half of calculus. It enables the study of optimization (maxima/minima), rates of change, linear approximation, and differential equations. The Mean Value Theorem connects derivatives to function behavior.

---

### PRINCIPLE 4: The Riemann Integral

- **Formal Statement:** ∫_a^b f(x) dx = lim(||P||→0) Σ f(x_i*) Δx_i, where P is a partition of [a,b], ||P|| is the mesh of the partition, and x_i* ∈ [x_{i-1}, x_i].
- **Plain Language:** The integral is the "area under the curve," computed as the limit of increasingly fine Riemann sums.
- **Historical Context:** Riemann (1854). Generalized by Lebesgue (1902) using measure theory, which handles a much wider class of functions.
- **Depends On:** Limits, completeness of ℝ.
- **Implications:** Integration is the other half of calculus. The Fundamental Theorem of Calculus links it to differentiation. Lebesgue's generalization is essential for modern probability, functional analysis, and PDE theory.

---

### THEOREM 1: The Fundamental Theorem of Calculus

- **Formal Statement:**
  1. If f is continuous on [a,b] and F(x) = ∫_a^x f(t) dt, then F'(x) = f(x).
  2. If F' = f on [a,b] and f is integrable, then ∫_a^b f(x) dx = F(b) - F(a).
- **Plain Language:** Differentiation and integration are inverse operations. The area function's rate of change is the original function.
- **Historical Context:** Newton and Leibniz (independently, 1660s-1680s). Rigorously proved by Cauchy (1823) and refined by Riemann and Lebesgue.
- **Depends On:** Continuity, derivative, integral, completeness.
- **Implications:** This theorem is arguably the most important single result in applied mathematics. It connects the two fundamental operations of calculus and enables the practical computation of integrals.

---

### PRINCIPLE 5: Convergence of Sequences and Series

- **Formal Statement:** A sequence (a_n) converges to L if ∀ε > 0, ∃N ∈ ℕ: n > N → |a_n - L| < ε. A series Σa_n converges if its partial sums converge.
- **Plain Language:** A sequence converges if its terms get arbitrarily close to a limit value and stay there.
- **Historical Context:** Cauchy (1821) introduced the Cauchy criterion: a sequence converges if and only if its terms get arbitrarily close to *each other*. This criterion is equivalent to completeness of ℝ.
- **Depends On:** Completeness of ℝ (Cauchy completeness).
- **Implications:** Convergence is the machinery that makes infinite processes rigorous — Taylor series, Fourier series, numerical methods, probability (law of large numbers). The Cauchy criterion extends to all complete metric spaces.

---

### PRINCIPLE 6: Compactness (Heine-Borel Theorem)

- **Formal Statement:** A subset of ℝⁿ is compact if and only if it is closed and bounded. Equivalently, every open cover has a finite subcover.
- **Plain Language:** Compact sets are the "nice" sets where infinite processes behave well — every sequence has a convergent subsequence, and continuous functions achieve their bounds.
- **Historical Context:** Bolzano (1817), Weierstrass, Heine (1872), Borel (1895). Generalized to abstract topological spaces by Alexandrov and Urysohn.
- **Depends On:** Completeness, Bolzano-Weierstrass theorem.
- **Implications:** Compactness is the key condition in analysis that ensures limits, maxima, and minima exist. The Extreme Value Theorem, uniform continuity on compact sets, and Arzelà-Ascoli theorem all depend on compactness.

---

### PRINCIPLE 7: Metric Space Axioms (Generalized Analysis)

- **Formal Statement:** A metric space (X, d) is a set X with a function d: X × X → [0,∞) satisfying:
  1. d(x,y) = 0 ↔ x = y (identity of indiscernibles)
  2. d(x,y) = d(y,x) (symmetry)
  3. d(x,z) ≤ d(x,y) + d(y,z) (triangle inequality)
- **Plain Language:** A metric space is any set with a notion of "distance" satisfying three natural properties.
- **Historical Context:** Fréchet (1906). Generalized the ε-δ framework from ℝ to arbitrary spaces. Hausdorff (1914) further generalized to topological spaces.
- **Depends On:** Set theory, the concept of a function.
- **Implications:** Metric spaces are the natural setting for analysis beyond ℝⁿ. Function spaces (C[a,b], L^p), sequence spaces (ℓ^p), and abstract spaces all carry natural metrics. The Banach fixed-point theorem, completeness, and compactness all generalize to metric spaces.

---

### PRINCIPLE 8: Measure and Integration (Lebesgue Theory)

- **Formal Statement:** A measure μ on a σ-algebra Σ of subsets of X satisfies:
  1. μ(∅) = 0
  2. μ(A) ≥ 0 for all A ∈ Σ
  3. μ(⋃ Aₙ) = Σ μ(Aₙ) for any countable collection of disjoint sets (countable additivity)
- **Plain Language:** A measure assigns a "size" (length, area, volume, probability) to sets in a way that is non-negative and additive.
- **Historical Context:** Lebesgue (1902). Solved the problem of integrating highly irregular functions that Riemann integration could not handle. Became the foundation of modern probability theory (Kolmogorov, 1933).
- **Depends On:** Set theory (σ-algebras), real number axioms.
- **Implications:** Lebesgue measure and integration are the backbone of modern analysis. They enable: L^p spaces, Fourier analysis on general spaces, probability theory, and ergodic theory. The dominated convergence theorem and Fubini's theorem are key tools.

---

---

### THEOREM 2: Banach Fixed-Point Theorem (Contraction Mapping Principle)

- **Formal Statement:** Let (X, d) be a complete metric space and T: X → X a contraction mapping (∃q ∈ [0,1): d(T(x), T(y)) ≤ q·d(x,y) for all x,y). Then T has a unique fixed point x* = T(x*), and for any x₀, the sequence T^n(x₀) → x*.
- **Plain Language:** If a map always brings points closer together in a complete space, it has exactly one fixed point, and iterating the map from anywhere converges to it.
- **Historical Context:** Stefan Banach (1922). One of the most widely applied theorems in all of mathematics.
- **Depends On:** Completeness of the metric space.
- **Implications:** The Banach fixed-point theorem proves: the Picard-Lindelöf theorem (existence and uniqueness of ODE solutions), convergence of iterative algorithms (Newton's method, successive approximation), and is used throughout numerical analysis, economics (contraction mapping approach to equilibrium), and game theory.

---

### THEOREM 3: The Implicit Function Theorem

- **Formal Statement:** If F: ℝⁿ⁺ᵐ → ℝᵐ is continuously differentiable, F(a,b) = 0, and the Jacobian ∂F/∂y evaluated at (a,b) is invertible, then near (a,b) the equation F(x,y) = 0 implicitly defines y as a function of x: y = g(x), and g is continuously differentiable.
- **Plain Language:** If a system of equations is satisfied at a point and a certain non-degeneracy condition holds, then the equations locally define some variables as smooth functions of the others.
- **Historical Context:** Cauchy (1831, single variable), Dini (1870s, several variables). A cornerstone of differential topology and differential geometry.
- **Depends On:** Completeness of ℝ, Banach fixed-point theorem, differentiability.
- **Implications:** The implicit function theorem guarantees: smooth manifolds are locally like ℝⁿ, Lagrange multipliers work, equilibria in economics exist and are smooth, and level sets of smooth functions are smooth. It is the foundation of differential geometry.

---

### THEOREM 4: Stokes' Theorem (General Form)

- **Formal Statement:** For an oriented smooth manifold M with boundary ∂M and a differential (n-1)-form ω: ∫_M dω = ∫_{∂M} ω.
- **Plain Language:** The integral of a derivative over a region equals the integral of the original form over the boundary. This single theorem unifies the fundamental theorem of calculus, Green's theorem, the divergence theorem, and the classical Stokes' theorem.
- **Historical Context:** Green (1828), Gauss, Ostrogradsky (1830s), Stokes (1854), Cartan (1945, general form using differential forms).
- **Depends On:** Differential forms, smooth manifolds, exterior derivative.
- **Implications:** The generalized Stokes' theorem is the deepest theorem in vector calculus and differential geometry. It connects: local differential information (derivatives) to global integral information (boundary values). It is the mathematical foundation for conservation laws in physics, de Rham cohomology, and gauge theory.

---

### PRINCIPLE 9: Banach and Hilbert Spaces (Functional Analysis)

- **Formal Statement:** A Banach space is a complete normed vector space. A Hilbert space is a complete inner product space. Key results: Hahn-Banach theorem (extension of linear functionals), Open Mapping Theorem (surjective bounded operators are open), Closed Graph Theorem, Riesz Representation Theorem (continuous linear functionals on Hilbert space are inner products).
- **Plain Language:** Functional analysis extends linear algebra and analysis to infinite-dimensional spaces — spaces of functions, sequences, and operators. Banach and Hilbert spaces are the "well-behaved" infinite-dimensional spaces.
- **Historical Context:** Banach (1920s-1930s), Hilbert (1900s), Riesz, von Neumann. Functional analysis became essential for quantum mechanics (Hilbert space of states) and PDE theory.
- **Depends On:** Completeness, vector space axioms, inner product.
- **Implications:** Hilbert spaces are the state spaces of quantum mechanics. Banach spaces are the natural setting for PDE theory, optimization, and numerical analysis. The spectral theorem for self-adjoint operators on Hilbert space is the mathematical backbone of quantum observable theory.

---

### THEOREM 5: Taylor's Theorem and Power Series

- **Formal Statement:** If f is n+1 times differentiable at a, then f(x) = Σ_{k=0}^{n} f^(k)(a)(x-a)^k/k! + R_n(x), where the remainder R_n satisfies |R_n(x)| ≤ M|x-a|^{n+1}/(n+1)! (Lagrange form). For analytic functions, the series converges to f.
- **Plain Language:** Any sufficiently smooth function can be approximated by a polynomial. The more terms you include, the better the approximation near the point of expansion.
- **Historical Context:** Taylor (1715), Lagrange (1797, remainder term). Extended to complex analysis by Cauchy and Weierstrass.
- **Depends On:** Differentiability, completeness of ℝ.
- **Implications:** Taylor series are the foundation of: numerical methods (truncated series), perturbation theory in physics, linearization in engineering, and complex analysis (where analyticity is equivalent to having a convergent power series).

---

---

### THEOREM 6: Hahn-Banach Theorem

**Formal Statement:**
Let V be a real (or complex) vector space, p: V → ℝ a sublinear functional, W ⊆ V a subspace, and f: W → ℝ a linear functional with f(w) ≤ p(w) for all w ∈ W. Then f can be extended to a linear functional F: V → ℝ with F(v) ≤ p(v) for all v ∈ V. In the normed space version: any bounded linear functional on a subspace can be extended to the whole space with the same norm.

**Plain Language:**
You can always extend a bounded linear measurement from a part of a space to the entire space without increasing its size. This guarantees a rich supply of linear functionals on any normed space.

**Historical Context:**
Hahn (1927) and Banach (1929), independently. One of the three pillars of functional analysis (along with the open mapping theorem and the uniform boundedness principle). The proof uses Zorn's lemma (Axiom of Choice).

**Depends On:**
- Vector space axioms, sublinear functionals
- Axiom of Choice (Zorn's Lemma)

**Implications:**
- Guarantees the existence of enough continuous linear functionals to separate points in normed spaces
- Foundation of duality theory in functional analysis
- Essential for optimization theory, the existence of supporting hyperplanes, and the theory of distributions

---

### THEOREM 7: Open Mapping Theorem (Banach-Schauder)

**Formal Statement:**
If X and Y are Banach spaces and T: X → Y is a surjective bounded linear operator, then T is an open map (i.e., T maps open sets to open sets). Consequently, if T is also injective, then T⁻¹ is automatically bounded (continuous).

**Plain Language:**
A surjective bounded linear map between complete spaces automatically maps open sets to open sets. Bijectivity plus continuity gives you continuity of the inverse for free.

**Historical Context:**
Banach (1929), Schauder (1930). Proved using the Baire category theorem. One of the cornerstones of functional analysis.

**Depends On:**
- Banach spaces (completeness)
- Baire category theorem

**Implications:**
- The bounded inverse theorem (corollary): every bijective bounded linear operator between Banach spaces has a bounded inverse
- The closed graph theorem follows as a consequence
- Essential for PDE theory, operator theory, and establishing equivalence of norms

---

### THEOREM 8: Closed Graph Theorem

**Formal Statement:**
If X and Y are Banach spaces and T: X → Y is a linear operator, then T is bounded (continuous) if and only if its graph {(x, Tx) : x ∈ X} is closed in X × Y.

**Plain Language:**
For a linear operator between complete spaces, you can verify continuity by checking a seemingly weaker condition: that the graph is a closed set. This is often much easier to verify in practice.

**Historical Context:**
Banach (1932). Follows from the open mapping theorem. A standard tool for proving operators are bounded without direct norm estimates.

**Depends On:**
- Banach spaces (completeness)
- Open mapping theorem

**Implications:**
- Provides an indirect method for proving continuity of linear operators
- Heavily used in PDE theory and operator theory
- The closed graph theorem for Frechet spaces and other generalizations are important in distribution theory

---

### THEOREM 9: Riesz Representation Theorem

**Formal Statement:**
(Hilbert space version) For every continuous linear functional f on a Hilbert space H, there exists a unique element y ∈ H such that f(x) = ⟨x, y⟩ for all x ∈ H, and ||f|| = ||y||. (Measure version) Every positive linear functional on C_c(X) (continuous functions with compact support on a locally compact Hausdorff space) corresponds to integration against a unique regular Borel measure.

**Plain Language:**
In a Hilbert space, every continuous linear measurement is secretly an inner product with some fixed element. This establishes a perfect duality between the space and its dual.

**Historical Context:**
Frigyes Riesz (1907, for L², 1909 for general Hilbert spaces). The measure-theoretic version is due to Riesz (1909) and Markov (1938), refined by Kakutani (1941).

**Depends On:**
- Hilbert space structure (inner product, completeness)
- For the measure version: topology, measure theory

**Implications:**
- Establishes the canonical isomorphism H ≅ H* for Hilbert spaces (self-duality)
- Foundation of the spectral theory of operators in quantum mechanics
- The measure-theoretic version connects functional analysis to measure theory, essential for probability and integration

---

### THEOREM 10: Stone-Weierstrass Theorem

**Formal Statement:**
Let X be a compact Hausdorff space and A ⊆ C(X, ℝ) a subalgebra that separates points and contains the constant functions. Then A is dense in C(X, ℝ) with the uniform norm. The classical Weierstrass approximation theorem (polynomials are dense in C[a,b]) is a special case.

**Plain Language:**
On a compact space, any "sufficiently rich" collection of continuous functions can approximate any continuous function as closely as desired. In particular, any continuous function on a closed interval can be uniformly approximated by polynomials.

**Historical Context:**
Weierstrass (1885, polynomial approximation). Stone (1937, 1948) generalized to arbitrary compact spaces and subalgebras. A landmark in the transition from classical to abstract analysis.

**Depends On:**
- Compactness, continuity
- Algebra structure on function spaces

**Implications:**
- Justifies the use of polynomial and trigonometric approximations throughout applied mathematics
- Foundation for approximation theory, numerical analysis, and spectral methods
- The complex version requires that A be closed under conjugation

---

### THEOREM 11: Spectral Theorem for Self-Adjoint Operators

**Formal Statement:**
Every bounded self-adjoint operator A on a Hilbert space H admits a spectral decomposition: A = integral from sigma(A) of lambda dE(lambda), where {E(lambda)} is a projection-valued measure (spectral measure) on the spectrum sigma(A). For compact self-adjoint operators, this reduces to A = sum of lambda_n <-, e_n> e_n with eigenvalues lambda_n -> 0 and orthonormal eigenvectors {e_n}. For finite dimensions, this is the diagonalization of symmetric matrices.

**Plain Language:**
Every self-adjoint operator can be "diagonalized" using a spectral measure. In finite dimensions, this is the familiar fact that symmetric matrices have real eigenvalues and orthogonal eigenvectors. In infinite dimensions, the spectrum may be continuous, requiring integration rather than summation, but the principle is the same.

**Historical Context:**
Hilbert (1906, for integral operators), von Neumann (1929, general spectral theorem for unbounded operators), Riesz (1930s). The spectral theorem is the mathematical foundation of quantum mechanics, where observables are self-adjoint operators and measurement outcomes are spectral values.

**Depends On:**
- Hilbert spaces, self-adjoint operators
- Measure theory (projection-valued measures)

**Implications:**
- Mathematical foundation of quantum mechanics: physical observables correspond to self-adjoint operators, and their spectra are possible measurement outcomes
- Enables the functional calculus: f(A) is defined via f(A) = integral f(lambda) dE(lambda) for any Borel function f
- Central to PDE theory (spectral methods for solving differential equations) and signal processing (spectral analysis)

---

### THEOREM 12: Fubini's Theorem

**Formal Statement:**
Let (X, mu) and (Y, nu) be sigma-finite measure spaces and f: X x Y -> R be measurable. If integral of |f| d(mu x nu) < infinity (or if f >= 0), then the double integral equals the iterated integrals: integral integral f d(mu x nu) = integral_X (integral_Y f(x,y) dnu(y)) dmu(x) = integral_Y (integral_X f(x,y) dmu(x)) dnu(y).

**Plain Language:**
When integrating a function of two variables, you can compute the double integral by integrating one variable at a time, in either order. The order does not matter, provided the function is sufficiently well-behaved (absolutely integrable).

**Historical Context:**
Guido Fubini (1907). Tonelli (1909) proved the version for non-negative functions (Tonelli's theorem) that does not require integrability as a hypothesis. These theorems are workhorses of analysis, probability, and physics.

**Depends On:**
- Lebesgue measure and integration (Principle 8)
- Product sigma-algebras, sigma-finiteness

**Implications:**
- Essential computational tool: reduces multidimensional integrals to iterated one-dimensional integrals
- Foundation for computing expectations of products, convolutions, and joint distributions in probability
- Used constantly in PDE theory, Fourier analysis, and physics (computing multidimensional integrals)

---

### THEOREM 13: Dominated Convergence Theorem

**Formal Statement:**
If {f_n} is a sequence of measurable functions converging pointwise to f, and there exists an integrable function g such that |f_n(x)| <= g(x) for all n and a.e. x, then f is integrable and lim integral f_n dmu = integral lim f_n dmu = integral f dmu. That is, the limit and the integral can be interchanged.

**Plain Language:**
If a sequence of functions converges pointwise and is uniformly bounded by an integrable function, then the limit of the integrals equals the integral of the limit. You can safely interchange limit and integration.

**Historical Context:**
Henri Lebesgue (1910). The dominated convergence theorem is arguably the most important single theorem in Lebesgue integration theory. It subsumes the monotone convergence theorem and Fatou's lemma as special cases and is the primary tool for passing limits through integrals.

**Depends On:**
- Lebesgue measure and integration (Principle 8)
- Fatou's lemma

**Implications:**
- The primary justification for interchanging limits and integrals throughout analysis
- Essential in probability theory (convergence of expectations), PDE theory, and Fourier analysis
- Enables differentiation under the integral sign (Leibniz rule) under appropriate conditions
- Foundation for proving continuity and differentiability of parameter-dependent integrals

---

### THEOREM 14: Arzela-Ascoli Theorem

**Formal Statement:**
A subset F of C(K, R) (continuous functions on a compact metric space K) is relatively compact in the uniform topology if and only if F is uniformly bounded (sup_{f in F} sup_{x in K} |f(x)| < infinity) and equicontinuous (for every epsilon > 0, there exists delta > 0 such that d(x,y) < delta implies |f(x) - f(y)| < epsilon for all f in F).

**Plain Language:**
A family of continuous functions on a compact space has a uniformly convergent subsequence if and only if the functions are uniformly bounded and "equally continuous" (equicontinuous). This is the function-space analogue of the Bolzano-Weierstrass theorem.

**Historical Context:**
Ascoli (1883-84) and Arzela (1895). The theorem characterizes compactness in function spaces and is one of the most important compactness results in analysis, alongside the Heine-Borel and Bolzano-Weierstrass theorems.

**Depends On:**
- Compactness (Principle 6), metric spaces (Principle 7)
- Uniform convergence, equicontinuity

**Implications:**
- Essential for proving existence of solutions to ODEs and PDEs (extracting convergent subsequences from approximate solutions)
- Used in the Peano existence theorem for ODEs (which, unlike Picard-Lindelof, does not require Lipschitz conditions)
- Foundation for the calculus of variations (direct method for proving existence of minimizers)
- Key tool in functional analysis and approximation theory

---

### THEOREM 15: Uniform Boundedness Principle (Banach-Steinhaus)

**Formal Statement:**
If {T_alpha} is a family of bounded linear operators from a Banach space X to a normed space Y such that sup_alpha ||T_alpha(x)|| < infinity for each x in X, then sup_alpha ||T_alpha|| < infinity. That is, pointwise boundedness of a family of operators implies uniform boundedness.

**Plain Language:**
If a family of linear operators is bounded at every individual point, then there is a single bound that works for all points and all operators simultaneously. Pointwise control automatically gives uniform control in the Banach space setting.

**Historical Context:**
Banach and Steinhaus (1927). One of the three pillars of functional analysis (along with the Hahn-Banach theorem and the open mapping theorem). The proof uses the Baire category theorem.

**Depends On:**
- Banach spaces (completeness)
- Baire category theorem

**Implications:**
- Proves the Principle of Condensation of Singularities: if bounded operators fail to converge, they must fail on a "large" (residual) set
- Used to prove that Fourier series of continuous functions can diverge (du Bois-Reymond, 1876)
- Essential in the theory of distributions and for proving convergence results in approximation theory
- One of the fundamental tools for studying families of operators in functional analysis

---

---

### THEOREM 16: The Sobolev Embedding Theorem

**Formal Statement:**
Let Omega be a bounded open subset of R^n with Lipschitz boundary. If u is in the Sobolev space W^{k,p}(Omega), then: (1) If kp < n, then W^{k,p} embeds continuously into L^{q} for q = np/(n - kp) (Sobolev conjugate exponent). (2) If kp = n, then W^{k,p} embeds into L^q for all q in [p, infinity) (Trudinger inequality gives exponential integrability). (3) If kp > n, then W^{k,p} embeds into C^{0,alpha} (Holder continuous functions) with alpha = k - n/p when this is not an integer.

**Plain Language:**
The Sobolev embedding theorem tells you that if a function has enough weak derivatives in L^p, it is automatically smoother than you might expect. Having k derivatives in L^p, when kp is large enough relative to the dimension, forces the function to be continuous or even Holder continuous. This is the fundamental regularity result in PDE theory.

**Historical Context:**
Sergei Sobolev (1938). The Sobolev spaces W^{k,p} were introduced to provide the natural function spaces for weak solutions of PDEs. The embedding theorems were refined by Morrey, Nirenberg, and Gagliardo. The Rellich-Kondrachov theorem provides the crucial compact embedding version.

**Depends On:**
- Lebesgue integration (Principle 8)
- Banach spaces (Principle 9)
- Distribution theory (Schwartz)

**Implications:**
- The fundamental tool for proving regularity of weak solutions to PDEs: solutions in Sobolev spaces are automatically classical solutions when kp > n
- The Rellich-Kondrachov compact embedding theorem is essential for proving existence of minimizers in the calculus of variations (direct method)
- Governs the critical exponents for nonlinear PDEs and determines which nonlinearities are subcritical, critical, or supercritical
- Foundation of modern PDE theory, finite element error analysis, and the theory of elliptic regularity

---

### THEOREM 17: The Lax-Milgram Theorem

**Formal Statement:**
Let H be a real Hilbert space and B: H x H -> R a bilinear form that is (1) continuous (|B(u,v)| <= M ||u|| ||v||) and (2) coercive (B(u,u) >= alpha ||u||^2 for some alpha > 0). Then for every continuous linear functional F in H*, there exists a unique u in H such that B(u,v) = F(v) for all v in H, and ||u|| <= (1/alpha)||F||.

**Plain Language:**
The Lax-Milgram theorem guarantees that a large class of variational problems have unique solutions. If you have a bilinear form that is bounded and "strongly positive" (coercive), then the associated equation always has exactly one solution. This is the abstract foundation for proving existence and uniqueness of solutions to elliptic PDEs.

**Historical Context:**
Peter Lax and Arthur Milgram (1954). The theorem generalizes the Riesz representation theorem from symmetric to non-symmetric bilinear forms and is the workhorse existence theorem for elliptic boundary value problems.

**Depends On:**
- Hilbert spaces (Principle 9)
- Riesz representation theorem (Theorem 9)

**Implications:**
- Proves existence and uniqueness for the weak formulation of elliptic PDEs (Laplace, Poisson, elasticity equations)
- The theoretical foundation of the finite element method: Cea's lemma gives error estimates directly from Lax-Milgram
- Generalized to the Babuska-Lax-Milgram theorem (inf-sup condition) for non-coercive problems, essential for mixed finite elements and Stokes equations
- Connects abstract functional analysis to concrete PDE solvability

---

### PRINCIPLE 10: Distribution Theory (Schwartz)

**Formal Statement:**
A distribution (generalized function) is a continuous linear functional on the space of test functions D(Omega) = C_c^infinity(Omega) equipped with a specific topology. Every locally integrable function f defines a distribution T_f via T_f(phi) = integral f phi dx, but distributions also include objects like the Dirac delta: delta(phi) = phi(0). Distributions can always be differentiated: (DT)(phi) = -T(Dphi), making every distribution infinitely differentiable in the distributional sense.

**Plain Language:**
Distribution theory extends calculus to "functions" that are too singular to be ordinary functions, like the Dirac delta "function" (zero everywhere except at one point, yet integrating to 1). In distribution theory, every generalized function can be differentiated as many times as you like, and operations like Fourier transforms apply universally. This provides the rigorous framework for the impulses, point sources, and singularities that pervade physics and engineering.

**Historical Context:**
Laurent Schwartz (1945-1950, *Theorie des distributions*, Fields Medal 1950). The theory systematized earlier ad hoc use of the delta function (Dirac, Heaviside) and provided the rigorous foundation for Fourier analysis on tempered distributions, fundamental solutions of PDEs, and quantum field theory.

**Depends On:**
- Functional analysis (Principle 9)
- Topological vector spaces
- Lebesgue integration (Principle 8)

**Implications:**
- Provides rigorous meaning to the Dirac delta, Heaviside step function, and their derivatives
- Every linear PDE with constant coefficients has a fundamental solution (Malgrange-Ehrenpreis theorem)
- The Fourier transform extends to tempered distributions, enabling the Fourier-analytic treatment of all L^p functions and beyond
- Foundation of the modern theory of PDEs (Hormander's theory of linear partial differential operators)

---

## Summary Table

| # | Name | Type | Core Statement | Dependencies |
|---|------|------|----------------|--------------|
| A1 | Complete Ordered Field (ℝ) | AXIOM SYSTEM | ℝ is the unique complete ordered field | Field axioms, order |
| P1 | ε-δ Definition of Limit | PRINCIPLE | Limit = quantified closeness | ℝ, absolute value |
| P2 | Continuity | PRINCIPLE | Small input → small output | Limits |
| P3 | Derivative | PRINCIPLE | Instantaneous rate of change | Limits |
| P4 | Riemann Integral | PRINCIPLE | Area as limit of sums | Limits, completeness |
| T1 | Fundamental Theorem of Calculus | THEOREM | Integration ↔ differentiation | Continuity, integral, derivative |
| P5 | Convergence | PRINCIPLE | Terms approach a limit | Completeness |
| P6 | Compactness | PRINCIPLE | Closed + bounded ↔ compact (in ℝⁿ) | Completeness, BW theorem |
| P7 | Metric Space Axioms | AXIOM SYSTEM | Distance satisfying 3 properties | Set theory |
| P8 | Measure Theory | AXIOM SYSTEM | Countably additive set function | σ-algebras, ℝ |
| T2 | Banach Fixed-Point | THEOREM | Contraction → unique fixed point | Complete metric space |
| T3 | Implicit Function Theorem | THEOREM | F(x,y)=0 locally defines y=g(x) | Differentiability, completeness |
| T4 | Stokes' Theorem (General) | THEOREM | ∫_M dω = ∫_{∂M} ω | Differential forms, manifolds |
| P9 | Banach & Hilbert Spaces | PRINCIPLE | Complete normed/inner product spaces | Vector spaces, completeness |
| T5 | Taylor's Theorem | THEOREM | f ≈ polynomial + remainder | Differentiability |
| T6 | Hahn-Banach Theorem | THEOREM | Bounded functionals extend to whole space | Vector spaces, Zorn's lemma |
| T7 | Open Mapping Theorem | THEOREM | Surjective bounded operator is open | Banach spaces, Baire category |
| T8 | Closed Graph Theorem | THEOREM | Closed graph ↔ bounded operator | Banach spaces |
| T9 | Riesz Representation Theorem | THEOREM | H* ≅ H via inner product | Hilbert spaces |
| T10 | Stone-Weierstrass Theorem | THEOREM | Rich subalgebras are dense in C(X) | Compactness, algebra |
| T11 | Spectral Theorem | THEOREM | Self-adjoint operators diagonalize via spectral measures | Hilbert spaces, measure theory |
| T12 | Fubini's Theorem | THEOREM | Double integral = iterated integrals (either order) | Lebesgue integration, product measures |
| T13 | Dominated Convergence | THEOREM | Pointwise limit under domination commutes with integral | Lebesgue integration, Fatou's lemma |
| T14 | Arzela-Ascoli Theorem | THEOREM | Bounded + equicontinuous ↔ relatively compact | Compactness, equicontinuity |
| T15 | Uniform Boundedness Principle | THEOREM | Pointwise bounded operators are uniformly bounded | Banach spaces, Baire category |
| T16 | Sobolev Embedding Theorem | THEOREM | W^{k,p} embeds into L^q or C^{0,alpha} | Sobolev spaces, Lebesgue integration |
| T17 | Lax-Milgram Theorem | THEOREM | Coercive bilinear form → unique solution | Hilbert spaces, Riesz representation |
| P10 | Distribution Theory (Schwartz) | PRINCIPLE | Generalized functions, universal differentiability | Functional analysis, topological vector spaces |

---

### THEOREM 18: Riesz-Thorin Interpolation Theorem

**Formal Statement:**
Let T be a linear operator that is bounded from L^{p_0} to L^{q_0} with norm M_0 and from L^{p_1} to L^{q_1} with norm M_1 (where 1 <= p_0, p_1, q_0, q_1 <= infinity). Then for any 0 < theta < 1, T is bounded from L^p to L^q with norm M <= M_0^{1-theta} M_1^theta, where 1/p = (1-theta)/p_0 + theta/p_1 and 1/q = (1-theta)/q_0 + theta/q_1. The proof uses the Hadamard three-lines theorem from complex analysis.

**Plain Language:**
If a linear operator works well on two different L^p spaces, it automatically works on all the intermediate spaces in between, with a bound that interpolates smoothly between the two extremes. This is one of the most powerful tools in analysis for proving that operators are bounded: you only need to check the endpoints, and the entire range of intermediate spaces comes for free.

**Historical Context:**
Marcel Riesz (1927), with a full proof by Thorin (1948) using complex interpolation. The Marcinkiewicz interpolation theorem (1939) provides a real-variable analogue that requires only weak-type bounds at the endpoints. Calderon and Zygmund (1952) developed the real interpolation method. Interpolation theory became central to harmonic analysis and PDE theory.

**Depends On:**
- L^p spaces, Lebesgue integration (Principle 8)
- Complex analysis (Hadamard three-lines theorem)

**Implications:**
- Proves boundedness of the Fourier transform on L^p for 1 <= p <= 2 (Hausdorff-Young inequality) by interpolating between L^1 -> L^infinity and L^2 -> L^2
- The Calderon-Zygmund theory of singular integrals relies heavily on interpolation between L^2 and weak-L^1
- Foundation of the entire theory of interpolation spaces (Besov spaces, Triebel-Lizorkin spaces)
- Essential tool throughout harmonic analysis, PDE theory, and probability theory

---

### THEOREM 19: The Baire Category Theorem

**Formal Statement:**
In a complete metric space (or locally compact Hausdorff space), the intersection of countably many dense open sets is dense. Equivalently, a complete metric space cannot be written as a countable union of nowhere-dense sets (it is of "second category" in itself). A set that is a countable intersection of dense open sets is called a G-delta set and is "generic" (residual).

**Plain Language:**
In a complete space, "most" points (in the topological sense) avoid any countable collection of "thin" (nowhere-dense) sets. This means that the "typical" element of a complete space avoids all countable obstructions. The Baire category theorem is the reason that "generic" behavior in analysis is often surprising: for example, the generic continuous function is nowhere differentiable.

**Historical Context:**
Rene Baire (1899, doctoral thesis). The theorem is the foundation of the three pillars of functional analysis: the uniform boundedness principle, the open mapping theorem, and the closed graph theorem all rely on it. Banach (1931) and Mazurkiewicz (1931) used it to show that "most" continuous functions are pathological (nowhere differentiable, nowhere monotone).

**Depends On:**
- Complete metric spaces (Principle 7)
- Topological concepts (open, dense, nowhere-dense)

**Implications:**
- Proves the uniform boundedness principle (Banach-Steinhaus), the open mapping theorem, and the closed graph theorem
- "Most" continuous functions on [0,1] are nowhere differentiable: the set of somewhere-differentiable functions is meager (first category)
- "Most" continuous functions are nowhere monotone, have graphs of Hausdorff dimension 2, etc.
- Foundation of generic analysis: understanding what happens "typically" rather than in special cases

---

### THEOREM 20: Carleson's Theorem (Pointwise Convergence of Fourier Series)

**Formal Statement:**
If f is in L^2([0, 2pi]), then the partial sums S_N f(x) = sum_{|n| <= N} f_hat(n) e^{inx} converge to f(x) for almost every x. More generally, for f in L^p with p > 1, the Fourier series converges pointwise almost everywhere. The maximal Carleson operator C*f(x) = sup_N |S_N f(x)| is bounded on L^p for 1 < p < infinity.

**Plain Language:**
If you decompose a square-integrable function into its Fourier series (sines and cosines), the partial sums of the series actually converge back to the original function at almost every point. This was a famous open problem for over a century: Fourier claimed convergence in 1807, but it took until 1966 to prove it rigorously for L^2 functions.

**Historical Context:**
Lennart Carleson (1966, proof for L^2; Fields Medal 1982). Extended to L^p (p > 1) by Richard Hunt (1968). Kolmogorov (1926) had shown that there exists an L^1 function whose Fourier series diverges everywhere, so L^2 is essentially optimal. Lacey and Thiele (2000) gave a simplified proof using time-frequency analysis.

**Depends On:**
- Fourier analysis, L^p spaces
- Measure theory (Principle 8)
- Hilbert spaces (Principle 9)

**Implications:**
- Resolves the oldest question in Fourier analysis: does the Fourier series of a "reasonable" function converge?
- The techniques (time-frequency analysis, tile decomposition) revolutionized harmonic analysis
- Led to the development of the theory of multilinear operators and the bilinear Hilbert transform
- Kolmogorov's counterexample shows the result fails for L^1, establishing L^2 as the critical threshold

---

### PRINCIPLE 11: Ultraproducts and Nonstandard Analysis

**Formal Statement:**
Given a family of structures (A_i)_{i in I} and an ultrafilter U on I, the ultraproduct prod A_i / U is the quotient of the product by the equivalence relation: (a_i) ~ (b_i) iff {i : a_i = b_i} in U. Los's theorem: a first-order sentence phi holds in the ultraproduct iff {i : A_i |= phi} in U. Taking the ultrapower *R of the reals R over a non-principal ultrafilter yields the hyperreals, containing infinitesimals (positive elements smaller than every 1/n) and infinite numbers. Robinson's transfer principle: a first-order statement holds in R iff it holds in *R.

**Plain Language:**
Nonstandard analysis provides a rigorous framework for infinitesimals -- infinitely small quantities that Leibniz and Euler used freely but that were banished by the epsilon-delta revolution. Using ultrafilters, one constructs an extension of the real numbers containing both infinitely small and infinitely large numbers, in which calculus can be done with infinitesimals instead of limits. Every standard theorem remains true in this extended system.

**Historical Context:**
Abraham Robinson (1961, *Non-standard Analysis*). The ultraproduct construction was developed by Jerzy Los (1955). Robinson showed that Leibniz's intuition about infinitesimals could be made completely rigorous. Edward Nelson (1977, Internal Set Theory) gave an axiomatic approach. Nonstandard methods have yielded new results in combinatorics, measure theory, and mathematical economics.

**Depends On:**
- Model theory, ultrafilters
- Real analysis (Axiom System 1)
- First-order logic

**Implications:**
- Provides an alternative foundation for analysis using infinitesimals, often yielding shorter and more intuitive proofs
- Los's theorem is a powerful tool in model theory for constructing models with prescribed properties
- Nonstandard methods proved Ramsey-theoretic results in combinatorics (e.g., Ren Jin's proof of Szemeredi regularity lemma applications)
- The Loeb measure construction connects nonstandard probability to standard measure theory

---

### PRINCIPLE 12: Optimal Transport and the Wasserstein Distance

**Formal Statement:**
The Monge-Kantorovich optimal transport problem: given probability measures mu on X and nu on Y, and a cost function c: X x Y -> R, find a transport plan gamma (a joint measure on X x Y with marginals mu and nu) minimizing the total cost integral c(x,y) d gamma(x,y). The Kantorovich relaxation admits a dual formulation: W_c(mu, nu) = sup {integral phi d mu + integral psi d nu : phi(x) + psi(y) <= c(x,y)}. When c(x,y) = d(x,y)^p on a metric space, this defines the p-Wasserstein distance: W_p(mu, nu) = (inf_gamma integral d(x,y)^p d gamma)^{1/p}. The Brenier theorem (1991): when X = Y = R^n, c = |x-y|^2, mu is absolutely continuous, the optimal transport map T = nabla phi is the gradient of a convex function phi (the Brenier potential).

**Plain Language:**
Optimal transport theory solves the problem of moving one distribution of mass to another at minimum cost. The Wasserstein distance measures how "far apart" two probability distributions are by computing the cheapest way to reshape one into the other. Unlike other distances between distributions (KL divergence, total variation), the Wasserstein distance respects the geometry of the underlying space and is well-behaved even for distributions with non-overlapping supports.

**Historical Context:**
Gaspard Monge (1781, original formulation for earth-moving). Leonid Kantorovich (1942, relaxation and duality; Nobel Prize in Economics 1975). Yann Brenier (1991, polar factorization and optimal maps). Cedric Villani (*Optimal Transport: Old and New*, 2009; Fields Medal 2010). The field has experienced explosive growth due to applications in machine learning (Wasserstein GANs, Arjovsky et al. 2017), statistics, and PDE theory.

**Depends On:**
- Measure theory, Lebesgue integration (Principle 8)
- Functional analysis (Principle 9)
- Convex analysis, duality theory

**Implications:**
- The Wasserstein distance metrizes weak convergence of probability measures on compact spaces and has become the standard metric in machine learning for comparing distributions
- Wasserstein GANs (Arjovsky et al. 2017) use optimal transport to stabilize generative adversarial network training
- Otto's calculus (2001): the Wasserstein space has a formal Riemannian structure, and many PDEs (heat equation, porous medium equation, Fokker-Planck) are gradient flows in Wasserstein space
- Applications in economics (matching theory), image processing (registration), and computational biology (cell trajectory inference)

---

### THEOREM 22: The Regularity Structures Framework (Hairer)

**Formal Statement:**
A regularity structure is a triple (A, T, G) where A is a discrete subset of R (the set of homogeneities), T = bigoplus_{alpha in A} T_alpha is a graded vector space (the model space), and G is a group of linear maps on T satisfying specific algebraic and analytical conditions. A model (Pi, Gamma) assigns to each point x a linear map Pi_x: T -> distributions and a re-expansion map Gamma_{xy}: T -> T. The reconstruction theorem: given a modelled distribution f, there exists a unique distribution Rf whose local behavior at each point x is described by Pi_x f(x). Renormalization is encoded algebraically in the structure group G, and the BPHZ renormalization procedure extends to this setting.

**Plain Language:**
Regularity structures provide a way to make mathematical sense of equations involving products of extremely rough (distributional) objects -- operations that are classically meaningless. The theory creates a "dictionary" that translates rough objects into a structured algebraic language where computations can be performed, then translates results back. This resolved a fundamental barrier in stochastic PDE theory: equations like the KPZ equation for random surface growth were previously beyond rigorous treatment.

**Historical Context:**
Martin Hairer (2014, *A Theory of Regularity Structures*; Fields Medal 2014). Developed to solve the KPZ equation and other singular stochastic PDEs. Simultaneously, Gubinelli, Imkeller, and Perkowski (2015) developed paracontrolled distributions. Bruned, Hairer, and Zambotti (2019) connected regularity structures to renormalization via Hopf algebras.

**Depends On:**
- Distribution theory (Principle 10)
- Functional analysis (Principle 9)
- Sobolev embedding (Theorem 16)

**Implications:**
- Solved the KPZ equation rigorously for the first time, establishing the mathematical foundation for random interface growth
- Provides systematic renormalization for singular SPDEs, connecting PDE theory to quantum field theory
- The algebraic structure (Hopf algebra of decorated trees) mirrors the Connes-Kreimer Hopf algebra of Feynman diagrams
- Opened the field of "singular SPDEs" with applications in statistical mechanics and mathematical physics

---

### THEOREM 23: Random Matrix Universality (Wigner-Dyson-Mehta)

**Formal Statement:**
Let H be an N x N Wigner matrix (symmetric/Hermitian with independent entries, mean 0, variance 1/N). The empirical spectral measure (1/N) sum delta_{lambda_i} converges to the Wigner semicircle distribution with density rho(x) = (2/pi) sqrt(1-x^2) on [-1,1]. Universality: the local eigenvalue statistics (spacing distribution, correlation functions) in the bulk are independent of the entry distribution and match the Gaussian ensembles (GOE, GUE, GSE). The k-point correlation function converges to det[K_sin(x_i - x_j)] for the GUE, where K_sin is the sine kernel. The Tracy-Widom distribution describes fluctuations of the largest eigenvalue.

**Plain Language:**
Random matrix universality is the discovery that the statistical behavior of eigenvalues of large random matrices is universal -- it depends only on the symmetry type and not on the specific distribution of entries. This universality is analogous to the Central Limit Theorem but for eigenvalues. The same statistical patterns appear in nuclear physics energy levels, zeros of the Riemann zeta function, bus arrival times, and growth processes.

**Historical Context:**
Eugene Wigner (1955, semicircle law). Freeman Dyson (1962, symmetry class classification). Tracy and Widom (1994, largest eigenvalue distribution). Erdos, Schlein, Yau (2009-2012) and Tao and Vu (2010-2012) proved universality for general Wigner matrices, a landmark in modern probability.

**Depends On:**
- Spectral theory, linear algebra
- Probability theory, convergence theorems
- Functional analysis (Principle 9)

**Implications:**
- Explains the Montgomery-Odlyzko observation that zeros of the Riemann zeta function follow GUE statistics, suggesting deep connections between number theory and random matrix theory
- The Tracy-Widom distribution appears universally in combinatorics (longest increasing subsequence), KPZ universality class, and statistics (PCA)
- Applications in wireless communications (MIMO channel capacity), machine learning (spectral methods), and quantitative finance
- One of the most striking examples of emergent mathematical structure: microscopic details wash out to reveal universal macroscopic behavior

---

## Summary Table

| # | Name | Type | Core Statement | Dependencies |
|---|------|------|----------------|--------------|
| A1 | Complete Ordered Field (R) | AXIOM SYSTEM | R is the unique complete ordered field | Field axioms, order |
| P1 | epsilon-delta Definition of Limit | PRINCIPLE | Limit = quantified closeness | R, absolute value |
| P2 | Continuity | PRINCIPLE | Small input -> small output | Limits |
| P3 | Derivative | PRINCIPLE | Instantaneous rate of change | Limits |
| P4 | Riemann Integral | PRINCIPLE | Area as limit of sums | Limits, completeness |
| T1 | Fundamental Theorem of Calculus | THEOREM | Integration <-> differentiation | Continuity, integral, derivative |
| P5 | Convergence | PRINCIPLE | Terms approach a limit | Completeness |
| P6 | Compactness | PRINCIPLE | Closed + bounded <-> compact (in R^n) | Completeness, BW theorem |
| P7 | Metric Space Axioms | AXIOM SYSTEM | Distance satisfying 3 properties | Set theory |
| P8 | Measure Theory | AXIOM SYSTEM | Countably additive set function | sigma-algebras, R |
| T2 | Banach Fixed-Point | THEOREM | Contraction -> unique fixed point | Complete metric space |
| T3 | Implicit Function Theorem | THEOREM | F(x,y)=0 locally defines y=g(x) | Differentiability, completeness |
| T4 | Stokes' Theorem (General) | THEOREM | integral_M d-omega = integral_{dM} omega | Differential forms, manifolds |
| P9 | Banach and Hilbert Spaces | PRINCIPLE | Complete normed/inner product spaces | Vector spaces, completeness |
| T5 | Taylor's Theorem | THEOREM | f approx polynomial + remainder | Differentiability |
| T6 | Hahn-Banach Theorem | THEOREM | Bounded functionals extend to whole space | Vector spaces, Zorn's lemma |
| T7 | Open Mapping Theorem | THEOREM | Surjective bounded operator is open | Banach spaces, Baire category |
| T8 | Closed Graph Theorem | THEOREM | Closed graph <-> bounded operator | Banach spaces |
| T9 | Riesz Representation Theorem | THEOREM | H* isomorphic to H via inner product | Hilbert spaces |
| T10 | Stone-Weierstrass Theorem | THEOREM | Rich subalgebras are dense in C(X) | Compactness, algebra |
| T11 | Spectral Theorem | THEOREM | Self-adjoint operators diagonalize via spectral measures | Hilbert spaces, measure theory |
| T12 | Fubini's Theorem | THEOREM | Double integral = iterated integrals | Lebesgue integration, product measures |
| T13 | Dominated Convergence | THEOREM | Pointwise limit under domination commutes with integral | Lebesgue integration, Fatou's lemma |
| T14 | Arzela-Ascoli Theorem | THEOREM | Bounded + equicontinuous <-> relatively compact | Compactness, equicontinuity |
| T15 | Uniform Boundedness Principle | THEOREM | Pointwise bounded operators are uniformly bounded | Banach spaces, Baire category |
| T16 | Sobolev Embedding Theorem | THEOREM | W^{k,p} embeds into L^q or C^{0,alpha} | Sobolev spaces, Lebesgue integration |
| T17 | Lax-Milgram Theorem | THEOREM | Coercive bilinear form -> unique solution | Hilbert spaces, Riesz representation |
| P10 | Distribution Theory (Schwartz) | PRINCIPLE | Generalized functions, universal differentiability | Functional analysis, topological vector spaces |
| T18 | Riesz-Thorin Interpolation | THEOREM | Bounded on endpoints -> bounded on intermediate L^p | L^p spaces, complex analysis |
| T19 | Baire Category Theorem | THEOREM | Complete space is not countable union of nowhere-dense sets | Complete metric spaces |
| T20 | Carleson's Theorem | THEOREM | L^2 Fourier series converge a.e. | Fourier analysis, measure theory |
| P11 | Ultraproducts and Nonstandard Analysis | PRINCIPLE | Rigorous infinitesimals via ultrafilters | Model theory, real analysis |
| T21 | Stochastic Homogenization | THEOREM | Random media → deterministic effective PDE | Ergodic theory, Sobolev spaces, PDE theory |
| P12 | Mean-Field Game Theory (Lasry-Lions) | PRINCIPLE | Continuum limit of N-player differential games | Optimal control, Fokker-Planck, Nash equilibrium |
| P13 | Regularity Structures (Hairer) | PRINCIPLE | Renormalization framework for singular SPDEs | Rough path theory, distribution theory, renormalization |
| T22 | Kakeya Conjecture Progress (Katz-Zahl-Wang) | THEOREM | Kakeya sets in R^n have full Hausdorff dimension (partial results) | Geometric measure theory, combinatorics, harmonic analysis |
| P14 | Szemerédi Regularity Lemma | PRINCIPLE | Every large graph approximated by bounded-complexity pseudorandom structure | Graph theory, combinatorics, analytic methods |
| T23 | Derived Categories in Mirror Symmetry | THEOREM | Equivalence of derived Fukaya and coherent sheaf categories | Homological algebra, symplectic geometry, algebraic geometry |
| P15 | Reproducing Kernel Hilbert Spaces (RKHS) | PRINCIPLE | Kernel trick lifts data to infinite-dimensional feature spaces; representer theorem | Hilbert spaces, functional analysis, ML |
| T24 | Schramm-Loewner Evolution (SLE) | THEOREM | Conformally invariant random curves classified by single parameter kappa | Complex analysis, probability, conformal invariance |

---

### THEOREM T21 — Stochastic Homogenization

**Formal Statement:**
Consider the elliptic PDE -div(a(x/epsilon, omega) grad u_epsilon) = f on a bounded domain D, where a(y, omega) is a stationary ergodic random field satisfying uniform ellipticity: lambda|xi|^2 <= a(y,omega)xi·xi <= Lambda|xi|^2. The homogenization theorem (Papanicolaou-Varadhan 1979, Kozlov 1979) states that as epsilon → 0, the solutions u_epsilon converge almost surely in H^1(D) to the solution u_0 of the homogenized equation -div(a_hom grad u_0) = f, where a_hom is a deterministic constant matrix determined by the statistics of a. The corrector equation: for each unit vector e_i, find chi_i(y,omega) stationary with ∇chi_i stationary and mean zero, satisfying -div(a(y,omega)(e_i + ∇chi_i)) = 0 in R^d. Then (a_hom)_{ij} = E[a(0,·)(e_j + ∇chi_j)·e_i]. Quantitative estimates (Gloria-Neukamm-Otto 2014-2020): |a_hom - a_hom^L| ≤ C(d,lambda,Lambda) L^{-d/2} where a_hom^L is computed on a box of side L, with optimal stochastic integrability.

**Plain Language:**
When a material has random microscopic structure (like a composite with randomly placed inclusions), the large-scale behavior is governed by a deterministic effective equation that averages out the randomness. Stochastic homogenization provides the mathematical theory for computing this effective behavior and quantifying how fast the random fluctuations average out. It explains why macroscopic physics is predictable even when microscopic details are random.

**Historical Context:**
George Papanicolaou and S.R.S. Varadhan (1979), S.M. Kozlov (1979) established the qualitative theory. Quantitative stochastic homogenization was developed by Antoine Gloria, Stefan Neukamm, and Felix Otto (2014-2020) using spectral gap estimates and sensitivity calculus. Scott Armstrong, Tuomo Kuusi, and Jean-Christophe Mourrat (2019, monograph) developed an alternative approach using variational methods and the additive structure of the corrector.

**Depends On:**
- Sobolev spaces and PDE theory (Theorem T16, T17)
- Ergodic theory (Birkhoff's theorem, from Probability)
- Measure theory (Axiom System P8)

**Implications:**
- Provides rigorous justification for effective medium theories used throughout materials science and engineering
- Quantitative estimates enable error bounds for computational multiscale methods
- The corrector theory connects to fluctuation results: CLT for the homogenization error (Gu-Mourrat 2016)
- Extends to nonlinear settings (stochastic Hamilton-Jacobi, random polymers) connecting to KPZ universality

---

### PRINCIPLE P12 — Mean-Field Game Theory (Lasry-Lions)

**Formal Statement:**
A mean-field game (MFG) describes the continuum limit of a symmetric N-player stochastic differential game as N → ∞. Each representative agent controls their state X_t via drift alpha_t, minimizing J(alpha) = E[∫_0^T L(X_t, alpha_t, m_t) dt + G(X_T, m_T)], where m_t is the population distribution. The MFG system couples a backward Hamilton-Jacobi-Bellman equation for the value function u with a forward Fokker-Planck equation for the density m: (1) -∂_t u - nu Δu + H(x, ∇u) = F(x, m_t), u(T,x) = G(x, m_T); (2) ∂_t m - nu Δm - div(m D_p H(x, ∇u)) = 0, m(0,x) = m_0(x). Under Lasry-Lions monotonicity conditions (F and G are monotone increasing in m in a suitable sense), this system has a unique solution, and the MFG solution provides an epsilon-Nash equilibrium for the N-player game with epsilon → 0 as N → ∞.

**Plain Language:**
Mean-field game theory describes what happens when a very large number of rational agents each make optimal decisions while being influenced by the collective behavior of everyone else. Instead of tracking each individual, the theory describes the crowd as a continuous density and derives coupled equations: one for the optimal strategy and one for how the crowd evolves. This provides a tractable framework for modeling phenomena from traffic flow to financial markets where millions of interacting decision-makers create emergent collective behavior.

**Historical Context:**
Jean-Michel Lasry and Pierre-Louis Lions (2006-2007, founding papers), independently Minyi Huang, Roland Malhame, and Peter Caines (2006, Nash certainty equivalence). Lions' lectures at College de France (2007-2012) developed the systematic theory. Pierre Cardaliaguet, Francois Delarue, Jean-Michel Lasry, and Pierre-Louis Lions (2019, *The Master Equation and Convergence Problem in Mean Field Games*) established the rigorous convergence from N-player games.

**Depends On:**
- Optimal control theory (from Applied Mathematics, Principle P14)
- Stochastic calculus (Ito's lemma, from Probability)
- PDE theory (Hamilton-Jacobi, Fokker-Planck equations)

**Implications:**
- Models large-population economics (price formation, wealth distribution) without tracking individual agents
- Applications in crowd dynamics, epidemic modeling (SIR with strategic agents), and energy markets
- The master equation (Lions) provides a single infinite-dimensional PDE that encodes the entire mean-field game
- Connects to optimal transport theory (Benamou-Brenier formulation) and Wasserstein geometry

---

### PRINCIPLE P13 — Regularity Structures (Hairer)

**Formal Statement:**
The theory of regularity structures (Martin Hairer, 2014) provides a framework for giving meaning to and solving singular stochastic partial differential equations (SPDEs) where the nonlinearity involves products of distributions. A regularity structure T = (A, T, G) consists of: an index set A ⊂ R (regularity exponents), a model space T = ⊕_{α∈A} T_α (graded vector space), and a structure group G acting on T. A model (Π, Γ) assigns to each point x a linear map Π_x: T → distributions and transition maps Γ_{xy}: T → T compatible with the local scaling. The reconstruction theorem: given a modelled distribution f (a function with values in T satisfying analytic bounds), there exists a unique distribution Rf approximating Π_x f(x) near each point x to the optimal order. For the KPZ equation ∂_t u = Δu + (∂_x u)² + ξ and the Φ⁴₃ equation ∂_t φ = Δφ - φ³ + ξ, the theory provides: (1) algebraic: an automated construction of the regularity structure encoding all necessary renormalization counterterms via decorated trees; (2) analytic: fixed-point arguments in spaces of modelled distributions; (3) probabilistic: convergence of renormalized solutions as the mollification parameter ε → 0.

**Plain Language:**
Regularity structures are a mathematical framework that makes sense of equations that should be meaningless. Many important equations in physics involve multiplying rough, noisy objects together, which is mathematically undefined. Hairer's theory provides a systematic way to "renormalize" these products by subtracting infinities in a controlled way, much as physicists do in quantum field theory but with full mathematical rigor. The framework converts the art of renormalization into a systematic, almost algorithmic procedure.

**Historical Context:**
Martin Hairer (2014, *Inventiones Mathematicae*; Fields Medal 2014 for this work). Simultaneously and independently, Martin Gubinelli, Peter Imkeller, and Nicolas Perkowski (2015) developed the parallel theory of paracontrolled distributions. Hairer's BPHZ theorem (with Bruned, Chandra, Chevyrev, 2019) automates the renormalization procedure using decorated trees, connecting to the Connes-Kreimer Hopf algebra of renormalization in quantum field theory. The theory has been applied to the KPZ equation, the Φ⁴₃ model, the stochastic quantization of Yang-Mills, and many other singular SPDEs.

**Depends On:**
- Distribution theory (Principle P10)
- Sobolev spaces and embedding theorems (Theorem T16)
- Rough path theory (Lyons, 1998)

**Implications:**
- Solves the KPZ equation, Φ⁴₃ equation, and other singular SPDEs that were previously beyond rigorous mathematical treatment
- The BPHZ theorem for regularity structures connects stochastic PDE theory to the Hopf-algebraic approach to renormalization in QFT
- Provides rigorous construction of quantum field theories in low dimensions via stochastic quantization
- The systematic renormalization framework suggests deep structural connections between probability theory and quantum field theory

---

### THEOREM T22 — The Kakeya Conjecture: Recent Breakthroughs

**Formal Statement:**
A Kakeya set (Besicovitch set) in R^n is a compact set containing a unit line segment in every direction. The Kakeya conjecture states that every Kakeya set in R^n has Hausdorff dimension n (and Minkowski dimension n). In R^2, this is known (Davies 1971). The conjecture remains open for n ≥ 3, but recent advances include: (1) Katz and Tao (2002) established dim_H(K) ≥ (2n+2)/3 + ε_n; (2) Nets Katz and Joshua Zahl (2019) proved new bounds using the polynomial method: if the joints conjecture holds, improved Kakeya estimates follow; (3) Hong Wang and Joshua Zahl (2025) proved the full Kakeya conjecture in R^3: every Kakeya set in R^3 has Hausdorff dimension 3, resolving a central problem in geometric measure theory and harmonic analysis. Their proof uses a sophisticated combination of the polynomial method, induction on scales, and refined estimates for sticky Kakeya sets.

**Plain Language:**
The Kakeya conjecture asks: if you have a set in space that contains a needle pointing in every direction, how small can that set be? Surprisingly, in the plane such sets can have zero area. The conjecture says that in higher dimensions, these sets must be large — they must have the maximum possible dimension. In 2025, Wang and Zahl proved this in three dimensions, resolving a problem that had resisted all attempts for decades. The techniques combine ideas from algebraic geometry (polynomial method) with intricate multiscale analysis.

**Historical Context:**
Soichi Kakeya (1917, original needle problem). Abram Besicovitch (1919, constructed zero-area Kakeya sets in R^2). Thomas Wolff (1995, Kakeya conjecture for n=2 and partial results for higher n). Nets Katz and Terence Tao (2002, breakthrough using the polynomial method). Zeev Dvir (2009, resolution of the finite field Kakeya conjecture). Hong Wang and Joshua Zahl (2025, proof of the Kakeya conjecture in R^3). The problem connects to fundamental questions in harmonic analysis (Bochner-Riesz conjecture, restriction conjecture) and additive combinatorics.

**Depends On:**
- Hausdorff dimension and geometric measure theory
- Harmonic analysis, oscillatory integrals
- The polynomial method (Dvir, Guth-Katz)

**Implications:**
- The R^3 result resolves a central conjecture in geometric measure theory that had been open for over a century
- Implies progress on the restriction conjecture and Bochner-Riesz conjecture in harmonic analysis via known reductions
- The polynomial method, originating in additive combinatorics, has proven to be a transformative tool in continuous geometry
- Opens the path to the full conjecture in all dimensions, with the three-dimensional techniques providing a template

---

### PRINCIPLE P14 — The Szemerédi Regularity Lemma and Graph Limits

**Formal Statement:**
The Szemerédi Regularity Lemma (1978): for every epsilon > 0, every graph G = (V, E) with |V| = n has a vertex partition V = V_0 ∪ V_1 ∪ ... ∪ V_k (with |V_0| ≤ epsilon*n and |V_1| = ... = |V_k|) such that all but at most epsilon*k^2 pairs (V_i, V_j) are epsilon-regular, meaning |d(A, B) - d(V_i, V_j)| < epsilon for all A ⊆ V_i, B ⊆ V_j with |A| ≥ epsilon|V_i|, |B| ≥ epsilon|V_j|. The number of parts k satisfies k ≤ T(1/epsilon) where T is a tower function. The regularity lemma generalizes to the theory of graph limits (Lovász-Szegedy 2006): the space of graphons W: [0,1]^2 -> [0,1] with the cut distance d_□ is compact, and every convergent graph sequence has a graphon limit. The counting lemma: the density of any fixed subgraph H in G is approximately determined by the regularity partition, enabling analytic methods for combinatorial problems.

**Plain Language:**
The regularity lemma says that every large graph, no matter how complex, can be approximated by a bounded-complexity "pseudorandom" structure. It is like a structure theorem for graphs: any graph can be decomposed into a bounded number of parts, where almost all pairs of parts behave like random bipartite graphs. This allows one to apply analytic and probabilistic techniques to prove results about arbitrary graphs, and it underlies some of the deepest results in combinatorics, including Szemerédi's theorem on arithmetic progressions.

**Historical Context:**
Endre Szemerédi (1978, regularity lemma as a tool for his arithmetic progressions theorem; Abel Prize 2012). Timothy Gowers (2001, quantitative bounds for the regularity lemma). László Lovász and Balázs Szegedy (2006, graph limits and graphons). The regularity method has become one of the most powerful and widely-used tools in extremal combinatorics, with connections to analysis via graphon theory.

**Depends On:**
- Measure theory, L^p spaces
- Graph theory, combinatorics
- Compactness in function spaces

**Implications:**
- Szemerédi's theorem (arithmetic progressions in dense sets) was the original application; the regularity lemma provides the structural backbone
- Graph limits (graphons) connect combinatorics to analysis: extremal graph theory questions become variational problems on the graphon space
- Flag algebras (Razborov 2007) use graphon theory to solve extremal problems via semidefinite programming
- Applications in computer science: property testing, algorithmic graph theory, and the theory of dense graph algorithms

---

### THEOREM T23 — Analytic Langlands Correspondence (Etingof-Frenkel-Kazhdan)

**Formal Statement:**
The Analytic Langlands Correspondence (Etingof-Frenkel-Kazhdan 2021) constructs a spectral decomposition of the space of L^2-functions on Bun_G(X) for a complex algebraic curve X and reductive group G. The Hecke operators T_V,x (parametrized by representations V of the Langlands dual group G^ and points x of X) form a commutative family of normal operators on L^2(Bun_G(X), mu) for a natural measure mu. The joint spectral decomposition yields a direct integral: L^2(Bun_G(X)) = integral_{LocSys_{G^}(X)} H_sigma d-mu(sigma), where the spectrum is the moduli space of G^-local systems on X. For G = GL_1, this reduces to the classical Fourier transform on the Jacobian. The key analytic input is the proof that the Hecke operators are compact (for parabolic induction) or trace-class, enabling spectral decomposition via the spectral theorem for commuting normal operators. The correspondence provides the analytic realization of the geometric Langlands correspondence of Beilinson-Drinfeld and Gaitsgory.

**Plain Language:**
The Analytic Langlands Correspondence bridges harmonic analysis and algebraic geometry by providing a spectral decomposition — analogous to the Fourier transform — on the space of functions on the moduli of bundles over a curve. Just as the Fourier transform decomposes functions into frequencies, this correspondence decomposes functions on geometric spaces into spectral components labeled by Langlands parameters. It gives an analytic (rather than purely algebraic) formulation of the geometric Langlands program, making functional analysis a central tool in modern number theory and representation theory.

**Historical Context:**
Pavel Etingof, Edward Frenkel, and David Kazhdan (2021, formulation and foundational results). Builds on the geometric Langlands program of Beilinson-Drinfeld (1990s) and the proof by Gaitsgory et al. (2024). The analytic approach was inspired by Langlands' own vision of relating automorphic forms to spectral theory. The compactness of Hecke operators is a key analytic input not present in the algebraic formulation.

**Depends On:**
- Functional analysis (spectral theorem, L^2 spaces, Principle P9)
- Algebraic geometry (moduli spaces, vector bundles)
- Representation theory of reductive groups

**Implications:**
- Provides an analytic realization of geometric Langlands, complementing the algebraic proof of Gaitsgory et al.
- The spectral decomposition yields new analytic number theory results via the function field analogy
- Connects harmonic analysis on infinite-dimensional spaces to the Langlands program
- Opens new directions combining PDE theory, spectral geometry, and arithmetic geometry

---

### PRINCIPLE P15 — Reproducing Kernel Hilbert Spaces (RKHS) and the Kernel Trick

**Formal Statement:**
A reproducing kernel Hilbert space (RKHS) on a set X is a Hilbert space H of functions f: X -> R (or C) such that for each x in X, the evaluation functional delta_x: f -> f(x) is continuous. By the Riesz representation theorem, there exists a unique K_x in H with f(x) = <f, K_x>_H for all f in H. The reproducing kernel K: X x X -> R defined by K(x,y) = K_y(x) = <K_x, K_y> is symmetric and positive definite. The Moore-Aronszajn theorem (1950): for every positive definite kernel K on X, there exists a unique RKHS H_K with reproducing kernel K. The representer theorem (Kimeldorf-Wahba 1970, Scholkopf-Herbrich-Smola 2001): the minimizer of a regularized empirical risk functional min_{f in H_K} sum_i L(y_i, f(x_i)) + lambda ||f||^2_{H_K} has the form f*(x) = sum_{i=1}^n alpha_i K(x_i, x), reducing an infinite-dimensional optimization to a finite-dimensional one. The kernel trick: inner products <phi(x), phi(y)> in a high-dimensional feature space can be computed as K(x,y) without explicitly computing phi.

**Plain Language:**
A reproducing kernel Hilbert space is a space of functions where you can evaluate any function at any point, and this evaluation is well-behaved (continuous). The key property is that there exists a special "kernel function" that acts as a similarity measure between points and completely determines the space. The representer theorem guarantees that even though you are optimizing over an infinite-dimensional space of functions, the solution depends on your data through finitely many kernel evaluations. This is the mathematical foundation of kernel methods in machine learning, enabling algorithms to work implicitly in very high-dimensional spaces.

**Historical Context:**
Nachman Aronszajn (1950, systematic development of RKHS theory). Stefan Bergman (1950, Bergman kernel in complex analysis, an early example). Grace Wahba and George Kimeldorf (1970, representer theorem for spline smoothing). Vladimir Vapnik and colleagues (1990s, support vector machines using the kernel trick). Bernhard Scholkopf, Ralf Herbrich, and Alex Smola (2001, generalized representer theorem). The RKHS framework unifies classical approximation theory, Gaussian process regression, and modern kernel-based machine learning.

**Depends On:**
- Hilbert space theory, Riesz representation theorem (Principle P9)
- Functional analysis, bounded linear functionals
- Positive definite functions, Bochner's theorem

**Implications:**
- The kernel trick enables support vector machines, Gaussian processes, and kernel PCA to operate in infinite-dimensional feature spaces
- Connections to Gaussian processes: a Gaussian process with covariance function K has sample paths in the RKHS H_K (in a precise sense via the Cameron-Martin theorem)
- The representer theorem reduces infinite-dimensional optimization to finite-dimensional linear algebra, the foundation of nonparametric statistics
- Applications in numerical analysis (radial basis function interpolation), signal processing (optimal filtering), and PDEs (meshless methods)

---

### THEOREM T24 — Schramm-Loewner Evolution (SLE) and Conformal Invariance

**Formal Statement:**
Schramm-Loewner evolution SLE_kappa (Oded Schramm 2000) is the unique one-parameter family of random fractal curves in the plane that is conformally invariant and satisfies the domain Markov property. SLE_kappa is defined via the Loewner equation: dg_t(z)/dt = 2/(g_t(z) - sqrt(kappa) B_t), g_0(z) = z, where B_t is standard Brownian motion and kappa > 0 is the parameter. The trace gamma_t = lim_{epsilon->0} g_t^{-1}(sqrt(kappa) B_t + i*epsilon) is a random curve in the upper half-plane. Phase transitions: for kappa in (0,4], the trace is a simple curve; for kappa in (4,8), it is self-touching but not space-filling; for kappa >= 8, it is space-filling. The Hausdorff dimension of the SLE_kappa trace is min(1 + kappa/8, 2) (Beffara 2008). Key identifications: SLE_2 = loop-erased random walk scaling limit, SLE_3 = Ising model interface, SLE_4 = Gaussian free field level line, SLE_6 = critical percolation interface (Smirnov 2001), SLE_8 = uniform spanning tree Peano curve.

**Plain Language:**
Schramm-Loewner evolution is a family of random curves that describes the interfaces in two-dimensional critical phenomena — the boundaries between phases in systems like percolation, the Ising model, and random walks at their critical points. Schramm's breakthrough insight was that conformal invariance and a natural Markov property uniquely determine these curves, reducing the entire zoology of 2D critical interfaces to a single one-parameter family. This provided the rigorous mathematical framework for understanding universality in two-dimensional statistical physics.

**Historical Context:**
Oded Schramm (2000, introduction of SLE, combining Loewner's classical equation from 1923 with Brownian motion). Stanislav Smirnov (2001, proved conformal invariance of critical percolation on the triangular lattice and identified its scaling limit with SLE_6; Fields Medal 2010). Gregory Lawler, Schramm, and Wendelin Werner (2001-2004, proved that SLE describes the scaling limits of loop-erased random walk and uniform spanning tree; Werner received Fields Medal 2006). Vincent Beffara (2008, Hausdorff dimension of SLE traces). The theory resolved longstanding predictions from conformal field theory about critical exponents in two dimensions.

**Depends On:**
- Complex analysis, conformal mappings, Loewner equation
- Probability theory, Brownian motion (Principle 8)
- Statistical mechanics, critical phenomena (Physics: Thermodynamics)

**Implications:**
- Provides the rigorous mathematical framework for two-dimensional conformal field theory predictions
- Confirmed critical exponents for percolation, self-avoiding walks, and the Ising model predicted by physicists using non-rigorous methods
- The SLE-CFT correspondence connects probability theory to quantum field theory and representation theory of the Virasoro algebra
- Applications to random planar maps, Liouville quantum gravity, and the mating-of-trees framework

---

## References

- Cauchy, A.-L. (1821). *Cours d'Analyse*. Paris.
- Riemann, B. (1854). "Über die Darstellbarkeit einer Function durch eine trigonometrische Reihe." Habilitation thesis.
- Dedekind, R. (1872). *Stetigkeit und irrationale Zahlen*. Vieweg.
- Lebesgue, H. (1902). "Intégrale, longueur, aire." *Annali di Matematica*, 7, 231–359.
- Fréchet, M. (1906). "Sur quelques points du calcul fonctionnel." *Rendiconti del Circolo Matematico di Palermo*, 22, 1–72.
- Baire, R. (1899). "Sur les fonctions de variables reelles." *Annali di Matematica*, 3(3), 1–123.
- Rudin, W. (1976). *Principles of Mathematical Analysis*. 3rd ed. McGraw-Hill.
- Royden, H.L. & Fitzpatrick, P. (2010). *Real Analysis*. 4th ed. Pearson.
- Folland, G. (1999). *Real Analysis: Modern Techniques and Their Applications*. 2nd ed. Wiley.
