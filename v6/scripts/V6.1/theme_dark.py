# -*- coding: utf-8 -*-
"""Tema oscuro para la plantilla V6.1 (pasada final sobre el libro ya construido).

Solo cambia colores: rellenos, fuentes, bordes, reglas de formato condicional y gráficos.
No toca valores, fórmulas, validaciones, controles ni la posición de ninguna celda.
Uso como módulo:  from theme_dark import apply_dark; apply_dark(wb)
Uso suelto:       python3 theme_dark.py entrada.xlsx salida.xlsx
"""
import copy
from openpyxl.styles import PatternFill, Font, Border, Side
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.chart.text import RichText
from openpyxl.drawing.text import Paragraph, ParagraphProperties, CharacterProperties, RichTextProperties

# ---------------------------------------------------------------- paleta
BG, PANEL, PANEL2, BORDER = '0E1116', '161B22', '1C2733', '30363D'
TEXT, MUTED, WHITE = 'E6EDF3', '8B949E', 'FFFFFF'
IN_BG, IN_FG, ACCENT, ON_BG = '1B2A41', '79C0FF', '58A6FF', '1F6FEB'
TITLE_BG, BAND_BG = '0D2137', '1B4F5B'
GOOD_BG, WARN_BG, BAD_BG, OFF_BG, DISC_BG = '12301F', '3A2E12', '3B1A1A', '262B33', '1F2A44'
GOOD_FG, WARN_FG, BAD_FG, DISC_FG = '3FB950', 'D29922', 'F85149', '8EA1FF'

# color claro (ARGB o RGB) → color oscuro (RGB)
FILL_MAP = {
    'FFFFFF': BG, 'F2F2F2': PANEL, 'EAF3F4': PANEL, 'DCE6EC': PANEL2, 'E7E9EB': OFF_BG, 'EDEDED': OFF_BG,
    '1F3A4D': TITLE_BG, '174F58': TITLE_BG, '2E6E78': BAND_BG, '1F6670': BAND_BG,
    'FFF6CC': IN_BG, 'FFF2CC': IN_BG,
    'C6EFCE': GOOD_BG, 'D9EAD3': GOOD_BG, 'FFE699': WARN_BG, 'FFEB9C': WARN_BG,
    'F8CBAD': BAD_BG, 'FFC7CE': BAD_BG, 'FCE8E6': BAD_BG, 'F4CCCC': BAD_BG,
    'D9E1F2': DISC_BG, '1F4E79': ON_BG, '2E75B6': ON_BG,
}
FONT_MAP = {
    None: TEXT, '000000': TEXT, '333333': TEXT, '262626': TEXT,
    '595959': MUTED, '666666': MUTED, '404040': MUTED, '7F7F7F': MUTED, '808080': MUTED,
    '0000FF': IN_FG, '1F4E79': ACCENT, '1F3A4D': ACCENT, '2E75B6': ACCENT,
    '006100': GOOD_FG, '008000': GOOD_FG, '7F6000': WARN_FG, '9C6500': WARN_FG, '9C0006': BAD_FG, 'FF0000': BAD_FG,
    '8EA1FF': DISC_FG, 'FFFFFF': WHITE,
}
SERIES_MAP = {'1F4E79': '58A6FF', '2E75B6': '388BFD', '9DC3E6': '1F4E79', '808080': '8B949E', 'FF0000': 'F85149'}


def _rgb(color):
    """Devuelve 'RRGGBB' de un Color de openpyxl, o None si no es RGB explícito."""
    if color is None or color.type != 'rgb' or not isinstance(color.rgb, str):
        return None
    return color.rgb[-6:].upper()


def _map_fill(f):
    if f is None or f.fill_type != 'solid':
        return PatternFill('solid', fgColor='FF' + BG)
    k = _rgb(f.fgColor)
    if k is None:
        return PatternFill('solid', fgColor='FF' + BG)
    return PatternFill('solid', fgColor='FF' + FILL_MAP.get(k, k))


def _map_font(fo):
    k = _rgb(fo.color) if fo is not None else None
    new = FONT_MAP.get(k, k if k else TEXT)
    f2 = copy.copy(fo) if fo is not None else Font()
    f2.color = 'FF' + new
    return f2


