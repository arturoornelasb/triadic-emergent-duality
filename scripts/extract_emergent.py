"""Extract emergent concepts from v6 collapse analysis for ConceptFlow."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load data
with open(os.path.join(ROOT, "data/primitivos.json")) as f:
    prims = json.load(f)
bit_names = {p["bit"]: p["nombre"] for p in prims["primitivos"]}

with open(os.path.join(ROOT, "dualidademergente+reptimeline/runs/v6/exploration.json")) as f:
    data = json.load(f)
sigs = data["signatures"]
groups = sorted(data["signature_uniqueness"]["collision_groups"], key=len, reverse=True)


def get_domain(name):
    parts = name.split("_")
    return parts[1] if (parts[0].isdigit() or parts[0] == "fp") and len(parts) > 1 else parts[0]


def get_subdomain(name):
    parts = name.split("_")
    if parts[0].isdigit() and len(parts) > 4:
        return "_".join(parts[2:-2])
    elif parts[0].isdigit():
        return "_".join(parts[2:])
    return "_".join(parts[1:])


# ── 1. Universal core ──────────────────────────────
top12 = groups[:12]
universal = None
for g in top12:
    bits = set(sigs[g[0]]["active_indices"])
    universal = bits if universal is None else universal & bits
universal_names = sorted([bit_names[b] for b in universal])

# ── 2. Domain archetypes (clusters >= 5 concepts) ──
archetypes = {}
for g in groups:
    bits = frozenset(sigs[g[0]]["active_indices"])
    domain = get_domain(g[0])
    sub = get_subdomain(g[0])
    key = f"{domain}_{sub}"
    if key not in archetypes and len(g) >= 5:
        archetypes[key] = {
            "bits": sorted([bit_names[b] for b in bits]),
            "size": len(g),
            "domain": domain,
            "subdomain": sub,
        }

# ── 3. Cross-domain MCDs (emergent bridge concepts, J>=0.90) ──
cluster_list = []
for g in groups:
    domain = get_domain(g[0])
    sub = get_subdomain(g[0])
    cluster_list.append({
        "bits": set(sigs[g[0]]["active_indices"]),
        "domain": domain,
        "sub": sub,
        "size": len(g),
    })

cross_mcds = []
seen = set()
for i in range(len(cluster_list)):
    for j in range(i + 1, len(cluster_list)):
        if cluster_list[i]["domain"] == cluster_list[j]["domain"]:
            continue
        a = cluster_list[i]["bits"]
        b = cluster_list[j]["bits"]
        shared = a & b
        union = a | b
        jacc = len(shared) / len(union) if union else 0
        if jacc < 0.90:
            continue
        mcd_key = frozenset(shared)
        if mcd_key in seen:
            continue
        seen.add(mcd_key)
        cross_mcds.append({
            "bits": sorted([bit_names[x] for x in shared]),
            "domains": sorted([cluster_list[i]["domain"], cluster_list[j]["domain"]]),
            "subs": [
                f"{cluster_list[i]['domain']}:{cluster_list[i]['sub']}",
                f"{cluster_list[j]['domain']}:{cluster_list[j]['sub']}",
            ],
            "jacc": jacc,
            "diff_a": sorted([bit_names[x] for x in a - shared]),
            "diff_b": sorted([bit_names[x] for x in b - shared]),
        })

# ── 4. Opposing domain pairs (lowest Jaccard) ──
opposing = []
seen_opp = set()
for i in range(len(cluster_list)):
    for j in range(i + 1, len(cluster_list)):
        a = cluster_list[i]["bits"]
        b = cluster_list[j]["bits"]
        shared = a & b
        union = a | b
        jacc = len(shared) / len(union) if union else 0
        if jacc > 0.35 or jacc == 0:
            continue
        dom_pair = tuple(sorted([cluster_list[i]["domain"], cluster_list[j]["domain"]]))
        if dom_pair in seen_opp:
            continue
        seen_opp.add(dom_pair)
        opposing.append({
            "jacc": jacc,
            "pole_a": {
                "domain": cluster_list[i]["domain"],
                "sub": cluster_list[i]["sub"],
                "bits": sorted([bit_names[x] for x in a]),
                "only": sorted([bit_names[x] for x in a - b]),
            },
            "pole_b": {
                "domain": cluster_list[j]["domain"],
                "sub": cluster_list[j]["sub"],
                "bits": sorted([bit_names[x] for x in b]),
                "only": sorted([bit_names[x] for x in b - a]),
            },
            "shared": sorted([bit_names[x] for x in shared]),
        })
opposing.sort(key=lambda x: x["jacc"])

# ── Build output ──
emergent = {
    "_meta": {
        "source": "dualidad_emergente v6 collapse analysis",
        "date": "2026-03-27",
        "method": "MCD of cross-domain collision clusters + domain archetypes + opposing pairs",
        "model": "gpt2_triadic_72_v6 (frozen base, 100K steps, 2166 concepts)",
    },
    "core_universal": {
        "en": "universal first-principle core",
        "bits": universal_names,
        "razon": f"MCD de los 12 clusters mas grandes. Firma base de todo first-principle segun el modelo.",
    },
}

# Domain archetypes
for key, arch in sorted(archetypes.items(), key=lambda x: -x[1]["size"])[:20]:
    safe_key = f"arquetipo_{arch['domain']}_{arch['subdomain']}"[:60].rstrip("_")
    emergent[safe_key] = {
        "en": f"{arch['domain']} {arch['subdomain']} archetype",
        "bits": arch["bits"],
        "razon": f"Firma compartida por {arch['size']} principios de {arch['domain']}:{arch['subdomain']}. Concepto emergente del colapso v6.",
    }

# Cross-domain bridges (top 15 unique)
for idx, mcd in enumerate(sorted(cross_mcds, key=lambda x: (-x["jacc"], -len(x["bits"])))[:15]):
    d1, d2 = mcd["domains"]
    safe_key = f"puente_{d1}_{d2}_{idx+1}"
    diff_a_str = ", ".join(mcd["diff_a"]) if mcd["diff_a"] else "ninguno"
    diff_b_str = ", ".join(mcd["diff_b"]) if mcd["diff_b"] else "ninguno"
    emergent[safe_key] = {
        "en": f"emergent bridge {d1}-{d2}",
        "bits": mcd["bits"],
        "razon": f"MCD cross-domain J={mcd['jacc']:.2f}. Puente entre {mcd['subs'][0]} y {mcd['subs'][1]}. Solo izq: [{diff_a_str}]. Solo der: [{diff_b_str}].",
    }

# Opposing pairs as dual concepts
for idx, opp in enumerate(opposing[:8]):
    pa, pb = opp["pole_a"], opp["pole_b"]
    emergent[f"polo_{pa['domain']}_vs_{pb['domain']}"] = {
        "en": f"{pa['domain']} pole (vs {pb['domain']})",
        "bits": pa["bits"],
        "razon": f"Polo de la dualidad {pa['domain']}/{pb['domain']} (J={opp['jacc']:.2f}). Bits exclusivos: [{', '.join(pa['only'])}].",
    }
    emergent[f"polo_{pb['domain']}_vs_{pa['domain']}"] = {
        "en": f"{pb['domain']} pole (vs {pa['domain']})",
        "bits": pb["bits"],
        "razon": f"Polo de la dualidad {pb['domain']}/{pa['domain']} (J={opp['jacc']:.2f}). Bits exclusivos: [{', '.join(pb['only'])}].",
    }
    emergent[f"eje_{pa['domain']}_{pb['domain']}"] = {
        "en": f"{pa['domain']}-{pb['domain']} axis",
        "bits": opp["shared"],
        "razon": f"Eje compartido (concepto-temperatura) entre {pa['domain']} y {pb['domain']}. Lo que une a los opuestos.",
    }

# Write
out_path = os.path.join(ROOT, "data/emergent_v6.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(emergent, f, ensure_ascii=False, indent=2)

n_entries = len([k for k in emergent if not k.startswith("_")])
n_archetypes = len([k for k in emergent if k.startswith("arquetipo")])
n_bridges = len([k for k in emergent if k.startswith("puente")])
n_poles = len([k for k in emergent if k.startswith("polo")])
n_axes = len([k for k in emergent if k.startswith("eje")])

print(f"Escrito: {out_path}")
print(f"  Total entradas: {n_entries}")
print(f"  Core universal: {len(universal_names)} bits")
print(f"  Arquetipos: {n_archetypes}")
print(f"  Puentes cross-domain: {n_bridges}")
print(f"  Polos opuestos: {n_poles}")
print(f"  Ejes (temperatura): {n_axes}")
