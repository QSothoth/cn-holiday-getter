#!/usr/bin/env python3
"""Fetch the Live2D sample rig and browser runtimes, then build local fan assets."""
from __future__ import annotations
import hashlib, json, shutil, subprocess, sys, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/'app/assets/model/aoyin'; RUNTIME=ROOT/'app/assets/runtime'
MODEL.mkdir(parents=True,exist_ok=True); (MODEL/'motion').mkdir(exist_ok=True); RUNTIME.mkdir(parents=True,exist_ok=True)
BASE='https://raw.githubusercontent.com/huangcheng/Seelie/main/assets/packs/haruto/model/'
FILES={
 'haruto.moc3':'aoyin.moc3', 'haruto.physics3.json':'aoyin.physics3.json',
 'haruto.cdi3.json':'aoyin.cdi3.json', 'haruto.model3.json':'_upstream.model3.json',
 'haruto.2048/texture_00.png':'_upstream-texture.png'
}
MOTIONS=['haruto_idle_01.motion3.json','haruto_idle_02.motion3.json','haruto_idle_03.motion3.json','haruto_m01.motion3.json','haruto_m02.motion3.json','haruto_m03.motion3.json','haruto_m04.motion3.json','haruto_m05.motion3.json','haruto_m06.motion3.json']
RUNTIMES={
 'https://cdn.jsdelivr.net/npm/pixi.js@6.5.10/dist/browser/pixi.min.js':'pixi.min.js',
 'https://cdn.jsdelivr.net/npm/pixi-live2d-display@0.4.0/dist/cubism4.min.js':'cubism4.min.js',
 'https://cubism.live2d.com/sdk-web/cubismcore/live2dcubismcore.min.js':'live2dcubismcore.min.js'
}

def get(url,path):
    if path.exists() and path.stat().st_size>100: print('keep',path.relative_to(ROOT)); return
    print('fetch',url)
    req=urllib.request.Request(url,headers={'User-Agent':'aoyin-live2d-bootstrap/0.2'})
    with urllib.request.urlopen(req,timeout=60) as r, path.open('wb') as f: shutil.copyfileobj(r,f)
    if path.stat().st_size<100: raise RuntimeError(f'download too small: {url}')

for src,dst in FILES.items(): get(BASE+src,MODEL/dst)
for name in MOTIONS: get(BASE+'motion/'+name,MODEL/'motion'/name)
for url,name in RUNTIMES.items(): get(url,RUNTIME/name)

d=json.loads((MODEL/'_upstream.model3.json').read_text()); fr=d['FileReferences']
fr['Moc']='aoyin.moc3'; fr['Textures']=['texture_00.png']; fr['Physics']='aoyin.physics3.json'; fr['DisplayInfo']='aoyin.cdi3.json'
for _,items in fr.get('Motions',{}).items():
    for item in items: item['File']='motion/'+Path(item['File']).name
(MODEL/'aoyin.model3.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
for script in ('make_aoyin_texture.py','make_overlays.py','make_icons.py'):
    subprocess.run([sys.executable,str(ROOT/'scripts'/script)],check=True)
rows=[]
for p in sorted((ROOT/'app/assets').rglob('*')):
    if p.is_file(): rows.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT)}")
(ROOT/'ASSET_SHA256SUMS.txt').write_text('\n'.join(rows)+'\n')
print('assets ready')
