import sys, subprocess, openpyxl, os, shutil
src, sheet, area, outpng = sys.argv[1:5]
tmp = 'render_tmp2'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
wb = openpyxl.load_workbook(src)
for ws in wb.worksheets:
    ws.sheet_state = 'visible'
for ws in wb.worksheets:
    ws.sheet_view.tabSelected = (ws.title == sheet)
    if ws.title != sheet: ws.sheet_state = 'hidden'
p = wb[sheet]; p.sheet_state = 'visible'; wb.active = wb.worksheets.index(p)
for ws in wb.worksheets:
    if ws.title != sheet:
        ws.sheet_state = 'hidden'
p.sheet_state = 'visible'
wb.active = wb.worksheets.index(p)
p.print_area = area
p.page_setup.orientation = 'landscape'
p.page_setup.fitToWidth = 1; p.page_setup.fitToHeight = 3
p.sheet_properties.pageSetUpPr.fitToPage = True
wb.save(f'{tmp}/r.xlsx')
subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp, f'{tmp}/r.xlsx'], capture_output=True, timeout=300)
subprocess.run(['pdftoppm', '-r', '110', '-png', f'{tmp}/r.pdf', f'{tmp}/pg'], capture_output=True)
for i, x in enumerate(sorted(x for x in os.listdir(tmp) if x.startswith('pg'))):
    shutil.copy(f'{tmp}/{x}', outpng.replace('.png', f'_{i + 1}.png'))
    print(outpng.replace('.png', f'_{i + 1}.png'))
