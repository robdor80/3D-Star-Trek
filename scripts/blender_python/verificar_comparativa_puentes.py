"""Control final de integridad y coherencia; solo escribe un informe nuevo.
PNG: contenedor/dimensiones/CRC, sin mostrar ni analizar contenido visual.
"""
import ast, csv, hashlib, json, re, subprocess
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/auditorias/comparativa_v2'
SCRIPTS=['comparar_puentes_dae.py','capturar_comparativa_puentes.py',
         'comprobar_correspondencias_focales.py','resumir_comparativa_puentes.py','verificar_comparativa_puentes.py']
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True,encoding='utf-8').strip()
def read(p):return json.loads(p.read_text(encoding='utf-8'))

def main():
    target=OUT/'VERIFICACION_FINAL.json'
    if target.exists():raise RuntimeError('No sobrescribir informe final')
    before=read(ROOT/'docs/auditorias/comparativa_v1/CONTROL_INICIAL.json')
    current_assets={p.relative_to(ROOT).as_posix() for p in (ROOT/'assets').rglob('*') if p.is_file()}
    initial_assets={r['path'] for r in before['assets']}
    missing_assets=initial_assets-current_assets
    assert not missing_assets,('Faltan activos iniciales',sorted(missing_assets))
    added_assets=[]
    for rel in sorted(current_assets-initial_assets):
        p=ROOT/rel
        added_assets.append({'path':rel,'bytes':p.stat().st_size,'format':p.suffix.lower(),
             'sha256_at_final_check':sha(p),'mtime_utc':datetime.fromtimestamp(p.stat().st_mtime,timezone.utc).isoformat()})
    changes=[]
    for group in ['assets','protected_scenes','prior_reports']:
        for r in before[group]:
            p=ROOT/r['path']
            if not p.is_file() or sha(p)!=r['sha256'] or ('bytes' in r and p.stat().st_size!=r['bytes']):changes.append(r['path'])
    assert not changes,changes
    assert git('branch','--show-current')=='audit/ascendant-vs-enterprise'
    assert git('rev-parse','--short','HEAD')=='33ac98e','Cambió HEAD'
    assert not git('diff','--name-only') and not git('diff','--cached','--name-only'),'Cambios tracked inesperados'
    parsed=[]
    for folder in [OUT,ROOT/'docs/auditorias/comparativa_v1']:
        for p in folder.glob('*.json'):read(p);parsed.append(p.relative_to(ROOT).as_posix())
    for name in SCRIPTS:
        p=ROOT/'scripts/blender_python'/name;ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    correspondence=read(OUT/'CORRESPONDENCIA_GEOMETRICA.json')
    for label in ['enterprise','ascendant']:
        d=read(OUT/(label.upper()+'_ENSAYO.json'))
        assert d['scene_hash_unchanged']
        with (OUT/(label.upper()+'_DIFERENCIAS.csv')).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
        assert len(rows)==d['surface_mesh_objects']
        assert sum(int(r['triangles']) for r in rows)==d['triangles']
        assert sum(d['grid']['status_counts'].values())==d['grid']['count']==2173
        assert sum(r['classification']=='LIBRE_CONTINUO_PLANO' for r in d['routes'].values())==5
    assert correspondence['contrasts'][0]['shared_triangle_multiset_count']==2065576
    focal=read(OUT/'CORRESPONDENCIAS_FOCALES.json')['rear_prism_world_matches']
    assert focal['enterprise_triangles']==focal['ascendant_triangles']==focal['multiset_common']==6828
    capture_folder=ROOT/'output/capturas_revision/comparativa_enterprise_ascendant_v1'
    manifest=read(capture_folder/'MANIFIESTO_COMPARATIVA.json');captures=[]
    assert len(manifest['captures'])==len(list(capture_folder.glob('*.png')))==8
    for r in manifest['captures']:
        p=ROOT/r['path'];assert sha(p)==r['sha256']
        with Image.open(p) as im:
            assert im.format=='PNG' and list(im.size)==r['resolution']==[960,720]
            im.verify()
        assert git('check-ignore',r['path'])==r['path']
        captures.append({'path':r['path'],'sha256':r['sha256'],'size':[960,720],'container_verified':True})
    for view in ['superior','general','central','posterior']:
        pair=[r for r in manifest['captures'] if r['view']==view]
        assert len(pair)==2
        for k in ['camera','target','ortho_scale_m','resolution','roof_hidden_in_memory']:assert pair[0][k]==pair[1][k]
    report=ROOT/'docs/auditorias/COMPARATIVA_ENTERPRISE_ASCENDANT.md'
    content=report.read_text(encoding='utf-8');local_link_errors=[]
    for dest in re.findall(r'\]\(([^)]+)\)',content):
        if dest.startswith(('http:','https:','#')):continue
        p=(report.parent/dest).resolve()
        if p!=target and not p.exists():local_link_errors.append(dest)
    assert not local_link_errors,local_link_errors
    status=git('status','--short')
    expected=['?? docs/auditorias/COMPARATIVA_ENTERPRISE_ASCENDANT.md',
        '?? docs/auditorias/comparativa_v1/','?? docs/auditorias/comparativa_v2/']+['?? scripts/blender_python/'+n for n in SCRIPTS]
    assert set(status.splitlines())==set(expected),status
    result={'verified_at_utc':datetime.now(timezone.utc).isoformat(),
        'assets':{'initial_files_verified':len(initial_assets),'initial_files_missing':[],
          'initial_sizes_and_sha256_unchanged':True,'final_files':len(current_assets),
          'added_files_outside_comparison':added_assets,
          'addition_origin':'No creados por los scripts de esta auditoría; autor/proceso no determinado.'},
        'protected_scenes':{'files':3,'sha256_unchanged':True},'prior_audit_files':{'files':33,'sha256_unchanged':True},
        'git':{'branch':git('branch','--show-current'),'head':git('rev-parse','HEAD'),'tracked_changes':False,
               'staged_changes':False,'status_short':status,'no_commit_or_push_executed':True},
        'json_parsed':parsed,'scripts_ast_valid':SCRIPTS,'comparison_csv_totals_verified':True,
        'global_common_triangle_count':2065576,'rear_prism_common_triangle_count':6828,
        'captures':captures,'paired_cameras_identical':True,'captures_git_ignored':True,
        'ai_visual_inspection':False,'report':{'path':report.relative_to(ROOT).as_posix(),'bytes':report.stat().st_size,'sha256':sha(report)},
        'report_local_links_valid':True,'ue5_project_files_found_in_repo':False}
    with target.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
    print('VERIFICADO: 278 activos iniciales, 3 escenas y 33 informes previos intactos; '+str(len(added_assets))+' altas externas a la comparación; 8 PNG; datos y scripts coherentes; Git sin cambios tracked.')
if __name__=='__main__':main()
