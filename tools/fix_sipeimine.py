import json,pathlib
root=pathlib.Path(r'D:\pyproject\chemnorm');p=root/'data/chemnorm/products.json';d=json.loads(p.read_text(encoding='utf8'));[x.update(structure_image='assets/structures/61825-98-7.png') for x in d if x.get('cas')=='61825-98-7'];p.write_text(json.dumps(d,ensure_ascii=False),encoding='utf8');(root/'assets/structures/61825-98-7.svg').unlink(missing_ok=True);print('fixed')
