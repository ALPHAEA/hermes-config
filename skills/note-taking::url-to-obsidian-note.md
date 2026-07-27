---
title: URL to Obsidian Note
description: Extract web page content, download images, and save as formatted Obsidian notes synced to Nutstore (坚果云) via WebDAV
name: url-to-obsidian-note
---

# URL → Obsidian Note Workflow

## Trigger Conditions
User provides a URL and asks to save it as an Obsidian note in the vault.

## Script Location
The tool is at: `~/Documents/Obsidian Vault/.obsidian/url-to-note.py`

```bash
python3 url-to-note.py <URL> [title] [--dir NOTE]
```

## Step-by-Step

### 1. Fetch page content
- Use browser tools (`web_extract_text`) first — it handles JS-rendered content
- If content too short (< 500 chars), or site has WAF/antibot: use Python requests with proper headers
- CSDN: needs `Referer: https://blog.csdn.net` and `User-Agent: Mozilla/5.0`, content in `.article_content`
- OSChina: needs browser tool (dynamic JS content), then extract from `#main` element
- **微信公众号 (mp.weixin.qq.com)**: Uses heavy JS rendering + anti-bot CAPTCHA. Must use Playwright (Firefox) to render the page, wait 5-8s for content to load, then extract with `page.query_selector('#js_content').inner_text()` or `.rich_media_area_primary.inner_text()`. See Pitfalls for detailed steps.

### 2. Get images
- Extract `<img>` tags from the content
- Download each to `_assets/<note-slug>/`
- Include in note as Obsidian Wikilink: `![[_assets/<slug>/<filename>]]`

### 3. Save note
- If content is about IDEs/coding/server setup → save under `NOTE/` directory
- Otherwise → save in vault root
- Format: clean Markdown with headings, bullet lists, embedded images
- Frontmatter: title + source URL + date

### 4. Sync to Nutstore
```bash
cd ~/Documents/Obsidian\ Vault
python3 .obsidian/sync-nutstore.py sync
```

## Pitfalls
- CSDN has WAF — always send Referer header matching the site domain
- OSChina blog content is JS-rendered, MUST use browser tool to get the rendered HTML from `#main`
- Do NOT use `web_extract_text` on CSDN or OSChina — they strip too much content
- **微信公众号 (mp.weixin.qq.com) — 强反爬 + JS 动态渲染**：
  - `curl`/`requests` → 拿到 2.3MB 的 JS/模板页面，但文章内容不在 HTML 中（`js_content` 是空的占位元素）
  - `r.jina.ai` 代理 → 可能被 CAPTCHA 拦截（返回"环境异常"），但**有些微信公众号文章可用**（尤其是页面源码中有 `var content = '<html>...'` 或 `__INITIAL_STATE__` 变量包含文章内容的类型）
  - `web.archive.org` → 429
  - **正确方法**：用 Playwright (Firefox) 打开页面，等待 5-8 秒让 JS 渲染完成，然后用 `query_selector('#js_content')` 或 `.rich_media_area_primary` 提取 `.inner_text()`
  - 安装: `pip install playwright && playwright install firefox`
- **微信公众号图片防盗链**：`mmbiz.qpic.cn` 图片直接 `requests.get` 会返回 400。正确下载方式（任选其一）：
  - **方法A（推荐）**：在 Playwright 页面上下文中用 `page.evaluate()` 执行 `fetch()` + `FileReader().readAsDataURL(blob)` 获取 base64 数据，然后用 `base64.b64decode()` 写入文件。利用页面已有的 cookies/referer 认证通过防盗链。
  - **方法B（简易）**：用 `wget` 或 `curl` 加 `User-Agent: Mozilla/5.0` 和 `Referer: https://mp.weixin.qq.com` 头。注意去掉 URL 末尾的 `/0` 或 `/640` 等后缀。示例：`wget --header="User-Agent: Mozilla/5.0" --header="Referer: https://mp.weixin.qq.com" "https://mmbiz.qpic.cn/.../0" -O img.jpg`
- **知乎 (zhuanlan.zhihu.com) — 高反爬，无法直接获取**：知乎使用 ZSE (知乎安全引擎) 全面防护，需要 JS 签名令牌。当前环境（无登录态、无浏览器 JS 执行）下所有方式均失败：
  - curl/requests/cloudscraper → 403 (ZSE 拦截)
  - 浏览器 → 空页面或验证页面
  - API 端点 (`/api/v4/articles/{id}`) → 403/10003
  - r.jina.ai 代理 → 返回登录验证页面
  - web.archive.org → 429
  - **替代方案**：让用户直接复制粘贴内容、用已登录浏览器手动保存页面、或者截图/PDF 发来后 OCR
- Images should be downloaded AFTER determining the note name (for the slug)
- sync-nutstore.py must sync all file types, not just .md, or images won't reach remote
- If images don't show in Obsidian, check _assets/ exists in remote (sync again), then restart Obsidian
- `sync` command can timeout when there are many images (11+ JPGs each 100KB-900KB). Use individual `push <file>` commands for each file instead — faster and more reliable per file
- After creating a note with images, always push the .md file first, then push images one by one or in a loop

## Vault Info
- Path: `~/Documents/Obsidian Vault`
- Sync: Nutstore WebDAV via `sync-nutstore.py`
- Remote: `https://dav.jianguoyun.com/dav/obsidian/`
