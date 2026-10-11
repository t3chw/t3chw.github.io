#!/usr/bin/env python3
"""Add explicit imports to CODE blocks that use stdlib names LeetCode may not pre-import."""
import ast, builtins, glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import check
FROM = {
 'collections': ['deque', 'defaultdict', 'Counter', 'OrderedDict'],
 'heapq': ['heappush', 'heappop', 'heapify', 'heappushpop', 'heapreplace', 'nlargest', 'nsmallest'],
 'bisect': ['bisect_left', 'bisect_right', 'bisect', 'insort'],
 'functools': ['lru_cache', 'cache', 'reduce', 'cmp_to_key'],
 'math': ['inf', 'gcd', 'comb', 'perm', 'sqrt', 'ceil', 'floor', 'log2', 'isqrt', 'lcm', 'factorial'],
 'itertools': ['accumulate', 'product', 'permutations', 'combinations', 'groupby', 'zip_longest', 'chain', 'islice'],
}
MODULES = ['collections', 'heapq', 'bisect', 'math', 'itertools', 'functools', 'string', 'random', 're', 'sys']
NAME2MOD = {n: m for m, ns in FROM.items() for n in ns}
PROVIDED = set(dir(builtins)) | {'ListNode', 'TreeNode'} | set(__import__('typing').__all__)

def needed(code):
    tree = ast.parse(code)
    bound, used = set(), set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Name):
            (used if isinstance(n.ctx, ast.Load) else bound).add(n.id)
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)): bound.add(n.name)
        elif isinstance(n, ast.arg): bound.add(n.arg)
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            for a in n.names: bound.add((a.asname or a.name).split('.')[0])
        elif isinstance(n, ast.ExceptHandler) and n.name: bound.add(n.name)
    free = used - bound - PROVIDED
    frm, mods = {}, []
    for name in sorted(free):
        if name in NAME2MOD: frm.setdefault(NAME2MOD[name], []).append(name)
        elif name in MODULES: mods.append(name)
    lines = [f'import {m}' for m in sorted(mods)] + [f'from {m} import ' + ', '.join(ns) for m, ns in sorted(frm.items())]
    return lines

changed = {}
for f in sorted(glob.glob(os.path.join(HERE, 'ds_*.txt'))):
    pats = check.parse(f)
    ins = {}
    for p in pats:
        for q in p['problems']:
            lines = needed(q['code'])
            if lines: ins[q['slug']] = lines
    if not ins: continue
    out, cur = [], None
    for line in open(f, encoding='utf-8').read().split('\n'):
        m = re.match(r'^@@ PROBLEM:\s*(.*)$', line)
        if m: cur = m.group(1).strip()
        out.append(line)
        if line.startswith('@@ CODE:') and cur in ins:
            out.extend(ins[cur]); out.append('')
    open(f, 'w', encoding='utf-8').write('\n'.join(out))
    changed[os.path.basename(f)] = ins
for f, ins in changed.items():
    print(f)
    for s, l in ins.items(): print('   ', s, '<-', '; '.join(l))
print(sum(len(v) for v in changed.values()), 'problems patched')
