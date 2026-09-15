---
name: arena-leaderboard-scraping
description: Scrape LMArena/Arena (arena.ai, formerly lmarena.ai) leaderboards — per-section URL map, JS table extraction, vendor→country mapping. Use for AI digest reports needing live Elo/Agent rankings with scores.
---

# Arena Leaderboard Scraping (arena.ai / LMArena)

Use when a report needs real-time model rankings with scores (Elo, net improvement %), votes, prices — e.g. daily AI digests. Complements `cron-news-report` (which is manually authored and cannot be patched; this skill carries the URL-level detail it lacks).

## Key facts (verified 2026-09-15)

- `lmarena.ai/leaderboard` redirects to `arena.ai/leaderboard` — that IS the real Chatbot Arena successor.
- The **Overview page** snapshot lists all sections' Top-10 model names but **without scores**. For Elo/votes/prices, visit each section's dedicated page.
- Each section page header shows: data date (e.g. "Sep 13, 2026"), total votes or sessions, model count — always capture these for the report.

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

**Pitfall — guessed paths 404**: `/leaderboard/webdev`, `/leaderboard/chat/vision`, `/leaderboard/image/text-to-image` all return "Leaderboard Not Found". Use the exact map above.

**Pitfall — Vision page slow render**: the initial snapshot may show only navigation chrome. Extract via browser_console JS instead of relying on the snapshot.

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

- China 🇨🇳: qwen/wan/happyhorse=Alibaba, kimi=Moonshot, deepseek=DeepSeek, glm=Z.ai, ernie=Baidu, seedance/seedream/dreamina=Bytedance, minimax/hailuo=MiniMax, kling=KlingAI, vidu=Shengshu, hy4=Tencent, pixverse
- US: claude=Anthropic, gpt/sora/gpt-image=OpenAI, gemini/veo=Google, muse=Meta, grok=SpaceXAI, mai=Microsoft, flux=Black Forest Labs

## News-source fallbacks (same session findings)

- `news.google.com/search` may redirect to `google.com/sorry` (bot check) from datacenter IPs. Fallback: Bing News with 24h filter (`https://www.bing.com/news/search?q=...&qft=interval%3d%2224%22`) + direct scrape of `techcrunch.com/category/artificial-intelligence/` (clean headlines + "N hours ago" in one snapshot).
- **Bing News does NOT support `OR` queries** — `OpenAI OR Anthropic OR Nvidia` returns zero results. One topic per query, or scrape TechCrunch for multi-company coverage.

## Verification

Cross-check the top 3 model names of at least one section between the Overview page and the dedicated section page before publishing — catches stale caches and wrong-path 404s.