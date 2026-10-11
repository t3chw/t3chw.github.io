# DSA patterns sheet: source data

`dsa-patterns/index.html` (the page at /dsa-patterns/) is generated from the files in this folder.
Jekyll skips `tools/`, so nothing here is published.

- `ds_NN.txt`: one file per data structure (15 in all). Each pattern has a "use this when" line and 2-4 free LeetCode questions, each with an approach, complexity, a Python solution and tests.
- `patterns.json`: the 15 data structures and 143 pattern names, from the "15 data structures and patterns" revision notes.
- `catalog.json`: LeetCode problem list (slug, title, difficulty, premium flag) used to validate every slug.
- `check.py`: checks every file and runs each solution against its tests. A solution sees only `typing`, `ListNode` and `TreeNode`, so any other name needs an explicit import in the code.
- `fix_imports.py`: adds missing standard-library imports to solutions.
- `build_page.py`: builds the page.

From this folder:

```bash
python3 check.py --all
python3 build_page.py ../../dsa-patterns/index.html
```
