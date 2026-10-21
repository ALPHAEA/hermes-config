---
name: web-scraping-fallbacks
description: Fallback extraction techniques for bot-protected websites (Cloudflare challenges, CAPTCHAs, 403s) — r.jina.ai reader proxy via curl, HTML-mode headers, JSON-LD/schema.org table recovery. Use when browser_navigate hits "Just a moment..." / security verification / 403, or when a rendered page drops table cell content.
---

# Web Scraping Fallbacks for Bot-Protected Sites

## When to use
- `browser_navigate` returns a Cloudflare "Just a moment..." challenge page, a CAPTCHA, or the site 403s direct curl.
- A page renders but tables lose cell content (names dropped, numbers only).
- Google News (`news.google.com`) shows the `/sorry/index` CAPTCHA — do not retry the browser. **The official RSS endpoint is NOT CAPTCHA-gated** (verified 2026-10-19 from a datacenter IP that got the browser CAPTCHA): `curl -s "https://news.google.com/rss/search?q=AI+when:1d&hl=en-US&gl=US&ceid=US:en" -H "User-Agent: Mozilla/5.0"` returns clean XML with title/source/pubDate for hundreds of items. Decode the `CBMi...` wrapper links to real URLs with pip `googlenewsdecoder` (API: `GoogleDecoder().decode_google_news_url(link)` — full pipeline in `references/google-news-rss-pipeline.md`, runnable script in `scripts/google_news_rss.py`). Only if RSS also fails, fall back to Bing News (`qft=interval%3d%2224%22` for 24h) or dedicated sites (TechCrunch, The Verge category pages).

## Technique 1: r.jina.ai reader proxy (verified 2026-10, bypassed Cloudflare on lmarena.ai/arena.ai)
Jina's reader renders the page server-side and returns markdown — no challenge, no API key needed for basic use:

```bash
curl -s -m 60 "https://r.jina.ai/https://TARGET-SITE/path" -o /tmp/page.md
```

- Output is markdown: `Title: ... / URL Source: ... / Markdown Content: ...`. Tables often come through as markdown pipe tables with full data (ranks, names, scores, CIs, dates, vote counts).
- Useful headers:
  - `-H "x-respond-with: html"` — get raw rendered HTML instead of markdown (large, ~1MB+, but contains everything the JS rendered).
  - `-H "x-wait-for-selector: table"` and `-H "x-timeout: 45"` — wait for dynamic content.
  - `-H "x-retry: 2"` — retry flaky renders.
- If markdown output drops table cell text (happens on some React/TanStack-Table pages), refetch with `x-respond-with: html` (Technique 2).

## LMArena (arena.ai / lmarena.ai) specifics (verified 2026-10-20)
- Put the **arena.ai** domain in the jina URL, not lmarena.ai: `curl -s -m 120 "https://r.jina.ai/https://arena.ai/leaderboard/chat/text"` — same paths under lmarena.ai return Jina 403s. (The overview page `r.jina.ai/https://lmarena.ai/leaderboard` does work.)
- Correct subpage paths — a wrong path (e.g. `/leaderboard/text`) silently 403s and wastes retry rounds:
  `chat/text`, `chat/vision`, `chat/document`, `chat/search`, `code/webdev`, `code/image-to-webdev`, `image/text-to-image`, `image/image-edit/single-image`, `video/text-to-video`, `video/image-to-video`, `video/video-edit`, `agent`.
