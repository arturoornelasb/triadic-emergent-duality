"""Statistical rigor module: permutation tests, bootstrap CIs, effect sizes,
and inter-rater agreement metrics for the 63-primitive model validation.

Importable module + standalone runner that applies all tests retroactively
to 7+1 domains (music, chemistry, biology, mathematics, philosophy, physics,
linguistics, + astrology control negative)."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import random
import math
from collections import defaultdict, Counter

# ========== 0. DATA LOADING ==========
DATA_DIR = r'C:\Github\triadic-microgpt\playground\danza_data'

with open(f'{DATA_DIR}/primitivos.json', 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

prims = prim_data['primitivos']
names = [p['nombre'] for p in prims]
deps_map = {p['nombre']: list(p['deps']) for p in prims}
capa_map = {p['nombre']: p['capa'] for p in prims}
name_set = set(names)
all_names_list = list(name_set)

# ######################################################################
#  SECTION 1: REUSABLE STATISTICAL FUNCTIONS
# ######################################################################

def anchor_consistency(anchors, deps_map):
    """Compute anchor consistency: fraction of dependencies within each
    anchor that are also members of the anchor.

    Args:
        anchors: dict mapping anchor_name -> list of primitive names
        deps_map: dict mapping primitive_name -> list of dependency names

    Returns:
        (total_present, total_deps, overall_consistency)
    """
    total_deps = 0
    present_deps = 0
    for anchor_prims in anchors.values():
        anchor_set = set(anchor_prims)
        for prim in anchor_prims:
            for dep in deps_map.get(prim, []):
                total_deps += 1
                if dep in anchor_set:
                    present_deps += 1
    consistency = present_deps / total_deps if total_deps > 0 else 0.0
    return present_deps, total_deps, consistency


def permutation_test(observed_consistency, anchors, all_primitives, deps_map,
                     n_perms=10000, seed=42):
    """Permutation test for anchor consistency.

    Shuffles primitive labels while preserving anchor sizes and dependency
    structure. Counts how often permuted consistency >= observed.

    Args:
        observed_consistency: float, the observed anchor consistency
        anchors: dict mapping anchor_name -> list of primitive names
        all_primitives: list of all primitive names
        deps_map: dict mapping primitive_name -> list of dependency names
        n_perms: number of permutations (default 10000)
        seed: random seed for reproducibility

    Returns:
        dict with keys: p_value, n_perms, null_distribution (list of floats),
        null_mean, null_std
    """
    rng = random.Random(seed)
    prim_list = list(all_primitives)
    anchor_sizes = [len(v) for v in anchors.values()]

    null_dist = []
    n_exceed = 0

    for _ in range(n_perms):
        shuffled = prim_list[:]
        rng.shuffle(shuffled)

        # Build shuffled anchors with same sizes
        total_d = 0
        present_d = 0
        idx = 0
        for size in anchor_sizes:
            anchor_set = set(shuffled[idx:idx + size])
            for prim in anchor_set:
                for dep in deps_map.get(prim, []):
                    total_d += 1
                    if dep in anchor_set:
                        present_d += 1
            idx += size

        perm_consistency = present_d / total_d if total_d > 0 else 0.0
        null_dist.append(perm_consistency)
        if perm_consistency >= observed_consistency:
            n_exceed += 1

    p_value = (n_exceed + 1) / (n_perms + 1)  # +1 for conservative estimate
    null_mean = sum(null_dist) / len(null_dist)
    null_std = (sum((x - null_mean)**2 for x in null_dist) / len(null_dist))**0.5

    return {
        'p_value': p_value,
        'n_perms': n_perms,
        'null_distribution': null_dist,
        'null_mean': null_mean,
        'null_std': null_std,
    }


def bootstrap_ci(anchors, deps_map, n_bootstrap=10000, alpha=0.05, seed=42):
    """Bootstrap confidence interval for anchor consistency.

    Resamples anchors with replacement and recalculates consistency.

    Args:
        anchors: dict mapping anchor_name -> list of primitive names
        deps_map: dict mapping primitive_name -> list of dependency names
        n_bootstrap: number of bootstrap samples (default 10000)
        alpha: significance level (default 0.05 for 95% CI)
        seed: random seed

    Returns:
        dict with keys: ci_lower, ci_upper, alpha, bootstrap_distribution,
        boot_mean, boot_std
    """
    rng = random.Random(seed)
    anchor_list = list(anchors.values())
    n_anchors = len(anchor_list)

    boot_dist = []
    for _ in range(n_bootstrap):
        # Resample anchors with replacement
        sample_indices = [rng.randint(0, n_anchors - 1) for _ in range(n_anchors)]
        total_d = 0
        present_d = 0
        for idx in sample_indices:
            anchor_set = set(anchor_list[idx])
            for prim in anchor_list[idx]:
                for dep in deps_map.get(prim, []):
                    total_d += 1
                    if dep in anchor_set:
                        present_d += 1
        boot_consistency = present_d / total_d if total_d > 0 else 0.0
        boot_dist.append(boot_consistency)

    boot_dist.sort()
    lower_idx = int(alpha / 2 * n_bootstrap)
    upper_idx = int((1 - alpha / 2) * n_bootstrap) - 1
    ci_lower = boot_dist[lower_idx]
    ci_upper = boot_dist[upper_idx]
    boot_mean = sum(boot_dist) / len(boot_dist)
    boot_std = (sum((x - boot_mean)**2 for x in boot_dist) / len(boot_dist))**0.5

    return {
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'alpha': alpha,
        'bootstrap_distribution': boot_dist,
        'boot_mean': boot_mean,
        'boot_std': boot_std,
    }


def effect_size_cohens_d(observed, null_distribution):
    """Cohen's d: standardized difference between observed and null mean.

    Args:
        observed: float, observed value
        null_distribution: list of floats, null distribution values

    Returns:
        float, Cohen's d
    """
    null_mean = sum(null_distribution) / len(null_distribution)
    null_std = (sum((x - null_mean)**2 for x in null_distribution)
                / len(null_distribution))**0.5
    if null_std == 0:
        return float('inf') if observed > null_mean else 0.0
    return (observed - null_mean) / null_std


def bonferroni_correction(p_values, alpha=0.05):
    """Bonferroni correction for multiple comparisons.

    Args:
        p_values: list of p-values
        alpha: overall significance level

    Returns:
        dict with keys: corrected_alpha, significant (list of bools),
        n_comparisons
    """
    n = len(p_values)
    corrected_alpha = alpha / n
    significant = [p < corrected_alpha for p in p_values]
    return {
        'corrected_alpha': corrected_alpha,
        'significant': significant,
        'n_comparisons': n,
    }


# ######################################################################
#  SECTION 2: INTER-RATER AGREEMENT FUNCTIONS
# ######################################################################

def cohens_kappa(rater1_classes, rater2_classes):
    """Compute Cohen's kappa for D/A/N classification.

    Args:
        rater1_classes: dict mapping primitive_name -> 'D'|'A'|'N'
        rater2_classes: dict mapping primitive_name -> 'D'|'A'|'N'

    Returns:
        dict with keys: kappa, po (observed agreement), pe (expected agreement),
        confusion_matrix
    """
    categories = ['D', 'A', 'N']
    common_keys = sorted(set(rater1_classes.keys()) & set(rater2_classes.keys()))
    n = len(common_keys)

    if n == 0:
        return {'kappa': 0.0, 'po': 0.0, 'pe': 0.0, 'confusion_matrix': {}}

    # Build confusion matrix
    matrix = {c1: {c2: 0 for c2 in categories} for c1 in categories}
    for key in common_keys:
        r1 = rater1_classes[key]
        r2 = rater2_classes[key]
        if r1 in categories and r2 in categories:
            matrix[r1][r2] += 1

    # Observed agreement
    po = sum(matrix[c][c] for c in categories) / n

    # Expected agreement
    pe = 0.0
    for c in categories:
        row_sum = sum(matrix[c][c2] for c2 in categories) / n
        col_sum = sum(matrix[c1][c] for c1 in categories) / n
        pe += row_sum * col_sum

    kappa = (po - pe) / (1 - pe) if pe < 1.0 else 1.0

    return {
        'kappa': kappa,
        'po': po,
        'pe': pe,
        'confusion_matrix': matrix,
    }


def krippendorffs_alpha(ratings_matrix, level='nominal'):
    """Compute Krippendorff's alpha for multiple raters.

    Simplified implementation for nominal/ordinal data with D/A/N categories.

    Args:
        ratings_matrix: list of dicts, each dict maps primitive -> 'D'|'A'|'N'
        level: 'nominal' or 'ordinal'

    Returns:
        dict with keys: alpha, Do (observed disagreement), De (expected disagreement)
    """
    categories = ['D', 'A', 'N']
    if level == 'ordinal':
        # Ordinal mapping: D=0, A=1, N=2
        ordinal_map = {'D': 0, 'A': 1, 'N': 2}
    else:
        ordinal_map = None

    # Collect all items rated by at least 2 raters
    all_items = set()
    for r in ratings_matrix:
        all_items |= set(r.keys())

    # Build coincidence matrix
    n_total = 0
    coincidence = {c1: {c2: 0.0 for c2 in categories} for c1 in categories}

    for item in all_items:
        ratings = [r[item] for r in ratings_matrix if item in r and r[item] in categories]
        m = len(ratings)
        if m < 2:
            continue
        for i in range(m):
            for j in range(m):
                if i != j:
                    coincidence[ratings[i]][ratings[j]] += 1.0 / (m - 1)
            n_total += 1

    if n_total == 0:
        return {'alpha': 0.0, 'Do': 0.0, 'De': 0.0}

    # Observed disagreement
    total_coincidence = sum(sum(coincidence[c1][c2] for c2 in categories) for c1 in categories)
    if total_coincidence == 0:
        return {'alpha': 0.0, 'Do': 0.0, 'De': 0.0}

    if level == 'ordinal' and ordinal_map is not None:
        Do = 0.0
        for c1 in categories:
            for c2 in categories:
                diff = abs(ordinal_map[c1] - ordinal_map[c2])
                Do += coincidence[c1][c2] * diff**2
        Do /= total_coincidence
    else:
        Do = 1.0 - sum(coincidence[c][c] for c in categories) / total_coincidence

    # Expected disagreement
    marginals = {c: sum(coincidence[c][c2] for c2 in categories) for c in categories}
    n_vals = sum(marginals.values())

    if level == 'ordinal' and ordinal_map is not None:
        De = 0.0
        for c1 in categories:
            for c2 in categories:
                diff = abs(ordinal_map[c1] - ordinal_map[c2])
                De += marginals[c1] * marginals[c2] * diff**2
        De /= (n_vals * (n_vals - 1)) if n_vals > 1 else 1
    else:
        De = 1.0 - sum(marginals[c]**2 for c in categories) / (n_vals * (n_vals - 1)) if n_vals > 1 else 0

    alpha = 1.0 - Do / De if De > 0 else 1.0

    return {
        'alpha': alpha,
        'Do': Do,
        'De': De,
    }


def confusion_matrix_dan(rater1, rater2):
    """3x3 confusion matrix for DIRECT/ANALOGICAL/NULL classifications.

    Args:
        rater1: dict mapping primitive_name -> 'D'|'A'|'N'
        rater2: dict mapping primitive_name -> 'D'|'A'|'N'

    Returns:
        dict with matrix and summary statistics
    """
    categories = ['D', 'A', 'N']
    labels = {'D': 'DIRECT', 'A': 'ANALOGICAL', 'N': 'NULL'}
    common_keys = sorted(set(rater1.keys()) & set(rater2.keys()))
    n = len(common_keys)

    matrix = {c1: {c2: 0 for c2 in categories} for c1 in categories}
    for key in common_keys:
        r1 = rater1[key]
        r2 = rater2[key]
        if r1 in categories and r2 in categories:
            matrix[r1][r2] += 1

    exact_agree = sum(matrix[c][c] for c in categories)
    pct_agree = exact_agree / n * 100 if n > 0 else 0

    return {
        'matrix': matrix,
        'labels': labels,
        'n': n,
        'exact_agreement': exact_agree,
        'pct_agreement': pct_agree,
    }


# ######################################################################
#  SECTION 3: DOMAIN ANCHOR DATA (imported from test scripts)
# ######################################################################

# --- Music (Test 8) anchors ---
MUS_ANCHORS = {
    'acorde_mayor':          ['unión', 'orden', 'equilibrio', 'uno'],
    'melodia':               ['mover', 'posición_temporal', 'flujo_temporal', 'información'],
    'ritmo':                 ['flujo_temporal', 'orden', 'más', 'fuerza'],
    'consonancia':           ['orden', 'equilibrio', 'unión', 'información'],
    'disonancia':            ['caos', 'separación', 'fuerza', 'información'],
    'forma_sonata':          ['orden', 'creación', 'destrucción', 'contención'],
    'tonalidad':             ['orden', 'contención', 'eje_vertical', 'uno'],
    'modulacion':            ['mover', 'orden', 'contención', 'posición_temporal'],
    'polifonia':             ['unión', 'separación', 'individual', 'colectivo'],
    'dinamica':              ['fuerza', 'más', 'menos', 'flujo_temporal'],
    'silencio':              ['vacío', 'información', 'flujo_temporal'],
    'contrapunto':           ['orden', 'separación', 'unión', 'mover'],
    'improvisacion':         ['caos', 'creación', 'libertad', 'hacer'],
    'compas':                ['flujo_temporal', 'orden', 'contención', 'más'],
    'escala':                ['orden', 'eje_vertical', 'más', 'uno'],
    'timbre':                ['información', 'contención', 'unión', 'oído'],
    'crescendo':             ['más', 'fuerza', 'flujo_temporal', 'mover'],
    'armonia':               ['unión', 'orden', 'equilibrio', 'información'],
    'cadencia':              ['orden', 'contención', 'flujo_temporal', 'posición_temporal'],
    'expresion':             ['fuerza', 'información', 'hacer', 'placer'],
    'variacion':             ['creación', 'orden', 'información', 'mover'],
    'ostinato':              ['orden', 'flujo_temporal', 'contención', 'más'],
    'fuga':                  ['orden', 'contención', 'unión', 'mover', 'creación'],
    'sincopa':               ['caos', 'orden', 'posición_temporal', 'fuerza'],
    'orquestacion':          ['colectivo', 'tipo_de', 'unión', 'equilibrio'],
}

# --- Chemistry (Test 9) anchors ---
CHEM_ANCHORS = {
    'enlace_covalente':      ['unión', 'fuerza', 'contención', 'orden'],
    'reaccion_quimica':      ['creación', 'destrucción', 'hacer', 'fuerza'],
    'equilibrio_quimico':    ['equilibrio', 'orden', 'flujo_temporal', 'contención'],
    'acido_base':            ['unión', 'separación', 'fuerza', 'contención'],
    'tabla_periodica':       ['orden', 'tipo_de', 'más', 'contención'],
    'estado_oxidacion':      ['más', 'menos', 'fuerza', 'orden'],
    'catalizador':           ['hacer', 'mover', 'orden', 'fuerza'],
    'entropia_quimica':      ['caos', 'orden', 'flujo_temporal', 'información'],
    'disolucion':            ['separación', 'mover', 'agua', 'contención'],
    'precipitacion':         ['unión', 'tierra', 'contención', 'separación'],
    'combustion':            ['destrucción', 'fuego', 'fuerza', 'creación'],
    'cristal':               ['orden', 'contención', 'tierra', 'unión'],
    'mol':                   ['muchos', 'uno', 'todo', 'más'],
    'ph':                    ['más', 'menos', 'orden', 'contención'],
    'orbital':               ['contención', 'orden', 'información', 'eje_profundidad'],
    'isomero':               ['orden', 'información', 'tipo_de', 'contención'],
    'polimero':              ['unión', 'más', 'orden', 'creación'],
    'termodinamica_quimica': ['flujo_temporal', 'orden', 'caos', 'equilibrio'],
    'electrolisis':          ['fuerza', 'separación', 'mover', 'hacer'],
    'valencia':              ['fuerza', 'unión', 'contención', 'orden'],
    'estado_materia':        ['tierra', 'agua', 'aire', 'fuego', 'orden'],
    'solucion':              ['unión', 'agua', 'contención', 'más'],
    'ley_conservacion':      ['debe', 'todo', 'equilibrio'],
    'alotropia':             ['tipo_de', 'orden', 'uno', 'contención'],
    'ion':                   ['más', 'menos', 'fuerza', 'separación'],
}

# --- Biology (Test 10) anchors ---
BIO_ANCHORS = {
    'celula':                ['contención', 'vida', 'información', 'orden'],
    'gen':                   ['información', 'orden', 'contención', 'uno'],
    'evolucion':             ['mover', 'flujo_temporal', 'creación', 'caos'],
    'mitosis':               ['creación', 'orden', 'contención', 'información'],
    'fotosintesis':          ['creación', 'fuego', 'orden', 'vida'],
    'ecosistema':            ['colectivo', 'equilibrio', 'vida', 'contención'],
    'metabolismo':           ['hacer', 'creación', 'destrucción', 'flujo_temporal'],
    'sistema_nervioso':      ['información', 'mover', 'oído', 'vista'],
    'homeostasis':           ['equilibrio', 'control', 'vida', 'contención'],
    'mutacion':              ['caos', 'información', 'creación', 'destrucción'],
    'simbiosis':             ['unión', 'vida', 'colectivo', 'equilibrio'],
    'depredacion':           ['destrucción', 'fuerza', 'mover', 'vida'],
    'reproduccion':          ['creación', 'vida', 'información', 'contención'],
    'tejido':                ['colectivo', 'tipo_de', 'contención', 'orden'],
    'organo':                ['contención', 'hacer', 'tipo_de', 'parte_de'],
    'virus':                 ['información', 'contención', 'destrucción', 'mover'],
    'inmunidad':             ['contención', 'separación', 'información', 'fuerza'],
    'adn':                   ['información', 'orden', 'contención', 'vida'],
    'especie':               ['tipo_de', 'colectivo', 'contención', 'vida'],
    'herencia':              ['información', 'flujo_temporal', 'orden', 'vida'],
    'seleccion_natural':     ['caos', 'orden', 'fuerza', 'vida', 'flujo_temporal'],
    'muerte_celular':        ['muerte', 'destrucción', 'orden', 'vida'],
    'desarrollo':            ['creación', 'orden', 'flujo_temporal', 'vida'],
    'sentidos':              ['vista', 'oído', 'tacto', 'información'],
    'conciencia_animal':     ['consciente', 'información', 'vida', 'mover'],
}

# --- Mathematics (Test 11) anchors ---
MATH_ANCHORS = {
    'numero_natural':        ['uno', 'más', 'orden'],
    'conjunto':              ['contención', 'parte_de', 'todo'],
    'funcion':               ['mover', 'información', 'orden', 'uno'],
    'demostracion':          ['porque', 'verdad', 'orden', 'si_entonces'],
    'infinito':              ['más', 'todo', 'contención'],
    'simetria':              ['orden', 'equilibrio', 'unión'],
    'grupo':                 ['unión', 'orden', 'contención', 'uno'],
    'topologia':             ['contención', 'mover', 'separación', 'unión'],
    'serie':                 ['más', 'flujo_temporal', 'orden', 'uno'],
    'limite':                ['mover', 'posición_temporal', 'contención'],
    'probabilidad':          ['tal_vez', 'información', 'más', 'todo'],
    'algebra':               ['orden', 'unión', 'separación', 'uno'],
    'geometria':             ['eje_profundidad', 'eje_vertical', 'eje_lateral', 'orden'],
    'logica':                ['verdad', 'mentira', 'si_entonces', 'porque'],
    'ecuacion':              ['equilibrio', 'orden', 'información'],
    'vector':                ['eje_profundidad', 'eje_vertical', 'mover', 'más'],
    'matriz':                ['orden', 'contención', 'eje_vertical', 'eje_lateral'],
    'grafo':                 ['unión', 'separación', 'contención', 'mover'],
    'categoria':             ['tipo_de', 'mover', 'orden', 'unión'],
    'axioma':                ['información', 'verdad', 'orden'],
    'cardinalidad':          ['muchos', 'más', 'todo', 'contención'],
    'continuo':              ['mover', 'flujo_temporal', 'más', 'contención'],
    'combinatoria':          ['más', 'algunos', 'todo', 'orden'],
    'contradiccion':         ['verdad', 'mentira', 'separación'],
    'recursion':             ['contención', 'orden', 'parte_de', 'si_entonces'],
}

# --- Philosophy (Test 12) anchors ---
PHIL_ANCHORS = {
    'ser':                   ['vacío', 'uno', 'información'],
    'no_ser':                ['vacío', 'menos', 'separación'],
    'devenir':               ['mover', 'flujo_temporal', 'creación', 'destrucción'],
    'sustancia':             ['uno', 'contención', 'orden'],
    'causa':                 ['porque', 'posición_temporal', 'hacer'],
    'libertad_fil':          ['libertad', 'puede', 'querer'],
    'justicia':              ['bien', 'equilibrio', 'orden', 'todo'],
    'verdad_fil':            ['verdad', 'información', 'orden'],
    'etica':                 ['bien', 'mal', 'debe', 'libertad'],
    'conciencia':            ['consciente', 'información', 'vida'],
    'voluntad':              ['querer', 'fuerza', 'hacer', 'libertad'],
    'razon':                 ['pensar', 'orden', 'porque', 'verdad'],
    'dialectica':            ['unión', 'separación', 'mover', 'creación'],
    'fenomeno':              ['vista', 'consciente', 'información'],
    'noumeno':               ['ausente', 'verdad', 'contención'],
    'tiempo_fil':            ['flujo_temporal', 'posición_temporal', 'consciente'],
    'muerte_fil':            ['muerte', 'consciente', 'flujo_temporal'],
    'belleza':               ['placer', 'orden', 'equilibrio', 'bien'],
    'absurdo':               ['caos', 'consciente', 'vacío', 'mentira'],
    'existencia':            ['vida', 'consciente', 'individual', 'flujo_temporal'],
    'lenguaje_fil':          ['decir', 'información', 'orden', 'verdad'],
    'poder':                 ['fuerza', 'control', 'hacer', 'colectivo'],
    'conocimiento':          ['saber', 'verdad', 'información', 'orden'],
    'yo':                    ['individual', 'consciente', 'temporal_obs'],
    'otro':                  ['individual', 'colectivo', 'receptivo', 'separación'],
}

# --- Physics (Test 13) anchors ---
PHYS_ANCHORS = {
    'fuerza_newton':           ['fuerza', 'mover', 'más', 'posición_temporal'],
    'gravitacion':             ['fuerza', 'más', 'eje_profundidad', 'todo'],
    'campo_electromagnetico':  ['fuerza', 'eje_profundidad', 'unión', 'separación', 'mover'],
    'termodinamica':           ['orden', 'caos', 'flujo_temporal', 'equilibrio', 'más'],
    'entropia':                ['caos', 'orden', 'flujo_temporal', 'información'],
    'conservacion_energia':    ['debe', 'todo', 'equilibrio', 'flujo_temporal'],
    'mecanica_cuantica':       ['tal_vez', 'información', 'puede', 'mover'],
    'superposicion':           ['unión', 'tal_vez', 'información'],
    'relatividad_especial':    ['mover', 'flujo_temporal', 'posición_temporal', 'debe'],
    'relatividad_general':     ['fuerza', 'eje_profundidad', 'flujo_temporal', 'mover', 'contención'],
    'particula':               ['individual', 'mover', 'fuerza', 'uno'],
    'onda':                    ['colectivo', 'mover', 'flujo_temporal', 'oído'],
    'estados_materia':         ['tierra', 'agua', 'aire', 'fuego', 'orden'],
    'transicion_fase':         ['orden', 'caos', 'creación', 'destrucción', 'equilibrio'],
    'ley_newton_3':            ['fuerza', 'unión', 'separación', 'equilibrio'],
    'principio_incertidumbre': ['tal_vez', 'información', 'mover', 'contención'],
    'decaimiento_radiactivo':  ['destrucción', 'flujo_temporal', 'tal_vez', 'individual'],
    'nucleosintesis':          ['creación', 'fuerza', 'unión', 'orden'],
    'par_produccion':          ['creación', 'separación', 'fuerza', 'información'],
    'aniquilacion':            ['destrucción', 'unión', 'fuerza', 'información'],
    'oscilador_armonico':      ['equilibrio', 'mover', 'fuerza', 'orden', 'flujo_temporal'],
    'caos_deterministico':     ['caos', 'orden', 'porque', 'si_entonces', 'mover'],
    'agujero_negro':           ['contención', 'fuerza', 'información', 'flujo_temporal', 'todo'],
    'dualidad_onda_particula': ['individual', 'colectivo', 'tal_vez', 'información'],
    'simetria_noether':        ['orden', 'debe', 'todo', 'mover', 'equilibrio'],
}

# --- Linguistics (Test 15) anchors ---
LING_ANCHORS = {
    'fonema':                ['uno', 'separación', 'oído', 'orden'],
    'morfema':               ['uno', 'información', 'parte_de', 'contención'],
    'oracion':               ['contención', 'orden', 'unión', 'verdad'],
    'acto_de_habla':         ['hacer', 'fuerza', 'decir', 'querer'],
    'metafora':              ['unión', 'creación', 'información', 'tipo_de'],
    'gramatica_universal':   ['orden', 'debe', 'todo', 'contención'],
    'cambio_linguistico':    ['mover', 'flujo_temporal', 'caos', 'creación'],
    'signo_saussure':        ['información', 'unión', 'uno', 'contención'],
    'deixis':                ['posición_temporal', 'individual', 'temporal_obs'],
    'negacion':              ['menos', 'vacío', 'separación'],
    'cuantificacion':        ['algunos', 'muchos', 'todo', 'uno'],
    'modalidad':             ['puede', 'debe', 'tal_vez', 'si_entonces'],
    'tiempo_verbal':         ['posición_temporal', 'flujo_temporal', 'orden'],
    'voz_pasiva_activa':     ['hacer', 'receptivo', 'creador_obs', 'control'],
    'idioma_vivo':           ['vida', 'colectivo', 'mover', 'creación'],
    'idioma_muerto':         ['muerte', 'flujo_temporal', 'ausente'],
    'pragmatica':            ['hacer', 'fuerza', 'consciente', 'querer'],
    'sinonimia_antonimia':   ['unión', 'separación', 'información', 'tipo_de'],
    'ambiguedad':            ['tal_vez', 'información', 'caos', 'puede'],
    'prosodia':              ['fuerza', 'oído', 'flujo_temporal', 'orden'],
    'escritura':             ['vista', 'información', 'orden', 'contención'],
    'pidgin_creole':         ['caos', 'creación', 'unión', 'colectivo'],
    'competencia_chomsky':   ['saber', 'orden', 'puede', 'todo'],
    'performativo_austin':   ['hacer', 'verdad', 'creación', 'fuerza'],
    'recursion':             ['contención', 'orden', 'parte_de', 'si_entonces'],
}

# --- Astrology control (Test 14) anchors ---
ASTRO_ANCHORS = {
    'horoscopo':             ['posición_temporal', 'individual', 'flujo_temporal'],
    'signo_zodiacal':        ['tipo_de', 'posición_temporal', 'contención'],
    'ascendente':            ['eje_vertical', 'posición_temporal', 'individual'],
    'casa_astrologica':      ['contención', 'eje_vertical', 'posición_temporal', 'orden'],
    'aspecto_planetario':    ['unión', 'separación', 'eje_lateral', 'fuerza'],
    'transito':              ['mover', 'posición_temporal', 'flujo_temporal'],
    'retrogrado':            ['mover', 'posición_temporal', 'caos'],
    'elemento_astro':        ['tierra', 'agua', 'aire', 'fuego'],
    'modalidad_astro':       ['tipo_de', 'orden', 'más'],
    'luna_llena':            ['flujo_temporal', 'eje_vertical', 'equilibrio'],
    'eclipse':               ['contención', 'vacío', 'vista', 'flujo_temporal'],
    'nodo_lunar':            ['mover', 'posición_temporal', 'flujo_temporal', 'contención'],
    'sinastria':             ['unión', 'individual', 'colectivo'],
    'progresion':            ['mover', 'flujo_temporal', 'posición_temporal', 'más'],
    'dignidad_planetaria':   ['bien', 'mal', 'eje_vertical', 'contención'],
    'revolucion_solar':      ['flujo_temporal', 'posición_temporal', 'individual', 'orden'],
    'luna_nueva':            ['vacío', 'creación', 'posición_temporal'],
    'medio_cielo':           ['eje_vertical', 'contención', 'posición_temporal'],
    'stellium':              ['unión', 'muchos', 'contención', 'fuerza'],
    'decanato':              ['tipo_de', 'más', 'orden', 'parte_de'],
}

ALL_DOMAIN_ANCHORS = {
    'Music (T8)':       MUS_ANCHORS,
    'Chemistry (T9)':   CHEM_ANCHORS,
    'Biology (T10)':    BIO_ANCHORS,
    'Mathematics (T11)':MATH_ANCHORS,
    'Philosophy (T12)': PHIL_ANCHORS,
    'Physics (T13)':    PHYS_ANCHORS,
    'Linguistics (T15)':LING_ANCHORS,
    'Astrology (T14)':  ASTRO_ANCHORS,
}


# ######################################################################
#  SECTION 4: STANDALONE RUNNER — APPLY TO ALL DOMAINS
# ######################################################################

if __name__ == '__main__':
    print('=' * 78)
    print('  STATISTICAL RIGOR MODULE — PERMUTATION TESTS + BOOTSTRAP CIs')
    print('  7 positive domains + 1 control negative (astrology)')
    print('=' * 78)
    print()

    N_PERMS = 10000
    N_BOOT = 10000
    ALPHA = 0.05

    results_table = []

    for domain_name, domain_anchors in ALL_DOMAIN_ANCHORS.items():
        print(f'--- {domain_name} ---')

        # 1. Observed consistency
        present, total, observed = anchor_consistency(domain_anchors, deps_map)
        print(f'  Observed consistency: {present}/{total} = {observed*100:.1f}%')

        # 2. Permutation test
        perm = permutation_test(observed, domain_anchors, all_names_list, deps_map,
                                n_perms=N_PERMS)
        print(f'  Permutation test (n={N_PERMS}): p = {perm["p_value"]:.4f}')
        print(f'  Null distribution: mean={perm["null_mean"]*100:.1f}%, '
              f'std={perm["null_std"]*100:.1f}%')

        # 3. Bootstrap CI
        boot = bootstrap_ci(domain_anchors, deps_map, n_bootstrap=N_BOOT, alpha=ALPHA)
        print(f'  Bootstrap 95% CI: [{boot["ci_lower"]*100:.1f}%, {boot["ci_upper"]*100:.1f}%]')

        # 4. Effect size
        d = effect_size_cohens_d(observed, perm['null_distribution'])
        print(f'  Cohen\'s d: {d:.2f}')

        # Interpret d
        if d >= 0.8:
            d_interp = 'LARGE'
        elif d >= 0.5:
            d_interp = 'MEDIUM'
        elif d >= 0.2:
            d_interp = 'SMALL'
        else:
            d_interp = 'NEGLIGIBLE'
        print(f'  Effect size interpretation: {d_interp}')

        results_table.append({
            'domain': domain_name,
            'observed': observed,
            'p_value': perm['p_value'],
            'ci_lower': boot['ci_lower'],
            'ci_upper': boot['ci_upper'],
            'd': d,
            'd_interp': d_interp,
            'null_mean': perm['null_mean'],
        })
        print()

    # ---- Consolidated Table ----
    print('=' * 78)
    print('  CONSOLIDATED RESULTS')
    print('=' * 78)
    print()
    print(f'  {"Domain":<22} {"Consist.":<10} {"p-value":<10} {"CI 95%":<20} '
          f'{"Cohen d":<10} {"Effect"}')
    print(f'  {"-"*80}')
    for r in results_table:
        ci_str = f'[{r["ci_lower"]*100:.1f}%, {r["ci_upper"]*100:.1f}%]'
        sig = '*' if r['p_value'] < 0.05 else ''
        print(f'  {r["domain"]:<22} {r["observed"]*100:.1f}%{"":<4} '
              f'{r["p_value"]:.4f}{sig:<3} {ci_str:<20} {r["d"]:.2f}{"":<5} '
              f'{r["d_interp"]}')
    print()

    # ---- Bonferroni Correction ----
    positive_domains = [r for r in results_table if r['domain'] != 'Astrology (T14)']
    p_values_positive = [r['p_value'] for r in positive_domains]
    bonf = bonferroni_correction(p_values_positive, alpha=ALPHA)

    print(f'Bonferroni correction for {bonf["n_comparisons"]} positive domains:')
    print(f'  Corrected alpha: {bonf["corrected_alpha"]:.4f}')
    for i, r in enumerate(positive_domains):
        sig_str = 'SIGNIFICANT' if bonf['significant'][i] else 'NOT SIGNIFICANT'
        print(f'  {r["domain"]:<22} p={r["p_value"]:.4f} -> {sig_str}')
    print()

    # ---- Control Negative Verification ----
    astro = [r for r in results_table if r['domain'] == 'Astrology (T14)']
    if astro:
        a = astro[0]
        print(f'CONTROL NEGATIVE (Astrology):')
        print(f'  p-value: {a["p_value"]:.4f} (expected > 0.05: {"YES" if a["p_value"] > 0.05 else "NO"})')
        print(f'  Cohen\'s d: {a["d"]:.2f} (expected < 0.5: {"YES" if a["d"] < 0.5 else "NO"})')
        print(f'  Interpretation: {"PASS — astrology indistinguishable from chance" if a["p_value"] > 0.05 else "UNEXPECTED — astrology shows significance"}')
    print()

    # ---- Monte Carlo: Random Models ----
    print('=' * 78)
    print('  MONTE CARLO: RANDOM 63-PRIMITIVE MODELS')
    print('=' * 78)
    print()

    N_MODELS = 1000
    rng = random.Random(42)
    model_consistencies = []

    # Use physics anchors as reference structure
    ref_anchors = PHYS_ANCHORS
    ref_sizes = [len(v) for v in ref_anchors.values()]

    for _ in range(N_MODELS):
        shuffled = all_names_list[:]
        rng.shuffle(shuffled)
        total_d = 0
        present_d = 0
        idx = 0
        for size in ref_sizes:
            anchor_set = set(shuffled[idx:idx + size])
            for prim in anchor_set:
                for dep in deps_map.get(prim, []):
                    total_d += 1
                    if dep in anchor_set:
                        present_d += 1
            idx += size
        c = present_d / total_d if total_d > 0 else 0
        model_consistencies.append(c)

    mc_mean = sum(model_consistencies) / len(model_consistencies)
    mc_std = (sum((x - mc_mean)**2 for x in model_consistencies) / len(model_consistencies))**0.5
    mc_max = max(model_consistencies)

    print(f'Generated {N_MODELS} random models with same layer/dependency structure.')
    print(f'  Mean consistency: {mc_mean*100:.1f}%')
    print(f'  Std:              {mc_std*100:.1f}%')
    print(f'  Max:              {mc_max*100:.1f}%')
    print()

    # Compare with actual domains
    for r in results_table:
        if r['domain'] == 'Astrology (T14)':
            continue
        sigma = (r['observed'] - mc_mean) / mc_std if mc_std > 0 else 0
        print(f'  {r["domain"]:<22} observed={r["observed"]*100:.1f}%  '
              f'sigma={sigma:.1f}σ above random')
    print()

    # ---- Text-based Forest Plot ----
    print('=' * 78)
    print('  FOREST PLOT (text-based): Bootstrap 95% CI by Domain')
    print('=' * 78)
    print()

    max_width = 60
    all_vals = [r['ci_lower'] for r in results_table] + [r['ci_upper'] for r in results_table]
    plot_min = min(all_vals) - 0.02
    plot_max = max(all_vals) + 0.02
    plot_range = plot_max - plot_min

    def val_to_pos(v):
        return int((v - plot_min) / plot_range * max_width)

    for r in results_table:
        lo = val_to_pos(r['ci_lower'])
        hi = val_to_pos(r['ci_upper'])
        obs = val_to_pos(r['observed'])

        bar = [' '] * (max_width + 1)
        for i in range(lo, hi + 1):
            bar[i] = '-'
        if 0 <= obs <= max_width:
            bar[obs] = '|'

        bar_str = ''.join(bar)
        sig = '*' if r['p_value'] < 0.05 else ' '
        print(f'  {r["domain"]:<22} {sig} [{bar_str}]')

    lo_label = f'{plot_min*100:.0f}%'
    hi_label = f'{plot_max*100:.0f}%'
    print(f'  {"":22}   {lo_label}{"":{max_width - len(lo_label) - len(hi_label)}}{hi_label}')
    print(f'  {"":22}   (* = p < 0.05)')
    print()

    print('=' * 78)
    print('  STATISTICAL RIGOR MODULE — COMPLETE')
    print('=' * 78)
