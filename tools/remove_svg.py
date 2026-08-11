import json,pathlib
root=pathlib.Path(r'D:\pyproject\chemnorm');p=root/'data/chemnorm/products.json';d=json.loads(p.read_text(encoding='utf8'));n=0
for x in d:
 if str(x.get('structure_image','')).lower().endswith('.svg'): x['structure_image']='';n+=1
p.write_text(json.dumps(d,ensure_ascii=False),encoding='utf8')
for f in (root/'assets/structures').glob('*.svg'): f.unlink()
print('cleared',n)
