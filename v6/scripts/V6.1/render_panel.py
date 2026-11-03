import sys, subprocess, openpyxl, os, shutil
src, outpng = sys.argv[1], sys.argv[2]
tmp = 'render_tmp'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
wb = openpyxl.load_workbook(src)
for ws in wb.worksheets:
    if ws.title != 'Panel':
        ws.sheet_state = 'hidden'
p = wb['Panel']
p.print_area = 'A1:O80'
p.page_setup.orientation = 'landscape'
p.page_setup.fitToWidth = 1; p.page_setup.fitToHeight = 1
p.sheet_properties.pageSetUpPr.fitToPage = True
wb.save(f'{tmp}/r.xlsx')
subprocess.run(['python3', 'add_sliders.py', f'{tmp}/r.xlsx', f'{tmp}/r2.xlsx'], check=True, capture_output=True)
subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp, f'{tmp}/r2.xlsx'], capture_output=True, timeout=300)
subprocess.run(['pdftoppm', '-r', '200', '-f', '1', '-l', '1', '-png', f'{tmp}/r2.pdf', f'{tmp}/pg'], capture_output=True)
pngs = sorted(x for x in os.listdir(tmp) if x.startswith('pg'))
shutil.copy(f'{tmp}/{pngs[0]}', outpng)
print('OK', outpng)
