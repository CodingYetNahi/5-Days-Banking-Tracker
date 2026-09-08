import json, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
q=urllib.parse.quote('"5 day banking" IBA DFS India')
url='https://news.google.com/rss/search?q='+q+'&hl=en-IN&gl=IN&ceid=IN:en'
try:
    root=ET.fromstring(urllib.request.urlopen(url,timeout=20).read())
    items=[]
    for x in root.findall('./channel/item')[:12]:
        title=x.findtext('title','').strip(); link=x.findtext('link','').strip()
        source=x.findtext('source','News').strip()
        pub=x.findtext('pubDate','')
        try: date=parsedate_to_datetime(pub).date().isoformat()
        except: date=''
        if title and link: items.append({'date':date,'type':'Automatic news discovery','title':title,'summary':'Automatically collected public news result. Verify with the linked source; this does not confirm implementation.','source':source,'url':link})
    if items:
        with open('docs/updates.json','w') as f: json.dump(items,f,ensure_ascii=False,indent=2)
except Exception as e: print('News refresh skipped:',e)
