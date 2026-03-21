"""Test 7: Formal extraction of the 63-primitive poset.
Verify DAG, compute Hasse diagram, width, depth, chains, antichains."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
from collections import defaultdict, deque

DATA_DIR = r'C:\Github\triadic-microgpt\playground\danza_data'

with open(f'{DATA_DIR}/primitivos.json', 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

prims = prim_data['primitivos']
names = [p['nombre'] for p in prims]
deps_map = {p['nombre']: list(p['deps']) for p in prims}
capa_map = {p['nombre']: p['capa'] for p in prims}

children = defaultdict(set)
parents = defaultdict(set)
for p in prims:
    for d in p['deps']:
        children[d].add(p['nombre'])
        parents[p['nombre']].add(d)

print(f'Total primitives: {len(prims)}')
print(f'Total direct dependency edges: {sum(len(p["deps"]) for p in prims)}')
print()

# ========== 1. VERIFY DAG ==========
print('=' * 70)
print('1. DAG VERIFICATION')
print('=' * 70)
print()

# Check for cycles using DFS
def has_cycle():
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in names}
    cycle_path = []

    def dfs(u):
        color[u] = GRAY
        for v in children.get(u, set()):
            if color[v] == GRAY:
                cycle_path.append((u, v))
                return True
            if color[v] == WHITE:
                if dfs(v):
                    return True
        color[u] = BLACK
        return False

    for n in names:
        if color[n] == WHITE:
            if dfs(n):
                return True, cycle_path
    return False, []

is_cyclic, cycle = has_cycle()
print(f'Graph is DAG (no cycles): {not is_cyclic}')
if is_cyclic:
    print(f'  CYCLE FOUND: {cycle}')
print()

# ========== 2. POSET PROPERTIES ==========
print('=' * 70)
print('2. POSET PROPERTIES')
print('=' * 70)
print()

# Transitive closure
def transitive_closure(node, visited=None):
    if visited is None:
        visited = set()
    if node in visited:
        return set()
    visited.add(node)
    result = set()
    for c in children.get(node, set()):
        result.add(c)
        result |= transitive_closure(c, visited)
    return result

# Compute for all nodes
tc = {n: transitive_closure(n) for n in names}
tc_up = {}
def ancestors(node, visited=None):
    if visited is None:
        visited = set()
    if node in visited:
        return set()
    visited.add(node)
    result = set()
    for p in parents.get(node, set()):
        result.add(p)
        result |= ancestors(p, visited)
    return result

tc_up = {n: ancestors(n) for n in names}

# Roots and leaves
roots = [n for n in names if not parents.get(n)]
leaves = [n for n in names if not children.get(n)]

print(f'Roots (minimal elements): {len(roots)}')
for r in roots:
    print(f'  {r} (capa {capa_map[r]}, {len(tc[r])} descendants)')
print()
print(f'Leaves (maximal elements): {len(leaves)}')
for l in sorted(leaves, key=lambda x: capa_map.get(x, 0)):
    print(f'  {l} (capa {capa_map[l]}, {len(tc_up[l])} ancestors)')
print()

# ========== 3. WIDTH AND DEPTH ==========
print('=' * 70)
print('3. WIDTH AND DEPTH')
print('=' * 70)
print()

# Width by layer
layer_counts = defaultdict(list)
for p in prims:
    layer_counts[p['capa']].append(p['nombre'])

print('Width by layer:')
for layer in sorted(layer_counts.keys()):
    members = layer_counts[layer]
    print(f'  Layer {layer} ({prim_data["capas"][str(layer)]["nombre"]}): {len(members)} primitives')
    print(f'    {", ".join(sorted(members))}')

max_width = max(len(v) for v in layer_counts.values())
max_width_layer = max(layer_counts.keys(), key=lambda k: len(layer_counts[k]))
print(f'\nMaximum width: {max_width} (layer {max_width_layer})')

# Depth: longest chain
def longest_chain_from(node, memo={}):
    if node in memo:
        return memo[node]
    if not children.get(node):
        memo[node] = 1
        return 1
    result = 1 + max(longest_chain_from(c, memo) for c in children[node])
    memo[node] = result
    return result

max_chain = 0
max_chain_root = None
for r in roots:
    lc = longest_chain_from(r, {})
    if lc > max_chain:
        max_chain = lc
        max_chain_root = r

print(f'\nMaximum chain length: {max_chain} (from {max_chain_root})')

# Find an actual longest chain
def find_longest_chain(node, memo={}):
    if not children.get(node):
        return [node]
    best = []
    for c in children[node]:
        chain = find_longest_chain(c, memo)
        if len(chain) > len(best):
            best = chain
    return [node] + best

longest = find_longest_chain(max_chain_root, {})
print(f'Longest chain: {" -> ".join(longest)}')

# ========== 4. HASSE DIAGRAM (transitive reduction) ==========
print()
print('=' * 70)
print('4. HASSE DIAGRAM (TRANSITIVE REDUCTION)')
print('=' * 70)
print()

# Hasse diagram = remove transitive edges
# For each edge (u, v), remove it if there's a path u -> w -> ... -> v of length >= 2
hasse_edges = []
removed_edges = []
for p in prims:
    for d in p['deps']:
        # Check if there's another path from d to p['nombre'] via some intermediate
        # i.e., does d have any descendant that is also an ancestor of p['nombre']?
        other_parents = set(p['deps']) - {d}
        # Is d an ancestor of any other parent of p?
        is_redundant = False
        for op in other_parents:
            if d in tc_up.get(op, set()):
                is_redundant = True
                break
        if is_redundant:
            removed_edges.append((d, p['nombre']))
        else:
            hasse_edges.append((d, p['nombre']))

print(f'Total direct edges: {sum(len(p["deps"]) for p in prims)}')
print(f'Hasse edges (after transitive reduction): {len(hasse_edges)}')
print(f'Removed (transitively redundant): {len(removed_edges)}')
print()

if removed_edges:
    print('Redundant edges removed:')
    for parent, child in sorted(removed_edges):
        print(f'  {parent} -> {child} (redundant: reachable via other path)')
print()

# ========== 5. MAXIMAL ANTICHAINS ==========
print('=' * 70)
print('5. MAXIMAL ANTICHAINS (largest sets of incomparable elements)')
print('=' * 70)
print()

# Two elements are comparable if one is ancestor of the other
def are_comparable(a, b):
    return b in tc.get(a, set()) or a in tc.get(b, set())

# Dilworth's theorem: max antichain width = min chain partition
# For our purposes, just find antichains by layer (each layer is an antichain
# if no two elements in the same layer are comparable)

for layer in sorted(layer_counts.keys()):
    members = layer_counts[layer]
    is_antichain = True
    for i in range(len(members)):
        for j in range(i+1, len(members)):
            if are_comparable(members[i], members[j]):
                is_antichain = False
                print(f'  Layer {layer} NOT antichain: {members[i]} and {members[j]} are comparable')
                break
        if not is_antichain:
            break
    if is_antichain:
        print(f'  Layer {layer}: antichain of size {len(members)}')

# ========== 6. CONNECTED COMPONENTS ==========
print()
print('=' * 70)
print('6. CONNECTED COMPONENTS (undirected)')
print('=' * 70)
print()

# Build undirected adjacency
adj = defaultdict(set)
for p in prims:
    for d in p['deps']:
        adj[p['nombre']].add(d)
        adj[d].add(p['nombre'])

visited = set()
components = []
for n in names:
    if n not in visited:
        # BFS
        component = set()
        queue = deque([n])
        while queue:
            v = queue.popleft()
            if v in visited:
                continue
            visited.add(v)
            component.add(v)
            for w in adj[v]:
                if w not in visited:
                    queue.append(w)
        components.append(component)

print(f'Number of connected components: {len(components)}')
for i, comp in enumerate(sorted(components, key=len, reverse=True)):
    roots_in = [r for r in roots if r in comp]
    print(f'  Component {i+1}: {len(comp)} nodes, roots: {roots_in}')

# ========== 7. LATTICE VERIFICATION ==========
print()
print('=' * 70)
print('7. LATTICE VERIFICATION')
print('Every pair should have a join (LUB) and meet (GLB)')
print('=' * 70)
print()

# For the 63-element poset, check if it's a lattice
# A poset is a lattice iff every pair has a join and a meet

# For efficiency, check a sample of pairs
import random
random.seed(42)
sample_size = 200
sample_pairs = []
for _ in range(sample_size):
    a, b = random.sample(names, 2)
    sample_pairs.append((a, b))

# Also include key pairs
key_pairs = [
    ('contención', 'porque'),
    ('contención', 'tipo_de'),
    ('porque', 'tipo_de'),
    ('vida', 'porque'),
    ('consciente', 'tipo_de'),
    ('vacío', 'información'),
    ('vacío', 'uno'),
    ('información', 'uno'),
]
sample_pairs.extend(key_pairs)

def find_join(a, b):
    """Find least upper bound (smallest common descendant)"""
    desc_a = tc.get(a, set()) | {a}
    desc_b = tc.get(b, set()) | {b}
    common = desc_a & desc_b
    if not common:
        return None
    # Find minimal elements of common
    minimal = set()
    for c in common:
        anc_c = tc_up.get(c, set()) | {c}
        if not (anc_c & common - {c}):
            # No element in common is an ancestor of c (other than c itself)
            # Wait, need to check if any other common element is a descendant of c
            pass
    # Simpler: find elements in common that have no ancestors in common
    for c in common:
        is_minimal = True
        for d in common:
            if d != c and c in tc.get(d, set()):
                is_minimal = False
                break
        if is_minimal:
            minimal.add(c)
    return minimal

def find_meet(a, b):
    """Find greatest lower bound (largest common ancestor)"""
    anc_a = tc_up.get(a, set()) | {a}
    anc_b = tc_up.get(b, set()) | {b}
    common = anc_a & anc_b
    if not common:
        return None
    # Find maximal elements of common
    maximal = set()
    for c in common:
        is_maximal = True
        for d in common:
            if d != c and d in tc.get(c, set()):
                is_maximal = False
                break
        if is_maximal:
            maximal.add(c)
    return maximal

has_join_count = 0
has_meet_count = 0
no_join = []
no_meet = []
multi_join = []
multi_meet = []

for a, b in sample_pairs:
    j = find_join(a, b)
    m = find_meet(a, b)

    if j is None or len(j) == 0:
        no_join.append((a, b))
    elif len(j) == 1:
        has_join_count += 1
    else:
        multi_join.append((a, b, j))

    if m is None or len(m) == 0:
        no_meet.append((a, b))
    elif len(m) == 1:
        has_meet_count += 1
    else:
        multi_meet.append((a, b, m))

total = len(sample_pairs)
print(f'Sample size: {total} pairs')
print(f'  Unique join exists: {has_join_count} ({has_join_count/total*100:.0f}%)')
print(f'  Multiple joins (not lattice): {len(multi_join)} ({len(multi_join)/total*100:.0f}%)')
print(f'  No join exists: {len(no_join)} ({len(no_join)/total*100:.0f}%)')
print(f'  Unique meet exists: {has_meet_count} ({has_meet_count/total*100:.0f}%)')
print(f'  Multiple meets (not lattice): {len(multi_meet)} ({len(multi_meet)/total*100:.0f}%)')
print(f'  No meet exists: {len(no_meet)} ({len(no_meet)/total*100:.0f}%)')
print()

if no_join:
    print('Pairs with NO join (no common descendant):')
    for a, b in no_join[:10]:
        print(f'  {a} and {b}')
    if len(no_join) > 10:
        print(f'  ... and {len(no_join) - 10} more')

if multi_join:
    print()
    print('Pairs with MULTIPLE joins (multiple minimal common descendants):')
    for a, b, j in multi_join[:10]:
        print(f'  {a} and {b}: joins = {sorted(j)}')

if multi_meet:
    print()
    print('Pairs with MULTIPLE meets (multiple maximal common ancestors):')
    for a, b, m in multi_meet[:10]:
        print(f'  {a} and {b}: meets = {sorted(m)}')

is_lattice = len(no_join) == 0 and len(no_meet) == 0 and len(multi_join) == 0 and len(multi_meet) == 0
print()
print(f'IS THE POSET A LATTICE? {"YES" if is_lattice else "NO"}')
if not is_lattice:
    reasons = []
    if no_join: reasons.append(f'{len(no_join)} pairs lack joins')
    if no_meet: reasons.append(f'{len(no_meet)} pairs lack meets')
    if multi_join: reasons.append(f'{len(multi_join)} pairs have multiple joins')
    if multi_meet: reasons.append(f'{len(multi_meet)} pairs have multiple meets')
    print(f'  Reasons: {"; ".join(reasons)}')
    print(f'  The poset is a DAG but NOT a lattice — it is a general poset.')

# ========== 8. SUMMARY STATISTICS ==========
print()
print('=' * 70)
print('8. SUMMARY')
print('=' * 70)
print()
print(f'Nodes: {len(names)}')
print(f'Direct edges: {sum(len(p["deps"]) for p in prims)}')
print(f'Hasse edges: {len(hasse_edges)}')
print(f'Is DAG: {not is_cyclic}')
print(f'Is lattice: {is_lattice}')
print(f'Roots: {len(roots)} ({", ".join(roots)})')
print(f'Leaves: {len(leaves)}')
print(f'Maximum chain: {max_chain}')
print(f'Maximum width: {max_width} (layer {max_width_layer})')
print(f'Layers: {len(layer_counts)} ({", ".join(str(k) for k in sorted(layer_counts.keys()))})')
print(f'Connected components: {len(components)}')
