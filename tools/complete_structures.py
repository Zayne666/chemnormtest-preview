import json, pathlib, urllib.request, urllib.parse, time
root=pathlib.Path(__file__).resolve().parents[1]
path=root/'data'/'chemnorm'/'products.json'
out=root/'assets'/'structures'; out.mkdir(parents=True,exist_ok=True)
data=json.loads(path.read_text(encoding='utf-8'))
ok=fail=0; failures=[]
for p in data:
    url=p.get('structure_image','')
    if not url.startswith(('http://','https://')): continue
    cas=str(p.get('cas') or '').strip(); product=str(p.get('product_no') or cas or 'compound').strip()
    dest=out/(product.replace('/','_')+'.png')
    candidates=[]
    for query in [cas, p.get('title','')]:
        if query: candidates.append('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'+urllib.parse.quote(str(query),safe='')+'/PNG?image_size=large')
    if cas: candidates.append('https://cactus.nci.nih.gov/chemical/structure/'+urllib.parse.quote(cas,safe='')+'/image')
    for candidate in candidates:
        try:
            req=urllib.request.Request(candidate,headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=30) as r: content=r.read()
            if len(content)>200 and content[:8]==b'\x89PNG\r\n\x1a\n':
                dest.write_bytes(content); p['structure_image']='assets/structures/'+dest.name; ok+=1; break
        except Exception: pass
    else: fail+=1; failures.append({'product_no':product,'cas':cas,'title':p.get('title'),'url':url})
    time.sleep(.08)
path.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
(root/'tools'/'structure_failures.json').write_text(json.dumps(failures,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'pubchem_downloaded={ok} remaining={fail}')
