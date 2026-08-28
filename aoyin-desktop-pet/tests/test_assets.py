from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def test_model_manifest_is_local():
    p=ROOT/'app/assets/model/aoyin/aoyin.model3.json'; d=json.loads(p.read_text())
    assert d['FileReferences']['Moc']=='aoyin.moc3'
    assert d['FileReferences']['Textures']==['texture_00.png']

def test_glasses_action_exists():
    js=(ROOT/'app/app.js').read_text()
    assert 'toggleGlasses' in js
    assert 'ParamEyeLOpen' in js and 'ParamAngleZ' in js

def test_no_svg_character_fallback():
    assert '<svg' not in (ROOT/'app/index.html').read_text().lower()