def _map_border(b):
    if b is None:
        return b
    sides = {}
    for nm in ('left', 'right', 'top', 'bottom'):
        s = getattr(b, nm)
        if s is not None and s.style:
            sides[nm] = Side(style=s.style, color='FF' + BORDER)
        else:
            sides[nm] = Side()
    return Border(**sides)


def _rich(color, sz, bold=False):
    cp = CharacterProperties(solidFill=color, sz=sz, b=bold)
    return RichText(bodyPr=RichTextProperties(), p=[Paragraph(pPr=ParagraphProperties(defRPr=cp), endParaRPr=cp)])


def dark_chart(ch):
    ch.graphical_properties = GraphicalProperties(solidFill=PANEL, ln=LineProperties(solidFill=BORDER))
    ch.plot_area.graphicalProperties = GraphicalProperties(solidFill=PANEL, ln=LineProperties(noFill=True))
    for ax in (ch.x_axis, ch.y_axis):
        ax.txPr = _rich(MUTED, 800)
        ax.graphicalProperties = GraphicalProperties(ln=LineProperties(solidFill=BORDER))
        if ax.majorGridlines is not None:
            ax.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill=BORDER))
    if ch.title is not None and ch.title.tx is not None and ch.title.tx.rich is not None:
        cp = CharacterProperties(solidFill=TEXT, sz=1000, b=True)
        for p in ch.title.tx.rich.p:
            p.pPr = ParagraphProperties(defRPr=cp)
            for r in (p.r or []):
                r.rPr = cp
    if ch.legend is not None:
        ch.legend.txPr = _rich(MUTED, 800)
    # series: colores de línea/relleno claros → equivalentes oscuros
    charts = [ch] + list(getattr(ch, '_charts', []))
    for sub in charts:
        for s in sub.series:
            gp = s.graphicalProperties
            if gp is None:
                continue
            if gp.solidFill is not None and isinstance(gp.solidFill, str):
                gp.solidFill = SERIES_MAP.get(gp.solidFill.upper(), gp.solidFill)
            if gp.line is not None and gp.line.solidFill is not None and isinstance(gp.line.solidFill, str):
                gp.line.solidFill = SERIES_MAP.get(gp.line.solidFill.upper(), gp.line.solidFill)


def apply_dark(wb, skip=('Motor',), extra_rows=40, extra_cols=6):
    for ws in wb.worksheets:
        if ws.title in skip:
            continue
        nrow = max(ws.max_row + extra_rows, 80)
        ncol = max(ws.max_column + extra_cols, 16)
        for row in ws.iter_rows(min_row=1, max_row=nrow, min_col=1, max_col=ncol):
            for c in row:
                c.fill = _map_fill(c.fill if c.has_style else None)
                c.font = _map_font(c.font if c.has_style else None)
                if c.has_style and c.border is not None and any(getattr(c.border, n) is not None and getattr(c.border, n).style for n in ('left', 'right', 'top', 'bottom')):
                    c.border = _map_border(c.border)
        # estilo por columna: lo que quede fuera del rango tratado también se ve oscuro
        for ci in range(1, 60):
            from openpyxl.utils import get_column_letter
            cd = ws.column_dimensions[get_column_letter(ci)]
            cd.fill = PatternFill('solid', fgColor='FF' + BG)
            cd.font = Font(name='Arial', size=10, color='FF' + TEXT)
        # formato condicional
        for rng in ws.conditional_formatting:
            for rule in rng.rules:
                d = rule.dxf
                if d is None:
                    continue
                if d.fill is not None:
                    for attr in ('fgColor', 'bgColor'):
                        col = getattr(d.fill, attr)
                        k = _rgb(col)
                        if k and k != '000000':
                            setattr(d.fill, attr, 'FF' + FILL_MAP.get(k, k))
                if d.font is not None and d.font.color is not None:
                    k = _rgb(d.font.color)
                    if k:
                        d.font.color = 'FF' + FONT_MAP.get(k, k)
        for ch in ws._charts:
            dark_chart(ch)
        ws.sheet_view.showGridLines = False
    return wb


if __name__ == '__main__':
    import sys, openpyxl
    wb = openpyxl.load_workbook(sys.argv[1])
    apply_dark(wb)
    wb.save(sys.argv[2])
    print('OK', sys.argv[2])
