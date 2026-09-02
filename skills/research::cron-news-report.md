---
name: cron-news-report
description: Generate a multi-section AI/tech news digest report as a cron job, with verified real-time data from live sources rather than subagent hallucination risk.
---

# Cron News Report Generation

## When to Use
- Generating a daily/weekly AI/tech news digest as a scheduled cron job
- Any task that requires factual current-event data where accuracy matters
- Multi-section reports that combine news, leaderboard data, and analysis

## ⚠️ Important: Subagent Delegation Strategy (Revised)

**Subagent delegation IS effective for news/browser-based scraping** — contrary to earlier guidance that said to avoid it entirely. The key is giving subagents the RIGHT toolset:

- ✅ **`toolsets=["browser"]`** works well — subagents can navigate to news sites and extract content
- ✅ **`toolsets=["web"]`** works for search when available
- ❌ **`toolsets=["search"]`** is unreliable — subagents may exit prematurely after 1-2 calls

**Best practice**: Delegate parallel subagents for broad news collection, then use browser tools in the main session for critical live leaderboard data.

### Recommended parallel delegation pattern (3 subagents):

1. **AI Model News** — keywords: GPT, Claude, Gemini, Llama, Qwen, NVIDIA, AMD, semiconductor AI
2. **LLM Benchmark Data** — target: arena.ai, swebench.com, artificialanalysis.ai, MMMU-Pro
3. **Agent Industry Trends** — keywords: AI Agent, MCP, Multi-Agent, Computer Use, OpenAI Agents SDK

Each subagent should get explicit source URLs to visit and extract from.

## Primary Data Sources

### ⚠️ arena.ai Domain Change
As of mid-2026, `arena.ai` redirects to an AI app builder product (NOT the LMSYS Chatbot Arena). The actual Chatbot Arena leaderboard lives at:
- **`lmarena.ai`** — the real successor to chat.lmsys.org
- **`huggingface.co/spaces/lmarena-ai/arena-leaderboard`** — Hugging Face Space (data inside Gradio iframe, may time out)

**Practical approach**: Use `delegate_task` with `toolsets=["browser"]` to have subagents scrape arena.ai/swE-bench data, and verify key findings (top 3-5 model names) in the main session.

### ✅ Verified 2026-08: Direct snapshot works for LMArena (simpler than subagents)
`browser_navigate("https://lmarena.ai/leaderboard")` returns an accessibility snapshot containing ALL arena sections (Agent, Text, WebDev, Vision, Document, Text-to-Image, Image Edit, Image-to-WebDev, Search, Text-to-Video, Image-to-Video, Video Edit) with ranks, model names, Elo scores, and confidence intervals — directly in the snapshot text. No subagent needed.
- Snapshot is large (~300KB, truncated); use the returned file path + `read_file(offset=...)` to page through remaining sections.
- Data format in snapshot: `StaticText "1" ... StaticText "claude-fable-5" ... StaticText "1506" StaticText "±5"`. Agent arena uses % net-improvement instead of Elo.
- Country attribution: model families map to vendors — claude=Anthropic, gpt/gemini/grok=US, qwen/kimi/deepseek/glm/ernie/wan=China, seedance/seedream=Bytedance, minimax/kling=China. Mark Chinese models with 🇨🇳 per user preference.

### Reliable Sources (verified working)

| Source | URL | Method | Notes |
|--------|-----|--------|-------|
| Arena AI (Leaderboard) | `lmarena.ai/?leaderboard` | Subagent browser scrape | Gradio-loaded inside iframe |
| SWE-bench | `https://swebench.com/` | `browser_navigate` + snapshot | Table on index.html, NOT verified.html |
| Artificial Analysis | `https://artificialanalysis.ai/leaderboards/models` | `browser_navigate` + snapshot | Accessible HTML table with Intelligence Index |
| TechCrunch AI | `https://techcrunch.com/category/artificial-intelligence/` | Subagent browser scrape | Clean HTML, updated hourly |
| The Verge AI | `https://www.theverge.com/ai-artificial-intelligence` | Subagent browser scrape | Good fallback |
| Hacker News | `https://news.ycombinator.com/` | `browser_navigate` + console JS | Great for filtering top stories |
| Bing News | `https://www.bing.com/news/search?q=...&qft=interval%3d%2224%22` | `browser_navigate` | Use `qft=interval%3d%2224%22` for 24h news |

### SWE-bench: Use index.html, NOT verified.html
The leaderboard table is server-rendered on **`swebench.com/`** (index.html). `verified.html` only shows description text.

## Data Extraction Methods