- Subpage markdown = plain-text table (Rank / Rank Spread / Model / Score±CI / Votes) with data timestamp, total votes, and model count at top. Overview page gives "Top 10 Agents" with % net-improvement, e.g. `1 Claude Opus 5.5 (Max)20.35%`.
- Jina intermittently rate-limits even with 25–60s sleeps: blocked responses are **270–550 bytes** starting with `Title: Just a moment...` or containing `Warning: Target URL returned error 403`. Success heuristic: size > 2000 bytes (markdown) or > 50000 bytes (html mode — blocked html responses are ~5900 bytes with `Just a moment` in `<title>`). Retry each page up to 3× with 20–30s gaps; some pages may never come through — report those sections as "no data" instead of fabricating.
- **2026-10-21 validation: jina block rate got much worse.** Browser Cloudflare-blocked (checkbox click doesn't pass), jina markdown mode failed on ALL 7 boards (~280–500 byte challenge pages), and `x-respond-with: html` succeeded on only 1 of 7 (webdev, 1.4MB) across ~15 attempts / 20 min. Plan for PARTIAL success as the normal case: fetch whatever comes through, parse it, and explicitly label missing boards "今日暂无数据（源站反爬拦截）" in the report. Never fabricate rankings.
- Long multi-minute retry loops: run via `terminal(background=true)` + `process(action=poll/wait)`, NOT `execute_code` — execute_code has a hard 300s timeout, kills the loop mid-run and loses progress.
- HF Space `lmarena-ai/arena-leaderboard` is stale (CSVs stop 2025-08) and its app.py just iframes the origin — never useful for current data. The static Space URL `lmarena-ai-arena-leaderboard.static.hf.space` also just iframes `lmarena.ai/leaderboard` (cross-origin, unreadable).
- **Parsing LMArena webdev markdown+html (verified 2026-10-21)**: markdown rows are TWO lines each — a rank line `"<rank> <rank_spread>"` then a score line `"<spread> <ELO>+<ci>/-<ci> <votes>$<price> <ctx>"`. The FIRST number of the score line is rank spread, NOT the rank — pair names from the html JSON-LD ItemList by position, and FILTER OUT the BreadcrumbList entries (`"Leaderboard"`, `"Code"`, `"WebDev"` also carry position/name fields and pollute the ranking). Total-votes figure (`903,893 votes`) and data timestamp (`2026-10-19` date strings) are extractable from the html via regex.

## Technique 2: recover tables from embedded JSON-LD / Next.js flight data
Rendered HTML (from jina or the site itself) often embeds the full dataset even when visible text extraction fails:

- **schema.org ItemList**: leaderboard/ranking pages frequently inject JSON-LD like
  `{"@type":"ListItem","position":1,"name":"claude-opus-5.5-max"},...`
  Recover the complete ordered ranking with:
  ```bash
  grep -o '"position":[0-9]*,"name":"[^"]*"' page.html
  ```
- **Next.js flight data**: `self.__next_f.push(...)` blobs contain props/state; grep for model names or score patterns and print surrounding context with Python (`data.find(...)` ± window).
- **Model-name grep census**: `grep -o 'claude-[a-z0-9.-]*\|gpt-[a-z0-9.-]*\|gemini-[a-z0-9.-]*\|qwen[a-z0-9.-]*' page.html | sort | uniq -c | sort -rn` quickly shows which entities the page actually contains.

## Technique 3: check mirrors before the origin
- Hugging Face Spaces sometimes mirror data — but VERIFY freshness first: list files via `https://huggingface.co/api/spaces/OWNER/SPACE` (returns `siblings` with filenames; check CSV/pkl dates), and check whether the Space iframe just embeds the blocked origin (`document.querySelector('iframe').src` via browser_console) — an embedded iframe gives you no bypass at all.
- Wayback (`web.archive.org`) is rate-limited (429) from datacenter IPs; don't rely on it in cron jobs.

## Pitfalls
- Clicking the Cloudflare "Verify you are human" checkbox via `browser_click` typically does NOT pass (managed challenge fingerprints the automation); don't loop on retries — switch to the reader proxy immediately.
- Google News `/sorry/index` = browser IP-blocked; don't retry the browser — but the RSS endpoint (`/rss/search?q=...`) usually still works from the same IP. Also: after a browser session hits the `/sorry` interstitial, later `browser_navigate` calls may fail with temp-file errors (broken session); switch to curl entirely rather than fighting the browser.
- DuckDuckGo HTML endpoint (`html.duckduckgo.com/html/`) returns an empty shell — useless, never attempt.
- Bing News search with boolean OR syntax (`q=OpenAI+OR+Anthropic+OR+...`) returns ZERO results (verified 2026-10-21) — use one plain keyword per query and issue several searches instead.
- `curl https://lmarena.ai/...` directly gives 301 → arena.ai → 403. Only the jina reader worked (as of 2026-10).
- Markdown-mode jina output for dense tables can be lossy; when numbers appear without names, always escalate to `x-respond-with: html` + JSON-LD extraction rather than guessing names.

## Real-world validation (2026-10-16, cron news report)
- lmarena.ai + arena.ai: browser blocked by Cloudflare → `r.jina.ai` markdown worked for 6 of 7 boards (text/vision/t2i/t2v/i2v + overview); WebDev names missing in markdown → recovered full 143-model ranking from schema.org ItemList in `x-respond-with: html` output.
- Google News CAPTCHA → TechCrunch category page via browser worked cleanly (fresh timestamps, article slugs); article detail via `r.jina.ai/<techcrunch-url>` for 2-3 sentence summaries.
