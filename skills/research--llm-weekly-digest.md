---
name: llm-weekly-digest
description: Generate comprehensive multi-section AI/LLM industry digests by scraping real-time leaderboard data (LMSYS Chatbot Arena, SWE-bench) and parallel-delegated news research. Covers model updates, benchmark rankings, Agent trends, and tech industry news.
tags: [leaderboard, benchmark, lmsys, swe-bench, news-digest, arena-ai]
---

# LLM Weekly Digest Generator

A systematic approach for generating comprehensive AI/LLM industry digests covering:
1. AI model & generative AI news
2. LLM benchmark rankings (live scraped)
3. Agent industry trends
4. Broader tech news

## Key URLs (updated as of July 2026)

### LMSYS Chatbot Arena (moved from lmarena.ai → arena.ai)
- **Main leaderboard**: `https://arena.ai/leaderboard/` (overview with all categories)
- **Text arena**: `https://arena.ai/leaderboard/text` (Elo scores, 7M+ votes, 368 models)
- **Agent arena**: `https://arena.ai/leaderboard/agent`
- **Data freshness**: Shows "Jun 25, 2026" — typically updated every few days
- **Breakdown of text categories**: Scroll to the "Categories" filter to switch between Overall, Expert, Math, Coding, Multi-Turn, Creative Writing, etc.
- **Model price info**: The table shows `Price $/M` column (input/output per million tokens) and `Context` length

### SWE-bench Verified (coding benchmark)
- **Main page**: `https://swebench.com/` → click "Verified" button
- **Direct URL**: `https://www.swebench.com/verified.html`
- **Filter controls**:
  - Agent dropdown: `mini-SWE-agent v2` (default), `All OSS agents`, `All agents`
  - Model dropdown: `All models`, `Open source only`, `Proprietary only`
- **Columns**: Model, % Resolved, Avg. $ (cost per run), Trajs, Org, Date, Agent
- **New models** are marked with 🆕 prefix
- **Verification links**: Click the `` icon for detailed run traces

### Hugging Face Open LLM Leaderboard
- **Space**: `https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard`
- Note: This is a Gradio Space — the folder page shows org info. Navigate to the Space's "App" tab to see the actual leaderboard.
- Results dataset: `https://huggingface.co/datasets/open-llm-leaderboard/results`

### Artificial Analysis
- **Main**: `https://artificialanalysis.ai/`
- Shows changelog with recent model evaluations (date-stamped)
- Intelligence Index, Speed, Cost per Task widget
- **Key recent updates** often appear as highlighted cards or in the changelog sidebar

## Workflow

### Phase 1: Parallel delegate_task for broad research (fallback)

Use `delegate_task` with 3 parallel tasks for news collection:
1. AI models & generative AI (GPT, Claude, Gemini, Llama, Qwen + NVIDIA/AMD/Intel chip news)
2. LLM benchmark data (give the subagent instructions on which sites to scrape)
3. Agent industry trends

Each subagent's goal should **explicitly include** the list of keywords/sources to check.

**⚠️ Important caveat**: Subagents with `toolsets: ["search"]` may exit prematurely after only 1-2 searches. This is known (see Pitfalls). Still worth running as a first pass — even partial results provide useful context. **Do NOT rely on subagent output alone**; always do Phase 2 browser scraping for authoritative data.

### Phase 2: Direct browser scraping for live data (PRIMARY source)

After delegate_task returns, use `browser_navigate` to scrape live data from these sources **in the main session**:

#### Priority sources (always scrape these):
1. **`https://arena.ai/leaderboard/text`** — LMSYS Chatbot Arena Elo scores, pricing, context length
   - Use `browser_console` with JS to extract table rows (see Data Extraction Tips below)
   - Click category buttons (💻 Coding, 🧮 Math) to get sub-rankings — extract data again after clicking
2. **`https://swebench.com/`** (index.html, NOT verified.html) — SWE-bench Verified coding rankings
   - The table is server-rendered in index.html — visible in the initial `browser_navigate` snapshot
   - verified.html only shows description text (no table data)
   - Extract rows with `browser_console` JS targeting the table
   - Data columns: Model, % Resolved, Avg. $, Agent, Date
