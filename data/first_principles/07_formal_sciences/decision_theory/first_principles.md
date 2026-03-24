# First Principles of Decision Theory

## Overview

Decision theory is the formal study of **rational choice under uncertainty**. It provides axiomatic foundations for how an ideal rational agent should make decisions when outcomes are uncertain and preferences must be weighed. Decision theory bridges mathematics, economics, philosophy, and artificial intelligence, providing the formal backbone for utility theory, game theory, and rational agency.

## Prerequisites

- Logic (formal reasoning)
- Probability & Statistics (Kolmogorov axioms, Bayes' theorem)

---

## First Principles

### AXIOM SYSTEM 1: Von Neumann-Morgenstern Utility Axioms (Expected Utility Theory)

For a rational agent choosing among **lotteries** (probability distributions over outcomes):

#### AXIOM 1.1: Completeness
- **Formal Statement:** For any lotteries L₁, L₂: either L₁ ≽ L₂, or L₂ ≽ L₁, or both (indifference).
- **Plain Language:** A rational agent can always compare any two options — no pair is "incomparable."

#### AXIOM 1.2: Transitivity
- **Formal Statement:** If L₁ ≽ L₂ and L₂ ≽ L₃, then L₁ ≽ L₃.
- **Plain Language:** Preferences are consistent — no cycles.

#### AXIOM 1.3: Continuity (Archimedean Property)
- **Formal Statement:** If L₁ ≻ L₂ ≻ L₃, then there exists some probability p ∈ (0,1) such that pL₁ + (1-p)L₃ ~ L₂.
- **Plain Language:** There are no "infinitely good" or "infinitely bad" outcomes — you can always find a mixture that matches any intermediate preference.

#### AXIOM 1.4: Independence
- **Formal Statement:** If L₁ ≽ L₂, then for any L₃ and any p ∈ (0,1]: pL₁ + (1-p)L₃ ≽ pL₂ + (1-p)L₃.
- **Plain Language:** Mixing two options with a common third option does not change the preference ordering between the first two.

**Von Neumann-Morgenstern Theorem:** If these four axioms hold, then there exists a utility function u such that the agent's preferences are represented by expected utility: L₁ ≽ L₂ ↔ E[u(L₁)] ≥ E[u(L₂)]. Moreover, u is unique up to positive affine transformation.

- **Historical Context:** Von Neumann & Morgenstern (1944), *Theory of Games and Economic Behavior*. Building on earlier work by Bernoulli (1738, St. Petersburg paradox).
- **Depends On:** Probability theory, preference relations.
- **Implications:** Expected utility theory is the standard normative model of rational choice under uncertainty. It underlies: microeconomics, finance (portfolio theory), insurance, game theory, and AI decision-making. Violations of these axioms (Allais paradox, Ellsberg paradox) motivated alternatives like prospect theory.

---

### AXIOM SYSTEM 2: Savage's Axioms (Subjective Expected Utility)

Savage (1954) derived both probability and utility from preferences over **acts** (functions from states of the world to outcomes):

#### Key Axioms:
- **P1 (Complete Preorder):** Preferences over acts are complete and transitive.
- **P2 (Sure-Thing Principle):** If two acts agree on event E's complement, preference depends only on consequences given E.
- **P3 (Eventwise Monotonicity):** For any non-null event, preferring one outcome to another within that event preserves preference.
- **P4 (Comparative Probability):** Preferences reveal a consistent probability ordering over events.
- **P5 (Non-Triviality):** Not all outcomes are equally preferred.
- **P6 (Fine-Grained Events):** Events can be made arbitrarily small in probability.
- **P7 (Dominance):** If an act's consequences are all preferred, then the act is preferred.

**Savage's Theorem:** These axioms imply the existence of a unique probability measure P and a utility function u (unique up to positive affine transformation) such that the agent maximizes expected utility: E_P[u(f)] for act f.

- **Historical Context:** Leonard Savage (1954), *The Foundations of Statistics*. This is one of the most elegant axiomatizations in all of decision theory — it derives *both* probability and utility from a single set of behavioral axioms.
- **Depends On:** Acts, outcomes, states of the world.
- **Implications:** Savage's framework provides the philosophical foundation for subjective (Bayesian) probability. It shows that a rational agent who satisfies these axioms *behaves as if* they have beliefs (probabilities) and desires (utilities).

---

### PRINCIPLE 1: The Principle of Dominance

- **Formal Statement:** If act A yields an outcome at least as good as act B in every possible state of the world, and strictly better in at least one state, then A is strictly preferred to B.
- **Plain Language:** If one option is better in some scenarios and no worse in any, choose it.
- **Historical Context:** One of the most basic and uncontroversial principles of rational choice.
- **Depends On:** Preference ordering over outcomes.
- **Implications:** Dominance is the "easy case" of decision-making. It is universally accepted and is the starting point for more complex decision criteria.

---

### PRINCIPLE 2: Bayes' Rule as a Decision Principle

- **Formal Statement:** A rational agent updates beliefs using Bayes' rule: P(θ|data) ∝ P(data|θ) · P(θ). Decision-making under the updated beliefs uses posterior expected utility.
- **Plain Language:** When you observe new evidence, update your probabilities using Bayes' theorem, then make decisions based on your updated beliefs.
- **Historical Context:** Bayes (1763), Laplace (1774), axiomatized by Savage (1954) and de Finetti (1937).
- **Depends On:** Savage's axioms, Kolmogorov axioms, Bayes' theorem.
- **Implications:** Bayesian updating is the normative standard for learning from evidence. It provides a complete framework for sequential decision-making, hypothesis testing, and experimental design.

---

### PRINCIPLE 3: Minimax and Maximin (Decision Under Ignorance)

- **Formal Statement:** The minimax principle: choose the act that minimizes the maximum possible loss. The maximin principle: choose the act that maximizes the minimum possible payoff.
- **Plain Language:** Prepare for the worst case.
- **Historical Context:** Wald (1950), von Neumann & Morgenstern (1944, for zero-sum games). The minimax theorem for zero-sum games is one of the foundational results of game theory.
- **Depends On:** Preference ordering, but NOT probability (this is for decision under complete uncertainty).
- **Implications:** Minimax is the foundation of: worst-case analysis in algorithms, robust optimization, the minimax theorem in game theory, and Rawlsian justice theory in political philosophy.

---

### PRINCIPLE 4: Prospect Theory (Kahneman-Tversky)

- **Formal Statement:** Prospect theory replaces expected utility with a two-phase model: (1) Editing phase: outcomes are coded as gains or losses relative to a reference point. (2) Evaluation phase: V(prospect) = Σ π(pᵢ) · v(xᵢ), where v is a value function that is concave for gains, convex for losses, and steeper for losses than gains (loss aversion: v(−x) > −v(x) for x > 0), and π is a probability weighting function that overweights small probabilities and underweights large ones. Cumulative Prospect Theory (Tversky & Kahneman, 1992) applies rank-dependent probability weighting.
- **Plain Language:** People do not evaluate outcomes in absolute terms but relative to a reference point (usually the status quo). Losses hurt about twice as much as equivalent gains feel good (loss aversion). People also overweight unlikely events (why we buy lottery tickets and insurance) and underweight likely events. This explains many "irrational" behaviors that expected utility theory cannot.
- **Historical Context:** Daniel Kahneman & Amos Tversky (1979), "Prospect Theory: An Analysis of Decision under Risk." This paper is the most cited in all of economics. Kahneman received the Nobel Prize in Economics (2002). Prospect theory was motivated by systematic violations of expected utility theory, including the Allais paradox (1953).
- **Depends On:** VNM utility axioms (as the baseline being modified), reference dependence, probability weighting.
- **Implications:** Foundation of behavioral economics. Explains the equity premium puzzle, the disposition effect (selling winners too early, holding losers too long), status quo bias, endowment effect, and framing effects. Prospect theory has transformed economics, finance, insurance, marketing, and public policy ("nudge" theory). It demonstrates that descriptively accurate models of choice must depart from expected utility axioms.

---

### PRINCIPLE 5: Minimax Regret (Savage)

- **Formal Statement:** For each act a and state s, the regret is r(a, s) = max_{a'} u(a', s) − u(a, s): the difference between the best possible outcome in state s and the outcome of act a. The minimax regret criterion selects the act that minimizes the maximum regret across all states: choose a* = argmin_a max_s r(a, s).
- **Plain Language:** Instead of minimizing the worst outcome, minimize the worst "I wish I had done something else" feeling. Regret is the gap between what you got and what you could have gotten if you had chosen the best option for that state of the world. Minimax regret picks the action whose worst-case regret is smallest.
- **Historical Context:** Leonard Savage (1951), "The Theory of Statistical Decision." Savage proposed minimax regret as an alternative to both minimax (too conservative) and expected utility (requires probabilities). Loomes & Sugden (1982) developed regret theory as a descriptive model.
- **Depends On:** Preference ordering, state space, the concept of opportunity cost.
- **Implications:** Minimax regret is widely used in robust decision-making, robust statistics, and operations research. It is less conservative than minimax because it measures relative performance rather than absolute worst case. Regret-based models explain observed violations of independence and transitivity. In machine learning, regret minimization is the foundation of online learning and multi-armed bandit algorithms.

---

### PRINCIPLE 6: Ellsberg Paradox and Ambiguity Aversion

- **Formal Statement:** The Ellsberg paradox (1961): an urn contains 30 red balls and 60 balls that are either black or yellow in unknown proportions. Most people prefer betting on red over black (known vs. unknown probability) and simultaneously prefer betting on "black or yellow" over "red or yellow." These preferences jointly violate the Sure-Thing Principle (Savage's P2) and cannot be represented by any subjective probability distribution. Ambiguity aversion is the preference for known risks over unknown risks (Knightian uncertainty). Maxmin expected utility (Gilboa & Schmeidler, 1989): the agent has a set of priors C and maximizes min_{P∈C} E_P[u].
- **Plain Language:** People dislike not knowing the odds, above and beyond disliking risk itself. Given a choice between a bet with known 50/50 odds and a bet where the odds are completely unknown, most people prefer the known odds — even though a Bayesian agent should be indifferent. This "ambiguity aversion" violates standard expected utility theory.
- **Historical Context:** Daniel Ellsberg (1961), "Risk, Ambiguity, and the Savage Axioms." Frank Knight (1921) distinguished risk (known probabilities) from uncertainty (unknown probabilities). Gilboa & Schmeidler (1989) provided axiomatic foundations for decision-making under ambiguity with multiple priors.
- **Depends On:** Savage's axioms (as the violated baseline), the distinction between risk and uncertainty.
- **Implications:** Ambiguity aversion has significant implications for finance (equity premium puzzle, portfolio choice), insurance (unwillingness to insure ambiguous risks), regulation (precautionary principle), and organizational behavior. The multiple priors framework has spawned a rich literature in robust decision theory and robust control. The Ellsberg paradox is one of the strongest challenges to Bayesian decision theory.

---

### THEOREM 7: Arrow's Impossibility Theorem (Social Choice)

- **Formal Statement:** There is no social welfare function f that aggregates individual preference orderings over three or more alternatives into a social ordering while satisfying: (1) Unrestricted domain: f is defined for all possible profiles of individual preferences. (2) Pareto efficiency: if all individuals prefer x to y, the social ordering ranks x above y. (3) Independence of irrelevant alternatives (IIA): the social ranking of x vs y depends only on individuals' rankings of x vs y. (4) Non-dictatorship: no single individual's preferences always determine the social ordering. Any f satisfying (1)-(3) must be dictatorial.
- **Plain Language:** There is no perfect way to aggregate individual preferences into a group decision. Any voting rule that works for all possible preferences, respects unanimity, and considers only relevant comparisons must give one person dictatorial power. Democracy, in a precise mathematical sense, cannot be designed to satisfy all reasonable fairness conditions simultaneously.
- **Historical Context:** Kenneth Arrow (1951), *Social Choice and Individual Values*. Nobel Prize in Economics (1972). The theorem generalizes Condorcet's voting paradox (1785). It launched the field of social choice theory and profoundly influenced political science, economics, and philosophy.
- **Depends On:** Complete and transitive individual preferences, three or more alternatives.
- **Implications:** Central to welfare economics, voting theory, and political philosophy. All voting systems must sacrifice at least one of Arrow's conditions. Related results: Gibbard-Satterthwaite theorem (all non-dictatorial voting rules with 3+ alternatives are manipulable), Sen's Liberal Paradox (tension between Pareto efficiency and individual rights). Informs practical electoral system design and the analysis of democratic institutions.

---

### PRINCIPLE 8: Bayesian Decision Theory

- **Formal Statement:** A Bayesian decision-maker has a prior probability distribution P(θ) over states of the world θ ∈ Θ, a set of available actions A, a utility function u(a, θ), and updates beliefs via Bayes' rule: P(θ|data) ∝ P(data|θ)P(θ). The optimal decision maximizes posterior expected utility: a* = argmax_a E_{θ|data}[u(a, θ)] = argmax_a ∫ u(a, θ) P(θ|data) dθ. The value of information: the expected improvement in decision quality from observing additional data before acting.
- **Plain Language:** A Bayesian decision-maker starts with beliefs about the world, updates those beliefs as evidence arrives using Bayes' theorem, and then chooses the action that maximizes expected utility under the updated beliefs. This framework unifies statistical inference with decision-making: what you should believe and what you should do are answered in one coherent framework.
- **Historical Context:** Builds on Savage (1954) and de Finetti (1937). Raiffa & Schlaifer (1961) developed the theory for practical statistical decisions. The Bayesian approach contrasts with frequentist decision theory (Wald, 1950) and has become dominant in machine learning and AI (Bayesian networks, Bayesian optimization).
- **Depends On:** Savage's axioms, Bayes' theorem, prior distributions.
- **Implications:** The normative gold standard for sequential decision-making under uncertainty. Underlies: Bayesian statistics, Bayesian networks, reinforcement learning, optimal experimental design, medical decision-making, and financial portfolio theory. The choice of prior remains controversial (subjectivism vs. objectivism). Bayesian decision theory provides the formal backbone of rational agency in AI.

---

### PRINCIPLE 9: Multi-Criteria Decision Analysis (MCDA)

- **Formal Statement:** When decisions involve multiple conflicting objectives (criteria) c₁, ..., c_k, Multi-Criteria Decision Analysis provides structured methods for evaluation. Key approaches: (1) Multi-attribute utility theory (MAUT, Keeney & Raiffa, 1976): construct a multi-attribute utility function U(x) = f(u₁(x₁), ..., u_k(x_k)). Under preferential independence conditions, U is additive: U(x) = Σ wᵢ uᵢ(xᵢ). (2) Analytic Hierarchy Process (AHP, Saaty, 1980): pairwise comparison of criteria and alternatives. (3) Pareto optimality: an alternative is Pareto optimal if no other alternative is better on all criteria simultaneously. The Pareto frontier is the set of all Pareto optimal alternatives.
- **Plain Language:** Real decisions often involve trade-offs between multiple goals that cannot be reduced to a single number. How do you choose a job balancing salary, location, and work-life balance? MCDA provides systematic methods for weighing, scoring, and comparing alternatives across multiple criteria, making trade-offs transparent and rational.
- **Historical Context:** Keeney & Raiffa (1976), *Decisions with Multiple Objectives*. Saaty (1980) developed AHP. The field synthesizes operations research, utility theory, and practical decision support. Pareto optimality originates from Vilfredo Pareto (1896).
- **Depends On:** Utility theory, preference ordering over multiple attributes.
- **Implications:** Widely applied in engineering design, environmental policy, healthcare resource allocation, infrastructure planning, and corporate strategy. MCDA makes value trade-offs explicit and defensible. In optimization, multi-objective optimization seeks the entire Pareto frontier rather than a single optimum. In AI, multi-objective reinforcement learning balances competing objectives.

---

## Summary Table

| # | Name | Type | Core Statement | Dependencies |
|---|------|------|----------------|--------------|
| A1 | VNM Utility Axioms | AXIOM SYSTEM | Completeness, transitivity, continuity, independence → E[u] | Probability, preferences |
| A2 | Savage's Axioms | AXIOM SYSTEM | 7 axioms on acts → subjective probability + utility | States, outcomes, acts |
| P1 | Dominance | PRINCIPLE | Better in all states → preferred | Preference ordering |
| P2 | Bayesian Updating | PRINCIPLE | Update beliefs via Bayes' rule | Savage/VNM, probability |
| P3 | Minimax/Maximin | PRINCIPLE | Minimize worst-case loss | Preference ordering |
| P4 | Prospect Theory | PRINCIPLE | Loss aversion, reference dependence, probability weighting | VNM axioms (modified) |
| P5 | Minimax Regret | PRINCIPLE | Minimize worst-case regret (gap from best possible) | Preference ordering, states |
| P6 | Ellsberg Paradox / Ambiguity Aversion | PRINCIPLE | Preference for known over unknown probabilities | Savage's axioms (violated) |
| T7 | Arrow's Impossibility Theorem | THEOREM | No fair social welfare function satisfying four conditions | Preferences, ≥3 alternatives |
| P8 | Bayesian Decision Theory | PRINCIPLE | Maximize posterior expected utility after Bayesian updating | Savage's axioms, Bayes |
| P9 | Multi-Criteria Decision Analysis | PRINCIPLE | Structured evaluation under multiple conflicting objectives | Utility theory, Pareto |

---

### AXIOM SYSTEM 3: Anscombe-Aumann Framework

**Formal Statement:**
The Anscombe-Aumann (1963) framework simplifies Savage's approach by assuming an objective probability space (lotteries) already exists. Acts map states of the world to lotteries (objective probability distributions over outcomes). Preferences over acts satisfy: (1) Completeness and transitivity, (2) Independence (for acts), (3) Continuity, (4) Monotonicity. The representation theorem yields: subjective probability P over states and vNM utility u over outcomes, such that the agent maximizes ∫_S E_u[f(s)] dP(s).

**Plain Language:**
The Anscombe-Aumann framework is a cleaner way to derive subjective expected utility. By assuming lotteries are already understood (from vNM theory), it isolates the problem of deriving subjective probabilities from preferences over "acts" that map uncertain states to known gambles.

**Historical Context:**
Anscombe & Aumann (1963), "A Definition of Subjective Probability." This framework became the standard workhorse for theoretical work in decision theory because its axioms are more transparent than Savage's and the proof is simpler.

**Depends On:**
- VNM utility theory (Axiom System 1)
- Probability theory (objective lotteries)

**Implications:**
- Standard framework for modern theoretical work in decision theory and game theory
- Simpler to extend to models of ambiguity aversion (Gilboa-Schmeidler multiple priors fit naturally here)
- The horse-race/roulette-wheel distinction: states are "horses" (subjective), lotteries are "roulette" (objective)

---

### PRINCIPLE 10: Regret Theory

**Formal Statement:**
In regret theory (Loomes & Sugden, 1982; Bell, 1982), the decision-maker evaluates an action not only by its outcome but by comparing that outcome to what would have resulted from alternative actions. The utility of choosing action a in state s includes a regret-rejoice function R: V(a) = Σ_s p(s)[u(a,s) + R(u(a,s) - u(a*,s))], where a* is the alternative action. R is increasing with R(0) = 0, concave for gains and convex for losses.

**Plain Language:**
Regret theory says people care not just about what they get, but about what they could have gotten if they had chosen differently. The pain of a bad choice is amplified when a better option was available. This explains many violations of expected utility theory without abandoning the idea of optimizing a well-defined objective.

**Historical Context:**
Bell (1982) and Loomes & Sugden (1982), independently. Regret theory provides a unified explanation for the Allais paradox, preference reversals, and violations of transitivity observed in experimental settings.

**Depends On:**
- Utility theory (as baseline)
- Counterfactual reasoning

**Implications:**
- Explains Allais paradox and common ratio effect without probability weighting
- Foundation for regret minimization in online learning and multi-armed bandits (computer science)
- Applications in medical decision-making (regret about treatment choices) and financial behavior
- Provides a bridge between normative and descriptive decision theory

---

### PRINCIPLE 11: Value of Information

**Formal Statement:**
The value of information (VOI) is the maximum amount a decision-maker would pay to observe a signal before making a decision. For a Bayesian decision-maker: VOI = E_X[max_a E_{θ|X}[u(a,θ)]] - max_a E_θ[u(a,θ)]. VOI is always non-negative (information never hurts a Bayesian decision-maker). Perfect information value: EVPI = E_θ[max_a u(a,θ)] - max_a E_θ[u(a,θ)].

**Plain Language:**
How much is it worth to learn something before you decide? The value of information quantifies this: it is the expected improvement in your decision from having the information versus not having it. A rational agent should never pay more than this for information, and information is always worth at least zero.

**Historical Context:**
Raiffa & Schlaifer (1961). Howard (1966) formalized the value of information framework for sequential decision problems. Central to experimental design, medical testing, and information economics.

**Depends On:**
- Bayesian decision theory (Principle 8)
- Expected utility maximization

**Implications:**
- Guides optimal experimental design: which experiments are worth running?
- Medical testing: when is an additional diagnostic test worth its cost?
- Information economics: pricing of data, design of information markets
- Active learning and Bayesian optimization in machine learning use VOI to select queries

---

### PRINCIPLE 12: Causal Decision Theory vs Evidential Decision Theory

**Formal Statement:**
Evidential Decision Theory (EDT, Jeffrey 1965): choose the act that maximizes expected utility conditional on the act being performed: max_a E[u | do(a)] where conditioning uses evidential (correlational) probability. Causal Decision Theory (CDT, Gibbard & Harper 1978, Lewis 1981): choose the act that maximizes expected utility under causal interventions: max_a sum_s P(s || a) u(a,s), where P(s || a) is the probability of state s given that a is causally brought about (not merely correlated). EDT and CDT diverge in Newcomb-like problems where acts are correlated with states but do not cause them.

**Plain Language:**
Should you make decisions based on what your action would cause to happen (causal decision theory), or based on what your action is evidence for (evidential decision theory)? In most cases they agree, but in Newcomb's problem and similar paradoxes they give different answers. This is one of the deepest open debates in the foundations of rational choice.

**Historical Context:**
Newcomb's problem (Nozick, 1969). Jeffrey (1965, *The Logic of Decision*) developed EDT. Lewis (1981) and Gibbard & Harper (1978) formalized CDT. The debate remains unresolved and is central to AI alignment (what decision theory should an artificial agent use?).

**Depends On:**
- Expected utility theory (Axiom System 1)
- Causal reasoning vs correlational reasoning

**Implications:**
- Central to AI alignment: which decision theory should artificial agents implement?
- Functional Decision Theory (FDT, Yudkowsky & Soares, 2018) and other recent proposals attempt to resolve the debate
- Connections to Pearl's do-calculus and causal inference
- Implications for game theory: how agents reason about their own counterfactual choices

---

### PRINCIPLE 13: Proper Scoring Rules and Calibration

**Formal Statement:**
A scoring rule S(p, omega) assigns a score to a probability forecast p when outcome omega is realized. A scoring rule is proper if the expected score is maximized when the agent reports their true beliefs: E_q[S(q, omega)] >= E_q[S(p, omega)] for all p != q. It is strictly proper if equality holds only when p = q. Key strictly proper scoring rules: logarithmic score S(p, omega) = log p(omega), Brier score S(p, omega) = 2p(omega) - ||p||^2. An agent is calibrated if, among events to which probability p is assigned, the long-run frequency of occurrence is p.

**Plain Language:**
A proper scoring rule rewards honest probability assessments: if you truly believe rain is 70% likely, a proper scoring rule makes it optimal for you to report 70%, not some other number. Calibration is the empirical counterpart: a forecaster is calibrated if events they call "70% likely" actually happen about 70% of the time. Proper scoring rules incentivize both accuracy and honesty.

**Historical Context:**
Brier (1950, Brier score for weather forecasts). Good (1952) and Savage (1971) developed the theory of proper scoring rules. Dawid (1982) connected scoring rules to calibration. de Finetti used scoring rules to justify subjective probability.

**Depends On:**
- Probability theory, Bayesian framework
- Expected utility theory

**Implications:**
- Foundation of probabilistic forecasting: weather, finance, epidemiology
- Strictly proper scoring rules incentivize truthful elicitation of beliefs (mechanism design for information)
- Calibration is a necessary (but not sufficient) condition for good probability forecasts
- Connection to information theory: the logarithmic scoring rule is equivalent to cross-entropy loss in machine learning

---

### PRINCIPLE 14: Jeffrey's Rule of Probability Kinematics

**Formal Statement:**
Jeffrey's rule generalizes Bayesian conditionalization to cases where the evidence does not make any proposition certainly true or false, but shifts the probabilities of a partition {E_i}. If the agent's new probabilities for the partition become P_new(E_i), then for any proposition A: P_new(A) = sum_i P_old(A | E_i) * P_new(E_i). This reduces to standard Bayesian conditionalization when P_new(E_j) = 1 for some j.

**Plain Language:**
Standard Bayesian updating assumes you learn something for certain: "event E occurred." But real evidence is often uncertain -- you might become more confident in E without being certain. Jeffrey's rule handles this: it updates all your beliefs proportionally to how your confidence in the evidence partition has shifted, without requiring certainty about anything.

**Historical Context:**
Richard Jeffrey (1965, *The Logic of Decision*). Jeffrey's rule was motivated by the observation that perceptual evidence (e.g., seeing something in dim light) shifts probabilities without making any proposition certain. It has been axiomatized by several authors and is a cornerstone of evidential decision theory.

**Depends On:**
- Kolmogorov axioms, Bayes' theorem
- Conditional probability

**Implications:**
- Extends Bayesian reasoning to soft evidence (uncertain observations)
- Foundation of evidential decision theory (Jeffrey, 1965)
- Applications in sensor fusion, uncertain perception, and imprecise evidence processing
- Connects to Pearl's theory of interventions: Jeffrey conditioning on evidence vs do-calculus conditioning on actions

---

## Summary Table (Updated)

| # | Name | Type | Core Statement | Dependencies |
|---|------|------|----------------|--------------|
| A1 | VNM Utility Axioms | AXIOM SYSTEM | Completeness, transitivity, continuity, independence → E[u] | Probability, preferences |
| A2 | Savage's Axioms | AXIOM SYSTEM | 7 axioms on acts → subjective probability + utility | States, outcomes, acts |
| P1 | Dominance | PRINCIPLE | Better in all states → preferred | Preference ordering |
| P2 | Bayesian Updating | PRINCIPLE | Update beliefs via Bayes' rule | Savage/VNM, probability |
| P3 | Minimax/Maximin | PRINCIPLE | Minimize worst-case loss | Preference ordering |
| P4 | Prospect Theory | PRINCIPLE | Loss aversion, reference dependence, probability weighting | VNM axioms (modified) |
| P5 | Minimax Regret | PRINCIPLE | Minimize worst-case regret (gap from best possible) | Preference ordering, states |
| P6 | Ellsberg Paradox / Ambiguity Aversion | PRINCIPLE | Preference for known over unknown probabilities | Savage's axioms (violated) |
| T7 | Arrow's Impossibility Theorem | THEOREM | No fair social welfare function satisfying four conditions | Preferences, ≥3 alternatives |
| P8 | Bayesian Decision Theory | PRINCIPLE | Maximize posterior expected utility after Bayesian updating | Savage's axioms, Bayes |
| P9 | Multi-Criteria Decision Analysis | PRINCIPLE | Structured evaluation under multiple conflicting objectives | Utility theory, Pareto |
| A3 | Anscombe-Aumann Framework | AXIOM SYSTEM | Acts → lotteries; derives subjective probability | VNM utility, probability |
| P10 | Regret Theory | PRINCIPLE | Utility includes comparison to foregone alternatives | Utility theory, counterfactuals |
| P11 | Value of Information | PRINCIPLE | VOI = expected improvement from observing signal | Bayesian decision theory |
| P12 | Causal vs Evidential Decision Theory | PRINCIPLE | CDT (causal intervention) vs EDT (conditional evidence) | Expected utility, causal reasoning |
| P13 | Proper Scoring Rules | PRINCIPLE | Honest reporting maximizes expected score | Probability, expected utility |
| P14 | Jeffrey's Rule | PRINCIPLE | Update beliefs under uncertain evidence | Bayes' theorem, conditional probability |
| P15 | Imprecise Probabilities | PRINCIPLE | Credal sets replace single P; robust decision criteria | Probability, decision theory, ambiguity |
| P16 | Mean Field Games | PRINCIPLE | HJB + Fokker-Planck for large-population strategic equilibrium | Game theory, optimal control, PDEs |
| T17 | Revenue Equivalence | THEOREM | All standard auctions yield same expected revenue under IPV | Expected utility, mechanism design |
| T18 | Secretary Problem | THEOREM | Optimal 1/e stopping rule; reject first n/e, then take best-so-far | Probability, optimal stopping |
| P17 | Info-Gap Decision Theory | PRINCIPLE | Robustness to severe uncertainty via maximizing horizon of uncertainty for satisficing | Decision theory, robustness |
| P18 | Algorithmic Decision Theory | PRINCIPLE | Computational constraints on decision-making; bounded rationality formalized | Decision theory, complexity theory |
| P23 | Imprecise Probabilities (Walley) | PRINCIPLE | Credal sets replace point probabilities; Choquet EU captures ambiguity aversion | Expected utility; Bayesian decision theory |
| P24 | Bounded Rationality (Simon/Sims) | PRINCIPLE | Rational inattention: optimal info acquisition under Shannon capacity constraints | Expected utility; information theory |
| P25 | Ambiguity Aversion and Maxmin Expected Utility (Gilboa-Schmeidler) | PRINCIPLE | max_{P in C} min_{P} E_P[u]; axiomatizes decision under ambiguity via multiple priors | Savage's axioms; Ellsberg paradox; convex analysis |
| P26 | Optimal Stopping Theory (Generalized) | PRINCIPLE | Snell envelope and Gittins index characterize optimal stopping in Markov and bandit settings | Bayesian decision theory; martingale theory; dynamic programming |
| P27 | Causal Decision Theory (Pearl-Halpern) | PRINCIPLE | Decisions via do-calculus interventions on structural equation models; resolves Newcomb's Problem | Bayesian decision theory; CDT vs EDT; VNM utility |
| P28 | Cooperative AI and Multi-Principal Decision Theory | PRINCIPLE | AI agents serving multiple principals with conflicting objectives; CIRL and assistance games | VNM utility; AI alignment; Bayesian decision theory |

### PRINCIPLE 15: Imprecise Probabilities and Robust Bayesianism

**Formal Statement:**
Imprecise probability theory generalizes standard probability by replacing a single probability measure P with a set of probability measures P (a credal set). A lower probability P_*(A) = inf_{P ∈ P} P(A) and upper probability P*(A) = sup_{P ∈ P} P(A) bound the agent's uncertainty about event A. Decision criteria include: Gamma-maximin (maximize minimum expected utility over P), maximality (choose a if no b has higher expected utility under every P ∈ P), and E-admissibility (choose a if a maximizes expected utility under some P ∈ P). The theory encompasses: Dempster-Shafer belief functions, interval-valued probabilities, and Walley's theory of coherent lower previsions.

**Plain Language:**
Standard probability theory assumes you have a single precise probability for every event. But often, you genuinely don't know enough to assign a precise number. Imprecise probability theory allows you to say "the probability is between 0.3 and 0.7" rather than being forced to pick 0.5. It provides rigorous decision rules for acting under this deeper form of uncertainty, bridging the gap between probability theory and robust decision-making.

**Historical Context:**
Boole (1854, interval probabilities), Koopman (1940, comparative probability), Smith (1961), Walley (1991, *Statistical Reasoning with Imprecise Probabilities*). Levi (1974, E-admissibility). The theory has gained prominence in AI safety, climate science, and engineering reliability, where precise probability assignments are unjustified.

**Depends On:**
- Probability theory (Kolmogorov axioms)
- Decision theory (VNM axioms, Savage's axioms)
- Ellsberg paradox / ambiguity aversion (Principle 6)

**Implications:**
- Provides a rigorous framework for decision-making when precise probabilities cannot be justified (Knightian uncertainty)
- Applications in robust control, AI safety (where model uncertainty is critical), and climate policy under deep uncertainty
- Generalizes Bayesian decision theory: a singleton credal set recovers standard Bayesian analysis
- Connects to robust optimization, distributionally robust optimization, and worst-case analysis in machine learning

---

### PRINCIPLE 16: Mean Field Games

**Formal Statement:**
Mean field game (MFG) theory studies strategic decision-making in large populations of rational agents, where each agent interacts with the aggregate behavior (mean field) of the population rather than with individual agents. In the continuous-time formulation, a representative agent solves a Hamilton-Jacobi-Bellman (HJB) equation for optimal control: -∂_t u - H(x, ∇u, m) = 0, coupled to a Fokker-Planck (FP) equation for the population distribution: ∂_t m - div(m ∇_p H) - σ²Δm = 0, where u is the value function, m(x,t) is the population density, H is the Hamiltonian, and σ is the diffusion coefficient. The MFG equilibrium is a fixed point: each agent optimizes given m, and m is consistent with optimal behavior.

**Plain Language:**
When millions of agents make strategic decisions simultaneously (commuters choosing routes, traders choosing portfolios, firms setting prices), tracking every individual interaction is impossible. Mean field game theory replaces these individual interactions with the statistical average of the population, producing a tractable pair of coupled equations. The solution describes the equilibrium behavior of the entire population and the optimal strategy for a representative individual.

**Historical Context:**
Independently introduced by Lasry and Lions (2006-2007) and Huang, Malhame, and Caines (2006). Lions (Fields Medal 2010, partly for contributions to MFG). The theory draws on optimal control, PDEs, probability, and game theory. Applications have grown rapidly in economics, finance, epidemiology, and crowd dynamics.

**Depends On:**
- Game theory (Nash equilibrium)
- Optimal control theory, Hamilton-Jacobi-Bellman equations
- Probability theory (stochastic differential equations)

**Implications:**
- Models large-scale strategic interactions in economics (heterogeneous agent models), finance (high-frequency trading, systemic risk), and urban planning (traffic flow)
- Epidemic modeling: MFG describes individual vaccination/social distancing decisions coupled to disease dynamics
- Crowd dynamics and evacuation modeling: agents choose paths considering aggregate crowd density
- Connects to deep reinforcement learning: multi-agent RL with mean field approximation scales to large populations

---

---

### THEOREM 17: Revenue Equivalence Theorem

**Formal Statement:**
Consider n risk-neutral bidders with independent private values drawn from the same continuous distribution F on [0, omega]. Any two auction mechanisms that (1) always allocate the item to the bidder with the highest value and (2) give zero expected payment to a bidder with value 0 yield the same expected revenue to the seller and the same expected payment by each bidder type. Specifically, the expected payment of a bidder with value v is: m(v) = v F(v)^{n-1} - integral_0^v F(t)^{n-1} dt, regardless of the auction format. Consequently, the first-price sealed-bid, second-price (Vickrey), English, and Dutch auctions all yield the same expected revenue: E[Revenue] = E[second-highest value].

**Plain Language:**
The revenue equivalence theorem is one of the most surprising results in economics: under standard assumptions (risk-neutral bidders, independent private values, same distribution), all "reasonable" auction formats generate exactly the same expected revenue for the seller. It does not matter whether you run an English auction (ascending bids), a Dutch auction (descending price), a first-price sealed bid, or a Vickrey (second-price) auction -- the seller's expected earnings are identical. This profoundly simplifies auction design by showing that, under these conditions, the format is irrelevant.

**Historical Context:**
Vickrey (1961, showed equivalence of several auction formats, Nobel Prize 1996). Myerson (1981, general revenue equivalence theorem and optimal auction design) and Riley and Samuelson (1981) independently proved the general result. The theorem fails when its assumptions are relaxed: risk aversion, affiliated values, asymmetric bidders, or collusion all break revenue equivalence, leading to a rich theory of optimal mechanism design.

**Depends On:**
- Expected utility theory (Axiom System 1)
- Bayesian games (Game Theory: Principle 10)
- Mechanism design (Game Theory: Principle 3)

**Implications:**
- Under the theorem's assumptions, auction format selection is irrelevant for expected revenue -- designers should focus on other criteria (simplicity, robustness, collusion resistance)
- When revenue equivalence fails (risk aversion, correlated values), specific formats dominate: Milgrom-Weber (1982) showed that English auctions raise more revenue with affiliated values
- Myerson's optimal auction (which maximizes revenue by setting a reserve price) builds directly on revenue equivalence
- Applications in spectrum auctions, online advertising (Google, Meta), procurement, and treasury bond sales

---

### THEOREM 18: The Secretary Problem (Optimal Stopping)

**Formal Statement:**
In the secretary problem, n candidates arrive in random order. After interviewing each, you must immediately accept or reject. The goal is to maximize the probability of selecting the best overall candidate. The optimal strategy: reject the first k* = floor(n/e) candidates (the "observation phase"), then accept the first subsequent candidate who is better than all previous ones. This strategy selects the best candidate with probability approaching 1/e ~ 36.8% as n -> infinity. More precisely, the optimal stopping time tau* satisfies: P(X_{tau*} = best) -> 1/e and the optimal threshold k*/n -> 1/e. For the variant where the objective is to maximize the expected rank, the optimal strategy differs and achieves expected rank ~ 3.87 for large n.

**Plain Language:**
You are interviewing candidates one by one, and after each interview you must decide: hire this person or move on. You cannot go back to previous candidates. The optimal strategy is to interview and reject roughly the first 37% of candidates (using them to calibrate your standards), then hire the first person who exceeds all those you have seen. This simple strategy gives you about a 37% chance of getting the absolute best candidate -- surprisingly good odds given that you have no advance information and cannot reconsider.

**Historical Context:**
First published by Lindley (1961), also known as the "marriage problem" or "Googol game." The 1/e law was proved by Dynkin (1963). The problem has generated an enormous literature with variants: multiple choices, random n, partial recall, group interviews, and cost-based objectives. It is the canonical problem of optimal stopping theory and has applications in hiring, house-buying, parking, and online algorithms.

**Depends On:**
- Probability theory, order statistics
- Dynamic programming, backward induction
- Optimal stopping theory (Wald)

**Implications:**
- Establishes the 1/e rule as a benchmark for online selection problems where decisions are irrevocable
- The threshold strategy generalizes to prophet inequalities (Krengel-Sucheston 1977): an online player can achieve at least 1/2 the expected reward of a "prophet" who sees all values in advance
- Applications in online algorithms: competitive ratios for secretary-type problems appear in online ad auctions, resource allocation, and streaming algorithms
- The Bayesian generalization (Bruss 2000, "odds algorithm") provides an explicit optimal stopping rule for general independent observations

---

### PRINCIPLE 17: Info-Gap Decision Theory

**Formal Statement:**
Info-gap decision theory (IGDT) addresses decision-making under severe (Knightian) uncertainty, where the probability distribution over uncertain parameters is unknown and the uncertainty may be unbounded. Given a decision q, a performance requirement r_c (satisficing threshold), and an info-gap uncertainty model U(α, ũ) = {u : |u - ũ| ≤ α} (a nested family of sets expanding with the horizon of uncertainty α ≥ 0 around a nominal estimate ũ), the robustness function is: α̂(q, r_c) = max{α ≥ 0 : max_{u ∈ U(α,ũ)} R(q,u) ≤ r_c}, measuring the greatest horizon of uncertainty α under which decision q still satisfies the performance requirement. The opportuneness function β̂(q, r_w) = min{α ≥ 0 : min_{u ∈ U(α,ũ)} R(q,u) ≤ r_w} measures the minimum uncertainty needed for a windfall outcome r_w. The decision principle: choose q to maximize robustness α̂(q, r_c), sacrificing optimality for robustness.

**Plain Language:**
When you face deep uncertainty -- you do not even know the probabilities, and your estimates could be wildly wrong -- standard expected utility theory has nothing to stand on. Info-gap theory takes a different approach: instead of maximizing expected payoff, you ask "how wrong can my estimate be before my decision fails?" and choose the decision that tolerates the most error. This is like choosing a route that gets you to your destination even if the map is somewhat wrong, rather than the route that is fastest only if the map is perfectly accurate. It prioritizes robustness over optimality.

**Historical Context:**
Yakov Ben-Haim (2001, 2006, *Info-Gap Decision Theory: Decisions Under Severe Uncertainty*). Developed initially for structural engineering under uncertainty (how robust is a bridge design to unknown loads?) and extended to ecology, economics, military planning, and climate policy. Related to robust optimization (Ben-Tal, El Ghaoui, Nemirovski) and robust satisficing (Schwartz 2011).

**Depends On:**
- Decision theory fundamentals (utility, preferences)
- Satisficing (Herbert Simon)
- Set-based uncertainty models

**Implications:**
- Provides a principled framework when probabilities are unavailable or unreliable (climate change policy, pandemic response, national security)
- The robustness-opportuneness tradeoff: more robust decisions typically sacrifice upside potential (a formalized version of the conservatism-opportunity tradeoff)
- Applications in ecology (species conservation under climate uncertainty), water resource management, and structural engineering
- Contrasts with Bayesian approaches: IGDT does not require prior distributions and is appropriate for deep uncertainty

---

### PRINCIPLE 18: Algorithmic Decision Theory

**Formal Statement:**
Algorithmic decision theory studies decision-making when computational constraints are explicitly modeled. A computationally bounded agent with resource bound t (time, space, or sample complexity) faces a decision problem (S, A, u, P) where S is the state space, A the action space, u the utility function, and P the prior. The agent must select a ∈ A using a decision procedure D_t that runs in at most t steps. Key results: (1) Bounded optimality (Russell & Subramanian, 1995): the optimal program for an agent is one that maximizes expected utility given its computational architecture and resource constraints. (2) Computational complexity of Bayesian updating: exact Bayesian inference is #P-hard in general (Cooper 1990); approximate inference (MCMC, variational methods) introduces systematic errors. (3) Computational considerations in mechanism design: an auction mechanism must be both incentive-compatible and computationally tractable for bidders; combinatorial auctions are NP-hard, motivating polynomial-time approximation mechanisms. (4) Rational metareasoning (Horvitz 1989, Russell & Wefald 1991): the agent decides how much computation to perform before acting, treating computation itself as a decision with costs and benefits.

**Plain Language:**
Classical decision theory assumes the decision-maker has unlimited computational power to evaluate all options and compute optimal strategies. In reality, computation takes time and effort. Algorithmic decision theory explicitly models these constraints: a chess player cannot compute the game tree to the end, a bidder in a complex auction cannot solve an NP-hard optimization, and even Bayesian updating is computationally intractable for complex models. This theory asks: what is the best decision you can make given your computational limitations? It bridges decision theory, computer science, and artificial intelligence.

**Historical Context:**
Herbert Simon (1955, bounded rationality and satisficing). Russell and Subramanian (1995, bounded optimality). Papadimitriou and Yannakakis (1994, computational complexity of game-theoretic solution concepts). Nisan and Ronen (1999, algorithmic mechanism design). Lipton and Markakis (2004, computational aspects of Nash equilibria). The field has grown with AI: modern large language models and reinforcement learning agents face algorithmic decision problems at scale.

**Depends On:**
- Expected utility theory (Axiom System 1)
- Computational complexity (P, NP, #P)
- Bayesian decision theory (Principle 8)

**Implications:**
- Explains why human and artificial agents use heuristics: optimal computation of the optimal decision is itself computationally intractable
- Algorithmic mechanism design ensures that game-theoretic mechanisms (auctions, voting) remain computationally tractable for participants
- Rational metareasoning (deciding how long to think) is fundamental to AI systems that must balance computation time against action quality
- Connects bounded rationality (Simon) to formal complexity theory: cognitive limitations can be modeled as computational resource constraints

---

### PRINCIPLE 19: Logical Decision Theory and Functional Decision Theory

**Formal Statement:**
Functional Decision Theory (FDT; Yudkowsky and Soares, 2018) and its predecessor Timeless Decision Theory (TDT; Yudkowsky, 2010) propose that rational agents should make decisions by considering the output of their decision procedure as a mathematical function, choosing the action that maximizes expected utility conditional on the logical fact that the agent's decision algorithm outputs that action. The decision is modeled as: choose a such that E[U | DA() = a] is maximized, where DA is the agent's decision algorithm. FDT differs from Causal Decision Theory (CDT) and Evidential Decision Theory (EDT) in problems involving logical correlations between agents. Key examples: (1) Newcomb's problem: FDT one-boxes (like EDT) because the agent's decision algorithm determines the predictor's action. (2) Prisoner's dilemma against a copy: FDT cooperates because both copies run the same decision algorithm. (3) Parfit's hitchhiker: FDT commits to paying because the driver's prediction depends on the agent's decision procedure. FDT provides a unified resolution to decision-theoretic paradoxes by conditioning on the logical output of the decision procedure rather than on causal or evidential connections.

**Plain Language:**
Standard decision theory comes in two flavors: causal (act based on what your actions cause) and evidential (act based on what your actions tell you about the world). Both fail on some puzzles. Functional Decision Theory offers a third approach: decide as if you are choosing the output of your decision algorithm, knowing that other agents may be running the same or similar algorithms. If you are playing Prisoner's Dilemma against a copy of yourself, your decision determines your copy's decision too, so you should cooperate. FDT handles paradoxes like Newcomb's problem and Parfit's hitchhiker more coherently than either CDT or EDT.

**Historical Context:**
Nozick (1969) formalized Newcomb's problem. Gibbard and Harper (1978) developed CDT. Jeffrey (1965) developed EDT. Yudkowsky (2010) proposed Timeless Decision Theory. Yudkowsky and Soares (2018, MIRI) formalized FDT. The theory is motivated by AI alignment: advanced AI systems may face decision problems involving predictions of their own behavior, logical correlations with other agents, and self-referential reasoning.

**Depends On:**
- Expected utility theory (Axiom System 1)
- Causal and evidential decision theory
- Computational decision theory

**Implications:**
- Provides a unified resolution to decision-theoretic paradoxes (Newcomb, Prisoner's Dilemma with copies, Parfit's hitchhiker)
- Directly relevant to AI alignment: AI systems must handle problems involving predictions of their own behavior
- Challenges the CDT/EDT dichotomy that has dominated decision theory for decades
- Raises foundational questions about the nature of agency, causation, and logical counterfactuals

---

### PRINCIPLE 20: Rational Inattention (Sims)

**Formal Statement:**
Rational inattention theory (Sims, 2003; Matejka and McKay, 2015) models decision-makers who face information processing costs measured by Shannon mutual information. The agent chooses a signal structure (information acquisition strategy) to maximize expected utility minus information cost: max_{P(s|omega)} E[u(a(s), omega)] - lambda * I(omega; s), where omega is the state, s is the signal, a(s) is the action, and I(omega; s) is the mutual information between the state and the signal. Key results: (1) Optimal attention allocation follows a posterior-based logit model: the probability of choosing action a is proportional to exp(u(a, omega)/lambda), reproducing the multinomial logit as a rational information-processing outcome (Matejka and McKay, 2015). (2) Agents rationally ignore information about states that have small utility differences, explaining inattention as optimal rather than irrational. (3) Entropy reduction as the cost metric captures the idea that the difficulty of acquiring information depends on how much uncertainty it resolves. (4) Applications: pricing behavior (firms adjust prices sluggishly because processing price information is costly), portfolio choice (investors under-diversify), and macroeconomic dynamics (sticky information models).

**Plain Language:**
Paying attention is costly. Every piece of information you process takes mental effort, and rational inattention theory says decision-makers optimally choose what to pay attention to and what to ignore. A consumer does not compare every price at the grocery store -- they focus on the items where the savings matter most. This is not irrationality; it is optimal given limited information-processing capacity. Remarkably, when you model attention costs using Shannon's mutual information, the resulting choice behavior looks exactly like the logit model that economists and psychologists have used for decades, providing a deep theoretical foundation for observed choice patterns.

**Historical Context:**
Christopher Sims (2003, Nobel Prize 2011) introduced rational inattention. Matejka and McKay (2015) derived the logit model as the optimal solution. The theory provides microfoundations for sticky prices in macroeconomics (Mackowiak and Wiederholt, 2009), inattentive consumers (Gabaix, 2014), and limited attention in financial markets. It connects information theory to behavioral economics and decision theory.

**Depends On:**
- Expected utility theory (Axiom System 1)
- Shannon information theory (mutual information)
- Bayesian decision theory (Principle 8)

**Implications:**
- Provides a rational foundation for "irrational" behaviors like inattention, price stickiness, and under-diversification
- The information-theoretic cost function (mutual information) gives a principled measure of attention costs
- The logit model emerges as the unique optimal choice rule under rational inattention, providing deep foundations for discrete choice econometrics
- Connects information theory to macroeconomics, explaining sluggish price adjustment and business cycle dynamics

---

### PRINCIPLE 21 — Moral Uncertainty and Intertheoretic Value Comparison

**Formal Statement:**
Moral uncertainty arises when an agent has positive credence in multiple moral theories. Given theories T_1,...,T_n with credences p_i and value functions V_i, the agent chooses a* = argmax_a sum_i p_i * V_i(a) (expected moral value maximization, MacAskill 2014). Intertheoretic comparability is required: how to normalize V_i across theories. When comparability fails, alternatives include parliamentary models, moral hedging, and ordinal aggregation.

**Plain Language:**
We are often uncertain which ethical theory is correct. Moral uncertainty theory provides a principled framework for decision-making when ethical theories conflict, analogous to expected utility under factual uncertainty. This is directly relevant to AI alignment.

**Historical Context:**
Lockhart (2000). MacAskill, Bykvist, and Ord (2020). Central to AI alignment since AI systems must navigate moral uncertainty rather than commit to a single ethic.

**Depends On:**
- Expected Utility Theory (Axiom System 1)
- Bayesian Decision Theory (Principle 8)

**Implications:**
- Provides principled framework for ethical decision-making under normative uncertainty
- Central to AI alignment design
- Intertheoretic comparability remains a fundamental open problem

---

### PRINCIPLE 22 — AI Alignment Decision Theory (CIRL and Assistance Games)

**Formal Statement:**
Cooperative Inverse Reinforcement Learning (CIRL, Hadfield-Menell et al. 2016) models human-AI interaction as a cooperative game where the AI's reward depends on the human's unknown reward function. The AI infers preferences from observations while maximizing the human's utility. Corrigibility: the AI allows shutdown/modification because its uncertainty about human preferences makes deferring to oversight utility-maximizing. Russell's (2019) assistance games generalize: the AI maximizes the human's utility, not its own, preventing instrumental convergence toward self-preservation.

**Plain Language:**
How should AI systems be designed to remain under human control? By making them uncertain about what humans want and designing them to learn preferences through interaction. This uncertainty ensures the AI is willing to be corrected -- it is not confident enough in its goals to resist.

**Historical Context:**
Russell (2019, *Human Compatible*). Hadfield-Menell et al. (2016, CIRL). Soares et al. (2015, corrigibility). Bostrom (2014, instrumental convergence).

**Depends On:**
- Expected Utility Theory (Axiom System 1)
- Moral Uncertainty (Principle 21)

**Implications:**
- Provides mathematical foundation for designing AI that remains under human control
- Uncertainty about values is a feature ensuring deference to humans
- Addresses instrumental convergence through structural design rather than constraints

---

### PRINCIPLE 23 — Imprecise Probabilities and Robust Bayesianism

**Formal Statement:**
Imprecise probability theory (Walley 1991) generalizes classical probability by replacing a single probability measure P with a convex set of probability measures (credal set) C = {P : P satisfies constraints}. Lower probability P_*(A) = inf_{P in C} P(A) and upper probability P*(A) = sup_{P in C} P(A) bound beliefs when a unique prior cannot be justified. Desirability: a gamble f is desirable if inf_{P in C} E_P[f] > 0 (E-admissibility) or if f is undominated (Gamma-maximin). Choquet expected utility with non-additive capacities (Schmeidler 1989) captures ambiguity aversion, explaining the Ellsberg paradox. The theory of coherent lower previsions (Walley 1991) provides the most general consistent framework, subsuming Dempster-Shafer belief functions, possibility theory, and interval probabilities. Applications: robust Bayesian inference uses epsilon-contamination neighborhoods; climate risk assessment under deep uncertainty uses imprecise probabilities to represent model disagreement.

**Plain Language:**
Classical probability requires you to assign exact numbers to your beliefs, but often you genuinely do not know enough to pick a single probability. Imprecise probabilities let you say "the probability is somewhere between 30% and 70%" and make decisions accordingly. This captures real-world ambiguity — the kind of uncertainty where you do not even know the odds — and explains why people behave differently when facing known risks versus genuine uncertainty (the Ellsberg paradox).

**Historical Context:**
Keynes (1921) and Knight (1921) distinguished risk from uncertainty. Ellsberg (1961) demonstrated ambiguity aversion. Dempster (1967) and Shafer (1976) developed belief functions. Walley (1991, *Statistical Reasoning with Imprecise Probabilities*) provided the definitive framework. Schmeidler (1989) axiomatized Choquet expected utility. The Society for Imprecise Probability (ISIPTA) was founded in 1999. Applications to AI safety and climate economics are growing rapidly.

**Depends On:**
- Expected Utility Theory (Axiom System 1)
- Bayesian Decision Theory (Principle 8)

**Implications:**
- Provides a principled framework for decision-making under deep uncertainty (climate, AI safety)
- Explains Ellsberg paradox and ambiguity-averse behavior that classical theory cannot
- Robust Bayesian methods protect against prior misspecification in machine learning
- Foundation for cautious AI systems that recognize and act on their own uncertainty

---

### PRINCIPLE 24 — Bounded Rationality and Computational Decision Theory

**Formal Statement:**
Bounded rationality (Simon 1955) recognizes that agents have limited cognitive and computational resources. The theory of rational inattention (Sims 2003) models agents as optimally allocating finite information-processing capacity: an agent with Shannon capacity kappa bits/period optimally acquires information by solving max_{P(a|s)} E[u(a,s)] - lambda * I(S;A), where I(S;A) is the mutual information between states and actions. This produces logit-like choice probabilities: P(a|s) ~ exp(u(a,s)/lambda). Satisficing (Simon 1956): agents choose the first option exceeding an aspiration level rather than maximizing. Resource-rational analysis (Lieder and Griffiths 2020): cognitive biases are optimal strategies under computational constraints — the brain is doing the best it can with limited time and energy. Computationally bounded agents face the "value of computation" problem: deciding how much to think before acting.

**Plain Language:**
Real decision-makers are not omniscient calculators. They have limited time, attention, and brainpower. Bounded rationality theory takes these limits seriously: instead of asking "what is the optimal decision?" it asks "what is the best decision you can make given your cognitive limitations?" The surprising finding is that many apparent "biases" in human thinking are actually rational adaptations to computational constraints — the brain is efficiently allocating its scarce processing resources.

**Historical Context:**
Simon (1955, 1956) introduced bounded rationality and satisficing (Nobel Prize 1978). Sims (2003) developed rational inattention (Nobel Prize 2011). Kahneman and Tversky (1979) documented cognitive biases. Lieder and Griffiths (2020) proposed resource rationality as a unifying framework. Papadimitriou and Yannakakis (1994) connected to computational complexity: finding Nash equilibria is PPAD-complete even for two players.

**Depends On:**
- Expected Utility Theory (Axiom System 1)
- Information Theory (Shannon Entropy)

**Implications:**
- Explains cognitive biases as rational adaptations to computational constraints
- Rational inattention models explain sticky prices, portfolio inertia, and political ignorance
- Foundation for AI systems that allocate computational resources optimally (meta-reasoning)
- Connects decision theory to information theory and computational complexity

---

### PRINCIPLE 25 — Maxmin Expected Utility and Ambiguity Aversion (Gilboa-Schmeidler)

**Formal Statement:**
Maxmin Expected Utility (MEU, Gilboa-Schmeidler 1989) axiomatizes decision-making under ambiguity (Knightian uncertainty). The decision-maker evaluates an act f by V(f) = min_{P in C} E_P[u(f)], where C is a closed convex set of probability measures (the "credal set") and u is a VNM utility function. The axioms replace Savage's sure-thing principle with: (1) certainty independence: mixing with a constant act preserves preference, (2) uncertainty aversion: if f ~ g, then alpha*f + (1-alpha)*g >= f. This captures the Ellsberg paradox: agents prefer known to unknown probabilities. Generalizations: alpha-MEU interpolates between optimism and pessimism: V(f) = alpha * min_{P in C} E_P[u(f)] + (1-alpha) * max_{P in C} E_P[u(f)]. Maccheroni, Marinacci, and Rustichini (2006) developed variational preferences: V(f) = min_P {E_P[u(f)] + c(P)} with convex penalty function c. The smooth ambiguity model (Klibanoff, Marinacci, Mukerji 2005) uses V(f) = E_mu[phi(E_P[u(f)])] with concave phi capturing ambiguity attitude.

**Plain Language:**
When you do not know the exact probabilities — like betting on an urn with unknown composition — standard expected utility theory says you should not care. But real people strongly prefer known probabilities (the Ellsberg paradox). Maxmin expected utility explains this rationally: the decision-maker considers a whole set of possible probability distributions and optimizes against the worst case. The degree of ambiguity aversion reflects how cautious the agent is about unknown probabilities.

**Historical Context:**
Ellsberg (1961) demonstrated ambiguity aversion experimentally. Gilboa and Schmeidler (1989) axiomatized maxmin EU. Epstein (1999) distinguished ambiguity aversion from risk aversion. Maccheroni et al. (2006) generalized to variational preferences. Klibanoff et al. (2005) introduced smooth ambiguity. Applications span financial economics (portfolio choice under model uncertainty), climate policy (deep uncertainty about damages), and robust control theory (Hansen and Sargent 2008).

**Depends On:**
- Ellsberg Paradox (Principle 6)
- Expected Utility Theory (Axiom System 1)
- Bayesian Decision Theory (Principle 8)

**Implications:**
- Provides a rigorous foundation for decision-making under deep uncertainty (unknown unknowns)
- Explains portfolio under-diversification and home bias in finance via ambiguity aversion
- Foundation for robust control theory: Hansen and Sargent's model uncertainty framework
- Guides climate and pandemic policy where probability distributions are genuinely unknown

---

### PRINCIPLE 26 — Gittins Index and Optimal Stopping in Bandit Problems

**Formal Statement:**
The Gittins Index Theorem (Gittins and Jones 1974, Gittins 1979) solves the multi-armed bandit problem: a decision-maker must sequentially allocate resources among projects (arms) to maximize total discounted reward. Despite the exponential state space, the optimal policy has a simple index form: at each time, play the arm with the highest Gittins index. The index for arm i in state s is nu_i(s) = sup_{tau > 0} E[sum_{t=0}^{tau-1} beta^t R_i(t) | s] / E[sum_{t=0}^{tau-1} beta^t | s], interpretable as the "fair subsidy" for not playing. For continuous-time diffusion bandits, the index satisfies a free-boundary PDE. Extensions: Whittle's restless bandit index (1988) extends to arms that evolve when not played (NP-hard optimal policy, but the Whittle index policy is near-optimal). Thompson sampling (1933, rediscovered 2012) provides a Bayesian alternative with optimal regret bounds. The explore-exploit tradeoff is fundamental: UCB algorithms achieve O(sqrt(KT log T)) regret for K arms over T rounds.

**Plain Language:**
Imagine you are in a casino with many slot machines, each with unknown payoff rates. How do you balance trying new machines (exploring) versus sticking with the best one you have found (exploiting)? The Gittins index gives the optimal answer: assign each machine a single number based on your current beliefs, and always play the highest-numbered machine. This elegant solution reduces an impossibly complex planning problem to a simple ranking, and the same principle applies to clinical trials, online advertising, and any sequential resource allocation under uncertainty.

**Historical Context:**
Robbins (1952) formulated the multi-armed bandit problem. Gittins and Jones (1974) discovered the index, initially classified as military research. Gittins (1979) published the theorem. Whittle (1988) extended to restless bandits. Auer et al. (2002) developed UCB algorithms. Thompson sampling (1933) was rediscovered and proved optimal by Agrawal and Goyal (2012). Bandit algorithms now power recommendation systems, clinical trials, and A/B testing at scale.

**Depends On:**
- Bayesian Decision Theory (Principle 8)
- Value of Information (Principle 11)
- Dynamic Programming (via Bellman equation)

**Implications:**
- Provides the optimal solution to the explore-exploit tradeoff in sequential decision-making
- Foundation for adaptive clinical trials, recommendation systems, and online advertising
- Whittle index extends to restless bandits (NP-hard in general, but tractable approximation)
- Thompson sampling and UCB algorithms power modern A/B testing and personalization

---

### PRINCIPLE 27 — Causal Decision Theory with Structural Equations (Pearl-Halpern)

**Formal Statement:**
Structural Causal Decision Theory (Pearl 2000; Halpern 2016) formalizes decision-making using structural equation models (SEMs). A structural causal model M = (U, V, F, P(U)) consists of exogenous variables U with distribution P(U), endogenous variables V, and structural equations V_i = f_i(pa_i, U_i) determining each endogenous variable from its parents and noise. An intervention do(X = x) replaces the equation for X with the constant x, producing a modified model M_x. The expected utility of action a is EU(a) = E_{M_{do(A=a)}}[U(Y)] where Y is the outcome and U is the utility function. This resolves Newcomb's Problem and the Smoking Lesion: interventional probabilities P(Y | do(A=a)) differ from conditional probabilities P(Y | A=a) exactly when confounding exists. Halpern and Pass (2017) extend to game-theoretic settings where players reason about structural interventions. The Causal Influence Diagram (CID) framework (Everitt et al. 2021) uses graphical models for multi-agent decision problems with causal reasoning.

**Plain Language:**
Traditional decision theory asks "what is the probability of the outcome if I observe myself taking this action?" Causal decision theory instead asks "what would happen if I intervened to take this action?" The difference matters when your action is correlated with the outcome for reasons other than causation. Structural equation models make this precise: they encode the causal mechanisms of the world, and "doing" something means surgically changing one mechanism while leaving the rest intact. This is the foundation for making decisions in a world where correlation and causation diverge.

**Historical Context:**
Lewis (1981) and Gibbard and Harper (1978) formulated counterfactual causal decision theory. Pearl (2000) provided the structural equation formalization via do-calculus. Halpern (2016) developed the formal framework connecting structural models to decision theory. Joyce (1999) provided philosophical foundations for causal decision theory. Everitt et al. (2021, DeepMind) developed causal influence diagrams for AI safety applications. The framework is now central to AI alignment: ensuring AI agents reason causally about the effects of their actions.

**Depends On:**
- Bayesian Decision Theory (Principle 8)
- Causal Decision Theory vs Evidential (Principle 12)
- Von Neumann-Morgenstern Utility (Axiom System 1)

**Implications:**
- Resolves classic decision-theoretic paradoxes (Newcomb, Smoking Lesion) by distinguishing intervention from observation
- Provides formal foundations for AI systems that must reason about the causal effects of their actions
- Connects decision theory to Pearl's causal inference framework, enabling data-driven decision-making
- Essential for AI safety: agents must understand whether they are causing outcomes or merely predicting them

---

### PRINCIPLE 28 — Cooperative AI and Multi-Principal Decision Theory

**Formal Statement:**
Multi-principal decision theory (Dafoe et al. 2020, 2021) formalizes decision-making by AI agents serving multiple principals (humans or organizations) with potentially conflicting objectives. The agent's objective is a social welfare function W: U^n -> R over the utility functions u_1, ..., u_n of n principals, subject to individual rationality constraints W(u) >= W_i^0 for each principal's reservation utility. Key frameworks: (1) Cooperative Inverse Reinforcement Learning (CIRL, Hadfield-Menell et al. 2016): the AI and human play a cooperative game where the AI learns the human's utility by observing their actions, yielding behavior that is naturally helpful and deferential. The optimal CIRL policy satisfies: the AI asks clarifying questions when uncertain about human preferences, and defers to the human when its utility estimate has high variance. (2) Bargaining-based delegation (Zhang et al. 2023): when multiple principals disagree, the AI implements a Nash bargaining solution over their preferences. (3) The "assistance game" framework (Russell 2019): the AI's utility is defined as the human's utility, creating an inherently cooperative structure.

**Plain Language:**
When an AI assistant serves multiple people or organizations with different goals, whose preferences should it follow? Multi-principal decision theory addresses this fundamental challenge. Instead of optimizing a single objective, the AI must balance competing interests fairly. One elegant solution: the AI explicitly does not know its own objective and must learn it by observing human behavior, which naturally makes it ask questions when unsure and defer to humans on value-laden decisions. This "cooperative" framing avoids the dangers of an AI that confidently pursues the wrong goal.

**Historical Context:**
Russell (2019, *Human Compatible*) proposed assistance games as the foundation for beneficial AI. Hadfield-Menell et al. (2016) formalized CIRL. Dafoe et al. (2020, 2021, DeepMind) developed the cooperative AI framework. Zhang et al. (2023) applied bargaining theory to multi-stakeholder AI. The multi-principal problem becomes increasingly urgent as AI agents are deployed in contexts (healthcare, law, governance) where they serve multiple parties with conflicting interests.

**Depends On:**
- Von Neumann-Morgenstern Utility (Axiom System 1)
- AI Alignment Decision Theory (Principle 22)
- Bayesian Decision Theory (Principle 8)

**Implications:**
- Provides theoretical foundations for AI systems that serve multiple stakeholders with conflicting objectives
- CIRL's key insight: uncertainty about the objective function produces naturally helpful and deferential AI behavior
- Essential for deploying AI in multi-stakeholder settings (healthcare, governance, organizations)
- Connects decision theory to AI alignment: the structure of the decision problem shapes whether AI is safe

---

### PRINCIPLE 29 — Hyperbolic Discounting and Intertemporal Choice

**Formal Statement:**
Hyperbolic discounting (Ainslie 1975; Laibson 1997) describes the empirically observed pattern where agents discount future rewards at a decreasing rate, producing time-inconsistent preferences. The quasi-hyperbolic model (Laibson 1997): U_t = u_t + beta * sum_{k=1}^{T-t} delta^k * u_{t+k}, where beta in (0,1) captures present bias (immediate over-weighting) and delta in (0,1) is the long-run discount factor. For beta < 1, the agent exhibits present bias: at time t, he prefers $100 today over $110 tomorrow, but at time t-30, he prefers $110 at t+1 over $100 at t — violating time consistency. O'Donoghue and Rabin (1999): sophisticated agents (aware of their future present bias) use commitment devices; naive agents (unaware) procrastinate. The Strotz-Pollak equilibrium (1955, 1968): the agent's current self plays a sequential game against future selves, yielding a subgame perfect equilibrium where each self best-responds to anticipated future behavior.

**Plain Language:**
Standard economics assumes people discount the future at a constant rate — they are equally patient about delays at any point in time. Hyperbolic discounting captures what actually happens: people are very impatient about immediate delays but much more patient about delays in the distant future. You might prefer $100 now over $110 tomorrow, but also prefer $110 in 31 days over $100 in 30 days — even though both involve waiting one day. This "present bias" explains procrastination, under-saving for retirement, addiction, and the demand for commitment devices (like automatic savings plans or deadlines).

**Historical Context:**
Strotz (1955) first analyzed time-inconsistent preferences. Ainslie (1975) documented hyperbolic discounting in humans and animals. Laibson (1997) introduced the quasi-hyperbolic model in economics. O'Donoghue and Rabin (1999) analyzed naivete versus sophistication. Thaler and Benartzi (2004) designed the "Save More Tomorrow" program using commitment devices. The framework is central to behavioral economics and has influenced pension policy, health policy, and addiction research.

**Depends On:**
- Expected Utility Theory (Axiom System 1)
- Bayesian Decision Theory (Principle 8)
- Bounded Rationality (Principle 24)

**Implications:**
- Explains procrastination, under-saving, and addiction through a single mechanism: present bias
- Commitment devices (automatic enrollment, deadlines, penalties) are rational responses to anticipated self-control problems
- The Save More Tomorrow program increased retirement savings for millions of workers
- Sophisticated versus naive agents face fundamentally different optimal strategies — self-knowledge matters

---

### PRINCIPLE 30 — Imprecise Probabilities and Decision-Making under Deep Uncertainty

**Formal Statement:**
Imprecise probability theory (Walley 1991; Augustin et al. 2014) generalizes Bayesian decision theory to settings where the agent's beliefs cannot be represented by a single probability distribution. Instead, the agent's epistemic state is a credal set C — a closed convex set of probability distributions. Decision criteria: (1) Gamma-maximin: choose the act maximizing the minimum expected utility over C. (2) E-admissibility (Levi 1974): an act is admissible if it maximizes expected utility for at least one P in C. (3) Maximality: act a is preferred to b iff E_P[u(a)] >= E_P[u(b)] for all P in C with strict inequality for some. The Dempster-Shafer theory of belief functions provides a specific model where upper and lower probabilities are derived from a mass function over a frame of discernment. Robust Bayesian analysis (Berger 1985) studies how conclusions change over a class of priors, yielding sensitivity analysis. Applications: climate policy under deep uncertainty, nuclear safety assessment, and AI systems that must express and reason about uncertainty honestly.

**Plain Language:**
Standard Bayesian reasoning requires a precise probability for every event. But for many real decisions — the probability of a novel pandemic, the chance of AI catastrophe, the risk from climate tipping points — we genuinely do not know enough to assign a single number. Imprecise probabilities formalize this honest uncertainty: instead of a single probability, you work with a set of probabilities capturing everything from the most optimistic to most pessimistic assessments. Decision-making with imprecise probabilities is harder but more honest, and it naturally leads to precautionary behavior when the stakes are high and the uncertainty is deep.

**Historical Context:**
Keynes (1921) and Knight (1921) distinguished risk from uncertainty. Dempster (1967) developed belief functions. Walley (1991, *Statistical Reasoning with Imprecise Probabilities*) provided the comprehensive framework. Augustin et al. (2014, *Introduction to Imprecise Probabilities*) established the modern treatment. Applications to climate policy (IPCC AR6 uses imprecise probabilities for tipping point risk) and AI safety (expressing calibrated uncertainty in AI predictions) are growing.

**Depends On:**
- Bayesian Decision Theory (Principle 8)
- Maxmin Expected Utility (Principle 25)
- Ellsberg Paradox (Principle 6)

**Implications:**
- Formalizes honest expression of deep uncertainty without forcing artificial precision
- Naturally leads to precautionary decision-making when uncertainty is large and stakes are high
- Applications to AI safety: AI systems should express imprecise confidence when evidence is insufficient
- Connects to robust statistics and sensitivity analysis: conclusions that hold across all plausible priors are most trustworthy

---

## References

- Bernoulli, D. (1738). "Specimen Theoriae Novae de Mensura Sortis." *Commentarii Academiae Scientiarum Imperialis Petropolitanae*, 5, 175–192.
- von Neumann, J. & Morgenstern, O. (1944). *Theory of Games and Economic Behavior*. Princeton University Press.
- Savage, L.J. (1954). *The Foundations of Statistics*. Wiley.
- Wald, A. (1950). *Statistical Decision Functions*. Wiley.
- Myerson, R. (1981). "Optimal auction design." *Mathematics of Operations Research*, 6(1), 58–73.
- Luce, R.D. & Raiffa, H. (1957). *Games and Decisions*. Wiley.
- Peterson, M. (2009). *An Introduction to Decision Theory*. Cambridge University Press.
