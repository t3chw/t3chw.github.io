#!/usr/bin/env python3
"""Parse + verify pattern files.   usage: check.py ds_01.txt [ds_02.txt ...] | check.py --all  [--no-run] [--dump out.json]"""
import sys, re, json, subprocess, tempfile, os, glob, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = {r['slug']: r for r in json.load(open(os.path.join(HERE, 'catalog.json')))}
STRUCTS = {o['n']: o for o in json.load(open(os.path.join(HERE, 'patterns.json')))}
BASE = r'''
from typing import *
class ListNode:
    def __init__(self, val=0, next=None): self.val = val; self.next = next
class TreeNode:
    def __init__(self, val=0, left=None, right=None): self.val = val; self.left = left; self.right = right
'''
HELPERS = r'''
import collections, heapq, bisect, math, itertools, functools, string, random, re, sys
from collections import deque, defaultdict, Counter, OrderedDict
from functools import lru_cache, cache
from heapq import heappush, heappop, heapify
from bisect import bisect_left, bisect_right
from math import inf
def ll(a):
    d = ListNode(); t = d
    for x in a: t.next = ListNode(x); t = t.next
    return d.next
def to_list(h):
    out = []
    while h: out.append(h.val); h = h.next
    return out
def tree(a):
    if not a or a[0] is None: return None
    root = TreeNode(a[0]); q = deque([root]); i = 1
    while q and i < len(a):
        n = q.popleft()
        if i < len(a) and a[i] is not None: n.left = TreeNode(a[i]); q.append(n.left)
        i += 1
        if i < len(a) and a[i] is not None: n.right = TreeNode(a[i]); q.append(n.right)
        i += 1
    return root
def tree_to_list(root):
    if not root: return []
    out = []; q = deque([root])
    while q:
        n = q.popleft()
        if n is None: out.append(None); continue
        out.append(n.val); q.append(n.left); q.append(n.right)
    while out and out[-1] is None: out.pop()
    return out
'''
RUNNER = r'''
import sys, json
BASE, HELPERS = %r, %r
d = json.load(open(sys.argv[1]))
ns1 = {'__name__': 'solution'}
exec(BASE, ns1)
exec(d['code'], ns1)             # CODE sees ONLY typing + ListNode/TreeNode: any other name needs an explicit import
ns2 = {k: v for k, v in ns1.items() if k != '__builtins__'}
exec(HELPERS, ns2)               # test-only helpers and convenience imports, invisible to the solution's globals
exec(d['test'], ns2)
print("OK")
'''

KEYS = ('PATTERN', 'SPOT', 'PROBLEM', 'APPROACH', 'COMPLEXITY', 'CODE', 'TEST')
SINGLE = ('PATTERN', 'SPOT', 'PROBLEM', 'COMPLEXITY')

def parse(path):
    pats, cur_pat, cur = [], None, None
    key = None; buf = []
    def flush():
        nonlocal key, buf, cur
        if key in ('APPROACH', 'CODE', 'TEST') and cur is not None:
            cur[key.lower()] = '\n'.join(buf).strip('\n')
        key, buf = None, []
    for line in open(path, encoding='utf-8').read().split('\n'):
        m = re.match(r'^@@ (\w+):\s*(.*)$', line)
        if m and m.group(1) in KEYS:
            flush()
            k, v = m.group(1), m.group(2).strip()
            if k == 'PATTERN': cur_pat = dict(name=v, spot='', problems=[]); pats.append(cur_pat); cur = None
            elif k == 'SPOT': cur_pat['spot'] = v
            elif k == 'PROBLEM': cur = dict(slug=v); cur_pat['problems'].append(cur)
            elif k == 'COMPLEXITY': cur['complexity'] = v
            else: key = k; buf = [v] if v else []
        else:
            if key: buf.append(line)
    flush()
    return pats

def run_one(args):
    path, pi, qi, code, test = args
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as j: json.dump(dict(code=code, test=test), j); jn = j.name
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as f: f.write(RUNNER % (BASE, HELPERS)); fn = f.name
    try:
        r = subprocess.run([sys.executable, fn, jn], capture_output=True, text=True, timeout=30)
        ok = r.returncode == 0 and r.stdout.strip().endswith('OK')
        return (pi, qi, ok, (r.stderr or r.stdout).strip().split('\n')[-3:])
    except subprocess.TimeoutExpired:
        return (pi, qi, False, ['TIMEOUT >30s'])
    finally:
        os.unlink(fn); os.unlink(jn)

