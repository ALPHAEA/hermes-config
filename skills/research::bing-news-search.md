---
name: bing-news-search
description: Gather news and compile reports using Bing News via browser — the most reliable fallback when web_search tool is unavailable and Google/DuckDuckGo are CAPTCHA-blocked.
---

# Bing News Search via Browser

Use Bing News (`bing.com/news/search`) as a primary news gathering tool when:
- `web_search` tool is not available
- Google/DuckDuckGo return CAPTCHA challenges
- You need real, verifiable news results for a report

## Why Bing News

- Bing generally accepts programmatic access without CAPTCHAs when Google/DuckDuckGo block them
- Structured news results with headlines, source names, timestamps, and URLs
- Works reliably from non-residential proxy IPs (unlike Google)
- Results appear in the browser snapshot in plain text for easy extraction

## Technique

### 1. Construct the Bing News URL

Basic format:
```
https://www.bing.com/news/search?q={KEYWORDS}&qft=interval%3d%2230%22&form=YFNR
```

Parameters explained:
- `q={KEYWORDS}` — URL-encoded search keywords
- `qft=interval%3d%2230%22` — past 30 days (change number for other windows: `7` = 7 days, `24` = 24 hours)
- `form=YFNR` — news search form

Time interval parameter:
- `interval%3d%2224%22` — past 24 hours
- `interval%3d%227%22` — past 7 days
- `interval%3d%2230%22` — past 30 days

**Note**: Bing Japan (`www.bing.com`) returns news in Japanese. To get English results, use English keywords and the time-interval parameter. It still works fine for English-language news.

### 2. Navigate and Read Results

```python
browser_navigate(url="https://www.bing.com/news/search?q=OpenAI+GPT+latest+news+2025&qft=interval%3d%2230%22&form=YFNR")
```

The snapshot returns structured data with:
- `heading` elements — news article titles (clickable links via ref IDs)
- `text` elements — article descriptions/summaries
- Source attribution (e.g., "VentureBeatからニュースを検索")

### 3. Extract Information

The snapshot contains all key data:
- **Title**: in `<heading>` elements
- **Description**: in adjacent `<text>` elements
- **Source URL**: in the `<link>` URL (contains the full article URL)
- **Time**: shown as relative time ("4 時間前", "1 日", etc.)

### 4. Search Strategy for Comprehensive Reports

For multi-topic reports (like a 5-section news digest):

1. **Search broad first**: `AI+agent+latest+news+June+2025`
2. **Then narrow per topic**:
   - `OpenAI+GPT+latest+news+2025`
   - `Anthropic+Claude+latest+model+2025`
   - `Meta+Llama+Google+Gemini+open+source+model+2025`
   - `AI+chip+NVIDIA+AMD+semiconductor+June+2025`
   - `AI+regulation+US+China+export+control+2026+June`
3. **Use specific timeframes**: Past 30 days gives the most comprehensive results
4. **Check multiple pages**: For deep coverage, search different keyword combinations

### 5. Cross-reference from Snapshot Text

The snapshot shows text like:
```
"VentureBeat · 4 時間前"
"heading: OpenAI's updated GPT-5.5 Instant..."
"text: OpenAI is moving away from models..."
"url: https://venturebeat.com/technology/..."
```

Read these as real results. Each `link` element with a URL is a news article; the adjacent `heading` is the title and `text` is the summary.

### 6. Special Note on `delegate_task`

**DO NOT use `delegate_task` for web search** — subagents hit tool call limits too quickly and produce inadequate results. Always use `browser_navigate` directly for news gathering.

## Pitfalls

1. **Bing Japan default**: Bing's Japanese instance (`www.bing.com`) shows Japanese UI and may prioritize Japanese news. Use English keywords and broader time intervals to get relevant results.
2. **CAPTCHAs still possible**: Bing may occasionally CAPTCHA, but much less frequently than Google.
3. **Snapshot truncation**: For long result lists, use `browser_snapshot(full=true)` or scroll down to reveal more results.
4. **Results not always newest-first**: Some results may be older. Check the relative time shown in the results.

## Example: Full News Digest Workflow

1. Search 10+ keyword combinations across 5 topic areas
2. Collect titles, summaries, URLs from each snapshot
3. Organize by topic area
4. Cross-check dates (relative times like "4 時間前", "1 日" = "4 hours ago", "1 day ago")
5. Compile final report with source URLs

## Verification

After collecting results, you can open specific article URLs with `browser_navigate` to read full content and verify details.
