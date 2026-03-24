"""Test 2: Betweenness centrality for all primitives"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import os
from collections import defaultdict, deque

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')

with open(f'{DATA_DIR}/primitivos.json', 'r', encoding='utf-8') as f:
    prim_data = json.load(f)

prims = prim_data['primitivos']
names = [p['nombre'] for p in prims]
deps_map = {p['nombre']: p['deps'] for p in prims}
capa_map = {p['nombre']: p['capa'] for p in prims}

# Build directed graph (parent -> children) and (child -> parents)
children = defaultdict(set)
parents = defaultdict(set)
for p in prims:
    for d in p['deps']:
        children[d].add(p['nombre'])
        parents[p['nombre']].add(d)

# ========== BETWEENNESS CENTRALITY ==========
print('=' * 60)
print('TEST 2: BETWEENNESS CENTRALITY')
print('=' * 60)
print()

# Build undirected adjacency for BFS
adj = defaultdict(set)
for p in prims:
    for d in p['deps']:
        adj[p['nombre']].add(d)
        adj[d].add(p['nombre'])

def bfs_centrality(source):
    """BFS from source, returns partial betweenness contributions"""
    dist = {source: 0}
    num_paths = defaultdict(int)
    num_paths[source] = 1
    preds = defaultdict(list)
    queue = deque([source])
    order = []

    while queue:
        v = queue.popleft()
        order.append(v)
        for w in adj[v]:
            if w not in dist:
                dist[w] = dist[v] + 1
                queue.append(w)
            if dist[w] == dist[v] + 1:
                num_paths[w] += num_paths[v]
                preds[w].append(v)

    delta = defaultdict(float)
    for w in reversed(order):
        for v in preds[w]:
            if num_paths[w] > 0:
                delta[v] += (num_paths[v] / num_paths[w]) * (1 + delta[w])
        if w != source:
            yield w, delta[w]

betweenness = defaultdict(float)
all_names = list(set(names))

for s in all_names:
    for node, contrib in bfs_centrality(s):
        betweenness[node] += contrib

# Normalize
n = len(all_names)
if n > 2:
    norm = 1.0 / ((n - 1) * (n - 2))
else:
    norm = 1.0
for k in betweenness:
    betweenness[k] *= norm

sorted_bc = sorted(betweenness.items(), key=lambda x: -x[1])

key_prims = {'uno', 'contención', 'vida', 'consciente', 'porque', 'tipo_de',
             'fuerza', 'mover', 'orden', 'parte_de', 'información'}

print('Top 30 primitives by betweenness centrality:')
print(f'{"Rank":<5} {"Primitive":<22} {"Layer":<6} {"Centrality":<12} {"Key?"}')
print('-' * 60)

for i, (name, bc) in enumerate(sorted_bc[:30]):
    capa = capa_map.get(name, '?')
    marker = ' <<<' if name in key_prims else ''
    print(f'{i+1:<5} {name:<22} {capa:<6} {bc:.6f}{marker}')

print()
print('Key duality primitives ranked:')
print(f'{"Primitive":<22} {"Layer":<6} {"Centrality":<12} {"Rank":<6} {"Predicted role"}')
print('-' * 75)

predictions = {
    'uno': 'Root hub (d8)',
    'contención': 'Main trunk hub (d10)',
    'vida': 'Reunification hub',
    'consciente': 'Terminal hub (d14)',
    'fuerza': 'Dynamic root',
    'mover': 'Temporal path',
    'orden': 'Pattern hub (d7)',
    'información': 'Data root',
    'porque': 'Causal dead-end (d11)',
    'tipo_de': 'Classif. leaf (d12)',
    'parte_de': 'Mereological (d13)',
}

for target in ['uno', 'contención', 'fuerza', 'mover', 'información', 'orden',
               'vida', 'consciente', 'porque', 'tipo_de', 'parte_de']:
    if target in betweenness:
        rank = [name for name, _ in sorted_bc].index(target) + 1
        capa = capa_map.get(target, '?')
        pred = predictions.get(target, '')
        print(f'{target:<22} {capa:<6} {betweenness[target]:.6f} #{rank:<5} {pred}')

print()

# ========== DEGREE ANALYSIS ==========
print('=' * 60)
print('DEGREE ANALYSIS (directed graph)')
print('=' * 60)
print()
print(f'{"Primitive":<22} {"In-deg":<8} {"Out-deg":<8} {"Total":<8} {"Layer"}')
print('-' * 55)
for target in ['uno', 'contención', 'fuerza', 'información', 'mover',
               'orden', 'vida', 'consciente', 'porque', 'tipo_de', 'parte_de',
               'separación', 'más', 'vacío']:
    in_deg = len(parents.get(target, set()))
    out_deg = len(children.get(target, set()))
    capa = capa_map.get(target, '?')
    print(f'{target:<22} {in_deg:<8} {out_deg:<8} {in_deg + out_deg:<8} {capa}')

print()

# ========== FLOW CENTRALITY (DAG-specific) ==========
print('=' * 60)
print('DAG FLOW CENTRALITY (paths from roots to leaves)')
print('=' * 60)
print()

# Count paths from each root through the DAG
roots = [p['nombre'] for p in prims if not p['deps']]
leaves = [name for name in names if not children.get(name)]

print(f'Roots: {roots}')
print(f'Leaves ({len(leaves)}): {leaves[:10]}...')
print()

# Count how many root-to-leaf paths pass through each node
def count_paths_through(node):
    """Count paths from any root to any leaf passing through node"""
    # Count paths from roots to node
    paths_to = defaultdict(int)
    for r in roots:
        paths_to[r] = 1

    # Topological sort
    topo = []
    in_degree = defaultdict(int)
    for p in prims:
        for d in p['deps']:
            in_degree[p['nombre']] += 1

    queue = deque([n for n in names if in_degree[n] == 0])
    while queue:
        v = queue.popleft()
        topo.append(v)
        for c in children.get(v, set()):
            in_degree[c] -= 1
            if in_degree[c] == 0:
                queue.append(c)

    # Forward pass: count paths from roots to each node
    paths_from_root = defaultdict(int)
    for r in roots:
        paths_from_root[r] = 1
    for v in topo:
        for c in children.get(v, set()):
            paths_from_root[c] += paths_from_root[v]

    # Backward pass: count paths from each node to leaves
    paths_to_leaf = defaultdict(int)
    for l in leaves:
        paths_to_leaf[l] = 1
    for v in reversed(topo):
        for c in children.get(v, set()):
            paths_to_leaf[v] += paths_to_leaf[c]

    return paths_from_root, paths_to_leaf

paths_from_root, paths_to_leaf = count_paths_through(None)

# Flow = paths_from_root * paths_to_leaf (for intermediate nodes)
flow = {}
for name in names:
    flow[name] = paths_from_root[name] * paths_to_leaf[name]

sorted_flow = sorted(flow.items(), key=lambda x: -x[1])

print('Top 20 by DAG flow centrality (root-to-leaf paths through node):')
print(f'{"Rank":<5} {"Primitive":<22} {"Layer":<6} {"Flow":<10} {"Key?"}')
print('-' * 55)
for i, (name, f) in enumerate(sorted_flow[:20]):
    capa = capa_map.get(name, '?')
    marker = ' <<<' if name in key_prims else ''
    print(f'{i+1:<5} {name:<22} {capa:<6} {f:<10}{marker}')

print()
print('Key primitives by flow:')
for target in ['uno', 'contención', 'fuerza', 'mover', 'información', 'orden',
               'vida', 'consciente', 'porque', 'tipo_de', 'parte_de']:
    if target in flow:
        rank = [name for name, _ in sorted_flow].index(target) + 1
        print(f'  {target}: flow={flow[target]}, rank #{rank}')
