"""Map cascade bits from V9_xray_zoom2 to primitivos and layers."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import os
from collections import Counter

DATA_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))

with open(os.path.join(DATA_DIR, 'primitivos.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

prims = data['primitivos']
bit_map = {p.get('bit'): p for p in prims if p.get('bit') is not None}

waves = [
    ('Semilla (5060)', [12, 41, 23, 47, 31, 35]),
    ('Oleada 2 (5065)', [11, 3, 33, 69, 58, 8, 7, 59]),
    ('Oleada 3 (5070)', [67, 30, 5, 28, 61]),
    ('Oleada 4 (5075)', [18, 17, 43, 14]),
    ('Oleada 5 (5080)', [4]),
    ('Oleada 6 (5085)', [52, 57, 42, 66]),
    ('Oleada 7 (5100)', [0, 44, 39]),
    ('Estables (no cambian)', [60, 63, 68, 70, 71]),
]

for name, bits in waves:
    print(f'=== {name} ===')
    capas = []
    for b in bits:
        p = bit_map.get(b, {})
        nombre = p.get('nombre', '?')
        capa = p.get('capa', '?')
        dual = p.get('dual', '-')
        capas.append(capa)
        print(f'  bit {b:>2}: {nombre:<20} capa={capa}  dual={dual}')
    dist = Counter(capas)
    print(f'  >> Distribucion capas: {dict(sorted(dist.items()))}')
    print()

# Summary table
print('=== RESUMEN: CAPAS POR OLEADA ===')
print(f'  {"Oleada":<22} {"N":>3}  L1  L2  L3  L4  L5  L6')
print(f'  {"-"*22} {"-"*3}  {"-"*3} {"-"*3} {"-"*3} {"-"*3} {"-"*3} {"-"*3}')
for name, bits in waves:
    capas = [bit_map.get(b, {}).get('capa', '?') for b in bits]
    dist = Counter(capas)
    row = f'  {name:<22} {len(bits):>3}'
    for l in range(1, 7):
        row += f'  {dist.get(l, 0):>3}'
    print(row)