3. **`https://www.anthropic.com/news`** — Check for Anthropic model releases, policy announcements
   - Clean layout with date stamps — excellent for recent announcements
   - The featured article banner shows the most important news

#### Secondary sources (as time permits):
1. **`https://news.ycombinator.com/`** — Hacker News front page
   - Excellent for real-time AI/tech news with community vote scores
   - Extract with `browser_console`...
2. **`https://artificialanalysis.ai/leaderboards/models`** — LLM Intelligence Index leaderboard with live data
   - **Directly scrapeable via browser tools** — shows ranked table with Intelligence Score (0-100), Blended USD/1M Tokens, Median Tokens/s, Latency, Context Window
   - Example data (July 2026): Claude Fable 5 (60), GPT-5.6 Sol max (59), GPT-5.6 Sol xhigh (58), GPT-5.6 Sol high (56), Claude Opus 4.8 max (56)
   - The overview paragraph at the top gives a quick summary: "Claude Fable 5 (with fallback) and GPT-5.6 Sol (max) are the highest intelligence models"
   - Table has filter controls (Weights, Size, Price, Reasoning, Status) — can accept default filters for quick snapshot
   - **Treated as a primary source, not secondary** — provides authoritative intelligence index scores that complement arena.ai Elo data
3. **Bing News** (`https://www.bing.com/news/search?q=...&qft=interval%3d%2224%22&form=YFNR`): Works well for news gathering despite bot protections. Use `qft=interval%3d%2224%22` for past 24 hours, `%227%22` for 7 days. **Note**: Bing Japan (`www.bing.com`) returns Japanese UI labels (「トップ記事」「IT・科学」etc.) but the English-language news content is still fully usable — the article titles, URLs, and descriptions remain in English.
   - For recent news, search with `q=OpenAI+GPT+Claude+Gemini+latest+news+July+2026` pattern
   - For chip news: `q=NVIDIA+AMD+Intel+chip+AI+semiconductor+July+2026`
   - For Agent news: `q=AI+agent+autonomous+multi-agent+CrewAI+LangChain+2026+July`
   - Best practice: run 5-6 separate searches with different keyword combos to cover all sections
4. **Google News**: CAPTCHA-prone — avoid if Bing is sufficient
5. **Hacker News** (`https://news.ycombinator.com/`): Excellent for filtering the most important AI/tech stories. 100+ points = major news; 50+ = notable. AI-related stories often dominate top 10.

#### Sources to AVOID:
- **OpenAI blog** (`openai.com/blog`) — aggressive Cloudflare bot detection, page returns empty (title: "Just a moment...")
- Instead, find OpenAI news via Hacker News, Reddit, or Anthropic's news page (they often comment on competitor moves)

### Phase 3: Compile report

Organize into 4-5 sections with clear emoji headers:
- 🔥 AI大模型与生成式AI最新动态
- 📊 全球大模型排行榜（live data）
- 🤖 Agent行业趋势与前沿架构
- 🗞️ 科技圈其他重要新闻
- 🔮 今日观点 (1-2 key trends)

## Data Extraction Tips

### From arena.ai text leaderboard (arena.ai/leaderboard/text)
The leaderboard data is rendered with **custom React/WebComponent elements** — standard `role="row"` or `<tr>` selectors may NOT work in JS extraction. The snapshot (accessibility tree) does show the data in readable `row` elements.

**Primary extraction method**: Use `browser_snapshot(full=true)` and read the text from the snapshot. The table data appears as accessible `row` elements with cell contents concatenated (e.g., `"1 1 6 Anthropic claude-fable-5 1509 ±9 4,299 $10 / $50 1M"`).

**Fallback JS extraction** (when snapshot is truncated): Use `querySelectorAll('*')` with text-matching heuristics:
```javascript
(() => { const all = document.querySelectorAll('*'); const texts = []; 
all.forEach(el => { const t = el.textContent?.trim(); 
  if(t && /claude|gpt|qwen|llama|gemini|deepseek|mistral/i.test(t) && t.length < 200 && /±/.test(t) && !texts.some(x=>x.includes(t))) 
    texts.push(t.substring(0,150)); 
}); return texts.slice(0,30).join('\n'); })()
```
This works because React renders the score (±N) and model names as deeply nested text nodes that get picked up by broad DOM traversal.

