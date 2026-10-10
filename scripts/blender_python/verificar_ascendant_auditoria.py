"""Verifica integridad local y salidas de auditoría; no modifica fuentes.
Ejecutar con Python y Pillow existentes. Rechaza sobrescribir su informe.
"""
import argparse,ast,hashlib,json,subprocess
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--salida',type=Path,default=ROOT/'docs/auditorias/ascendant_bpy_v1/VERIFICACION_FINAL.json');args=parser.parse_args()
    target=args.salida.resolve()
    if target.exists() or (ROOT/'assets').resolve() in target.parents:raise RuntimeError('Salida nueva fuera de assets requerida')
    src=json.loads((ROOT/'docs/auditorias/ascendant_fuentes_v1/FUENTES_ASCENDANT.json').read_text(encoding='utf-8'))
    base=ROOT/'docs/auditorias/ascendant_bpy_v1';contrast=json.loads((base/'CONTRASTE_FORMATOS_ASCENDANT.json').read_text());model=ROOT/src['root']
    actual={p.relative_to(model).as_posix() for p in model.rglob('*') if p.is_file()};expected={f['path'] for f in src['files']};assert actual==expected
    assets=[]
    for f in src['files']:
        p=model/f['path'];ok=sha(p)==f['sha256'] and p.stat().st_size==f['bytes'];assert ok
        assets.append({'path':f['path'],'sha256_unchanged':ok})
    assert sorted(p.relative_to(model).as_posix() for p in model.rglob('*') if p.is_dir())==sorted(src['directories'])
    protected=[]
    for f in src['protected_scenes_hashes_only_no_geometry_read']:
        ok=sha(ROOT/f['path'])==f['sha256'];assert ok;protected.append({'path':f['path'],'sha256_unchanged':ok,'sha256':f['sha256']})
    scenes=[]
    for fmt,f in contrast['scenes'].items():
        p=ROOT/f['path'];ok=sha(p)==f['sha256'];assert ok
        scenes.append({'format':fmt,'path':f['path'],'bytes':p.stat().st_size,'sha256':f['sha256'],'unchanged_after_diagnostics':ok})
    captures=[];folder=ROOT/'output/capturas_revision/ascendant_v1';manifest=json.loads((folder/'MANIFIESTO_CAPTURAS.json').read_text(encoding='utf-8'))
    for f in manifest['captures']:
        p=ROOT/f['path'];assert sha(p)==f['sha256']
        with Image.open(p) as img:assert img.size==(960,720);img.verify()
        captures.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'header_resolution':[960,720],
                         'sha256':f['sha256'],'valid_png':True,'no_ai_visual_review':True})
    assert len(captures)==8;assert manifest['scene_sha256_before']==manifest['scene_sha256_after']
    metadata_noai=[]
    for f in src['files']:
        if 'image' not in f:continue
        with Image.open(model/f['path']) as img:
            text=(str(img.info)+str(dict(img.getexif()))).lower()
            if 'noai' in text or 'no ai' in text:metadata_noai.append(f['path'])
    assert not metadata_noai
    scripts=[]
    for p in sorted((ROOT/'scripts/blender_python').glob('*ascendant*.py')):
        ast.parse(p.read_text(encoding='utf-8'));scripts.append({'path':p.relative_to(ROOT).as_posix(),'syntax_ok':True,'sha256':sha(p)})
    for p in base.glob('*.json'):json.loads(p.read_text(encoding='utf-8'))
    def git(*args):return subprocess.check_output(['git',*args],text=True,cwd=ROOT)
    branch=git('branch','--show-current').strip();assert branch=='audit/ascendant-vs-enterprise'
    status=git('status','--porcelain').splitlines();assert all(x.startswith('?? ') for x in status)
    paths=[src['root']+'/uss_ascendant_bridge.glb']+[x['path'] for x in scenes]+[x['path'] for x in captures]
    ignored=git('check-ignore','--',*paths).splitlines();assert set(ignored)==set(paths)
    report=ROOT/'docs/auditorias/AUDITORIA_ASCENDANT_LOCAL.md';assert report.is_file()
    summary={'date':'2026-10-10','branch':branch,'head':git('rev-parse','HEAD').strip(),
        'source_file_count':len(actual),'source_total_bytes':src['total_bytes'],'source_file_set_unchanged':True,
        'source_directory_set_unchanged':True,'source_files_sha256':assets,'protected_scenes_hashes_only_no_geometry_read':protected,
        'analysis_scenes':scenes,'captures':captures,'external_image_text_metadata_noai_matches':metadata_noai,
        'scripts':scripts,'json_reports_parse_ok':True,'report':{'path':report.relative_to(ROOT).as_posix(),'bytes':report.stat().st_size,'sha256':sha(report)},
        'git_status':status,'tracked_changes':False,'commit_performed':False,'push_performed':False,
        'assets_and_analysis_binary_paths_ignored':True,'third_party_content_sent_to_external_services':False,
        'ai_visual_review':False,'other_bridges_geometry_comparison':False}
    target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:summary[k] for k in ['branch','source_file_count','source_total_bytes','source_file_set_unchanged','tracked_changes']},ensure_ascii=False))
    print('Escenas locales',[(x['format'],x['bytes']) for x in scenes]);print('Capturas PNG válidas',len(captures));print('Informe',report.stat().st_size,'bytes')
if __name__=='__main__':main()
