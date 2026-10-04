---
name: arena-leaderboard-scraping
description: Scrape LMArena/Arena (arena.ai, formerly lmarena.ai) leaderboards — per-section URL map, JS table extraction, vendor→country mapping. Use for AI digest reports needing live Elo/Agent rankings with scores.
---

# Arena Leaderboard Scraping (arena.ai / LMArena)

Use when a report needs real-time model rankings with scores (Elo, net improvement %), votes, prices — e.g. daily AI digests. Complements `cron-news-report` (which is manually authored and cannot be patched; this skill carries the URL-level detail it lacks).

## Key facts (verified 2026-09-15)

- `lmarena.ai/leaderboard` redirects to `arena.ai/leaderboard` — that IS the real Chatbot Arena successor.
- The **Overview page** snapshot lists all sections' Top-10 model names. Scores may or may not hydrate: on a **first cold load it can render names+ranks WITHOUT Elo**; simply `browser_navigate` to Overview **again** — the second load typically contains full scores ± CI for every section (verified 2026-09-23). **However (verified 2026-09-30): Overview may render NO section tables at all** — only the "Top 10 Agents" widget, Pareto Optimal Models, and New Release ticker, and clicking its category tabs ("Best Text Models" etc.) does NOT swap in tables. Don't retry-loop on Overview; go straight to per-section URLs when you need Elo/votes/prices/timestamps. Overview's Agent widget + Pareto remain extractable via `document.body.innerText` (see below).
- Each section page header shows: data date (e.g. "Sep 13, 2026"), total votes or sessions, model count — always capture these for the report. Overview section cards lack these headers; grab them from the dedicated page (e.g. text page: "Sep 13, 2026 · 8,146,274 votes · 402 models"; agent page: "Sep 16, 2026 · 1,850,083 sessions · 46 models").

## Per-section URL map (working paths)

| Section | URL | Score type |
|---|---|---|
| Overview | `https://arena.ai/leaderboard` | names only |
| Text/Chat | `https://arena.ai/leaderboard/text` | Elo ±CI |
| Agent | `https://arena.ai/leaderboard/agent` | Net improvement % ±CI; extra cols: Confirmed Success, Steerability, Sessions, Cost/Task P50 |
| WebDev | `https://arena.ai/leaderboard/code/webdev` | Elo |
| Vision | `https://arena.ai/leaderboard/vision` | Elo |
| Text-to-Image | `https://arena.ai/leaderboard/text-to-image` | Elo |
| Text-to-Video | `https://arena.ai/leaderboard/text-to-video` | Elo |
| Image-to-Video | `https://arena.ai/leaderboard/image-to-video` | Elo |

Additional working paths (harvested from footer links, verified reachable 2026-09-25): `/leaderboard/image-edit`, `/leaderboard/video-edit`, `/leaderboard/document`, `/leaderboard/search`, `/leaderboard/code/image-to-webdev`. All map re-verified 2026-09-25 — text/webdev/vision/text-to-image/text-to-video/image-to-video all rendered full tables with Elo ±CI in the initial snapshot.

**Pitfall — guessed paths 404**: `/leaderboard/webdev`, `/leaderboard/code-webdev`, `/leaderboard/chat/vision`, `/leaderboard/image/text-to-image` all return "Leaderboard Not Found". Use the exact map above.

**URL discovery via footer (verified 2026-10-02)**: on any Arena page, `browser_console` with:
```javascript
Array.from(document.querySelectorAll('a')).filter(a=>/leaderboard/i.test(a.href)).map(a=>a.textContent.trim()+' => '+a.href).join('\n')
```
returns the complete canonical leaderboard URL list (the page footer enumerates all 13 boards). Cheaper than guessing or reading a truncated snapshot.

**Re-verified 2026-10-02**: text / code/webdev / vision / text-to-image / text-to-video / image-to-video all rendered full tables (rank, model, vendor, score ±CI, votes, price, context + data-date header) in the compact `browser_navigate` snapshot on first load — no JS fallback or second load needed. Overview page again showed NO section tables, only the Top 10 Agents widget (which DOES include model names + net-improvement % inline in its snapshot) — that widget alone is sufficient for an Agent-board Top-5/10 without visiting `/leaderboard/agent`.

**Pitfall — section pages sometimes render only nav chrome on first load** (seen on Vision, Agent, Text): the compact snapshot shows just sidebar/nav. Fix without re-navigating: `browser_console` with `document.body.innerText.length` then `.substring(0, 6000)` — the hydrated table is almost always present in innerText even when the accessibility snapshot lags (re-verified 2026-09-27 on /leaderboard/agent and /leaderboard/text: innerText returned full rows with ranks, Elo ±CI, votes, prices immediately after a chrome-only snapshot). Alternatively one follow-up `browser_snapshot` returns the hydrated table.

## Overview page: cheap innerText extraction (verified 2026-09-25)

The Overview page (`arena.ai/leaderboard`) carries **Agent Top 10 (net-improvement %)**, **Pareto Optimal Models with $/task costs**, and a **"NEW RELEASE RANKINGS" ticker** (fresh models + entry ranks, e.g. "GPT 6 Sol is #5 in WebDev" — ideal source for 排名变动 commentary). All of this fits in the first ~3.8KB of `document.body.innerText` — grab it via browser_console with `document.body.innerText.substring(0, 3800)`; no snapshot, no scrolling, no subagent needed.

## Fast extraction JS (browser_console)

Returns top N rows as pipe-delimited text — much cheaper than parsing the ~300KB overview snapshot:

```javascript
(() => { const rows = document.querySelectorAll('table tbody tr'); const out = [];
rows.forEach((r,i)=>{ if(i<5){ const cells=[...r.querySelectorAll('td')].map(c=>c.innerText.trim().replace(/\n+/g,' | '));
out.push(cells.join(' || ')); } });
return out.join('\n') || document.body.innerText.slice(0,500); })()
```

