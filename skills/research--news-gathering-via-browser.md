---
name: News Gathering via Browser
description: Gather and compile multi-topic news digests using browser tools (since web_search tool is unavailable). Uses Google News for search and structured result extraction.
---

# News Gathering via Browser

Use this approach when you need to gather current news across multiple topics but the `web_search` tool is not available.

## Prerequisites

- `browser_navigate`, `browser_snapshot`, `browser_scroll`, `browser_click` tools available
- No `web_search` tool available — this method replaces it

## Step-by-Step Process

### 1. Navigate to Google News with a Specific Search Query

**CRITICAL: Use `when` parameter for freshness.** Append `&when=1d` (past 24h), `&when=3d`, or `&when=7d` (past week) to filter by recency. Without this parameter, Google News returns content from weeks or months ago regardless of your query keywords.

```diff
- https://news.google.com/search?q=OpenAI+Claude+LLM&hl=en-US&gl=US&ceid=US%3Aen
+ https://news.google.com/search?q=OpenAI+Claude+LLM&hl=en-US&gl=US&ceid=US%3Aen&when=1d
```

More examples with recency filter:
- `https://news.google.com/search?q=AI+Agent+multi-agent+MCP+autonomous&hl=en-US&gl=US&ceid=US%3Aen&when=7d`
- `https://news.google.com/search?q=DeepSeek+V4+Llama+Qwen+open+source&hl=en-US&gl=US&ceid=US%3Aen&when=7d`
- `https://news.google.com/search?q=NVIDIA+AMD+AI+chip+semiconductor&hl=en-US&gl=US&ceid=US%3Aen&when=3d`

Construct a Google News search URL:

```
https://news.google.com/search?q=<URL-encoded-query>&hl=en-US&gl=US&ceid=US%3Aen
```

Examples:
- `https://news.google.com/search?q=OpenAI+Claude+Gemini+LLM+model&hl=en-US&gl=US&ceid=US%3Aen`
- `https://news.google.com/search?q=NVIDIA+AMD+Intel+semiconductor+chip&hl=en-US&gl=US&ceid=US%3Aen`
- `https://news.google.com/search?q=AI+agent+autonomous&hl=en-US&gl=US&ceid=US%3Aen`
- `https://news.google.com/search?q=大模型+AI+最新新闻&hl=zh-CN&gl=CN&ceid=CN%3Azh-Hans&when=7d`

**Use Chinese locale (`hl=zh-CN&gl=CN`) for Chinese-language news coverage.** Note that Chinese Google News tends to return older content (weeks/months) compared to the English version, so always pair with `&when=7d` or another recency filter.

### 2. Extract Results from Snapshot

After `browser_navigate`, the returned snapshot contains news items in this format:
```
- text: SourceName
- button "More - Headline Text" [ref=eXX]
- link "Headline Text - SourceName - TimeAgo - By Author" [ref=eYY]:
    - /url: ./read/CBMi...?hl=en-US&gl=US&ceid=US%3Aen
- time: X hours ago / Yesterday / X days ago
```

Each story has:
- **Source**: e.g., "VentureBeat", "CNBC", "The Guardian"
- **Headline**: Clickable link with headline text
- **Time**: Relative time (e.g., "3 hours ago", "Yesterday")
- **Author**: After "By" in the link text
- **URL**: The `/url:` value under the link — prepend `https://news.google.com` to access it.

### 3. Use Google News Topic Tabs for Broader Coverage

Navigate to the Technology section and click on subtabs:
```
browser_navigate("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en")
```
Then click subtabs like:
- `@e43` — "Artificial intelligence" tab
- `@e26` — "Technology" > "Latest" tab
- Scroll down (`browser_scroll(direction="down")`) to load more stories

### 4. Handle the Google News URL Prefix

All links in Google News are relative (`./read/CBMi...`). To get actual URLs:
- The full URL is constructed as `https://news.google.com/read/CBMi...?hl=en-US&gl=US&ceid=US%3Aen`
- Note: Google News wraps links — the actual source URL is not directly available from the snapshot. For the report, linking to the Google News redirect URL is acceptable.

### 5. Search Multiple Queries in Parallel

Since you can only navigate to one URL at a time, use this workflow for multiple queries:
1. Navigate to URL for query 1 → read snapshot → record results
2. Navigate to URL for query 2 → read snapshot → record results
3. Repeat for remaining queries

### 6. Handling Blocked Sites

Most major news sites (Axios, Reuters, Fortune, VentureBeat, NYT) are blocked by Cloudflare/Vercel bot detection when accessed via browser_navigate. **Don't waste time trying to access them directly.** Instead:

- Extract maximum signal from Google News search result summaries themselves — headlines + source + relative timestamp + author
- Triangulate story details by searching different keyword combinations
- For longer-form content, use contextual reasoning across multiple Google News search results

### 7. Results Parsing Pattern (Google News Snapshot)

The snapshot follows this pattern around each article:
```
- text: PublisherName                <-- publisher (text before button)
- button "More - Headline" [ref=eN]: <-- article button
- link "Headline - Publisher - TimeAgo - By Author" [ref=eM]:
  - /url: ./read/CBMi...?hl=...       <-- Google redirect URL
- text: Headline                     <-- repeated headline text
- time: X hours ago / Yesterday      <-- recency
- text: By Author Name               <-- author
```

**Key interpretation rule**: The `text:` line immediately before a `button "More -"` is the **publisher**. The `time:` line immediately after the link gives **recency**. The `By ...` text after time gives the **author**.

### 8. Use delegate_task for Parallel Deep-Dive Searches (Optional)

After getting an overview from Google News, you can delegate deeper searches to parallel subagents. Note: subagents spawned via `delegate_task` may also lack `web_search` — they inherit the parent's toolset. Use `delegate_task(toolsets=["web"])` if available, otherwise subagents will need to use the same browser-based approach.

### 7. Compile Structured Report

Format each section with:
- **Emoji header** (🔥 for hot, 📉 for market, ⚡ for industry impact)
- **Bold headline** followed by 2-3 sentence summary
- **Source link** at the bottom of each item
- **Relative time** indicates freshness (prioritize items labeled "hours ago" or "Yesterday")

## Pitfalls to Avoid

- ❌ Do NOT attempt `web_search` directly — it doesn't exist in this toolset
- ❌ Don't rely on `browser_snapshot(full=true)` for Google News — content may still be truncated; use the compact snapshot which shows interactive elements clearly
- ❌ Don't navigate directly to blocked sites like Axios, Reuters, Fortune, VentureBeat — Cloudflare/Vercel block
- ❌ Don't forget the `&when=` parameter — Google News returns months-old content without it
- 🟡 **Blocked sites are common**: Expect Cloudflare challenges on most premium news sites. Triangulate from Google News summaries instead.
- ✅ Always check the "time" label next to each item for recency
- ✅ Search in both English and Chinese for comprehensive international coverage

## Example Cron Job Prompt Pattern

When creating a cron job for daily news gathering, structure the prompt as a self-contained instruction:

```
搜索并整理以下N个板块的最新内容...
板块一：XXX
板块二：XXX

格式要求：
- 每个板块用清晰的emoji标题和分隔线
- 每条新闻包含标题、摘要、来源URL
- 末尾添加「今日观点」
```
