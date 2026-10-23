---
name: web-article-recipes
description: Site-specific web article extraction recipes (HTML→Markdown, tables, images) for the URL→Obsidian-note workflow. Patchable companion to the hand-authored url-to-obsidian-note / zhihu-article-fetch skills.
tags: [web-scraping, obsidian, markdown, recipes]
---

# Web Article Extraction Recipes

Class-level umbrella for per-site extraction techniques learned during URL→note tasks. The hand-authored skills `url-to-obsidian-note` and `zhihu-article-fetch` carry the main workflows but **refuse curator patches** — record new site recipes and conversion pitfalls HERE instead.

## General HTML→Markdown conversion pitfalls

- **Zhihu draft tables**: `article.content` may contain `<table data-draft-node="block" data-draft-type="table">`. Convert row-by-row (`<tr>` → `| cell | cell |`, first row = header + separator). Watch for accidental leading double-pipe `||` lines when joining — check output and fix.
- **Zhihu external links**: `<a href="https://link.zhihu.com/?target=<urlencoded>">` redirects must be unwrapped via `urllib.parse.unquote` on the `target` param; link text lives in `<span class="visible">`.
- **Timestamps**: `created`/`updated` in article JSON are unix seconds (UTC) — use for frontmatter date.

## Zhihu (zhuanlan.zhihu.com)

Main workflow in `zhihu-article-fetch` skill. Additional verified experience (2026-10):

1. **Empty page on first article navigation** → navigate to `https://www.zhihu.com` (homepage/signin) first to establish the session, then navigate to `https://www.zhihu.com/column/p/{article_id}`. This reliably fixes the empty-page result.
2. **New-style article IDs are 19-digit numbers** (e.g. 2082214691443585569); the `column/p/{id}` path works the same as for old short IDs.
3. Extract via `script[type="text/json"]` → `initialState.entities.articles` (title, content HTML, author.name, created).
4. Note naming convention for this user: `NOTE/Network/【知乎】<标题>.md` (or other NOTE subdirectory by topic).

## Conversion script

`scripts/html_to_md.py` — reusable HTML→Markdown converter (zhihu link unwrap, draft tables, double-pipe guard, frontmatter generation; reports `<img>` URLs to download afterwards). Usage:

```bash
python3 ~/.hermes/skills/note-taking/web-article-recipes/scripts/html_to_md.py \
  /tmp/content.html "<vault>/NOTE/Network/【知乎】<标题>.md" \
  --title "<标题>" --source "<URL>" --author "<作者>" --date <YYYY-MM-DD> --tags "知乎,..."
```

Prefer running this script over hand-writing conversion code each session. Save the raw article HTML (e.g. `window.__art.content` from browser console) to a temp file first.

## Site index

- Feishu wiki docs: see MEMORY (virtual-scroll + blob image recipe) — move here when it needs expansion.
- Toutiao: see MEMORY (mobile API recipe).
- Tencent Cloud developer: see MEMORY (static HTML, `.rno-markdown.new-version`).
- Zhihu: this file + `zhihu-article-fetch` skill.
