import json, pathlib, re, hashlib
root=pathlib.Path(r'D:\pyproject\chemnorm'); dp=root/'data/chemnorm/products.json'; assets=root/'assets/structures'; d=json.loads(dp.read_text(encoding='utf-8-sig'))
issues=[]; fixed=0
for i,p in enumerate(d):
    cas=str(p.get('cas') or '').strip(); u=str(p.get('structure_image') or '')
    if not cas: issues.append({'index':i,'type':'missing_cas','title':p.get('title')})
    if 'noimage' in u.lower() or u.startswith(('http://','https://')): issues.append({'index':i,'type':'external_or_noimage','title':p.get('title'),'cas':cas,'url':u})
    if u.startswith('assets/structures/'):
        f=assets/pathlib.Path(u).name
        if not f.exists(): issues.append({'index':i,'type':'missing_local_file','title':p.get('title'),'cas':cas,'file':u})
        elif f.stat().st_size<100: issues.append({'index':i,'type':'tiny_file','title':p.get('title'),'cas':cas,'file':u})
        if cas and not f.stem.startswith(re.sub(r'[^A-Za-z0-9._-]+','_',cas)): issues.append({'index':i,'type':'filename_not_cas','title':p.get('title'),'cas':cas,'file':u})
    if not p.get('product_no'): issues.append({'index':i,'type':'missing_product_id','title':p.get('title'),'cas':cas})
    if not p.get('smiles'): issues.append({'index':i,'type':'missing_smiles','title':p.get('title'),'cas':cas})
(root/'tools/product_audit_report.json').write_text(json.dumps({'records':len(d),'issues':len(issues),'issue_types':{k:sum(1 for x in issues if x['type']==k) for k in sorted(set(x['type'] for x in issues))},'items':issues},ensure_ascii=False,indent=2),encoding='utf-8')
print('records',len(d),'issues',len(issues)); print({k:sum(1 for x in issues if x['type']==k) for k in sorted(set(x['type'] for x in issues))})