**Category switching**: Click the category button (e.g., `@e41` labeled "💻 Coding") to switch categories. Wait for re-render, then run the JS extraction again. Categories include: 🏆 Overall (default), 💻 Coding, 🧮 Math, 💬 Multi-Turn, ✍️ Creative Writing, 🤓 Expert, etc.

Key data patterns:
- Rows appear as: `{rank}{spread}{org}{model-name}{score}±{CI}{votes}{price-in}/{price-out}{context}`
- Example: `"1 1 6 Anthropic claude-fable-5 Anthropic · Proprietary 1509 ±9 4,299 $10 / $50 1M"`
- Price format: `$10 / $50` means input $10/M, output $50/M
- Context: `1M`, `200K`, `128K`, etc.
- Vote counts help gauge data reliability: 30K+ votes is very stable

### From artificialanalysis.ai/leaderboards/models
The LLM Intelligence Index leaderboard is rendered as a standard HTML `<table>` in the browser snapshot. The data appears as clean text rows:

```
"Claude Fable 5 (with fallback) 1M Anthropic Anthropic 60 $7.70 63 159.92 167.86"
"GPT-5.6 Sol (max) 1M OpenAI OpenAI 59 $4.35 -- -- --"
```

Columns: Model | Context Window | Creator | Intelligence Index (0-100) | Blended USD/1M Tokens | Median Tokens/s | Latency First Chunk | Total Response Time

**Use `browser_snapshot(full=true)`** to see the table — the data shows in the snapshot as structured rows. Scrolling down via `browser_scroll(direction="down")` reveals more entries.

**Headline summary**: The page's intro paragraph (visible in snapshot) names current leaders: "Claude Fable 5 (with fallback) and GPT-5.6 Sol (max) are the highest intelligence models"

**Reliability**: Directly scrapeable without bot protection — **treat as a primary source** alongside arena.ai, not secondary. The Intelligence Index provides a complementary score to arena.ai's Elo.

### From SWE-bench (index.html)
Row format:
```
"row Select Claude 4.5 Opus (high reasoning) 🆕 Claude 4.5 Opus (high reasoning) 76.80 $0.75  2026-02-17 2.0.0"
```
Parsing pattern: `Select {Model} 🆕? {Model} {% Resolved} ${Avg Cost} icon {Date} {Agent Version}`

Extraction JS:
```javascript
(() => { const rows = document.querySelectorAll('table tbody tr'); 
  const data = []; 
  rows.forEach((row, i) => { if(i < 30) { 
    const cells = row.querySelectorAll('td'); 
    if(cells.length >= 7) { 
      const modelName = cells[1]?.querySelector('a')?.textContent?.trim() || cells[1]?.textContent?.trim(); 
      data.push({
        modelName: modelName.replace(/🆕\s*/, '').trim(),
        resolved: cells[2]?.textContent?.trim(),
        cost: cells[3]?.textContent?.trim(),
        date: cells[5]?.textContent?.trim(),
        agent: cells[6]?.textContent?.trim()
      }); 
    } 
  } }); 
  return JSON.stringify(data); 
})()
```

⚠️ **Always use `index.html`** (the main landing page), NOT `verified.html`. The table is server-rendered on `index.html`. `verified.html` only shows description text.

### From Hacker News (news.ycombinator.com)
The page uses a clean structure with pairs of `<tr>` rows (title row + metadata row). Extract with:

```javascript
(() => { const rows = document.querySelectorAll('.athing'); 
  const data = []; 
  rows.forEach((row, i) => { if(i < 30) { 
    const titleEl = row.querySelector('.titleline a');
    const title = titleEl?.textContent?.trim() || '';
    const url = titleEl?.href || '';
    const subrow = row.nextElementSibling;
    const pointsEl = subrow?.querySelector('.score');
    data.push({
      rank: i+1,
      title,
      url,
      points: pointsEl?.textContent?.trim(),
      user: subrow?.querySelector('.hnuser')?.textContent?.trim() || ''
    }); 
  } }); 
  return JSON.stringify(data, null, 2);
})()
```

