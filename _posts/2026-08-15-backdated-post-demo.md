---
layout: post
title: "Backdating Posts in Jekyll"
date: 2026-08-15 09:30:00 +0000
categories: [Tech]
tags: [Jekyll, Demo, Blogging]
---

This post was written well after 15 August 2026, but it is dated then. Jekyll is happy to publish it that way, and it slots into the archive as if it had always been there.

---

## How it works

Jekyll sorts posts by date, not by when the file was committed. Two places carry the date:

- The **filename**: `_posts/2026-08-15-backdated-post-demo.md`{: .filepath }
- The **front matter**: `date: 2026-08-15 09:30:00 +0000`

Set both to the date you want and the post lands there — on the home page, in `Archives`, and in the sitemap. Nothing else is needed.

## Past dates versus future dates

The two directions behave very differently:

| Date | Built by default? |
|------|-------------------|
| In the past | Yes |
| In the future | No |

Backdating always works. **Forward**-dating does not: Jekyll's `future` setting defaults to `false`, so a post dated tomorrow is silently skipped at build time. To publish those, add this to `_config.yml`{: .filepath }:

```yaml
future: true
```

> A post that "disappears" after a push is very often just a future date combined with a timezone gap. This site leaves `timezone` unset in `_config.yml`{: .filepath }, so dates are interpreted as **UTC** — which is 5 hours 30 minutes behind IST. Writing at 11 AM IST and stamping the post 11:00 +0000 puts it in the future.
{: .prompt-warning }

The safest habit is to write the offset explicitly in the front matter, as `+0000` or `+0530`, rather than leaving it off.

## Drafts, the other option

If the goal is to hide a post rather than to date it, use `_drafts`{: .filepath } instead. Files there need no date in the filename and are excluded from builds unless you pass `--drafts` locally:

```bash
bundle exec jekyll serve --drafts
```

Backdating is for reordering history. Drafts are for keeping things out of it.
