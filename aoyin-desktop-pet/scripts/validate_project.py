#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]; checks=[]
def ok(cond,msg): checks.append((bool(cond),msg))
model=ROOT/'app/assets/model/aoyin/aoyin.model3.json'; ok(model.exists(),'model3 manifest exists')
if model.exists():
 d=json.loads(model.read_text()); fr=d['FileReferences']; ok((model.parent/fr['Moc']).exists(),'moc3 exists'); ok(all((model.parent/t).exists() for t in fr['Textures']),'texture exists'); ok(len(fr.get('Motions',{}))>=2,'motion groups exist')
ok((ROOT/'app/assets/runtime/cubism4.min.js').exists(),'Cubism renderer exists')
ok((ROOT/'app/assets/runtime/live2dcubismcore.min.js').exists(),'Live2D Cubism Core exists')
js=(ROOT/'app/app.js').read_text(); ok('toggleGlasses' in js and 'ParamEyeLOpen' in js,'remove-glasses action drives Live2D parameters'); ok('svg' not in js.lower(),'no SVG character fallback')
conf=json.loads((ROOT/'src-tauri/tauri.conf.json').read_text()); win=conf['app']['windows'][0]
ok(win['transparent'] and win['alwaysOnTop'] and not win['decorations'],'transparent always-on-top frameless window')
ok((ROOT.parent/'.github/workflows/aoyin-live2d-build.yml').exists() or (ROOT/'.github/workflows/release.yml').exists(),'cross-platform build workflow exists')
for passed,msg in checks: print(('PASS' if passed else 'FAIL'),msg)
if not all(p for p,_ in checks): sys.exit(1)
