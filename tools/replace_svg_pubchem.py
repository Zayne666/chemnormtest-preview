import json,pathlib,urllib.request,urllib.parse,time
root=pathlib.Path(r'D:\pyproject\chemnorm');p=root/'data/chemnorm/products.json';a=root/'assets/structures';d=json.loads(p.read_text(encoding='utf8'));ok=fail=0;failed=[]
for x in d:
 f=root/str(x.get('structure_image',''))
 if f.suffix.lower()!='.svg': continue
 cas=str(x.get('cas') or '').strip();
 if not cas: fail+=1;failed.append(x.get('title'));continue
 try:
  u='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'+urllib.parse.quote(cas,safe='')+'/PNG?image_size=large'; req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}); b=urllib.request.urlopen(req,timeout=30).read(); out=a/(cas+'.png'); out.write_bytes(b); x['structure_image']='assets/structures/'+out.name; f.unlink(missing_ok=True); ok+=1
 except Exception: fail+=1;failed.append({'title':x.get('title'),'cas':cas})
 time.sleep(.1)
p.write_text(json.dumps(d,ensure_ascii=False),encoding='utf8');(root/'tools/svg_replace_failures.json').write_text(json.dumps(failed,ensure_ascii=False,indent=2),encoding='utf8');print('replaced',ok,'failed',fail)