Filtering: prioritize stories with 100+ points for "big news", 50+ for notable items. Check the rank position — top 5 stories are usually the hottest topics of the day.

### From anthropic.com/news
The news page has a featured banner article followed by a reverse-chronological list. The featured article's linked heading + paragraph summary gives you the key announcement. Date stamps are in `<time>` elements.

### From arena.ai agent arena (arena.ai/leaderboard/agent)
The Agent Arena uses a different table format with 8+ metric columns. Extract similarly with broad DOM traversal:
```javascript
(() => { const all = document.querySelectorAll('*'); const texts = []; 
all.forEach(el => { const t = el.textContent?.trim(); 
  if(t && (t.includes('Claude') || t.includes('GPT') || t.includes('Gemini') || t.includes('Qwen') || t.includes('DeepSeek')) && /[\d.]+%/.test(t) && t.length < 300 && !texts.some(x=>x.includes(t))) 
    texts.push(t.substring(0,200)); 
}); return texts.slice(0,20).join('\n'); })()
```
Key columns: Rank | Model | Net Improvement (↑↓%) | Confirmed Success | Praise vs Complaint | Steerability | Bash Recovery | Tool Hallucination | Sessions
- Positive values in Net Improvement = the model's agentic performance improved over baseline
- Tool Hallucination = lower is better (shown as ↓X.XX%)
- Sessions = sample size; 30K+ is reliable
- The page shows a date stamp (e.g., "Jul 8, 2026") and total session count (e.g., "947,000 sessions")

## On-the-fly Workflow: When Standard Search Fails

### The Problem

In some environments (especially cron jobs), all search methods fail:
- `web_search` tool may not be available
- Google requires JavaScript (returns blank)
- DuckDuckGo Lite returns CAPTCHA
- Bing search via `execute_code` returns empty

### The Solution: Two-Phase Fallback with Known News Sites

**Phase 1: Parallel delegate_task with browser tools**
```python
# Launch 3-4 subagents in parallel, each targeting specific known sources
delegate_task(
    goal="Search TechCrunch AI category for latest AI news...",
    context="Use browser_navigate to https://techcrunch.com/category/artificial-intelligence/ ...",
    toolsets=["browser"]
)
```
Each subagent visits a dedicated news site (not a search engine) and scrapes the content.

**Reliable sources for Phase 1** (no bot protection, clean HTML):
- `https://techcrunch.com/category/artificial-intelligence/` — AI-specific news, updated hourly
- `https://www.theverge.com/ai-artificial-intelligence` — AI news coverage
- `https://venturebeat.com/category/ai/` — AI industry analysis
- `https://www.artificialanalysis.ai/` — LLM intelligence index rankings
- `https://www.swebench.com/` — Coding benchmark leaderboard

**Fallback sources when primary ones are blocked:**
- `https://www.theverge.com/news` — General tech news
- `https://news.ycombinator.com/` — Hacker News (sorted by points)

**Phase 2: Compile from returned data**
The subagents return structured summaries (titles + summaries + URLs). Cross-reference and deduplicate in the main session.

### Why This Works Better Than Search
- Dedicated news sites are optimized for crawlers/bots (better SEO = easier scraping)
- No CAPTCHA or JavaScript required
- Content is already curated by editorial teams (less noise)
- TechCrunch/The Verge/VentureBeat update continuously throughout the day

### Pitfall: delegate_task with only `toolsets=["search"]` is unreliable
Subagents that only have `web_search` (not browser) may exit prematurely after 1-2 calls. Always include `toolsets=["browser"]` for news collection subagents.

### Pitfall: LMSYS domain changes
- `arena.ai` (as of mid-2026) redirects to `arena.ai` (a different product — AI app builder, not the leaderboard)
- `lmarena.ai` is the actual Chatbot Arena domain
- The Hugging Face Space at `huggingface.co/spaces/lmarena-ai/arena-leaderboard` still exists but data is inside an iframe that's hard to scrape
- **Most reliable approach for leaderboard data**: Artificial Analysis (`artificialanalysis.ai`) and SWE-bench (`swebench.com`) — they both render data in accessible HTML

