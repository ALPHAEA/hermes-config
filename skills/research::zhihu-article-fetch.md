---
name: zhihu-article-fetch
description: Bypass zhihu.com/zhuanlan.zhihu.com anti-scraping to extract article content using browser tools. Handles ZSE WAF, IP blocking, and JS-rendered content.
tags: [zhihu, zhuanlan, scraping, waf-bypass, browser-automation]
---

# Zhihu Article Fetch

## Problem

Zhihu has aggressive multi-layer anti-scraping:
- `zhuanlan.zhihu.com` subdomain often triggers IP-level 403 (code 40362: "请求参数异常")
- ZSE (Zhihu Security Engine) requires JS signature cookies (`__zse_ck`)
- Direct curl/requests/cloudscraper all get blocked
- Jina.ai / archive.is / Google cache all hit CAPTCHAs

## Solution

Use browser tools (`browser_navigate` + `browser_console`) on **`www.zhihu.com`** instead of `zhuanlan.zhihu.com`. The main domain has different WAF rules and often allows access even when the zhuanlan subdomain is blocked.

### Steps

1. **Navigate** via `www.zhihu.com/column/p/{article_id}` (not zhuanlan.zhihu.com/p/{id})

   ```python
   # Instead of:
   browser_navigate("https://zhuanlan.zhihu.com/p/634120476")  # ❌ Likely blocked
   
   # Use:
   browser_navigate("https://www.zhihu.com/column/p/634120476")  # ✅ Often works
   ```

2. **Extract article data** from the JSON script tag

   The article data is stored in a `<script type="text/json">` tag as `initialState.entities.articles[{id}]` — **NOT** `window.__INITIAL_STATE__` (which was the old zhuanlan format).

   Use this JavaScript in `browser_console`:

   ```javascript
   (() => {
     const scripts = document.querySelectorAll('script[type="text/json"]');
     for (const s of scripts) {
       try {
         const data = JSON.parse(s.textContent);
         if (data.initialState?.entities?.articles) {
           const articleId = Object.keys(data.initialState.entities.articles)[0];
           const article = data.initialState.entities.articles[articleId];
           return JSON.stringify({
             title: article.title,
             content: article.content,           // HTML content
             excerpt: article.excerpt,            // text excerpt
             author: article.author?.name,
             created: article.created,            // unix timestamp
             contentId: articleId
           }, null, 2);
         }
       } catch(e) {}
     }
     return 'Article data not found in JSON scripts';
   })()
   ```

3. **Parse the HTML content** — `article.content` is raw HTML string. You can extract text/links/images from it using regex or DOMParser.

4. **Download images** — Image URLs from the HTML content are typically `https://pic4.zhimg.com/v2-{hash}_{size}.jpg`. Download with `curl` and reference in notes via Obsidian wikilinks.

## Pitfalls

- **IP blocking persists within a browser session.** If a zhuanlan subdomain request triggered a 403, the same Browserbase session may remain blocked for both `zhuanlan.zhihu.com` and `www.zhihu.com` because they share the same IP. A full new browser session (new Browserbase instance) is often needed.
- **Navigate to homepage first.** Always try navigating to `https://www.zhihu.com` first to establish a session cookie before hitting the article URL. This can sometimes bypass the WAF.
- **Check `initialState.entities.articles` vs `initialState.entities.zhuanhaos`.** The article data lives under `initialState.entities.articles[{articleId}]` — NOT `initialState.entities.zhuanhaos` (which contains author profile info, not the article itself).
- **The `content` field is HTML, not rendered DOM.** It's a raw HTML string within JSON, containing `<p>`, `<img>`, `<h2>`, etc. tags. Parse it in Python with `from bs4 import BeautifulSoup` or via regex.
- **Image extraction from HTML content.** Images in `article.content` use standard `<img>` tags with `src` attributes like `https://pic4.zhimg.com/v2-{hash}_{size}.jpg`. Do NOT try to extract `data-*` attributes — those may be missing in the HTML string. Use `BeautifulSoup(content, 'html.parser').find_all('img')` and get `img['src']`.
- **Obsidian note storage.** When saving images to Obsidian vault, note that vault paths may contain spaces (e.g., `~/Documents/Obsidian Vault`). Use `shlex.quote()` or wrap paths in double quotes for shell commands. Use `![[image.png]]` wikilinks in markdown.
- **After creating notes, sync.** Run the sync script (e.g., `python ~/Documents/Obsidian\ Vault/.obsidian/sync-nutstore.py sync`) to push to cloud storage.
- **Article IDs can be recycled.** If a zhuanlan article was deleted, the ID may now point to a different article. Verify the title matches expectations.
- **No login needed** — content is publicly accessible without authentication, just needs WAF bypass.
- **Navigate to `about:blank` between attempts** to force a new page load rather than relying on the same browser session.
- **Article IDs can be recycled.** If a zhuanlan article was deleted, the ID may now point to a different article. Verify the title matches expectations.
- **No login needed** — content is publicly accessible without authentication, just needs WAF bypass.
- **The `content` field is HTML string** (not rendered DOM). Use `json_parse` in Python or `JSON.parse` in JS console.

## Example Output Structure

```json
{
  "title": "windows搭建sock5代理服务器",
  "content": "<h2>1、下载3proxy</h2><p data-pid=\"...\">...</p>...",
  "excerpt": "<img src=\"...\"/>1、下载3proxy...",
  "author": "渔Tech",
  "created": 1685676584
}
```

## Alternative: When Everything is Blocked

If both domains are blocked from the current IP, try:
1. Navigate to `https://www.zhihu.com` first (homepage), let it fully load
2. Then navigate to the article URL
3. If still blocked, navigate to a completely unrelated zhihu page first to establish trust
