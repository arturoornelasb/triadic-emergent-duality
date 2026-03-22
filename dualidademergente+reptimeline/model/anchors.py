"""
Multi-domain anchor concepts for 65 primitivos.

Generates gold_primes_65.json: maps ~500 concepts from 8 scientific
domains to their 65-bit signatures based on which primitivos are
Definitorio (D) or Accesorio (A) for each concept.

Strategy:
  1. Load primitivos.json for bit positions and dependency structure.
  2. Load reference_domains.json for domain-level D-A-N classifications.
  3. For each anchor concept, determine its primary domain(s).
  4. Active bits = primitivos classified D in the concept's domain.
  5. Concept-specific overrides for finer precision.
  6. Expand dependencies: if a primitivo is active, its deps are also active.

Usage:
    python anchors.py              # Generate gold_primes_65.json
    python anchors.py --stats      # Show statistics only

Solo stdlib + json.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))

# ######################################################################
#  SECTION 0: DATA LOADING
# ######################################################################

with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

with open(os.path.join(DATA_DIR, 'reference_domains.json'), 'r', encoding='utf-8') as f:
    dom_data = json.load(f)

prims = prim_data['primitivos']
name_to_bit = {p['nombre']: p['bit'] for p in prims}
name_to_primo = {p['nombre']: p['primo'] for p in prims}
bit_to_name = {p['bit']: p['nombre'] for p in prims}
deps_map = {p['nombre']: list(p['deps']) for p in prims}
N_BITS = 65  # 0-64

domains = dom_data['domains']


def get_domain_d_bits(domain_name):
    """Return set of bit positions classified D in a domain."""
    classes = domains[domain_name]['classes']
    return {name_to_bit[name] for name, cls in classes.items() if cls == 'D'}


def get_domain_da_bits(domain_name):
    """Return set of bit positions classified D or A in a domain."""
    classes = domains[domain_name]['classes']
    return {name_to_bit[name] for name, cls in classes.items() if cls in ('D', 'A')}


def expand_deps(active_bits):
    """Expand active bits to include all transitive dependencies."""
    active_names = {bit_to_name[b] for b in active_bits if b in bit_to_name}
    expanded = set(active_names)
    changed = True
    while changed:
        changed = False
        for name in list(expanded):
            for dep in deps_map.get(name, []):
                if dep not in expanded:
                    expanded.add(dep)
                    changed = True
    return {name_to_bit[n] for n in expanded}


def bits_to_signature(active_bits):
    """Convert set of active bit positions to 65-element binary list."""
    sig = [0] * N_BITS
    for b in active_bits:
        if 0 <= b < N_BITS:
            sig[b] = 1
    return sig


def bits_to_prime(active_bits):
    """Convert active bits to composite prime product."""
    product = 1
    for b in active_bits:
        if b in bit_to_name:
            product *= name_to_primo[bit_to_name[b]]
    return product


# ######################################################################
#  SECTION 1: ANCHOR DEFINITIONS
# ######################################################################

# Each anchor: (english_word, primary_domain, [optional extra active primitivos])
# The base bits come from domain-level D classification.
# Extra bits add concept-specific primitivos beyond the domain default.
# Negative bits (prefixed with -) remove primitivos.

ANCHORS = {
    # ============================================================
    # PHYSICS (~70 concepts)
    # ============================================================
    'gravity': ('Physics', ['fuerza', 'mover', 'eje_profundidad']),
    'mass': ('Physics', ['fuerza', 'contención', 'uno']),
    'energy': ('Physics', ['fuerza', 'mover', 'creación', 'destrucción']),
    'momentum': ('Physics', ['fuerza', 'mover', 'posición_temporal']),
    'velocity': ('Physics', ['mover', 'posición_temporal', 'flujo_temporal']),
    'acceleration': ('Physics', ['fuerza', 'mover', 'flujo_temporal']),
    'force': ('Physics', ['fuerza']),
    'entropy': ('Physics', ['caos', 'orden', 'flujo_temporal']),
    'temperature': ('Physics', ['fuerza', 'mover', 'tacto']),
    'pressure': ('Physics', ['fuerza', 'contención']),
    'wave': ('Physics', ['mover', 'flujo_temporal', 'orden']),
    'particle': ('Physics', ['uno', 'contención']),
    'atom': ('Physics', ['uno', 'contención', 'parte_de']),
    'electron': ('Physics', ['fuerza', 'mover', 'uno']),
    'photon': ('Physics', ['mover', 'información', 'vista']),
    'field': ('Physics', ['fuerza', 'contención', 'mover']),
    'spacetime': ('Physics', ['eje_profundidad', 'eje_vertical', 'eje_lateral', 'posición_temporal']),
    'relativity': ('Physics', ['posición_temporal', 'mover', 'proporción']),
    'quantum': ('Physics', ['uno', 'tal_vez', 'información']),
    'spin': ('Physics', ['mover', 'uno', 'información']),
    'charge': ('Physics', ['fuerza', 'separación', 'unión']),
    'magnetism': ('Physics', ['fuerza', 'mover', 'unión']),
    'electricity': ('Physics', ['fuerza', 'mover', 'fuerza']),
    'friction': ('Physics', ['fuerza', 'contención', 'quietud']),
    'inertia': ('Physics', ['quietud', 'fuerza']),
    'equilibrium': ('Physics', ['equilibrio', 'quietud', 'fuerza']),
    'oscillation': ('Physics', ['mover', 'flujo_temporal', 'orden']),
    'frequency': ('Physics', ['flujo_temporal', 'orden', 'proporción']),
    'wavelength': ('Physics', ['eje_profundidad', 'proporción', 'mover']),
    'amplitude': ('Physics', ['fuerza', 'más', 'menos']),
    'conservation': ('Physics', ['orden', 'todo', 'flujo_temporal']),
    'symmetry': ('Physics', ['equilibrio', 'orden', 'información']),
    'decay': ('Physics', ['destrucción', 'flujo_temporal']),
    'fusion': ('Physics', ['unión', 'fuerza', 'creación']),
    'fission': ('Physics', ['separación', 'fuerza', 'destrucción']),
    'radiation': ('Physics', ['fuerza', 'mover', 'vista']),
    'vacuum': ('Physics', ['vacío']),
    'density': ('Physics', ['contención', 'proporción', 'más']),
    'torque': ('Physics', ['fuerza', 'mover', 'eje_lateral']),
    'buoyancy': ('Physics', ['fuerza', 'agua', 'equilibrio']),

    # ============================================================
    # CHEMISTRY (~60 concepts)
    # ============================================================
    'molecule': ('Chemistry', ['unión', 'parte_de', 'contención']),
    'reaction': ('Chemistry', ['creación', 'destrucción', 'flujo_temporal']),
    'bond': ('Chemistry', ['unión', 'fuerza', 'contención']),
    'catalyst': ('Chemistry', ['hacer', 'flujo_temporal', 'orden']),
    'acid': ('Chemistry', ['separación', 'fuerza', 'agua']),
    'base': ('Chemistry', ['unión', 'fuerza', 'agua']),
    'oxidation': ('Chemistry', ['separación', 'fuerza', 'fuego']),
    'reduction': ('Chemistry', ['unión', 'fuerza']),
    'solvent': ('Chemistry', ['agua', 'separación', 'contención']),
    'solute': ('Chemistry', ['parte_de', 'contención']),
    'solution': ('Chemistry', ['unión', 'agua', 'contención']),
    'crystal': ('Chemistry', ['orden', 'tierra', 'contención']),
    'polymer': ('Chemistry', ['unión', 'muchos', 'parte_de']),
    'ion': ('Chemistry', ['separación', 'fuerza', 'uno']),
    'isotope': ('Chemistry', ['uno', 'más', 'menos']),
    'element': ('Chemistry', ['uno', 'tipo_de']),
    'compound': ('Chemistry', ['unión', 'tipo_de', 'parte_de']),
    'mixture': ('Chemistry', ['muchos', 'parte_de', 'separación']),
    'pH': ('Chemistry', ['proporción', 'orden', 'agua']),
    'concentration': ('Chemistry', ['proporción', 'contención']),
    'equilibrium_chem': ('Chemistry', ['equilibrio', 'orden', 'flujo_temporal']),
    'precipitate': ('Chemistry', ['separación', 'tierra', 'agua']),
    'combustion': ('Chemistry', ['fuego', 'destrucción', 'aire']),
    'distillation': ('Chemistry', ['separación', 'flujo_temporal', 'agua']),
    'titration': ('Chemistry', ['proporción', 'orden', 'hacer']),
    'mole': ('Chemistry', ['muchos', 'uno', 'proporción']),
    'valence': ('Chemistry', ['unión', 'orden', 'fuerza']),
    'alloy': ('Chemistry', ['unión', 'tierra', 'muchos']),
    'corrosion': ('Chemistry', ['destrucción', 'flujo_temporal', 'tierra']),
    'sublimation': ('Chemistry', ['mover', 'aire', 'tierra']),

    # ============================================================
    # BIOLOGY (~70 concepts)
    # ============================================================
    'cell': ('Biology', ['vida', 'contención', 'parte_de']),
    'DNA': ('Biology', ['información', 'orden', 'vida']),
    'evolution': ('Biology', ['flujo_temporal', 'creación', 'vida']),
    'photosynthesis': ('Biology', ['vida', 'creación', 'fuego', 'agua']),
    'respiration': ('Biology', ['vida', 'aire', 'destrucción']),
    'metabolism': ('Biology', ['hacer', 'creación', 'destrucción']),
    'protein': ('Biology', ['información', 'orden', 'hacer']),
    'gene': ('Biology', ['información', 'parte_de', 'vida']),
    'mutation': ('Biology', ['caos', 'información', 'creación']),
    'mitosis': ('Biology', ['creación', 'separación', 'vida']),
    'meiosis': ('Biology', ['creación', 'separación', 'muchos']),
    'ecosystem': ('Biology', ['colectivo', 'vida', 'contención']),
    'predator': ('Biology', ['destrucción', 'vida', 'fuerza']),
    'symbiosis': ('Biology', ['unión', 'vida', 'colectivo']),
    'organism': ('Biology', ['vida', 'individual', 'contención']),
    'species': ('Biology', ['tipo_de', 'vida', 'colectivo']),
    'habitat': ('Biology', ['contención', 'vida', 'tierra']),
    'adaptation': ('Biology', ['orden', 'vida', 'flujo_temporal']),
    'reproduction': ('Biology', ['creación', 'vida', 'muchos']),
    'death_bio': ('Biology', ['muerte', 'vida', 'flujo_temporal']),
    'brain': ('Biology', ['consciente', 'información', 'vida']),
    'nerve': ('Biology', ['información', 'mover', 'vida']),
    'blood': ('Biology', ['mover', 'vida', 'agua']),
    'bone': ('Biology', ['tierra', 'vida', 'contención']),
    'muscle': ('Biology', ['fuerza', 'mover', 'vida']),
    'virus': ('Biology', ['información', 'destrucción', 'parte_de']),
    'bacteria': ('Biology', ['vida', 'uno', 'parte_de']),
    'fungus': ('Biology', ['vida', 'destrucción', 'tierra']),
    'plant': ('Biology', ['vida', 'creación', 'quietud']),
    'animal': ('Biology', ['vida', 'mover', 'consciente']),
    'hormone': ('Biology', ['información', 'hacer', 'vida']),
    'enzyme': ('Biology', ['hacer', 'orden', 'vida']),
    'nutrition': ('Biology', ['vida', 'hacer', 'contención']),
    'immunity': ('Biology', ['vida', 'contención', 'destrucción']),
    'growth': ('Biology', ['vida', 'más', 'flujo_temporal']),

    # ============================================================
    # MATHEMATICS (~60 concepts)
    # ============================================================
    'number': ('Mathematics', ['uno', 'información', 'orden']),
    'zero': ('Mathematics', ['vacío', 'uno']),
    'infinity': ('Mathematics', ['más', 'muchos']),
    'set': ('Mathematics', ['contención', 'muchos']),
    'function': ('Mathematics', ['hacer', 'información', 'orden']),
    'proof': ('Mathematics', ['porque', 'verdad', 'orden']),
    'theorem': ('Mathematics', ['verdad', 'orden', 'información']),
    'axiom': ('Mathematics', ['verdad', 'uno', 'orden']),
    'equation': ('Mathematics', ['equilibrio', 'información', 'proporción']),
    'variable': ('Mathematics', ['uno', 'información', 'tal_vez']),
    'constant': ('Mathematics', ['uno', 'quietud', 'verdad']),
    'addition': ('Mathematics', ['más', 'unión', 'hacer']),
    'subtraction': ('Mathematics', ['menos', 'separación', 'hacer']),
    'multiplication': ('Mathematics', ['más', 'hacer', 'proporción']),
    'division': ('Mathematics', ['separación', 'proporción', 'hacer']),
    'prime_number': ('Mathematics', ['uno', 'orden', 'separación']),
    'fraction': ('Mathematics', ['parte_de', 'proporción']),
    'ratio': ('Mathematics', ['proporción', 'orden']),
    'limit': ('Mathematics', ['contención', 'más', 'flujo_temporal']),
    'derivative': ('Mathematics', ['flujo_temporal', 'proporción', 'mover']),
    'integral': ('Mathematics', ['todo', 'más', 'contención']),
    'matrix': ('Mathematics', ['orden', 'muchos', 'contención']),
    'vector': ('Mathematics', ['mover', 'eje_profundidad', 'información']),
    'topology': ('Mathematics', ['contención', 'orden', 'eje_profundidad']),
    'symmetry_math': ('Mathematics', ['equilibrio', 'orden', 'verdad']),
    'group': ('Mathematics', ['contención', 'orden', 'hacer']),
    'ring': ('Mathematics', ['contención', 'hacer', 'orden']),
    'probability': ('Mathematics', ['tal_vez', 'proporción', 'orden']),
    'statistics': ('Mathematics', ['muchos', 'orden', 'proporción']),
    'geometry': ('Mathematics', ['eje_profundidad', 'eje_vertical', 'eje_lateral']),
    'algebra': ('Mathematics', ['información', 'orden', 'hacer']),
    'logic': ('Mathematics', ['verdad', 'mentira', 'porque']),
    'sequence': ('Mathematics', ['orden', 'muchos', 'flujo_temporal']),
    'graph': ('Mathematics', ['unión', 'muchos', 'orden']),
    'dimension': ('Mathematics', ['eje_profundidad', 'eje_vertical', 'eje_lateral']),

    # ============================================================
    # PHILOSOPHY (~60 concepts)
    # ============================================================
    'truth': ('Philosophy', ['verdad', 'información', 'orden']),
    'existence': ('Philosophy', ['uno', 'vacío', 'información']),
    'consciousness': ('Philosophy', ['consciente', 'información', 'vida']),
    'free_will': ('Philosophy', ['libertad', 'hacer', 'consciente']),
    'determinism': ('Philosophy', ['control', 'orden', 'porque']),
    'ethics': ('Philosophy', ['bien', 'mal', 'hacer']),
    'justice': ('Philosophy', ['bien', 'equilibrio', 'colectivo']),
    'beauty': ('Philosophy', ['bien', 'orden', 'proporción']),
    'knowledge': ('Philosophy', ['saber', 'verdad', 'información']),
    'belief': ('Philosophy', ['pensar', 'verdad', 'tal_vez']),
    'reality': ('Philosophy', ['verdad', 'información', 'contención']),
    'illusion': ('Philosophy', ['mentira', 'información', 'consciente']),
    'meaning': ('Philosophy', ['información', 'porque', 'consciente']),
    'purpose': ('Philosophy', ['porque', 'hacer', 'bien']),
    'identity': ('Philosophy', ['uno', 'individual', 'información']),
    'change': ('Philosophy', ['mover', 'flujo_temporal', 'creación']),
    'permanence': ('Philosophy', ['quietud', 'uno', 'flujo_temporal']),
    'causation': ('Philosophy', ['porque', 'si_entonces', 'flujo_temporal']),
    'freedom': ('Philosophy', ['libertad', 'hacer', 'puede']),
    'duty': ('Philosophy', ['debe', 'hacer', 'bien']),
    'virtue': ('Philosophy', ['bien', 'hacer', 'orden']),
    'evil': ('Philosophy', ['mal', 'destrucción', 'caos']),
    'death_phil': ('Philosophy', ['muerte', 'vida', 'flujo_temporal']),
    'soul': ('Philosophy', ['consciente', 'vida', 'individual']),
    'god': ('Philosophy', ['eterno_obs', 'todo', 'creación']),
    'nothing': ('Philosophy', ['vacío', 'ausente']),
    'being': ('Philosophy', ['uno', 'vida', 'consciente']),
    'becoming': ('Philosophy', ['mover', 'creación', 'flujo_temporal']),
    'dialectic': ('Philosophy', ['verdad', 'mentira', 'creación']),
    'paradox': ('Philosophy', ['verdad', 'mentira', 'contención']),
    'wisdom': ('Philosophy', ['saber', 'bien', 'orden']),
    'doubt': ('Philosophy', ['tal_vez', 'pensar', 'verdad']),

    # ============================================================
    # LINGUISTICS (~60 concepts)
    # ============================================================
    'phoneme': ('Linguistics', ['información', 'oído', 'uno']),
    'morpheme': ('Linguistics', ['información', 'parte_de', 'contención']),
    'syntax': ('Linguistics', ['orden', 'contención', 'información']),
    'semantics': ('Linguistics', ['información', 'verdad', 'contención']),
    'pragmatics': ('Linguistics', ['hacer', 'decir', 'consciente']),
    'grammar': ('Linguistics', ['orden', 'contención', 'hacer']),
    'word': ('Linguistics', ['información', 'uno', 'contención']),
    'sentence': ('Linguistics', ['contención', 'orden', 'muchos']),
    'paragraph': ('Linguistics', ['contención', 'muchos', 'orden']),
    'language': ('Linguistics', ['información', 'colectivo', 'decir']),
    'speech': ('Linguistics', ['decir', 'oído', 'hacer']),
    'writing': ('Linguistics', ['información', 'hacer', 'vista']),
    'vowel': ('Linguistics', ['oído', 'aire', 'información']),
    'consonant': ('Linguistics', ['oído', 'contención', 'información']),
    'noun': ('Linguistics', ['uno', 'tipo_de', 'información']),
    'verb': ('Linguistics', ['hacer', 'mover', 'información']),
    'adjective': ('Linguistics', ['información', 'tipo_de', 'más']),
    'metaphor': ('Linguistics', ['información', 'unión', 'creación']),
    'translation': ('Linguistics', ['información', 'mover', 'verdad']),
    'dialect': ('Linguistics', ['separación', 'colectivo', 'información']),
    'etymology': ('Linguistics', ['flujo_temporal', 'información', 'porque']),
    'discourse': ('Linguistics', ['decir', 'muchos', 'orden']),
    'narrative': ('Linguistics', ['flujo_temporal', 'hacer', 'información']),
    'symbol': ('Linguistics', ['información', 'uno', 'verdad']),
    'reference': ('Linguistics', ['información', 'verdad', 'uno']),
    'ambiguity': ('Linguistics', ['tal_vez', 'información', 'caos']),
    'rhetoric': ('Linguistics', ['decir', 'hacer', 'bien']),
    'prosody': ('Linguistics', ['oído', 'flujo_temporal', 'orden']),
    'lexicon': ('Linguistics', ['muchos', 'información', 'contención']),
    'creole': ('Linguistics', ['creación', 'unión', 'colectivo']),

    # ============================================================
    # PSYCHOLOGY (~60 concepts)
    # ============================================================
    'perception': ('Psychology', ['consciente', 'información', 'vista']),
    'memory': ('Psychology', ['información', 'posición_temporal', 'consciente']),
    'emotion': ('Psychology', ['consciente', 'placer', 'dolor']),
    'motivation': ('Psychology', ['querer', 'hacer', 'fuerza']),
    'learning': ('Psychology', ['información', 'flujo_temporal', 'consciente']),
    'attention': ('Psychology', ['consciente', 'información', 'control']),
    'personality': ('Psychology', ['individual', 'orden', 'consciente']),
    'cognition': ('Psychology', ['pensar', 'información', 'consciente']),
    'behavior': ('Psychology', ['hacer', 'mover', 'consciente']),
    'anxiety': ('Psychology', ['dolor', 'tal_vez', 'flujo_temporal']),
    'depression': ('Psychology', ['dolor', 'ausente', 'menos']),
    'trauma': ('Psychology', ['dolor', 'destrucción', 'consciente']),
    'attachment': ('Psychology', ['unión', 'vida', 'individual']),
    'empathy': ('Psychology', ['consciente', 'colectivo', 'placer']),
    'intelligence': ('Psychology', ['pensar', 'saber', 'orden']),
    'creativity': ('Psychology', ['creación', 'pensar', 'consciente']),
    'dream': ('Psychology', ['ausente', 'información', 'creación']),
    'instinct': ('Psychology', ['hacer', 'vida', 'porque']),
    'habit': ('Psychology', ['hacer', 'orden', 'flujo_temporal']),
    'desire': ('Psychology', ['querer', 'placer', 'consciente']),
    'fear': ('Psychology', ['dolor', 'fuerza', 'consciente']),
    'anger': ('Psychology', ['fuerza', 'destrucción', 'consciente']),
    'joy': ('Psychology', ['placer', 'consciente', 'vida']),
    'grief': ('Psychology', ['dolor', 'muerte', 'consciente']),
    'self_concept': ('Psychology', ['individual', 'consciente', 'uno']),
    'development': ('Psychology', ['flujo_temporal', 'creación', 'vida']),
    'conditioning': ('Psychology', ['porque', 'hacer', 'orden']),
    'consciousness_psy': ('Psychology', ['consciente', 'información', 'vida']),
    'unconscious': ('Psychology', ['ausente', 'información', 'hacer']),
    'stress': ('Psychology', ['dolor', 'fuerza', 'contención']),

    # ============================================================
    # MUSIC (~50 concepts)
    # ============================================================
    'melody': ('Music', ['orden', 'flujo_temporal', 'mover']),
    'harmony': ('Music', ['unión', 'orden', 'equilibrio']),
    'rhythm': ('Music', ['flujo_temporal', 'orden', 'mover']),
    'tempo': ('Music', ['flujo_temporal', 'proporción', 'mover']),
    'pitch': ('Music', ['información', 'eje_vertical', 'oído']),
    'timbre': ('Music', ['información', 'oído', 'tipo_de']),
    'dynamics': ('Music', ['más', 'menos', 'fuerza']),
    'chord': ('Music', ['unión', 'orden', 'muchos']),
    'scale': ('Music', ['orden', 'proporción', 'muchos']),
    'key': ('Music', ['orden', 'contención', 'uno']),
    'cadence': ('Music', ['orden', 'flujo_temporal', 'quietud']),
    'dissonance': ('Music', ['caos', 'separación', 'oído']),
    'consonance': ('Music', ['orden', 'unión', 'oído']),
    'counterpoint': ('Music', ['separación', 'unión', 'orden']),
    'fugue': ('Music', ['orden', 'mover', 'muchos']),
    'sonata': ('Music', ['orden', 'contención', 'flujo_temporal']),
    'symphony': ('Music', ['muchos', 'colectivo', 'todo']),
    'improvisation': ('Music', ['creación', 'libertad', 'hacer']),
    'composition': ('Music', ['creación', 'orden', 'hacer']),
    'silence': ('Music', ['quietud', 'vacío', 'oído']),
    'crescendo': ('Music', ['más', 'fuerza', 'flujo_temporal']),
    'diminuendo': ('Music', ['menos', 'flujo_temporal']),
    'staccato': ('Music', ['separación', 'flujo_temporal']),
    'legato': ('Music', ['unión', 'flujo_temporal', 'mover']),
    'vibrato': ('Music', ['mover', 'flujo_temporal', 'oído']),
    'octave': ('Music', ['proporción', 'eje_vertical', 'orden']),
    'interval': ('Music', ['separación', 'proporción', 'eje_vertical']),
    'rest': ('Music', ['quietud', 'vacío', 'flujo_temporal']),
    'beat': ('Music', ['flujo_temporal', 'uno', 'fuerza']),
    'measure': ('Music', ['contención', 'parte_de', 'orden']),
}


# ######################################################################
#  SECTION 2: GENERATE SIGNATURES
# ######################################################################

def generate_gold_primes():
    """Generate gold primes JSON from anchor definitions."""
    gold = {}
    stats = {d: 0 for d in domains if d != 'Astrology'}

    for concept, (domain, extra_prims) in ANCHORS.items():
        # Base bits from domain-level D classification
        active_bits = get_domain_d_bits(domain)

        # Add concept-specific extra primitivos
        for pname in extra_prims:
            if pname in name_to_bit:
                active_bits.add(name_to_bit[pname])

        # Expand dependencies (if bit X is active, its deps should be too)
        active_bits = expand_deps(active_bits)

        # Generate signature
        sig = bits_to_signature(active_bits)
        prime = bits_to_prime(active_bits)

        gold[concept] = {
            'domain': domain,
            'binary_signature': sig,
            'prime_factor': prime,
            'n_active': sum(sig),
        }
        stats[domain] = stats.get(domain, 0) + 1

    return gold, stats


# ######################################################################
#  SECTION 3: MAIN
# ######################################################################

if __name__ == '__main__':
    import sys

    gold, stats = generate_gold_primes()

    print('=' * 70)
    print('  MULTI-DOMAIN ANCHOR GENERATION')
    print('=' * 70)
    print()
    print(f'  Total anchors: {len(gold)}')
    print()
    print(f'  {"Domain":<16} {"Anchors":>8}')
    print(f'  {"-" * 26}')
    for d, count in sorted(stats.items()):
        print(f'  {d:<16} {count:>8}')

    # Bit activation stats
    print()
    all_active = [0] * N_BITS
    for concept, data in gold.items():
        for i, b in enumerate(data['binary_signature']):
            all_active[i] += b

    print(f'  {"Primitivo":<22} {"Bit":>4} {"Active in":>10} {"%":>6}')
    print(f'  {"-" * 46}')
    for p in sorted(prims, key=lambda x: x['bit']):
        bit = p['bit']
        if bit < N_BITS:
            count = all_active[bit]
            pct = count / len(gold) * 100
            print(f'  {p["nombre"]:<22} {bit:>4} {count:>10} {pct:>5.1f}%')

    if '--stats' not in sys.argv:
        out_path = os.path.join(SCRIPT_DIR, 'gold_primes_65.json')
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(gold, f, indent=2, ensure_ascii=False)
        print()
        print(f'  Saved to: {out_path}')
        print(f'  {len(gold)} concepts x {N_BITS} bits')
