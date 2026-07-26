---
name: obsidian
description: Read, search, create notes, URL→note conversion with images, and WebDAV sync via 坚果云.
---

# Obsidian Vault

**Location:** `~/Documents/Obsidian Vault` (set in `~/.bashrc` as `OBSIDIAN_VAULT_PATH`)
**WebDAV Sync:** 坚果云 `https://dav.jianguoyun.com/dav/obsidian` (user: yizhiqiangvip@163.com)

## Quick Commands

### Read / List / Search

```bash
VAULT="$HOME/Documents/Obsidian Vault"
cat "$VAULT/Note Name.md"           # read a note
find "$VAULT" -name "*.md" -type f  # list all notes
grep -rli "keyword" "$VAULT" --include="*.md"  # search by content
```

### Create a note

```bash
VAULT="$HOME/Documents/Obsidian Vault"
cat > "$VAULT/New Note.md" << 'ENDNOTE'
# Title

Content here.
ENDNOTE
```

## URL → Obsidian Note (with images)

Use `url-to-note.py` for simple pages. For complex/dynamic sites, use browser tools:

```bash
cd ~/Documents/Obsidian\ Vault && python3 .obsidian/url-to-note.py <URL> [title]
```

### Site-specific notes

**CSDN**: Use `requests` with `Referer: https://blog.csdn.net/` header to bypass WAF. Extract from `div#article_content` or `div#content_views`. Download `<img>` tags to `_assets/<note-name>/`.

**OSChina (开源中国)**: Content is dynamically rendered. Use browser snapshot + browser_console to extract text and image URLs from `<main>` element. Image URLs are typically `https://static.oschina.net/uploads/space/...png`. Assemble manually — the generic parser won't work.

**Generic sites**: The script handles simple static pages with `article`, `main`, `.post-content` selectors.

### Image handling

- All images are downloaded to `_assets/<note-name>/` directory
- Referenced in notes via Obsidian wikilink: `![[_assets/note-name/img.png]]`
- The sync script now handles non-`.md` files (images) and auto-creates remote directories
- After note creation, run `python3 .obsidian/sync-nutstore.py sync` to push everything

## WebDAV Sync (坚果云)

Sync script: `~/Documents/Obsidian Vault/.obsidian/sync-nutstore.py`

```bash
cd ~/Documents/Obsidian\ Vault
python3 .obsidian/sync-nutstore.py sync   # bidirectional sync (sends all files: .md + .png + anything in vault)
python3 .obsidian/sync-nutstore.py down    # remote → local only
python3 .obsidian/sync-nutstore.py up      # local → remote only
python3 .obsidian/sync-nutstore.py push <file>  # push single file (auto-creates remote dirs)
```

IMPORTANT: `sync` now uploads ALL files (not just `.md`), and `push` auto-creates remote parent directories via MKCOL.

## NOTE 目录规范

NOTE 目录下的笔记按以下规则组织：

```
NOTE/
├── Java/                    ← 分类目录（按技术/主题）
│   └── idea-jboss-war-deploy.md
├── Network/
│   ├── socks5-proxy-server.md
│   └── wifi6-wifi7-router-guide.md
├── SmartHome/
│   └── smart-home-renovation.md
├── IDE/
│   └── intellij-idea-plugins.md
└── ...                       ← 按需新增
```

**规则：**
1. **文件名**：英文简短描述，全小写连字符，如 `idea-jboss-war-deploy.md`
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
3. **来源标记**：通过 `source:` + `tags:` 标记，不做来源目录
4. **_assets 文件夹**：与笔记文件同名（去掉 `.md`）：
   - `idea-jboss-war-deploy.md` → `_assets/idea-jboss-war-deploy/`
   - 笔记内引用：`![[_assets/note-name/img.png]]`
5. **改名联动**：改名时同步更新 _assets 文件夹名和笔记内所有 `![[_assets/...]]` 引用

## 笔记整理（批量操作）

当需要整理 NOTE 目录时，按此流程：

1. 列出 vault 所有 .md 和 _assets 目录，确认全貌
2. 确定分类目录（按技术/主题，不用来源维度）
3. 对每篇笔记：
   - 添加统一 frontmatter
   - 重命名文件为英文短描述
   - 重命名对应 _assets 文件夹
   - 替换笔记内所有 `![[_assets/旧路径/...]]` 为 `![[_assets/新路径/...]]`
4. 删除旧文件（原位置残留）
5. `sync-nutstore.py up` 上传到坚果云
6. 远程清理旧文件（见 obsidian-webdav-jianguoyun skill）

## File Structure

```
~/Documents/Obsidian Vault/
  ├── NOTE/                    # Organized subdirectories
  │   └── Note.md
  ├── Note 1.md
  ├── _assets/                 # Downloaded images for notes
  │   ├── note-name-1/
  │   │   ├── 01_hash.png
  │   │   └── 02_hash.png
  │   └── note-name-2/
  └── .obsidian/
      ├── sync-nutstore.py     # WebDAV sync (handles all file types)
      └── url-to-note.py       # URL → note converter (static pages only)
```

## Wikilinks

Use `[[Note Name]]` for linking, `![[_assets/.../img.png]]` for images.
