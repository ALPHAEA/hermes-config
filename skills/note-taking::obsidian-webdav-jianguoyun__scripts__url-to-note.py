#!/usr/bin/env python3
"""从 URL 抓取内容并保存为 Obsidian Markdown 笔记，然后同步到坚果云。"""
import sys, os, re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

VAULT = os.path.expanduser("~/Documents/Obsidian Vault")
SYNC = os.path.join(VAULT, ".obsidian", "sync-nutstore.py")

def sanitize(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)[:120]

def convert(url, custom_title=None):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
    r = requests.get(url, headers=headers, timeout=20)
    r.encoding = r.apparent_encoding or "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    for t in soup(["script","style","nav","footer","aside","noscript"]): t.decompose()
    title = custom_title or (soup.title.string.strip() if soup.title and soup.title.string else urlparse(url).netloc)
    fpath = os.path.join(VAULT, sanitize(title) + ".md")

    main = soup.select_one("article,main,.post-content,.article-content,.entry-content,#content,.content") or soup.body or soup
    lines = []
    for e in main.find_all(["p","h1","h2","h3","h4","h5","h6","li","pre","blockquote"]):
        t = e.get_text(strip=True)
        if not t: continue
        tag = e.name
        if tag.startswith("h") and len(tag)==2: lines.append(f"{'#'*int(tag[1])} {t}")
        elif tag == "li": lines.append(f"- {t}")
        elif tag == "pre": lines.append(f"```\n{e.get_text()}\n```")
        elif tag == "blockquote": lines.append(f"> {t}")
        else: lines.append(t)
    body = "\n\n".join(dict.fromkeys(l for l in lines if len(l)>5))

    note = f"# {title}\n\n> 来源: [{url}]({url})\n> 抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n\n{body[:50000]}"
    with open(fpath, "w", encoding="utf-8") as f: f.write(note)
    return fpath, title

if __name__ == "__main__":
    fpath, title = convert(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else None)
    print(f"✅ {os.path.basename(fpath)} ({os.path.getsize(fpath)} bytes)")
    if os.path.exists(SYNC):
        import subprocess
        subprocess.run(["python3", SYNC, "push", fpath]).check_return()
        print("☁️  Synced to 坚果云")
