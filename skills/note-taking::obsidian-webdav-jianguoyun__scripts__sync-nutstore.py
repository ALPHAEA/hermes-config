#!/usr/bin/env python3
"""Obsidian vault ↔ 坚果云 WebDAV 双向同步"""
import os, sys, xml.etree.ElementTree as ET
from pathlib import Path
from email.utils import parsedate_to_datetime
from requests import request, auth as http_auth
from urllib.parse import unquote

VAULT = os.path.expanduser("~/Documents/Obsidian Vault")
BASE_URL = "https://dav.jianguoyun.com/dav/obsidian"
AUTH = http_auth.HTTPBasicAuth("your_email@example.com", "your_app_password")
NS = {"d": "DAV:"}

def dav(method, path, **kw):
    url = BASE_URL.rstrip("/") + "/" + path.lstrip("/")
    return request(method, url, auth=AUTH, timeout=15, **kw)

def parse_mtime(s):
    try:
        return parsedate_to_datetime(s).timestamp()
    except:
        return 0

def list_all_md(remote_path="/"):
    results = []; queue = [remote_path]; visited = set()
    prop_xml = b'<?xml version="1.0"?><d:propfind xmlns:d="DAV:"><d:prop><d:displayname/><d:getlastmodified/><d:resourcetype/><d:getcontenttype/></d:prop></d:propfind>'
    while queue:
        cur = queue.pop(0); cur = cur.replace("//", "/")
        if cur != "/": cur = cur.rstrip("/") + "/"
        if cur in visited: continue
        visited.add(cur)
        r = dav("PROPFIND", cur, data=prop_xml, headers={"Depth": "1"})
        if r.status_code != 207: continue
        root = ET.fromstring(r.content)
        for resp in root.findall("d:response", NS):
            href = resp.find("d:href", NS).text; rel = href
            for pfx in ["/dav/obsidian", "/dav"]:
                if rel.startswith(pfx): rel = rel[len(pfx):]; break
            rel = unquote(rel).rstrip("/")
            if not rel or rel == cur.strip("/"): continue
            props = resp.find("d:propstat/d:prop", NS)
            is_coll = props.find("d:resourcetype/d:collection", NS) is not None
            if is_coll: queue.append(rel + "/")
            elif rel.endswith(".md"):
                results.append({"path": rel, "modified": props.findtext("d:getlastmodified", "")})
    return results

def sync_down():
    files = list_all_md("/")
    for f in files:
        rel, local = f["path"], os.path.join(VAULT, f["path"])
        if os.path.getmtime(local) if os.path.exists(local) else 0 >= parse_mtime(f["modified"]): continue
        os.makedirs(os.path.dirname(local), exist_ok=True)
        r = dav("GET", "/" + rel)
        with open(local, "wb") as fh: fh.write(r.content)
        print(f"  ↓  {rel}")
    return files

def sync_up(remote_cache=None):
    rm = {}
    if isinstance(remote_cache, list):
        for f in remote_cache: rm[f["path"]] = f["modified"]
    else:
        for f in list_all_md("/"): rm[f["path"]] = f["modified"]
    for fpath in Path(VAULT).rglob("*.md"):
        rel = str(fpath.relative_to(VAULT)); lm = os.path.getmtime(fpath)
        if rel in rm and lm <= parse_mtime(rm[rel]): continue
        parent = "/" + "/".join(rel.split("/")[:-1]) if "/" in rel else ""
        if parent:
            try: dav("MKCOL", parent + "/")
            except: pass
        with open(fpath, "rb") as fh: dav("PUT", "/" + rel, data=fh.read())
        print(f"  ↑  {rel}")

if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "sync"
    if c == "sync": print("=== ↓ 坚果云 → 本地 ==="); r = sync_down(); print("=== ↑ 本地 → 坚果云 ==="); sync_up(r); print("=== ✓ 同步完成 ===")
    elif c == "down": sync_down()
    elif c == "up": sync_up()
    elif c == "push":
        rel = os.path.relpath(sys.argv[2], VAULT)
        with open(sys.argv[2], "rb") as fh: dav("PUT", "/" + rel, data=fh.read())
        print(f"PUSHED /{rel}")
    else: print("Usage: sync-nutstore.py [sync|down|up|push <file>]")
