import json, pathlib, hashlib, concurrent.futures, urllib.request
root=pathlib.Path(__file__).resolve().parents[1]
data_path=root/'data'/'chemnorm'/'products.json'
out=root/'assets'/'structures'; out.mkdir(parents=True,exist_ok=True)
data=json.loads(data_path.read_text(encoding='utf-8'))
def job(item):
    i,p=item; u=p.get('structure_image','')
    if not u.startswith(('http://','https://')): return i,u,False
    ext=pathlib.Path(u.split('?')[0]).suffix.lower()
    if ext not in ('.png','.jpg','.jpeg','.webp'): ext='.png'
    name=(p.get('product_no') or p.get('cas') or hashlib.sha1(u.encode()).hexdigest()[:12])+ext
    dest=out/name
    try:
        if not dest.exists():
            for attempt in range(3):
                try:
                    req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0','Referer':'https://www.chemnorm.com/'})
                    with urllib.request.urlopen(req, timeout=25) as r:
                        dest.write_bytes(r.read())
                    break
                except Exception:
                    if attempt==2:
                        raise
        return i,'assets/structures/'+name,True
    except Exception: return i,u,False
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    results=list(ex.map(job,enumerate(data)))
ok=fail=0
for i,new,success in results:
    if success: data[i]['structure_image']=new; ok+=1
    else: fail+=1
data_path.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
print(f'downloaded={ok} failed_or_existing_external={fail} files={len(list(out.iterdir()))}')

