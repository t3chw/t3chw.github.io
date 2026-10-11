#!/usr/bin/env python3
"""Build the standalone DSA patterns page from ds_NN.txt files. usage: build_page.py OUT.html"""
import sys, os, re, json, glob, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import check
CAT = check.CATALOG
STRUCTS = check.STRUCTS
esc = html.escape

TOK = re.compile(r'''
 (?P<c>\#[^\n]*)
|(?P<s>[rbfRBF]{0,2}(?:"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'))
|(?P<d>\b(?:def|class)\s+)(?P<fn>[A-Za-z_]\w*)
|(?P<n>\b\d[\d_]*(?:\.\d+)?(?:e[+-]?\d+)?\b)
|(?P<k>\b(?:and|as|assert|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield|self)\b)
''', re.X)
def highlight(src):
    out, pos = [], 0
    for m in TOK.finditer(src):
        out.append(esc(src[pos:m.start()], quote=False)); pos = m.end()
        if m.group('c'): out.append('<span class="tk-c">%s</span>' % esc(m.group('c'), quote=False))
        elif m.group('s'): out.append('<span class="tk-s">%s</span>' % esc(m.group('s'), quote=False))
        elif m.group('d'): out.append('<span class="tk-k">%s</span><span class="tk-f">%s</span>' % (esc(m.group('d'), quote=False), esc(m.group('fn'), quote=False)))
        elif m.group('n'): out.append('<span class="tk-n">%s</span>' % esc(m.group('n'), quote=False))
        else: out.append('<span class="tk-k">%s</span>' % esc(m.group('k'), quote=False))
    out.append(esc(src[pos:], quote=False))
    return ''.join(out)

def build(out_path):
    files = sorted(glob.glob(os.path.join(HERE, 'ds_*.txt')))
    body, unique, n_pat, n_rows = [], set(), 0, 0
    for f in files:
        n = int(re.search(r'ds_(\d+)', os.path.basename(f)).group(1)); S = STRUCTS[n]
        pats = check.parse(f); rows = sum(len(p['problems']) for p in pats)
        sec = ['<details class="sec" open><summary>%d. %s <span class="count" data-count-sec="%d"></span></summary>' % (n, esc(S['name']), n),
               '<p class="intro">%s</p>' % esc(S['intro'])]
        for pi, p in enumerate(pats):
            n_pat += 1
            sec.append('<div class="subsec"><h3>%s <span class="count" data-count-sub="%d-%d"></span></h3><p class="spot">%s</p>' % (esc(p['name']), n, pi, esc(p['spot'])))
            for q in p['problems']:
                c = CAT[q['slug']]; unique.add(q['slug']); n_rows += 1
                sec.append(
                    '<div class="q" data-d="%s" data-slug="%s" data-sec="%d" data-sub="%d-%d">'
                    '<div class="row"><label><input type="checkbox" data-slug="%s"><span class="name">%s</span></label>'
                    '<span class="tag %s">%s</span><a href="https://leetcode.com/problems/%s/" target="_blank" rel="noopener">LeetCode #%d</a></div>'
                    '<details class="sol"><summary>Solution</summary><div class="solbody"><p class="appr">%s</p><p class="cx"><b>Complexity:</b> %s</p>'
                    '<div class="codewrap"><button type="button" class="copy">Copy</button><pre class="code"><code>%s</code></pre></div></div></details></div>'
                    % (c['diff'], q['slug'], n, n, pi, q['slug'], esc(c['title']), c['diff'], c['diff'], q['slug'], c['id'],
                       esc(q['approach']).replace('\n', '<br>'), esc(q['complexity']), highlight(q['code'])))
            sec.append('</div>')
        sec.append('</details>')
        body.append('\n'.join(sec))
    page = TEMPLATE.replace('@@BODY@@', '\n'.join(body)).replace('@@UNIQUE@@', str(len(unique))).replace('@@PATTERNS@@', str(n_pat)).replace('@@STRUCTS@@', str(len(files)))
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    open(out_path, 'w', encoding='utf-8').write(page)
    print(f'wrote {out_path}: {len(files)} data structures, {n_pat} patterns, {n_rows} questions ({len(unique)} unique), {len(page)//1024} KB')

TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DSA Patterns (@@UNIQUE@@ problems)</title>
<meta name="description" content="Learn DSA by pattern: @@PATTERNS@@ patterns across @@STRUCTS@@ data structures, each with LeetCode questions in learning order and a worked Python solution.">
<style>
  :root { --bg:#fff; --fg:#000; --mut:#666; --line:#000; --soft:#999; --code:#f4f4f4; --k:#7a2e9c; --s:#2a7a45; --n:#a64b12; --c:#777; --f:#1f55a3; }
  @media (prefers-color-scheme: dark) { :root { --bg:#111; --fg:#eee; --mut:#aaa; --line:#eee; --soft:#666; --code:#1c1c1c; --k:#d29bf0; --s:#8fd6a8; --n:#f0a070; --c:#888; --f:#8fb8f2; } }
  body { font-family: Arial, Helvetica, sans-serif; background: var(--bg); color: var(--fg); max-width: 860px; margin: 0 auto; padding: 16px; line-height: 1.4; }
  h1 { margin: 0 0 4px; font-size: 24px; }
  .sub { margin: 0 0 12px; font-size: 14px; }
  .sub a, footer a { color: var(--fg); }
  #top { border: 2px solid var(--line); padding: 10px; margin-bottom: 16px; position: sticky; top: 0; background: var(--bg); z-index: 2; }
  #bar { height: 10px; border: 1px solid var(--line); margin: 6px 0; }
  #fill { height: 100%; width: 0; background: var(--fg); }
  #stats { font-size: 13px; margin-bottom: 6px; }
  #top label { margin-right: 12px; font-size: 14px; }
  .ctrl { margin-top: 6px; }
  button { font: inherit; font-size: 13px; background: var(--bg); color: var(--fg); border: 1px solid var(--line); padding: 2px 8px; cursor: pointer; }
  button:hover, button.on { background: var(--fg); color: var(--bg); }
  details.sec { border: 1px solid var(--line); margin-bottom: 10px; }
  details.sec > summary { font-size: 18px; font-weight: bold; padding: 8px 10px; cursor: pointer; }
  details.sec[open] > summary { border-bottom: 1px solid var(--line); }
  .count { font-weight: normal; font-size: 14px; float: right; }
  .intro { margin: 8px 10px 0; font-size: 13px; color: var(--mut); }
  .subsec { padding: 6px 10px 6px; }
  .subsec h3 { margin: 10px 0 2px; font-size: 15px; text-decoration: underline; }
  .spot { margin: 0 0 6px; font-size: 13px; color: var(--mut); }
  .q { border-bottom: 1px dotted var(--soft); }
  .q:last-child { border-bottom: none; }
  .row { display: flex; align-items: center; gap: 10px; padding: 4px 0; font-size: 15px; flex-wrap: wrap; }
  .row label { flex: 1; min-width: 200px; cursor: pointer; }
  .row input { width: 16px; height: 16px; margin-right: 8px; vertical-align: middle; accent-color: var(--fg); cursor: pointer; }
  .q.done .name { text-decoration: line-through; color: var(--mut); }
  .tag { font-size: 11px; border: 1px solid var(--line); padding: 0 5px; min-width: 44px; text-align: center; }
  .tag.Easy { border-style: dotted; }
  .tag.Medium { font-weight: bold; }
  .tag.Hard { background: var(--fg); color: var(--bg); font-weight: bold; }
  .row a { color: var(--fg); font-size: 13px; white-space: nowrap; }
  .row a:hover { background: var(--fg); color: var(--bg); }
  details.sol { margin: 0 0 6px 24px; }
  details.sol > summary { cursor: pointer; font-size: 13px; width: max-content; border-bottom: 1px solid var(--line); }
  .solbody { padding: 6px 0 4px; font-size: 14px; }
  .appr { margin: 4px 0; }
  .cx { margin: 4px 0 8px; font-size: 13px; color: var(--mut); }
  .codewrap { position: relative; }
  .copy { position: absolute; top: 6px; right: 6px; font-size: 11px; padding: 0 6px; }
  pre.code { background: var(--code); border: 1px solid var(--soft); margin: 0; padding: 10px 12px; overflow: auto; font: 12.5px/1.55 ui-monospace, Menlo, Consolas, monospace; tab-size: 4; }
  pre.code code { font: inherit; }
  .tk-k { color: var(--k); } .tk-s { color: var(--s); } .tk-n { color: var(--n); } .tk-c { color: var(--c); font-style: italic; } .tk-f { color: var(--f); }
  .hide-done .q.done { display: none; }
  .f-Easy .q:not([data-d="Easy"]), .f-Medium .q:not([data-d="Medium"]), .f-Hard .q:not([data-d="Hard"]) { display: none; }
  footer { font-size: 12px; margin-top: 20px; }
  @media (max-width: 520px) { #top { position: static; } details.sol { margin-left: 4px; } .count { float: none; display: block; font-size: 12px; } }
</style>
</head>
<body>

<h1 id="title">DSA Patterns</h1>
<p class="sub">Learn DSA one pattern at a time. For each pattern: read the "use this when" line, try the questions in order (Easy, then Medium, then Hard), then open the solution to compare. Tick what you've solved. Progress is saved in this browser. Want the topic-wise list instead? <a href="/dsa-sheet/">Open the classic DSA sheet</a>.</p>

<div id="top">
  <b id="total">0 / 0 solved</b>
  <div id="bar"><div id="fill"></div></div>
  <div id="stats"></div>
  <div class="ctrl">
    Show:
    <button data-f="All" class="on">All</button>
    <button data-f="Easy">Easy</button>
    <button data-f="Medium">Medium</button>
    <button data-f="Hard">Hard</button>
  </div>
  <div class="ctrl">
    <label><input type="checkbox" id="hideDone"> Hide solved</label>
    <button id="openAll">Expand all</button>
    <button id="closeAll">Collapse all</button>
    <button id="openSol">Show all solutions</button>
    <button id="closeSol">Hide all solutions</button>
    <button id="reset">Reset progress</button>
  </div>
</div>

<div id="app">
@@BODY@@
</div>

<footer>
  Every link opens the exact LeetCode problem, and every problem is free (no premium needed).
  The solutions are Python 3 in LeetCode format, written for this sheet and each one was run against its own tests.
  A problem that appears under two patterns shares one tick.
  Try the problem yourself before opening the solution.
</footer>

<script>
const KEY = "dsa-patterns-solved-v1";
let solved = {};
try { solved = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) {}
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(solved)); } catch (e) {} };
const qs = s => Array.from(document.querySelectorAll(s));

function refresh() {
  const sec = {}, sub = {}, dif = { Easy: [0, 0], Medium: [0, 0], Hard: [0, 0] }, seen = new Set();
  let total = 0, done = 0;
  qs(".q").forEach(q => {
    const slug = q.dataset.slug, isDone = !!solved[slug];
    q.classList.toggle("done", isDone);
    q.querySelector("input").checked = isDone;
    for (const [m, k] of [[sec, q.dataset.sec], [sub, q.dataset.sub]]) { m[k] = m[k] || [0, 0]; m[k][1]++; if (isDone) m[k][0]++; }
    if (!seen.has(slug)) {
      seen.add(slug); total++; if (isDone) done++;
      const d = dif[q.dataset.d]; d[1]++; if (isDone) d[0]++;
    }
  });
  qs("[data-count-sec]").forEach(el => { const c = sec[el.dataset.countSec]; el.textContent = c[0] + "/" + c[1]; });
  qs("[data-count-sub]").forEach(el => { const c = sub[el.dataset.countSub]; el.textContent = c[0] + "/" + c[1]; });
  document.getElementById("total").textContent = done + " / " + total + " solved (" + (total ? Math.round(done * 100 / total) : 0) + "%)";
  document.getElementById("fill").style.width = (total ? done * 100 / total : 0) + "%";
  document.getElementById("stats").textContent = "Easy " + dif.Easy.join("/") + "  |  Medium " + dif.Medium.join("/") + "  |  Hard " + dif.Hard.join("/");
  document.getElementById("title").textContent = "DSA Patterns: " + total + " problems";
}
document.getElementById("app").addEventListener("change", e => {
  if (e.target.matches("input[type=checkbox]")) {
    const slug = e.target.dataset.slug;
    if (e.target.checked) solved[slug] = 1; else delete solved[slug];
    save(); refresh();
  }
});
document.getElementById("app").addEventListener("click", e => {
  if (e.target.matches("button.copy")) {
    const code = e.target.parentElement.querySelector("code").textContent;
    const ok = () => { e.target.textContent = "Copied"; setTimeout(() => e.target.textContent = "Copy", 1200); };
    try { navigator.clipboard.writeText(code).then(ok, () => {}); } catch (err) {}
  }
});
document.getElementById("hideDone").addEventListener("change", e => document.body.classList.toggle("hide-done", e.target.checked));
qs("button[data-f]").forEach(b => b.onclick = () => {
  qs("button[data-f]").forEach(x => x.classList.toggle("on", x === b));
  document.body.classList.remove("f-Easy", "f-Medium", "f-Hard");
  if (b.dataset.f !== "All") document.body.classList.add("f-" + b.dataset.f);
});
document.getElementById("openAll").onclick = () => qs("details.sec").forEach(d => d.open = true);
document.getElementById("closeAll").onclick = () => qs("details.sec").forEach(d => d.open = false);
document.getElementById("openSol").onclick = () => qs("details.sol").forEach(d => d.open = true);
document.getElementById("closeSol").onclick = () => qs("details.sol").forEach(d => d.open = false);
document.getElementById("reset").onclick = () => { if (confirm("Clear all solved marks?")) { solved = {}; save(); refresh(); } };
refresh();
</script>
</body>
</html>
'''
if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'out', 'index.html'))
