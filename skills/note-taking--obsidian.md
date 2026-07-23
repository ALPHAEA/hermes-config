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
