#!/usr/bin/env python3
"""Refresh public listing data without altering verified code claims or real reviews."""
import json,ssl,urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
p=Path(__file__).resolve().parent/'facts.json';old=json.loads(p.read_text())
with urllib.request.urlopen('https://itunes.apple.com/lookup?id=6754815949&country=us',context=ssl.create_default_context(cafile='/etc/ssl/cert.pem'),timeout=30) as response:new=json.load(response)['results'][0]
if new['bundleId']!='com.atabany.Clarity':raise SystemExit('Unexpected app identity; stop and inspect.')
if new['trackName']!=old['trackName']:raise SystemExit('The public name changed; review copy and URLs before refreshing.')
for k in old:
 if k in new:old[k]=new[k]
old['checkedDate']=datetime.now(ZoneInfo('Asia/Dubai')).date().isoformat()
p.write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n')
print('Updated verified public listing data; render and validate before publishing.')
