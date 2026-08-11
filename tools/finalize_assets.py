import json,pathlib,re,shutil,html
from PIL import Image
root=pathlib.Path(r'D:\pyproject\chemnorm'); dp=root/'data/chemnorm/products.json'; a=root/'assets/structures'; d=json.loads(dp.read_text(encoding='utf8')); used={}; generated=0; converted=0
for p in d:
 cas=re.sub(r'[^A-Za-z0-9._-]+','_',str(p.get('cas') or p.get('product_no') or 'unknown')); n=used.get(cas,0); used[cas]=n+1; target=a/(cas+(f'_{n+1}' if n else '')+'.png'); old=root/str(p.get('structure_image',''))
 valid=old.exists() and old.suffix.lower() in ('.png','.jpg','.jpeg') and old.stat().st_size>1000
 if valid:
  try:
   if old.resolve()!=target.resolve(): Image.open(old).convert('RGB').save(target,'PNG')
   p['structure_image']='assets/structures/'+target.name; converted+=1; continue
  except Exception: pass
 svg=a/(cas+(f'_{n+1}' if n else '')+'.svg'); title=html.escape(str(p.get('title') or 'Compound')); formula=html.escape(str(p.get('formula') or 'Formula unavailable')); cx=html.escape(cas)
 svg.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="520"><rect width="900" height="520" fill="#f7fbf9"/><text x="50" y="70" font-family="Arial" font-size="18" fill="#4b8f78">MOLECULAR STRUCTURE</text><text x="50" y="145" font-family="Arial" font-size="34" font-weight="bold" fill="#20342f">{title}</text><text x="50" y="205" font-family="Arial" font-size="24" fill="#4b635d">CAS {cx}</text><text x="50" y="265" font-family="Arial" font-size="22" fill="#4b635d">Formula: {formula}</text><path d="M80 390 L190 300 L310 370 L440 280 L570 360 L700 250 L820 330" stroke="#9bc7b8" stroke-width="5" fill="none"/><text x="50" y="470" font-family="Arial" font-size="14" fill="#70847e">Local structure information image</text></svg>',encoding='utf8'); p['structure_image']='assets/structures/'+svg.name; generated+=1
dp.write_text(json.dumps(d,ensure_ascii=False),encoding='utf8');
for f in a.iterdir():
 if f.suffix.lower() in ('.jpg','.jpeg'):
  try:
   cas=re.sub(r'[^A-Za-z0-9._-]+','_',f.stem); Image.open(f).convert('RGB').save(a/(cas+'.png'),'PNG'); f.unlink()
  except Exception: f.unlink()
print('mapped_png',converted,'generated_svg',generated,'jpg_remaining',len(list(a.glob('*.jpg')))+len(list(a.glob('*.jpeg'))))
