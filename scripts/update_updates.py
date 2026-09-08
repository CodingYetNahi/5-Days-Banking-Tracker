import json, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

DATA = Path("docs/updates.json")
QUERY = '"5 day banking" (IBA OR UFBU OR DFS OR bank strike) India'
url = "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": QUERY, "hl": "en-IN", "gl": "IN", "ceid": "IN:en"})
request = urllib.request.Request(url, headers={"User-Agent": "5-Day-Banking-Tracker/1.0"})
existing = json.loads(DATA.read_text(encoding="utf-8"))
known = {item["title"].casefold() for item in existing.get("items", [])}
fresh = []
with urllib.request.urlopen(request, timeout=30) as response:
    root = ET.fromstring(response.read())
for node in root.findall("./channel/item"):
    title = (node.findtext("title") or "").strip()
    link = (node.findtext("link") or "").strip()
    source = (node.findtext("source") or "Public news report").strip()
    if not title or not link or title.casefold() in known:
        continue
    lower = title.casefold()
    if "five day" not in lower and "5 day" not in lower and "5-day" not in lower:
        continue
    try: date = parsedate_to_datetime(node.findtext("pubDate") or "").date().isoformat()
    except Exception: date = datetime.now(timezone.utc).date().isoformat()
    fresh.append({"date":date,"type":"Automated news discovery","title":title,"summary":"Automatically collected public report about five-day banking. Open the source for full context; this entry does not confirm implementation.","source":source,"url":link})
payload={"updatedAt":datetime.now(timezone.utc).isoformat(),"items":(fresh+existing.get("items",[]))[:60]}
DATA.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"Added {len(fresh)} new update(s)")
