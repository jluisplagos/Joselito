# -*- coding: utf-8 -*-
"""Añade deslizadores reales (controles de formulario «barra de desplazamiento») al Panel de una hoja V6.

Va SIEMPRE al final: openpyxl pierde los controles al guardar. Cada deslizador está vinculado a Panel!E20:E25
(0–40, 20 = sin cambio) y se coloca encima de la columna D (Ajuste).
Uso: python3 add_sliders.py entrada.xlsx salida.xlsx
"""
import sys, re, zipfile, shutil

SRC, OUT = sys.argv[1], sys.argv[2]
ROWS = [20, 21, 22, 23, 24, 25]         # filas de Excel (1 = primera) · palancas del Panel V6.1
COL = 3                                 # columna D en base 0
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

zin = zipfile.ZipFile(SRC)
files = {n: zin.read(n) for n in zin.namelist()}
zin.close()

# hoja del Panel
wbx = files['xl/workbook.xml'].decode('utf-8')
rid = re.search(r'<sheet[^>]*name="Panel"[^>]*r:id="(rId\d+)"', wbx).group(1)
rels = files['xl/_rels/workbook.xml.rels'].decode('utf-8')
target = re.search(r'<Relationship[^>]*Target="([^"]+)"[^>]*Id="%s"|<Relationship[^>]*Id="%s"[^>]*Target="([^"]+)"' % (rid, rid), rels)
tgt = target.group(1) or target.group(2)
sheet_path = tgt.lstrip('/') if tgt.startswith('/') else 'xl/' + tgt
sheet_name = sheet_path.split('/')[-1]
rels_path = f'xl/worksheets/_rels/{sheet_name}.rels'

sheet = files[sheet_path].decode('utf-8')
srels = files.get(rels_path, b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>').decode('utf-8')

vml_id = 'rIdVml1'
ctrl_rids = [f'rIdCtl{i + 1}' for i in range(len(ROWS))]
new_rels = f'<Relationship Id="{vml_id}" Type="{R}/vmlDrawing" Target="../drawings/vmlDrawingPanel.vml"/>'
for i, cr in enumerate(ctrl_rids):
    new_rels += f'<Relationship Id="{cr}" Type="{R}/ctrlProp" Target="../ctrlProps/ctrlPropPanel{i + 1}.xml"/>'
srels = srels.replace('</Relationships>', new_rels + '</Relationships>')

# VML (forma heredada que Excel dibuja)
shapes = ''
for i, row in enumerate(ROWS):
    sid = 1025 + i
    shapes += (f'<v:shape id="_x0000_s{sid}" type="#_x0000_t201" style="position:absolute;z-index:{i + 1}" o:insetmode="auto">'
               f'<o:lock v:ext="edit" rotation="t"/>'
               f'<x:ClientData ObjectType="Scroll"><x:Anchor>{COL}, 4, {row - 1}, 4, {COL + 1}, 0, {row - 1}, 25</x:Anchor>'
               f'<x:Val>20</x:Val><x:Min>0</x:Min><x:Max>40</x:Max><x:Inc>1</x:Inc><x:Page>4</x:Page><x:Horiz/>'
               f'<x:FmlaLink>$E${row}</x:FmlaLink><x:Dx>22</x:Dx></x:ClientData></v:shape>')
vml = ('<xml xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" '
       'xmlns:x="urn:schemas-microsoft-com:office:excel">'
       '<o:shapelayout v:ext="edit"><o:idmap v:ext="edit" data="1"/></o:shapelayout>'
       '<v:shapetype id="_x0000_t201" coordsize="21600,21600" o:spt="201" path="m,l,21600r21600,l21600,xe">'
       '<v:stroke joinstyle="miter"/><v:path shadowok="f" o:extrusionok="f" strokeok="f" fillok="f" o:connecttype="rect"/>'
       '<o:lock v:ext="edit" shapetype="t"/></v:shapetype>' + shapes + '</xml>')
files['xl/drawings/vmlDrawingPanel.vml'] = vml.encode('utf-8')

# propiedades de cada control
for i, row in enumerate(ROWS):
    files[f'xl/ctrlProps/ctrlPropPanel{i + 1}.xml'] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<formControlPr xmlns="http://schemas.microsoft.com/office/spreadsheetml/2009/9/main" objectType="Scroll" '
        f'dx="22" fmlaLink="$E${row}" horiz="1" max="40" min="0" inc="1" page="4" val="20"/>').encode('utf-8')

# bloque <controls> en la hoja
ctrls = ''
for i, row in enumerate(ROWS):
    ctrls += (f'<mc:AlternateContent><mc:Choice Requires="x14"><control shapeId="{1025 + i}" r:id="{ctrl_rids[i]}" '
              f'name="Deslizador {i + 1}"><controlPr defaultSize="0" autoPict="0"><anchor moveWithCells="1">'
              f'<from><xdr:col>{COL}</xdr:col><xdr:colOff>38100</xdr:colOff><xdr:row>{row - 1}</xdr:row><xdr:rowOff>38100</xdr:rowOff></from>'
              f'<to><xdr:col>{COL + 1}</xdr:col><xdr:colOff>0</xdr:colOff><xdr:row>{row - 1}</xdr:row><xdr:rowOff>238125</xdr:rowOff></to>'
              f'</anchor></controlPr></control></mc:Choice></mc:AlternateContent>')
block = (f'<legacyDrawing xmlns:r="{R}" r:id="{vml_id}"/>'
         f'<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
         f'xmlns:x14="http://schemas.microsoft.com/office/spreadsheetml/2009/9/main" '
         f'xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" xmlns:r="{R}">'
         f'<mc:Choice Requires="x14"><controls>{ctrls}</controls></mc:Choice></mc:AlternateContent>')
m = re.search(r'<drawing [^>]*/>', sheet)
assert m, 'el Panel no tiene <drawing>'
sheet = sheet[:m.end()] + block + sheet[m.end():]
files[sheet_path] = sheet.encode('utf-8')
files[rels_path] = srels.encode('utf-8')

ct = files['[Content_Types].xml'].decode('utf-8')
if 'Extension="vml"' not in ct:
    ct = ct.replace('<Default ', '<Default Extension="vml" ContentType="application/vnd.openxmlformats-officedocument.vmlDrawing"/><Default ', 1)
for i in range(len(ROWS)):
    ct = ct.replace('</Types>', f'<Override PartName="/xl/ctrlProps/ctrlPropPanel{i + 1}.xml" '
                                f'ContentType="application/vnd.ms-excel.controlproperties+xml"/></Types>')
files['[Content_Types].xml'] = ct.encode('utf-8')

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in ['[Content_Types].xml'] + [k for k in files if k != '[Content_Types].xml']:
        z.writestr(n, files[n])
print('OK', OUT, '· 6 deslizadores en Panel!D20:D25 → E20:E25')
