"""
14_excel_escenarios.py
Agrega la hoja "Escenarios" al libro operativo: selector desplegable de
escenario (tabla de referencia con los 6 escenarios de 13_escenarios.py),
un bloque de 36 celdas EDITABLES (factor activo por mes x producto, que el
usuario llena copiando un preset o escribiendo su propio "que pasa si") y
el pronostico AJUSTADO resultante (litros/unidades), enlazado por formula
a la hoja Pronostico_2026 ya existente, con grafico comparativo nativo.
Debe correrse DESPUES de scripts/07_generar_excel.py y 13_escenarios.py.
"""
import json
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import LineChart, Reference
from openpyxl.utils import get_column_letter
import pandas as pd

from importlib.util import spec_from_file_location, module_from_spec
_spec = spec_from_file_location("esc", "scripts/13_escenarios.py")
_esc = module_from_spec(_spec); _spec.loader.exec_module(_esc)
ESCENARIOS = _esc.ESCENARIOS; MESES = _esc.MESES

NAVY="1F3864"; BLUE="0000FF"; GREEN="008000"
H=PatternFill("solid",fgColor=NAVY); SUBF=PatternFill("solid",fgColor="D9E1F2")
YEL=PatternFill("solid",fgColor="FFFF00"); GREY=PatternFill("solid",fgColor="F7F9FC")
ACT=PatternFill("solid",fgColor="FFF2CC")
T=lambda **k: Font(name="Times New Roman",**k)
thin=Side(style="thin",color="BFBFBF"); B=Border(left=thin,right=thin,top=thin,bottom=thin)
CEN=Alignment(horizontal="center",vertical="center",wrap_text=True)
LEF=Alignment(horizontal="left",vertical="center",wrap_text=True)
RIG=Alignment(horizontal="right",vertical="center")
def hdr(c,t): c.value=t;c.font=T(bold=True,color="FFFFFF",size=9.5);c.fill=H;c.alignment=CEN;c.border=B
def fx(c,f,fmt="#,##0"): c.value=f;c.font=T(color=GREEN,size=9.5);c.number_format=fmt;c.alignment=RIG;c.border=B
def inp(c,v,fmt="0.00",fill=YEL): c.value=v;c.font=T(color=BLUE,size=9.5);c.number_format=fmt;c.alignment=RIG;c.border=B;c.fill=fill
def lbl(c,t,b=False,size=9.5): c.value=t;c.font=T(bold=b,size=size);c.alignment=LEF;c.border=B

blocks = json.load(open("data/pronostico2026_celdas.json"))  # {P1:[st,total], P2:[...], P3:[...]}
PROD_COL_LIT = 3  # columna C = litros en Pronostico_2026

wb = load_workbook("Modelo_Fontibon_Operativo.xlsx")
if "Escenarios" in wb.sheetnames: del wb["Escenarios"]
ws = wb.create_sheet("Escenarios")
ws.sheet_view.showGridLines = False
widths = [3,20]+[9]*12+[10]
for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width = w
r=2
ws.cell(r,2,"ESCENARIOS DE DEMANDA — factores que suben o bajan el pronóstico base").font=T(bold=True,size=13,color=NAVY); r+=1
ws.cell(r,2,"1) Elija un escenario de referencia abajo y copie sus 12 factores a la fila 'FACTOR ACTIVO' de cada producto (o escriba los suyos: es libre). "
            "2) El pronóstico AJUSTADO se recalcula solo. 3) 'Personalizado' = escriba directamente, sin copiar nada.").font=T(italic=True,size=9); r+=2

# ---------- Tabla de referencia de escenarios (presets) ----------
ws.cell(r,2,"TABLA DE REFERENCIA — presets documentados (ver Referencias / data/escenarios_resumen.csv)").font=T(bold=True,size=11,color=NAVY); r+=1
REF_START = {}
for prod in ['P1','P2','P3']:
    ws.cell(r,2,f"Preset — {prod}").font=T(bold=True,size=10); r+=1
    hdr(ws.cell(r,2),"Escenario")
    for i,m in enumerate(MESES): hdr(ws.cell(r,3+i),m)
    r+=1; REF_START[prod]=r
    for nombre,esc in ESCENARIOS.items():
        lbl(ws.cell(r,2),nombre)
        for i,val in enumerate(esc[prod]):
            c=ws.cell(r,3+i); c.value=round(val,3); c.font=T(size=9); c.number_format="0.00"; c.alignment=RIG; c.border=B
            if r%2: c.fill=GREY
        r+=1
    r+=1

