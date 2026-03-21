"""I5: Resolve the 65 vs 63 discrepancy.

Identifies which primitivos have bit indices outside the 0-62 range
used by TriadicGPT, and documents the implications.

Solo stdlib: json, os, sys.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'data'))
RESULTS_DIR = os.path.join(SCRIPT_DIR, 'results')

# ######################################################################
#  SECTION 0: DATA LOADING
# ######################################################################

with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

prims = prim_data['primitivos']

# ######################################################################
#  SECTION 1: ANALYSIS
# ######################################################################

print("=" * 70)
print("I5: Discrepancy 65 vs 63")
print("=" * 70)

total = len(prims)
print(f"\nTotal primitivos in primitivos.json: {total}")

# Check bit assignments
bits_used = {}
no_bit = []
out_of_range = []

for p in prims:
    bit = p.get('bit')
    name = p['nombre']
    capa = p['capa']

    if bit is None:
        no_bit.append(p)
    elif bit < 0 or bit > 62:
        out_of_range.append(p)
        bits_used[bit] = name
    else:
        bits_used[bit] = name

# Bits in 0-62 not assigned
assigned_in_range = {b for b in bits_used if 0 <= b <= 62}
unassigned_bits = set(range(63)) - assigned_in_range

print(f"\nBits in range 0-62 assigned: {len(assigned_in_range)}")
print(f"Bits in range 0-62 unassigned: {len(unassigned_bits)}")
if unassigned_bits:
    print(f"  Unassigned bit indices: {sorted(unassigned_bits)}")

print(f"\nPrimitivos with no bit: {len(no_bit)}")
for p in no_bit:
    print(f"  - {p['nombre']} (capa {p['capa']}, primo {p['primo']})")

print(f"\nPrimitivos with bit outside 0-62: {len(out_of_range)}")
for p in out_of_range:
    print(f"  - {p['nombre']} (bit={p['bit']}, capa {p['capa']}, primo {p['primo']})")
    print(f"    deps: {p['deps']}")
    print(f"    def:  {p.get('def', 'N/A')}")

# Check for duplicate bits
bit_counts = {}
for p in prims:
    b = p.get('bit')
    if b is not None:
        bit_counts[b] = bit_counts.get(b, 0) + 1
duplicates = {b: c for b, c in bit_counts.items() if c > 1}
if duplicates:
    print(f"\nDuplicate bit assignments: {duplicates}")
else:
    print(f"\nNo duplicate bit assignments.")

# ######################################################################
#  SECTION 2: IMPLICATIONS
# ######################################################################

print("\n--- Implications ---\n")

extra_count = total - 63
if extra_count > 0:
    print(f"  {extra_count} primitivo(s) cannot be represented in a 63-bit code.")
    print("  Options:")
    print("    a) Redundant: covered by combination of other bits")
    print("    b) Meta-level: require composite representation")
    print("    c) Versioning: primitivos.json grew after fixing 63 bits")
elif extra_count == 0:
    print("  No discrepancy: 63 primitivos = 63 bits.")
else:
    print(f"  Fewer primitivos ({total}) than bits (63):")
    print(f"  {63 - total} bits have no assigned primitivo.")

# ######################################################################
#  SECTION 3: SAVE RESULTS
# ######################################################################

os.makedirs(RESULTS_DIR, exist_ok=True)
output = {
    'total_primitivos': total,
    'bits_in_range': len(assigned_in_range),
    'bits_unassigned': sorted(unassigned_bits),
    'primitivos_no_bit': [p['nombre'] for p in no_bit],
    'primitivos_out_of_range': [
        {'nombre': p['nombre'], 'bit': p['bit'], 'capa': p['capa'],
         'primo': p['primo'], 'deps': p['deps']}
        for p in out_of_range
    ],
    'duplicate_bits': duplicates,
    'extra_count': extra_count,
}

out_path = os.path.join(RESULTS_DIR, 'i5_discrepancia.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nResults saved to: {out_path}")
