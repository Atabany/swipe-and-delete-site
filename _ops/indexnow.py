#!/usr/bin/env python3
"""Submit changed public URLs. A 200/202 response does not prove indexing."""
import json,ssl,sys,urllib.request,urllib.parse
from pathlib import Path
root=Path(__file__).resolve().parent.parent
c=json.loads((root/'_ops/config.json').read_text());base=c['base'];host=urllib.parse.urlsplit(base).netloc
urls=sys.argv[1:]
if not urls:raise SystemExit('Provide the exact changed public URLs.')
if any(not u.startswith(base) for u in urls):raise SystemExit('Every URL must belong to the configured site.')
body={'host':host,'key':c['indexNowKey'],'keyLocation':base+c['indexNowKey']+'.txt','urlList':urls}
req=urllib.request.Request('https://api.indexnow.org/indexnow',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'},method='POST')
with urllib.request.urlopen(req,context=ssl.create_default_context(cafile='/etc/ssl/cert.pem'),timeout=30) as response:print('IndexNow HTTP',response.status)
