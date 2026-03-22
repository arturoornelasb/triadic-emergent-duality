"""
Generate gold_primitivos_65.json — V3 target file.

Each primitivo gets its own bit ON + all transitive dependency bits ON.
English translations + definitions for GPT-2 tokenization (Option D).

Usage:
    python generate_gold_primitivos.py
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))


# ######################################################################
#  ENGLISH TRANSLATIONS: nombre → (english_key, english_definition)
# ######################################################################

TRANSLATIONS = {
    "vacío": ("void", "Absence as substance, potential space"),
    "información": ("information", "Pattern, code, abstract structure"),
    "uno": ("one", "Singularity, unity"),
    "fuerza": ("force", "Capacity for change, push, potential"),
    "eje_profundidad": ("depth_axis", "Forward-backward dimension"),
    "contención": ("containment", "Inside and outside, limits and boundaries"),
    "más": ("more", "Increase, increment"),
    "menos": ("less", "Decrease, reduction"),
    "unión": ("union", "Join, connect, link"),
    "separación": ("separation", "Divide, isolate, disconnect"),
    "parte_de": ("part_of", "Inclusion, belonging"),
    "mover": ("move", "Displacement, change of position"),
    "posición_temporal": ("temporal_position", "Past, present, future"),
    "flujo_temporal": ("temporal_flow", "How time passes, duration"),
    "hacer": ("do", "Action, execution, production"),
    "creación": ("creation", "Generate something new"),
    "destrucción": ("destruction", "Eliminate, undo"),
    "orden": ("order", "Structure, regularity"),
    "caos": ("chaos", "Disorder, turbulence"),
    "porque": ("because", "Causality, reason"),
    "si_entonces": ("if_then", "Conditionality, implication"),
    "eje_vertical": ("vertical_axis", "Up-down dimension"),
    "eje_lateral": ("lateral_axis", "Left-right dimension"),
    "equilibrio": ("balance", "Balance, spatial orientation"),
    "vista": ("sight", "Visual perception"),
    "bien": ("good", "Positive moral pole"),
    "mal": ("evil", "Negative moral pole"),
    "verdad": ("truth", "Correspondence with reality"),
    "mentira": ("lie", "Distortion of reality"),
    "libertad": ("freedom", "Self-determination"),
    "control": ("control", "Restriction, regulation"),
    "tipo_de": ("type_of", "Classification, category"),
    "algunos": ("some", "Part, portion"),
    "muchos": ("many", "Plurality"),
    "todo": ("all", "Totality, completeness"),
    "puede": ("can", "Possibility, capability"),
    "debe": ("must", "Obligation, necessity"),
    "tal_vez": ("maybe", "Uncertainty, openness"),
    "tierra": ("earth", "Solidity, foundation, the tangible"),
    "agua": ("water", "Fluidity, adaptation, depth"),
    "aire": ("air", "Expansion, breathing, ubiquity"),
    "fuego": ("fire", "Transformation, heat, radiance"),
    "tacto": ("touch", "Pressure, temperature, texture"),
    "oído": ("hearing", "Sound, music, spoken language"),
    "gusto": ("taste", "Gustatory perception"),
    "olfato": ("smell", "Olfactory perception"),
    "interocepción": ("interoception", "Internal state of the body"),
    "vida": ("life", "Animation, growth"),
    "muerte": ("death", "Vital cessation, dissolution"),
    "placer": ("pleasure", "Positive hedonic experience"),
    "dolor": ("pain", "Negative hedonic experience"),
    "consciente": ("conscious", "Awareness, presence of consciousness"),
    "ausente": ("absent", "Absence of consciousness"),
    "individual": ("individual", "One alone, particular"),
    "colectivo": ("collective", "Group, community"),
    "querer": ("want", "Desire, will, intention"),
    "saber": ("know", "Knowledge, understanding"),
    "pensar": ("think", "Reasoning, reflection"),
    "decir": ("say", "Verbal communication"),
    "temporal_obs": ("mortal_observer", "Observer bound to time"),
    "eterno_obs": ("eternal_observer", "Observer outside of time"),
    "receptivo": ("receptive", "That receives, absorbs, listens"),
    "creador_obs": ("creator_observer", "That creates, actively produces"),
    "proporción": ("proportion", "Quantitative relation between magnitudes"),
    "quietud": ("stillness", "Absence of displacement, staying in position"),
}


# ######################################################################
#  TRANSITIVE DEPENDENCY EXPANSION
# ######################################################################

def expand_deps_recursive(prim_name, prims_by_name, visited=None):
    """Get all transitive dependencies for a primitivo."""
    if visited is None:
        visited = set()
    if prim_name in visited:
        return set()
    visited.add(prim_name)
    p = prims_by_name.get(prim_name)
    if not p:
        return set()
    result = set()
    for dep_name in p.get('deps', []):
        result.add(dep_name)
        result |= expand_deps_recursive(dep_name, prims_by_name, visited)
    return result


# ######################################################################
#  MAIN
# ######################################################################

def main():
    path = os.path.join(DATA_DIR, 'primitivos.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    prims = data['primitivos']
    prims_by_name = {p['nombre']: p for p in prims}
    name_to_bit = {p['nombre']: p['bit'] for p in prims}

    print('=' * 70)
    print('  GENERATING gold_primitivos_65.json (V3 targets)')
    print('=' * 70)
    print(f'  Source: {path}')
    print(f'  Primitivos: {len(prims)}')

    gold = {}
    missing = []

    for p in prims:
        nombre = p['nombre']
        bit = p['bit']
        capa = p['capa']

        if nombre not in TRANSLATIONS:
            missing.append(nombre)
            continue

        eng_key, eng_def = TRANSLATIONS[nombre]

        # Transitive deps → active bits
        all_deps = expand_deps_recursive(nombre, prims_by_name)
        active_bits = {bit}
        for dep_name in all_deps:
            if dep_name in name_to_bit:
                active_bits.add(name_to_bit[dep_name])

        # 65-bit signature
        sig = [0] * 65
        for b in active_bits:
            if b < 65:
                sig[b] = 1

        # Text for GPT-2: "word: definition"
        text = eng_key.replace('_', ' ') + ': ' + eng_def.lower()

        # Dual in English
        dual_es = p.get('dual', None)
        dual_en = None
        if dual_es and dual_es in TRANSLATIONS:
            dual_en = TRANSLATIONS[dual_es][0]

        gold[eng_key] = {
            'nombre': nombre,
            'english': eng_key,
            'text': text,
            'bit': bit,
            'capa': capa,
            'binary_signature': sig,
            'n_active': sum(sig),
            'active_bits': sorted(active_bits),
            'dual': dual_en,
            'deps_es': sorted(all_deps),
        }

    if missing:
        print(f'  WARNING: Missing translations: {missing}')

    # Uniqueness check
    sigs = set()
    for key, info in gold.items():
        sigs.add(tuple(info['binary_signature']))

    print()
    print(f'  Generated: {len(gold)} entries')
    print(f'  Unique signatures: {len(sigs)}/{len(gold)} ({len(sigs)/len(gold)*100:.1f}%)')

    # Per-capa stats
    by_capa = {}
    for key, info in gold.items():
        c = info['capa']
        if c not in by_capa:
            by_capa[c] = []
        by_capa[c].append(info)

    print()
    for capa in sorted(by_capa.keys()):
        items = by_capa[capa]
        bits = [i['n_active'] for i in items]
        print(f'  Capa {capa}: {len(items)} primitivos, {min(bits)}-{max(bits)} active bits')

    # Dual pairs
    print()
    dual_count = sum(1 for info in gold.values() if info['dual'])
    print(f'  Dual pairs: {dual_count // 2} (from {dual_count} entries with dual field)')

    # Save
    out_path = os.path.join(SCRIPT_DIR, 'gold_primitivos_65.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(gold, f, indent=2, ensure_ascii=False)

    print()
    print(f'  Saved: {out_path}')

    # Sample
    print()
    print('  Sample entries:')
    for key in list(gold.keys())[:5]:
        info = gold[key]
        print(f'    {key:20s} text="{info["text"]}"')
        print(f'    {"":20s} bits={info["n_active"]}  capa={info["capa"]}  dual={info["dual"]}')

    print()
    print('=' * 70)


if __name__ == '__main__':
    main()