def check(path, run=True):
    n = int(re.search(r'ds_(\d+)', os.path.basename(path)).group(1))
    S = STRUCTS[n]; errs = []; warns = []
    pats = parse(path)
    want = S['patterns']; got = [p['name'] for p in pats]
    if got != want: errs.append(f'pattern names/order differ.\n   expected: {want}\n   got:      {got}')
    seen = set(); jobs = []
    for pi, p in enumerate(pats):
        if not p['spot']: errs.append(f'[{p["name"]}] missing SPOT')
        if not 2 <= len(p['problems']) <= 4: errs.append(f'[{p["name"]}] has {len(p["problems"])} problems (need 2-4, aim for 3)')
        prev = 0
        for qi, q in enumerate(p['problems']):
            tag = f'[{p["name"]} / {q.get("slug")}]'
            c = CATALOG.get(q.get('slug'))
            if not c: errs.append(f'{tag} slug not found on LeetCode'); continue
            if c['paid']: errs.append(f'{tag} is premium-only: pick a free problem')
            if q['slug'] in seen: errs.append(f'{tag} duplicate problem inside this file')
            seen.add(q['slug'])
            lvl = {'Easy': 1, 'Medium': 2, 'Hard': 3}[c['diff']]
            if lvl < prev: warns.append(f'{tag} difficulty {c["diff"]} comes after a harder problem (order Easy -> Hard)')
            prev = max(prev, lvl)
            for k in ('approach', 'complexity', 'code', 'test'):
                if not q.get(k): errs.append(f'{tag} missing {k.upper()}')
            if q.get('code') and not re.search(r'^class \w+', q['code'], re.M): errs.append(f'{tag} CODE must define the LeetCode class (class Solution, or the design class such as MinStack)')
            if q.get('test') and 'assert' not in q['test']: errs.append(f'{tag} TEST has no assert')
            if q.get('code') and '"""' in q['code']: warns.append(f'{tag} avoid triple-quoted docstrings in CODE')
            if q.get('code') and q.get('test'): jobs.append((path, pi, qi, q['code'], q['test']))
    nprob = sum(len(p['problems']) for p in pats)
    if run and jobs:
        with cf.ThreadPoolExecutor(8) as ex:
            for pi, qi, ok, tail in ex.map(run_one, jobs):
                if not ok: errs.append(f'[{pats[pi]["name"]} / {pats[pi]["problems"][qi]["slug"]}] TEST FAILED: ' + ' | '.join(tail))
    return pats, errs, warns, nprob

if __name__ == '__main__':
    args = [a for a in sys.argv[1:]]
    run = '--no-run' not in args; args = [a for a in args if a != '--no-run']
    dump = None
    if '--dump' in args: i = args.index('--dump'); dump = args[i + 1]; del args[i:i + 2]
    files = sorted(glob.glob(os.path.join(HERE, 'ds_*.txt'))) if args == ['--all'] else args
    allp = {}; total_err = 0; slugs = {}
    for f in files:
        pats, errs, warns, nprob = check(f, run)
        n = int(re.search(r'ds_(\d+)', os.path.basename(f)).group(1)); allp[n] = pats
        print(f'== {os.path.basename(f)}: {len(pats)} patterns, {nprob} problems, {len(errs)} errors, {len(warns)} warnings')
        for e in errs: print('  ERROR', e)
        for w in warns: print('  warn ', w)
        total_err += len(errs)
        for p in pats:
            for q in p['problems']: slugs.setdefault(q.get('slug'), []).append(f'{n}:{p["name"]}')
    if args == ['--all'] or len(files) > 1:
        d = {s: w for s, w in slugs.items() if len(w) > 1}
        if d:
            print(f'-- {len(d)} problems used in more than one pattern (fine if intended):')
            for s, w in d.items(): print('   ', s, w)
    if dump: json.dump(allp, open(dump, 'w'), indent=1)
    sys.exit(1 if total_err else 0)