## Pitfalls

### 🔴 Critical: delegate_task subagent instability with search toolsets
Subagents using `toolsets: ["search"]` may **exit prematurely** — they call `web_search` but then stop before processing results. This is unreliable for critical data collection. 

**Fallback strategy**: If a delegate_task subagent returns suspiciously short/empty results:
1. **Do NOT re-try the same subagent** — it will likely fail again
2. **Use browser tools directly** in the main session to scrape authoritative source URLs
3. Priority targets for browser scraping: `arena.ai/leaderboard/text`, `arena.ai/leaderboard/agent`, `arena.ai/leaderboard/vision`, `swebench.com/`
4. This produces **better data** (live, full tables) than search-result summaries

### 🔴 Cron job execution: avoid fragile delegation
When running as a cron job:
- There is NO user to recover from failures
- `delegate_task` subagent failures cannot be recovered interactively
- **Prefer doing critical data collection via browser tools in the main session** over delegating to subagents
- The first subagent attempt is worth trying if the prompt is very detailed (listing exact keywords), but have a fallback plan
- **RECOMMENDED cron job workflow**: Run 3 `delegate_task` subagents + start Phase 2 browser scraping immediately (don't wait for subagents to finish). This way browser scraping completes even if subagents return empty.

### Other pitfalls

1. **arena.ai ≠ LMSYS Chatbot Arena**: As of mid-2026, `arena.ai` redirects to a different product (AI app builder). The actual Chatbot Arena (LMSYS) lives at `lmarena.ai`. The Hugging Face Space `hf.co/spaces/lmarena-ai/arena-leaderboard` is the authoritative source but data is inside an iframe. **Use Artificial Analysis (`artificialanalysis.ai`) and SWE-bench (`swebench.com`) as primary authoritative ranking sources** since they render accessible HTML tables.
2. **SWE-bench agent selection matters**: The leaderboard defaults to `mini-SWE-agent v2`. To see results with all agents, change the dropdown. The default agent may exclude some model results.
3. **SWE-bench page gotcha**: Use `index.html` not `verified.html`. The table is only server-rendered on the main `index.html` page. `verified.html` shows only description text.
4. **delegate_task subagents cannot browse**: Subagents called via `delegate_task` don't have browser access by default. Pass `toolsets=["web"]` for search or use the main session for `browser_navigate`.
5. **Google News CAPTCHA**: May trigger bot detection. Use Bing News (`bing.com/news/search`) or Hacker News as a fallback.
6. **OpenAI blog blocked**: Cloudflare/Cloudfront on `openai.com/blog` returns empty page ("Just a moment..."). Do not attempt. Find OpenAI news via HN or Anthropic news page.
7. **arena.ai uses Elo-style scores**: The scores range ~1200-1550. A 10-point gap is significant. Look at confidence intervals (±N) for reliability.
8. **Freshness check**: Check the date stamp on arena.ai ("Jul 2, 2026" format) and SWE-bench ("Date" column) to know data recency. If arena.ai shows no update in 5+ days, note "榜单近期未更新" in the report.
9. **Cost column meaning**: In SWE-bench, "Avg. $" is average cost per task run. In arena.ai, "Price $/M" is per million tokens for input and output.
10. **New cost-efficiency contenders**: As of mid-2026, models like MiniMax M2.5 (high reasoning) achieve 75.80% SWE-bench at only $0.07/task — worth calling out in the 性价比 section as the "best bang for buck" leader.
12. **Bing News time intervals work**: The `qft=interval%3d%2224%22` param sets past 24 hours. For past 7 days use `%227%22`, for 30 days use `%2230%22`. Bing may show Japanese UI labels but English content still works.
13. **Bing News limited results per page**: Bing News only shows ~6-10 results per page. Run multiple queries with different keyword combinations for comprehensive coverage rather than trying to paginate.
14. **When JS extraction returns empty arrays**: If `querySelectorAll('[role="row"]')` returns 0 results on arena.ai, the data is likely rendered in custom WebComponents. Fall back to the broad `querySelectorAll('*')` text-matching approach described above.
