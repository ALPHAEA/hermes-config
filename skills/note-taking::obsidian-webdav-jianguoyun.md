---
name: obsidian-webdav-jianguoyun
description: Set up Obsidian vault synced to 坚果云 (Jianguoyun) via WebDAV, with tools to convert URLs to notes and sync bidirectionally.
---

# Obsidian Vault + 坚果云 WebDAV 同步

坚果云 WebDAV 地址: `https://dav.jianguoyun.com/dav/`
应用目录: `/obsidian` (在坚果云 WebDAV 根目录下)

## 凭据

WebDAV 账号 = 坚果云邮箱账号，应用密码在坚果云「安全选项」中生成。

## 设置步骤

### 1. 创建本地 vault

```bash
mkdir -p ~/Documents/Obsidian\ Vault
```

### 2. 同步脚本

放在 vault 内的 `.obsidian/sync-nutstore.py`。

由于坚果云对第三方 WebDAV 库（webdavclient3、davfs2）兼容性差，改用 requests 直接构造 WebDAV 请求（PROPFIND/GET/PUT/MKCOL），最可靠。

**用法:**
```bash
python3 sync-nutstore.py sync   # 双向同步（先下载再上传）
python3 sync-nutstore.py down   # 只下载
python3 sync-nutstore.py up     # 只上传
python3 sync-nutstore.py push <文件>  # 推送单个文件
```

**脚本核心逻辑:**
- 使用 BFS + visited set 而非递归遍历远程目录，避免坚果云返回的"self"目录条目导致死循环
- 跳过 rel == cur.strip("/") 的条目（目录自引用）
- href 提取相对路径需 strip "/dav/obsidian" 或 "/dav" 前缀
- 用 unquote() 解码 URL 编码的中文路径
- MKCOL 创建远程目录时忽略 405(已存在)/409 错误

### 3. URL → Obsidian 笔记工具

脚本 `url-to-note.py` 自动从 URL 抓取网页内容→生成格式化 Markdown→保存到 vault→同步坚果云。

```bash
python3 url-to-note.py <URL> [自定义标题]
```

**特点:**
- **CSDN 专有解析器**: 加 Referer header 绕过 CSDN WAF（否则直接 GET 返回 403）
- 自动识别 `csdn.net` 域名，使用专用抓取逻辑
- BeautifulSoup 解析，提取标题、描述、正文段落
- 过滤 HTML 残留标签、尾部孤立标签（`info`, `warn`, `error`, `URL` 等）
- 去重连续相同段落，限制最终笔记不超过 5 万字符
- 自动推送新笔记到坚果云

### 4. 设置 OBSIDIAN_VAULT_PATH

添加到 `~/.bashrc`:
```bash
export OBSIDIAN_VAULT_PATH="$HOME/Documents/Obsidian Vault"
```

## 笔记目录整理

NOTE 目录下的组织规范：

```
NOTE/
├── Java/               ← 按技术/主题分目录
│   └── idea-jboss-war-deploy.md
├── Network/
│   ├── socks5-proxy-server.md
│   └── wifi6-wifi7-router-guide.md
├── ...
```

**规则：**
1. **文件名**：英文简短描述，全小写连字符（如 `idea-jboss-war-deploy.md`）
2. **frontmatter**：每篇笔记顶部统一格式：
   ```yaml
   ---
   title: 笔记标题
   source: 来源网站名     # 如：CSDN、知乎、微信公众号、OSChina
   source_url: 原文链接
   author: 原作者名
   created: YYYY-MM-DD
   tags: [标签1, 标签2]
   ---
   ```
3. **来源标记**：通过 frontmatter `source:` 字段 + `tags:` 标记，不做来源目录
4. **_assets 文件夹**：与笔记文件同名（去掉 `.md`），如 `idea-jboss-war-deploy.md` → `_assets/idea-jboss-war-deploy/`
5. **改名联动**：笔记改名时，对应的 _assets 文件夹和笔记内的 `![[_assets/...]]` 引用路径必须同步更新

## 远程旧文件清理（WebDAV DELETE）

坚果云同步脚本只会上传/下载新文件，不会删除远程旧文件。改名或删除笔记后，远程残留需要手动清理。

**列出远程目录：**
```bash
printf '<?xml version="1.0"?><d:propfind xmlns:d="DAV:"><d:prop><d:displayname/><d:getlastmodified/><d:resourcetype/></d:prop></d:propfind>' | \
  curl -s -u '邮箱:应用密码' -X PROPFIND -H "Depth: 1" -d @- \
  "https://dav.jianguoyun.com/dav/obsidian/NOTE/" | \
  python3 -c "
import sys, xml.etree.ElementTree as ET
from urllib.parse import unquote
data = sys.stdin.read()
root = ET.fromstring(data.encode())
NS = {'d': 'DAV:'}
for resp in root.findall('d:response', NS):
    href = resp.find('d:href', NS).text
    rel = href
    for prefix in ['/dav/obsidian', '/dav']:
        if rel.startswith(prefix):
            rel = rel[len(prefix):]
            break
    rel = unquote(rel).rstrip('/')
    if not rel:
        continue
    is_coll = resp.find('d:propstat/d:prop/d:resourcetype/d:collection', NS) is not None
    tag = '📁' if is_coll else '📄'
    print(f'{tag} /{rel}')
"
```

**删除远程文件/目录：**
```bash
# 删除文件
curl -s -u '邮箱:应用密码' -X DELETE \
  "https://dav.jianguoyun.com/dav/obsidian/NOTE/旧文件名.md" -w "HTTP %{http_code}\n"

# 删除目录（含子内容）
curl -s -u '邮箱:应用密码' -X DELETE \
  "https://dav.jianguoyun.com/dav/obsidian/_assets/旧文件夹名/" -w "HTTP %{http_code}\n"
```

**注意：**
- 中文路径在 URL 中会自动编码，curl 会处理
- 但如果有特殊字符（空格、# 等），需要手动 URL 编码
- DELETE 目录时末尾必须带 `/`
- 成功返回 204，不存在返回 404

## 已知问题 / Pitfalls

1. **不要用 davfs2 挂载坚果云** — 坚果云服务器不符合标准 WebDAV 规范，mount 会失败（"server does not support WebDAV"）
2. **不要用 webdavclient3** — PyPI 包对坚果云兼容差，LIST 的 check() 会因 403 失败
3. **坚果云 PROPFIND 返回的 href 包含完整路径前缀** (`/dav/obsidian/...`)，需要 strip 后匹配
4. **中文路径会被 URL 编码**（如 `/dav/obsidian/%e5%b7%a5%e4%bd%9c`），必须 unquote()
5. **递归获取文件时坚果云会把目录自身也列出来**（self 条目），不跳过会导致死循环
6. **坚果云有速率限制** — 多个快速请求可能导致超时
7. **CSDN 文章有 WAF 防护** — 需要 User-Agent + Referer header，不能用默认 UA
8. **CSDN 文章尾部常有多余的标签单词** — 代码标签、分类词等下会被当成正文段落，需要 stop_words 过滤
9. BeautifulSoup 解析 CSDN 时，代码块和行号（如 "12345" 数字行号）会被混入正文，需过滤纯数字行

## 使用示例

在 Hermes 中收到 URL 转笔记的请求时：

1. 尝试直接终端抓取（`python3 url-to-note.py <URL>`）
2. 如果页面有反爬（403 WAF），使用浏览器工具
3. 保存后自动同步到坚果云