# ---------- FACTOR ACTIVO (editable) + Pronostico ajustado ----------
ws.cell(r,2,"ESCENARIO ACTIVO — edite aquí (copie un preset de arriba o escriba su propio factor)").font=T(bold=True,size=11,color=NAVY); r+=1
FACT_ROWS = {}
AJUST_ROWS = {}
for prod in ['P1','P2','P3']:
    ws.cell(r,2,f"{prod} — factor activo").font=T(bold=True,size=10,color=NAVY); r+=1
    hdr(ws.cell(r,2),"Fila")
    for i,m in enumerate(MESES): hdr(ws.cell(r,3+i),m)
    r+=1
    lbl(ws.cell(r,2),"FACTOR ACTIVO",b=True)
    for i in range(12):
        inp(ws.cell(r,3+i), 1.00, "0.00", fill=ACT)
        ws.cell(r,3+i).comment = None
    FACT_ROWS[prod]=r; r+=1
    lbl(ws.cell(r,2),"Litros BASE (Pronóstico)")
    st,_ = blocks[prod]
    for i in range(12):
        fx(ws.cell(r,3+i), f"=Pronostico_2026!C{st+i}", "#,##0")
    BASE_ROW = r; r+=1
    lbl(ws.cell(r,2),"Litros AJUSTADO = base × factor",b=True)
    for i in range(12):
        col = get_column_letter(3+i)
        fx(ws.cell(r,3+i), f"={col}{BASE_ROW}*{col}{FACT_ROWS[prod]}", "#,##0")
        ws.cell(r,3+i).fill=SUBF
    AJUST_ROWS[prod]=r; r+=1
    lbl(ws.cell(r,2),"Δ % vs base",b=True)
    for i in range(12):
        col=get_column_letter(3+i)
        fx(ws.cell(r,3+i), f"={col}{AJUST_ROWS[prod]}/{col}{BASE_ROW}-1", "0.0%")
    r+=1
    lbl(ws.cell(r,2),"TOTAL AÑO (litros)",b=True)
    fx(ws.cell(r,3), f"=SUM(C{AJUST_ROWS[prod]}:N{AJUST_ROWS[prod]})", "#,##0")
    c=ws.cell(r,4); c.value="vs base:"; c.font=T(italic=True,size=9)
    fx(ws.cell(r,5), f"=SUM(C{BASE_ROW}:N{BASE_ROW})", "#,##0")
    fx(ws.cell(r,6), f"=C{r}/E{r}-1", "0.0%")
    r+=2

wb.save("Modelo_Fontibon_Operativo.xlsx")

# ---------- Grafico comparativo (Base vs Ajustado, P1 como ejemplo visible) ----------
wb2 = load_workbook("Modelo_Fontibon_Operativo.xlsx")
ws2 = wb2["Escenarios"]
for prod in ['P1','P2','P3']:
    ch = LineChart(); ch.title=f"{prod}: Base vs Ajustado (L/mes)"; ch.height=7; ch.width=16
    ch.y_axis.title="Litros"; ch.x_axis.title="Mes"
    base_row = AJUST_ROWS[prod]-2  # BASE_ROW relative
    data_base = Reference(ws2, min_col=3, max_col=14, min_row=base_row, max_row=base_row)
    data_aj = Reference(ws2, min_col=3, max_col=14, min_row=AJUST_ROWS[prod], max_row=AJUST_ROWS[prod])
    ch.add_data(data_base, titles_from_data=False); ch.series[0].tx = None
    ch.add_data(data_aj, titles_from_data=False)
    cats = Reference(ws2, min_col=3, max_col=14, min_row=FACT_ROWS[prod]-1, max_row=FACT_ROWS[prod]-1)
    ws2.add_chart(ch, f"P{FACT_ROWS[prod]}")
wb2.save("Modelo_Fontibon_Operativo.xlsx")
print("OK -> hoja 'Escenarios' agregada a Modelo_Fontibon_Operativo.xlsx")
