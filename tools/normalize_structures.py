import json, pathlib, re, shutil
from PIL import Image
root=pathlib.Path(r'D:\pyproject\chemnorm'); dp=root/'data/chemnorm/products.json'; assets=root/'assets/structures'; d=json.loads(dp.read_text(encoding='utf-8-sig')); report=[]; used={}
for p in d:
    cas=re.sub(r'[^A-Za-z0-9._-]+','_',str(p.get('cas') or p.get('product_no') or 'unknown')); old=root/str(p.get('structure_image',''))
    if not old.exists(): report.append({'type':'missing','title':p.get('title'),'cas':p.get('cas'),'old':str(old)}); continue
    n=used.get(cas,0); used[cas]=n+1; name=cas+(f'_{n+1}' if n else '')+'.png'; new=assets/name
    try:
        if old.suffix.lower()!='.png': Image.open(old).convert('RGB').save(new,'PNG')
        elif old.resolve()!=new.resolve(): shutil.copy2(old,new)
        p['structure_image']='assets/structures/'+name
    except Exception as e: report.append({'type':'convert_failed','title':p.get('title'),'cas':p.get('cas'),'error':str(e)})
dp.write_text(json.dumps(d,ensure_ascii=False),encoding='utf-8'); (root/'tools/normalize_report.json').write_text(json.dumps({'records':len(d),'issues':len(report),'items':report},ensure_ascii=False,indent=2),encoding='utf-8'); print('records',len(d),'issues',len(report),'pngs',len(list(assets.glob('*.png'))))
