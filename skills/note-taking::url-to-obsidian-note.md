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
- **微信公众号 (mp.weixin.qq.com)**: Uses heavy JS rendering + anti-bot CAPTCHA. Must use Playwright (Firefox) to render the page, wait 5-8s for content to load, then extract with `page.query_selector('#js_content').inner_text()` or `.rich_media_area_primary.inner_text()`. **Note: `#js_content`'s `<img>` elements get lazy-loaded and often replaced by placeholder `pic_blank` gifs during scroll — so DOM img extraction is unreliable. Extract image URLs from the raw HTML instead (regex).** See Pitfalls for detailed steps.

### 2. Get images
- Extract `<img>` tags from the content
- Download each to **vault 顶层 `_assets/<slug>/`**（切勿放到 NOTE/<子目录>/_assets/ 下）
- Include in note as Obsidian Wikilink: `![[_assets/<slug>/<filename>]]`（从 vault 根解析，NOTE 子目录里的笔记同样能指向顶层 _assets）

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
  - **方法A（实测易失败）**：在 Playwright 页面上下文中用 `page.evaluate()` 执行 `fetch()` + `FileReader().readAsDataURL(blob)` 获取 base64。**注意：fetch 必须保留 URL 的完整 query 参数**（如 `?wx_fmt=jpg&wxfrom=12&usePicPrefetch=1`）——这些参数携带防盗链签名，去掉后 fetch 会报 `NetworkError: attempt to fetch resource`。从 DOM 拿的 `src` 常常只剩 placeholder gif，所以此法在懒加载+反爬页面上常拿不到真实图。
  - **方法B（实测推荐/最可靠）**：用 `curl` 加 `User-Agent: Mozilla/5.0` 和 `Referer: https://mp.weixin.qq.com/` 头直接下载。**关键：必须保留 URL 结尾的 `/0` 尺寸后缀（全尺寸图）以及完整 query 参数——不要去掉它们**，否则下载会失败/拿到缩略图。正确示例（从 HTML 正则提取的完整 URL 直接喂给 curl）：
    ```
    curl -sL -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120" \
         -H "Referer: https://mp.weixin.qq.com/" \
         "https://mmbiz.qpic.cn/mmbiz_jpg/XXXX/0?wx_fmt=jpeg" -o img.jpg
    ```
  - 从 HTML 提取图片 URL 的可靠方法：用 Playwright 拿到 `page.content()`（或 `document.documentElement.innerHTML`，几 MB），然后正则 `https?://mmbiz\.qpic\.cn/[^"'\s<>\\]+` 提取所有 URL，**保留完整 query**，按出现顺序去重（含 `/0` 全尺寸与 `/300`/`/132`/`/400` 缩略图时，保留最大尺寸那一版，通常取 base path 以 `/0` 结尾的那个）。注意 `sz_mmbiz_jpg`/`mmbiz_jpg` 等前缀属于 appID 签名，必须完整保留。
  - 判断图是否下载成功：检查文件大小（正文长截图通常 100KB~300KB）；小于 ~3KB 的通常是二维码/小图标，但仍可保留。

### 微信公众号内容多样性的陷阱
- 引流推广文正文可能只有一段文字 + 大量长截图（无 `<p>` 正文段落）。若 `#js_content.innerText()` 只有一两句且图片是内容主体，说明图片 URL 都在 HTML 里——必须用上面的 regex + curl 方法抓全所有图并嵌入，否则笔记会严重缺失内容。用户常在发现图片没抓全后要求重做，所以**首轮就要把 HTML 正则提取的图片全部下载嵌入**，不要只依赖 DOM 的已加载 img。
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
- Sync: Nutstore WebDAV via `sync-nutstore.py`\n- Remote: `https://dav.jianguoyun.com/dav/obsidian/`\n- **删除远端旧/错误文件**：sync-nutstore.py 只上传/下载，不能删远端。若移动了资源位置（如从 NOTE/<子>/_assets 移到顶层 _assets），需手动用 curl WebDAV DELETE 清理远程旧目录：`curl -X DELETE -u "user:pass" "https://dav.jianguoyun.com/dav/obsidian/NOTE/AI/_assets/ca93d4c2"`（对目录 DELETE 会级联删子文件，返回 204 = 成功）。删除后再重新 push 正确位置的文件。
