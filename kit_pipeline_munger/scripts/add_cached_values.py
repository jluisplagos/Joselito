#!/usr/bin/env python3
"""Añade a cada fórmula del Excel evaluado su valor calculado (leído de la copia recalculada por
LibreOffice), para que los visores que no recalculan (vista previa, móvil, Vista protegida) muestren
los resultados. No toca ninguna fórmula, estilo, validación ni estructura: solo inserta <v> en las
celdas con <f>. Uso: add_cached_values.py <evaluada.xlsx> <recalc/evaluada.xlsx> <salida.xlsx>"""
import sys, zipfile, re, datetime
import openpyxl
from lxml import etree
src, rec, out = sys.argv[1:4]
NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
RNS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
zin = zipfile.ZipFile(src)
wbx = etree.fromstring(zin.read('xl/workbook.xml'))
rels = etree.fromstring(zin.read('xl/_rels/workbook.xml.rels'))
rid2t = {r.get('Id'): r.get('Target').lstrip('/') for r in rels}
sheetfile = {}
for s in wbx.find(f'{{{NS}}}sheets'):
    t = rid2t[s.get(f'{{{RNS}}}id')]
    sheetfile[t if t.startswith('xl/') else 'xl/' + t] = s.get('name')
rc = openpyxl.load_workbook(rec, data_only=True)
n = 0
newdata = {}
for path, name in sheetfile.items():
    ws = rc[name]
    root = etree.fromstring(zin.read(path))
    for c in root.iter(f'{{{NS}}}c'):
        f = c.find(f'{{{NS}}}f')
        if f is None: continue
        for v in c.findall(f'{{{NS}}}v'): c.remove(v)
        val = ws[c.get('r')].value
        if val is None: continue
        v = etree.SubElement(c, f'{{{NS}}}v')
        if isinstance(val, bool):
            c.set('t', 'b'); v.text = '1' if val else '0'
        elif isinstance(val, (int, float)):
            c.attrib.pop('t', None); v.text = repr(float(val)) if isinstance(val, float) else str(val)
        elif isinstance(val, (datetime.datetime, datetime.date)):
            c.attrib.pop('t', None)
            base = datetime.datetime(1899, 12, 30)
            d = val if isinstance(val, datetime.datetime) else datetime.datetime.combine(val, datetime.time())
            v.text = repr((d - base).total_seconds() / 86400)
        elif isinstance(val, str) and re.fullmatch(r'#(N/A|VALUE!|REF!|DIV/0!|NUM!|NAME\?|NULL!)', val):
            c.set('t', 'e'); v.text = val
        else:
            c.set('t', 'str'); v.text = str(val)
        n += 1
    newdata[path] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        zout.writestr(item, newdata.get(item.filename, zin.read(item.filename)))
print(f'OK: {n} fórmulas con valor guardado → {out}')
