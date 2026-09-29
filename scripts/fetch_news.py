#!/usr/bin/env python3
"""Fetch short publisher RSS summaries and write data/news.json. Standard library only."""
import json, re, time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "news.json"
FEEDS = [
    ("World", "BBC News", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("India", "BBC News: India", "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml"),
    ("India", "The Indian Express", "https://indianexpress.com/section/india/feed/"),
    ("Technology", "BBC News", "https://feeds.bbci.co.uk/news/technology/rss.xml"),
    ("Technology", "The Indian Express", "https://indianexpress.com/section/technology/feed/"),
    ("Science", "BBC News", "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"),
    ("Science", "The Indian Express", "https://indianexpress.com/section/technology/science/feed/"),
    ("Business", "BBC News", "https://feeds.bbci.co.uk/news/business/rss.xml"),
    ("Business", "The Indian Express", "https://indianexpress.com/section/business/feed/"),
]

class TextOnly(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self, data): self.parts.append(data)

def clean(value):
    p=TextOnly()
    try: p.feed(value or "")
    except Exception: pass
    return re.sub(r"\s+", " ", " ".join(p.parts)).strip()[:420]

def parse_date(value):
    if not value: return ""
    try:
        dt=parsedate_to_datetime(value)
        if dt.tzinfo is None: dt=dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat(timespec="minutes")
    except Exception: return ""

def local_name(tag): return tag.rsplit('}',1)[-1].lower()

def child_text(node, name):
    for c in list(node):
        if local_name(c.tag)==name.lower(): return ''.join(c.itertext()).strip()
    return ""

def parse_feed(raw, category, source):
    import xml.etree.ElementTree as ET
    root=ET.fromstring(raw)
    entries=[]
    # RSS 2.0 channel/item and Atom feed/entry
    for node in root.iter():
        if local_name(node.tag) not in ('item','entry'): continue
        title=child_text(node,'title')
        desc=child_text(node,'description') or child_text(node,'summary') or child_text(node,'content')
        link=child_text(node,'link')
        if not link:
            for c in list(node):
                if local_name(c.tag)=='link':
                    link=c.attrib.get('href','');
                    if c.attrib.get('rel','alternate')=='alternate': break
        pub=child_text(node,'pubdate') or child_text(node,'published') or child_text(node,'updated')
        if title and link.startswith(('https://','http://')):
            entries.append({'category':category,'source':source,'title':clean(title),'description':clean(desc),'link':link,'published':parse_date(pub)})
    return entries

def main():
    all_items=[]; errors=[]
    for category, source, url in FEEDS:
        try:
            req=Request(url,headers={'User-Agent':'DailyWorldBriefing/1.0 (RSS reader; contact: site maintainer)'})
            with urlopen(req,timeout=20) as resp: raw=resp.read(2_500_000)
            all_items.extend(parse_feed(raw,category,source))
            print(f"OK {category}: {source}")
        except Exception as exc:
            errors.append(f"{source} ({category}): {exc}")
            print(f"WARN {category}: {source}: {exc}")
        time.sleep(0.15)
    # Keep one copy per canonical link, sort newest first (unknown dates last), max 100.
    unique={}
    for item in all_items:
        key=item['link'].split('#')[0].rstrip('/')
        if key not in unique: unique[key]=item
    items=list(unique.values())
    items.sort(key=lambda x:x['published'] or '',reverse=True)
    payload={'updated_at':datetime.now(timezone.utc).isoformat(timespec='seconds'),'items':items[:100],'feeds_with_errors':errors}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"Wrote {len(payload['items'])} stories to {OUT}")
    if not items: raise SystemExit('No RSS items collected; leaving workflow failed so the problem is visible.')

if __name__=='__main__': main()