### From arena.ai / lmarena.ai (React/WebComponent rendered)
Use `browser_snapshot(full=true)` and read the snapshot text. Rows appear as:
`"1 1 6 Anthropic claude-fable-5 1509 ±9 4,299 $10 / $50 1M"`

For JS fallback when snapshot is truncated:
```javascript
(() => { const all = document.querySelectorAll('*'); const texts = []; 
all.forEach(el => { const t = el.textContent?.trim(); 
  if(t && /claude|gpt|qwen|llama|gemini|deepseek|mistral/i.test(t) && t.length < 200 && /±/.test(t) && !texts.some(x=>x.includes(t))) 
    texts.push(t.substring(0,150)); 
}); return texts.slice(0,30).join('\n'); })()
```

### From Artificial Analysis (accessible HTML table)
Use `browser_snapshot(full=true)` — the data shows as structured rows:
`"Claude Fable 5 (with fallback) 1M Anthropic Anthropic 60 $7.70 63 159.92 167.86"`
Columns: Model | Context | Creator | Intelligence Index | Blended USD/1M Tokens | Median Tokens/s | Latency

### From SWE-bench (index.html table)
Use `browser_snapshot` or JS extraction:
```javascript
(() => { const rows = document.querySelectorAll('table tbody tr'); 
  const data = []; 
  rows.forEach((row, i) => { if(i < 30) { 
    const cells = row.querySelectorAll('td'); 
    if(cells.length >= 7) { 
      data.push({
        model: cells[1]?.textContent?.trim().replace(/🆕\s*/,'').trim(),
        resolved: cells[2]?.textContent?.trim(),
        cost: cells[3]?.textContent?.trim(),
        date: cells[5]?.textContent?.trim()
      }); 
    } 
  } }); 
  return JSON.stringify(data); 
})()
```

### From Hacker News (news.ycombinator.com)
```javascript
(() => { const rows = document.querySelectorAll('.athing'); 
  const data = []; 
  rows.forEach((row, i) => { if(i < 30) { 
    const titleEl = row.querySelector('.titleline a');
    const subrow = row.nextElementSibling;
    const pointsEl = subrow?.querySelector('.score');
    data.push({
      rank: i+1,
      title: titleEl?.textContent?.trim() || '',
      url: titleEl?.href || '',
      points: pointsEl?.textContent?.trim() || '0'
    }); 
  } }); 
  return JSON.stringify(data, null, 2);
})()
```
Filter: 100+ points = major news; 50+ = notable.

## Report Structure
- Use clear emoji-delimited sections
- Leaderboard: table format with rank, model, score, price
- News: title + 2-3 sentence summary + source URL
- End with "今日观点 (Today's Insights)" — 1-2 key trends
- Use Chinese for all content (this is a Chinese-language report by default)

## Report Sections Template

```
# 🚀 AI 科技日报 — {date}

---

# 📡 板块一：AI大模型与生成式AI最新动态

...

# 🏆 板块二：全球大模型排行榜

...

# 🤖 板块三：Agent行业趋势与前沿架构

...

# 🌐 板块四：科技圈其他重要新闻

...

# 💡 今日观点

> **趋势一：...**
> **趋势二：...**
```

## Cron Job Delivery Note
The final response is AUTO-DELIVERED — no need to call `send_message`. Just output the report. If nothing new to report, respond with `[SILENT]` to suppress delivery.

## Pitfalls

### 🔴 DuckDuckGo HTML endpoint is useless for search
`curl -s "https://html.duckduckgo.com/html/?q=..."` returns only the static HTML shell without search results. Do not attempt. Use Bing News, Hacker News, or browser-based scraping of dedicated news sites instead.

### ✅ arena.ai redirect resolved (verified 2026-09-02)
`arena.ai` previously redirected to an AI app builder — that is now obsolete. As of 2026-09-02, `browser_navigate("https://lmarena.ai/leaderboard")` redirects to `https://arena.ai/leaderboard`, which serves the REAL Arena leaderboard. The Overview page snapshot contains all arena sections directly (Agent/Text/WebDev/Vision/Document/Text-to-Image/Image Edit/Search/Text-to-Video/Image-to-Video/Video Edit) with ranks, model names, scores and CIs — no subagent needed. Snapshot (~300KB) truncates to a file; page through remaining sections with `read_file(offset=...)` and `search_files` on the snapshot file (search for section headings like "Text-to-Video"). Google News `/read/` links resolve via JS redirect — after `browser_navigate`, read `window.location.href` via `browser_console` to get the real article URL.
- ✅ Always note the data timestamp from the source page
- ✅ For leaderboards, include total votes and model count
