"""Focused regression tests on disposable copies. Never changes delivered inputs."""
from pathlib import Path
import ast,json,sys,zipfile,xml.etree.ElementTree as ET,subprocess,math
import openpyxl

WORK=Path(sys.argv[2]).resolve()
PACKAGE=Path(sys.argv[1]).resolve().parent
WORK.mkdir(parents=True,exist_ok=True)
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'};N='{'+ns['s']+'}'
def copy_changes(src,dst,changes):
 with zipfile.ZipFile(src) as z:
  ws=ET.fromstring(z.read('xl/workbook.xml'))
  rels={r.attrib['Id']:r.attrib['Target'] for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
  sheets={s.attrib['name']:rels[s.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']].lstrip('/') for s in ws.find('s:sheets',ns)}
  sheets={k:v if v.startswith('xl/') else 'xl/'+v for k,v in sheets.items()};mods={}
  for sheet,values in changes.items():
   tree=ET.fromstring(z.read(sheets[sheet]));sd=tree.find('s:sheetData',ns)
   for ref,v in values.items():
    rn=''.join(c for c in ref if c.isdigit())
    row=sd.find(f's:row[@r="{rn}"]',ns)
    if row is None:row=ET.SubElement(sd,N+'row',{'r':rn})
    cell=row.find(f's:c[@r="{ref}"]',ns)
    if cell is None:cell=ET.SubElement(row,N+'c',{'r':ref})
    for child in list(cell):cell.remove(child)
    cell.attrib.pop('t',None)
    if isinstance(v,str) and v.startswith('='):ET.SubElement(cell,N+'f').text=v[1:]
    elif isinstance(v,str):
     cell.set('t','inlineStr');ET.SubElement(ET.SubElement(cell,N+'is'),N+'t').text=v
    elif v is not None:ET.SubElement(cell,N+'v').text=str(v)
   mods[sheets[sheet]]=ET.tostring(tree,encoding='utf-8',xml_declaration=True)
  with zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED) as out:
   for info in z.infolist():out.writestr(info.filename,mods.get(info.filename,z.read(info.filename)))

CM,AN,MO='Control maestro','Análisis','Motor'
selectors={'A':'Sí','B':'No · financiación cambia mucho','C':'No · banco o aseguradora'}
reference_values={'A':25.8903521530386,'B':30.7047681225928,'C':17.8908417408599}
data_common=[38,41,52,107,171,172,174,175]
hyp_common=[57,53,138,142,143,145,146,147,149,150,151,153,61,66,71,62,67,72]
data={'A':data_common+[43,44,45,46,48,108,109,110,112,114,116],
      'B':data_common+[108,109,112,117,124,125,126,127,128], 'C':data_common+[111,123]}
hyps={'A':hyp_common+[139,129,49,144,148,152], 'B':hyp_common+[139,144,148,152], 'C':hyp_common}
def complete(m):
    cm={'L4':'IFRS'}
    for r in data[m]:cm.update({f'F{r}':'Rellenado y verificado',f'J{r}':'FUENTE SINTÉTICA DE PRUEBA'})
    for r in hyps[m]:cm.update({f'F{r}':'Hipótesis confirmada',f'M{r}':'HIPÓTESIS SINTÉTICA DE PRUEBA'})
    return {AN:{'C62':selectors[m]},CM:cm}

pending='NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo'
cases=[]
for m in 'ABC':
    cases.append((m+'_empty',m,{'L4':None},pending,'falta norma contable'))
    cases.append((m+'_present',m,{},'LISTO','documentada'))
cases.extend([
    ('A_spaces','A',{'L4':'   '},pending,'falta norma contable'),
    ('B_formula_empty','B',{'L4':'=""'},pending,'falta norma contable'),
    ('C_invisible_whitespace','C',{'L4':' \t\n\u00a0 '},pending,'falta norma contable'),
    ('C_formula_present','C',{'L4':'="IFRS"'},'LISTO','documentada'),
    ('A_value_without_source','A',{'J175':None},pending,'sin fuente'),
    ('A_empty_estimate','A',{'L4':None,'F175':'Estimación declarada'},pending,'falta norma contable'),
    ('A_present_estimate','A',{'F175':'Estimación declarada'},'LISTO · PROVISIONAL (1 estimaciones justificadas)','estimación'),
    ('B_present_unverified','B',{'F175':'Dato no verificable'},pending,'no verificable'),
])
cases.sort(key=lambda item: item[0]!='C_invisible_whitespace')
for d in ['test_cases','test_recalc','delivered_recalc']:(WORK/d).mkdir(exist_ok=True)

def recalc(src,destination,profile):
    r=subprocess.run(['soffice','-env:UserInstallation=file://'+str(WORK/profile),'--headless','--convert-to','xlsx','--outdir',str(destination),str(src)],capture_output=True,text=True,timeout=55)
    p=destination/src.name
    if not p.exists():raise RuntimeError(r.stdout+'\n'+r.stderr)
    return p

if len(sys.argv)>3 and sys.argv[3]=='deliverables':
    results={}
    for src in (PACKAGE/'entregables').glob('*.xlsx'):
        p=recalc(src,WORK/'delivered_recalc','lo_deliverables')
        w=openpyxl.load_workbook(p,data_only=True)
        results[src.name]={f'{s}!{c}':w[s][c].value for s,c in [(AN,'C83'),(MO,'B266'),(CM,'L4'),(CM,'L206'),(CM,'D248')]}
        print(src.name,json.dumps(results[src.name],ensure_ascii=False),flush=True)
    (WORK/'delivered_recalc_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
else:
    results=[]
    for name,m,changes,state,evidence in cases:
        inputs=complete(m);inputs[CM].update(changes)
        src=WORK/'test_cases'/(name+'.xlsx')
        copy_changes(PACKAGE/'entregables/Ejemplo_V6.3_EmpresaX.xlsx',src,inputs)
        p=recalc(src,WORK/'test_recalc','lo_tests')
        w=openpyxl.load_workbook(p,data_only=True)
        value=w[AN]['C83'].value
        errors=[f'{s.title}!{c.coordinate}: {c.value}' for s in w for row in s for c in row if c.data_type=='e' and not (s.title==MO and 141<=c.row<=169 and 2<=c.column<=5 and c.value=='#N/A')]
        actual={'state':w[MO]['B266'].value,'evidence':w[CM]['L206'].value,'value':value,'errors':errors}
        passed=actual['state']==state and actual['evidence']==evidence and isinstance(value,(int,float)) and math.isclose(value,reference_values[m],abs_tol=1e-8) and not errors
        result={'name':name,'expected':{'state':state,'evidence':evidence,'value':reference_values[m]},'actual':actual,'passed':passed}
        results.append(result)
        (WORK/'test_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
        print(name,'PASS' if passed else 'FAIL',json.dumps(actual,ensure_ascii=False),flush=True)
    assert all(r['passed'] for r in results)
    print('TOTAL',len(results),'PASS',flush=True)