Row format: `rank || rank-spread || model | Lab · License || score ±CI [Preliminary] || votes || $in/$out || context`.

## Vendor → country mapping (for 🇨🇳 flags in Chinese reports)

- China 🇨🇳: qwen/wan/happyhorse=Alibaba, kimi=Moonshot, deepseek=DeepSeek, glm=Z.ai, ernie=Baidu, seedance/seedream/dreamina=Bytedance, minimax/hailuo=MiniMax, kling=KlingAI, vidu=Shengshu, hy4=Tencent, pixverse, hidream
- US: claude=Anthropic, gpt/sora/gpt-image=OpenAI, gemini/veo=Google, muse=Meta, grok=SpaceXAI, mai=Microsoft, flux=Black Forest Labs

## News-source fallbacks (same session findings)

- `news.google.com/search` may redirect to `google.com/sorry` (bot check) from datacenter IPs. Fallback: Bing News with 24h filter + direct scrape of `techcrunch.com/category/artificial-intelligence/` (clean headlines + "N hours ago" in one snapshot).
- **Bing News OR queries: inconsistent** — one session got zero results for `OpenAI OR Anthropic OR Nvidia`, but 2026-10-03 `OpenAI OR Anthropic OR Gemini OR Nvidia AI` (with `qft=interval%3d%227%22&setlang=en-US&cc=US`) returned fresh cards (33min–11h old). Treat OR as best-effort: try it once; if zero/stale results, fall back to one topic per query or scrape TechCrunch for multi-company coverage. Note generic queries (`AI artificial intelligence`) leak days-old cards even with the 24h filter — vendor-keyword queries stay much fresher.
- **Bing News locale fix (verified 2026-09-23)**: from Asian IPs, results come back localized (Japanese sources/UI) unless you append `&setlang=en-US&cc=US`:
  `https://www.bing.com/news/search?q=OpenAI&qft=interval%3d%2224%22&setlang=en-US&cc=US`
  Each result card includes source name + relative age ("4 hours ago") — exactly what sourced/timestamped digest reports need. Old cards leak into 24h-filtered results anyway; filter by displayed age.
- **Bing News sort-by-date (verified 2026-09-26)**: `interval%3d%2224%22` alone still returns relevance-ordered cards days/weeks old. For same-day digest news, use `qft=sortbydate%3d%221%22` instead — returns "Most recent" ordering with cards as fresh as minutes ago. Multi-keyword AND queries (`AI+OpenAI+Anthropic+Google+Gemini`) work in this mode.
- **Per-section pages render full tables in the compact `browser_navigate` snapshot (re-verified 2026-09-30)**: agent/text/code/webdev/vision/text-to-image/text-to-video/image-to-video all returned rank+model+vendor+score+votes+price inline, plus the data-date/votes/models header — no Overview second-load or JS extraction needed. Occasionally a sub-page first renders only nav chrome (Vision, code/webdev); one follow-up `browser_snapshot` returns the hydrated table.
- **TechCrunch article detail (verified 2026-09-30)**: the category listing snapshot gives headline + author + relative age for ~25 stories — often enough for digest entries without opening articles. To get details, construct the article URL as `techcrunch.com/YYYY/MM/DD/<headline-words-joined-by-dashes>/`; this works when the slug matches exactly but can 404 (e.g. Anthropic prospectus story). Safer: read the listing snapshot file for the actual `href`s, or click the headline's link ref — note that clicking a ref from a STALE snapshot (after a new navigate) may land back on the listing page, so re-snapshot first. A 404 page still usefully shows "Latest News" + "Most Popular" sidebars with fresh headlines.
- **TechCrunch curl-only pipeline (verified 2026-10-04, preferred over browser)**: no browser needed at all —
  1. List a given day's articles: `curl -s https://techcrunch.com/category/artificial-intelligence/ -H "User-Agent: Mozilla/5.0" | grep -oE 'href="https://techcrunch.com/2026/10/0[0-9]/[^"]+"' | sort -u` — URLs embed the publish date, so you can filter to today/yesterday precisely.
  2. Extract article lead: curl the URL and regex `<p>` tags via python, keep paragraphs >60–80 chars, take first 4–6 — reliably yields the who/what/why for a digest entry, plus the byline date ("9:30 AM PDT · October 3, 2026") appears in the page text.
  Avoid `browser_click` on listing links for detail pages: in one 2026-10-04 run the click landed on `about:blank` and `browser_back` didn't recover. curl is faster and deterministic.
- **Deep-rank lookup on big boards (verified 2026-10-04)**: Text-board snapshots (~4000 lines) truncate to a file. To find where Chinese models rank without paging through: `search_files` on the saved snapshot path with pattern `cell "(qwen|kimi|deepseek|glm|ernie|step|mimo)[^"]*"`, then `read_file` a few lines around the hit — the rank cell and Elo cell are ~2–6 lines above/below the model-name line.
- **Re-verified 2026-10-04**: Overview still shows NO tables (only Top-10-Agents widget / Pareto / New Release ticker); all per-section URLs (agent, text, code/webdev, vision, text-to-image, text-to-video, image-to-video) rendered full tables inline in the compact `browser_navigate` snapshot on first load, each with its own data-date header. `news.google.com/search` still redirects to the `google.com/sorry` bot check from datacenter IPs; generic Bing News query `AI artificial intelligence` with `interval%3d%2224%22` still leaked 13-days-old cards — skip straight to the TechCrunch curl pipeline for same-day news.

## Verification

Cross-check the top 3 model names of at least one section between the Overview page and the dedicated section page before publishing — catches stale caches and wrong-path 404s.