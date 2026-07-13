"""
07_generar_excel.py
Genera Modelo_Fontibon_Operativo.xlsx con:
  Notas | SKUs_Empaques | Pruebas | Pronostico_2026 (L->und->agrup->pallets->lote)
  Backtest_TS (MAD/CFE/MSE/MAPE + senal de rastreo) | Rotacion
Formato: Times New Roman; formulas Excel para todas las conversiones.
"""
import json, pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

NAVY="1F3864"; BLUE="0000FF"; GREEN="008000"
H=PatternFill("solid",fgColor=NAVY); SUBF=PatternFill("solid",fgColor="D9E1F2")
GREY=PatternFill("solid",fgColor="F7F9FC"); RED=PatternFill("solid",fgColor="FCE4E4")
T=lambda **k: Font(name="Times New Roman",**k)
thin=Side(style="thin",color="BFBFBF"); B=Border(left=thin,right=thin,top=thin,bottom=thin)
CEN=Alignment(horizontal="center",vertical="center",wrap_text=True)
RIG=Alignment(horizontal="right",vertical="center")
def hdr(c,t): c.value=t;c.font=T(bold=True,color="FFFFFF",size=10);c.fill=H;c.alignment=CEN;c.border=B
def lbl(c,t,b=False): c.value=t;c.font=T(bold=b,size=10);c.border=B;c.alignment=Alignment(horizontal="left",vertical="center",wrap_text=True)
def val(c,v,fmt="#,##0",blue=False):
    c.value=v;c.font=T(color=BLUE if blue else "000000",size=10);c.number_format=fmt;c.alignment=RIG;c.border=B
def fx(c,f,fmt="#,##0"): c.value=f;c.font=T(color=GREEN,size=10);c.number_format=fmt;c.alignment=RIG;c.border=B

hist=pd.read_csv("data/historico_planta.csv",parse_dates=['fecha'])
fc=pd.read_csv("data/pronostico_2026.csv",parse_dates=['fecha'])
bt=pd.read_csv("data/evaluacion_backtest.csv")
rot=pd.read_csv("data/rotacion_inventarios.csv")
pruebas=json.load(open("data/pruebas_estadisticas.json"))
hwp=json.load(open("data/hw_parametros.json"))
evr=json.load(open("data/evaluacion_resumen.json"))
ETIQ=['Abr-26','May-26','Jun-26','Jul-26','Ago-26','Sep-26','Oct-26','Nov-26','Dic-26','Ene-27','Feb-27','Mar-27']

wb=Workbook()

# ---------- NOTAS ----------
ws=wb.active; ws.title="Notas"; ws.sheet_view.showGridLines=False
ws.column_dimensions['A'].width=2; ws.column_dimensions['B'].width=112
r=2
ws.cell(r,2,"MODELO OPERATIVO — PLANTA KOF BOGOTÁ (FONTIBÓN) · DATOS TRIMESTRALES REALES 2021T1–2026T1 · PRONÓSTICO abr-26→mar-27").font=T(bold=True,size=14,color=NAVY); r+=2
for t,d in [
("Procedimiento formal","Sigue el diagrama de flujo del proyecto: análisis de datos → correlación → prueba de rachas → Kruskal-Wallis → Levene → autocorrelación (¿constante/tendencia/estacionalidad?) → ESTACIONALIDAD detectada (ACF lag-12 significativo, Ljung-Box p≈0) → Holt-Winters multiplicativo → error (MAD, CFE, MSE, MAPE) → señal de rastreo → pronóstico."),
("Modelo","Holt-Winters multiplicativo con tendencia amortiguada (φ<1, Gardner & McKenzie 1985): variante conservadora estándar en industria. Parámetros por máxima verosimilitud (statsmodels): ver hoja Backtest_TS."),
("Señal de rastreo — hallazgo","En el backtest trimestral la TS toca −4: sesgo por sobre-pronóstico con CAUSA ASIGNABLE = quiebre estructural del impuesto saludable (ene-2025). Es el comportamiento esperado de la señal: detectar el cambio de nivel. El modelo final, reentrenado con 2025 completo (α≈0,98), adapta el nivel y el pronóstico 2026 parte de la base corregida."),
("Empaque y lotes","Jerarquías reales de planta: P1 cajón×30 → capa 9 cajones → pallet 6 capas = 1.620 bot = 567 L. P2 pack×6 → capa 28 packs → pallet 5 capas = 840 bot = 1.260 L. P3 rack×6 = capa → pallet 5 capas = 30 garrafones = 750 L. La línea libera PALLETS COMPLETOS: lote mínimo e incremento = 1 pallet; lote estándar = demanda mensual/corridas_mes (parámetro de planeación, 20 por defecto; tiempos se estudiarán después)."),
("Rotación","Inventario de ciclo = Lote/2; Rotación = Demanda anual/(Lote/2); Cobertura = 365/Rotación. Se presenta bajo 3 escenarios de lote (diario≈20 corridas/mes, semanal≈4, mensual=1)."),
("ERP (Odoo)","Archivos de importación en erp_odoo/: uom_uom.csv (UdM por jerarquía), product_template.csv (SKU + EAN-13 prefijo 770 Colombia con dígito de control), product_packaging.csv (cajón/pack/rack, capa, pallet), pronostico_ventas.csv (demanda mensual en unidades). Códigos estilo catálogo real Coca-Cola (ref.: 75005771 'Cocacola 355 Ml Ret.', 7501032401917 'Agua Cristal 20lt')."),
]:
    ws.cell(r,2,f"■ {t}").font=T(bold=True,size=10.5,color=NAVY); r+=1
    c=ws.cell(r,2); c.value=d; c.font=T(size=9.5); c.alignment=Alignment(wrap_text=True,vertical="top"); ws.row_dimensions[r].height=52; r+=2

# ---------- SKUs_EMPAQUES ----------
ws=wb.create_sheet("SKUs_Empaques"); ws.sheet_view.showGridLines=False
w=[3,13,34,15,12,12,12,12,13,13,13]
for i,ww in enumerate(w,1): ws.column_dimensions[get_column_letter(i)].width=ww
r=2
ws.cell(r,2,"MAESTRO DE PRODUCTOS Y JERARQUÍA DE EMPAQUE (base ERP)").font=T(bold=True,size=13,color=NAVY); r+=2
cab=["SKU","Nombre comercial","EAN-13","Envase (L)","Und/agrup.","Agrup/capa","Capas/pallet","Und/capa","Und/pallet","L/pallet"]
for j,t in enumerate(cab): hdr(ws.cell(r,2+j),t)
r+=1; SKU0=r
datos=[("CC-RET-350","Coca-Cola 350 ml Vidrio Retornable","7701000000013",0.35,30,9,6),
       ("QT-NR-1500","QuAtro Toronja 1.5 L PET No Retornable","7701000000020",1.5,6,28,5),
       ("AG-GF-25000","Garrafón Agua 25 L Retornable","7701000000037",25.0,6,1,5)]
import math
def ean_fix(base12):
    d=[int(c) for c in base12]; chk=(10-(sum(d[0::2])+3*sum(d[1::2]))%10)%10
    return base12+str(chk)
for i,(sku,nom,_,L,ua,ac,cp) in enumerate(datos):
    ean=ean_fix(f"77010000000{i+1}")
    lbl(ws.cell(r,2),sku,b=True); lbl(ws.cell(r,3),nom); lbl(ws.cell(r,4),ean)
    val(ws.cell(r,5),L,"0.00",blue=True); val(ws.cell(r,6),ua,"0",blue=True)
    val(ws.cell(r,7),ac,"0",blue=True); val(ws.cell(r,8),cp,"0",blue=True)
    fx(ws.cell(r,9),f"=F{r}*G{r}")            # und/capa
    fx(ws.cell(r,10),f"=I{r}*H{r}")           # und/pallet
    fx(ws.cell(r,11),f"=J{r}*E{r}","#,##0.0") # L/pallet
    r+=1
r+=1
ws.cell(r,2,"Agrupación: P1=cajón, P2=pack, P3=rack (rack=capa). Lote mínimo/incremento de producción = 1 pallet (la línea libera pallets completos).").font=T(italic=True,size=9)

# ---------- PRUEBAS ----------
ws=wb.create_sheet("Pruebas"); ws.sheet_view.showGridLines=False
for i,ww in enumerate([3,12,16,16,16,16,16,16],1): ws.column_dimensions[get_column_letter(i)].width=ww
r=2
ws.cell(r,2,"ANÁLISIS ESTADÍSTICO FORMAL (ruta del diagrama de flujo)").font=T(bold=True,size=13,color=NAVY); r+=2
cab=["Categoría (dato real KOF)","Rachas p","Kruskal-Wallis p","Levene p","ACF lag-4 (Δserie)","Ljung-Box p","¿Estacional?"]
for j,t in enumerate(cab): hdr(ws.cell(r,2+j),t)
r+=1
for p in ['refrescos','agua','garrafon']:
    q=pruebas[p]
    lbl(ws.cell(r,2),p,b=True)
    val(ws.cell(r,3),q['rachas']['p'],"0.0000"); val(ws.cell(r,4),q['kruskal_wallis']['p'],"0.0000")
    val(ws.cell(r,5),q['levene']['p'],"0.0000"); val(ws.cell(r,6),q['acf_lag4_diff'],"0.000")
    val(ws.cell(r,7),q['ljungbox_lag4_p'],"0.000000")
    lbl(ws.cell(r,8),"SÍ" if q['estacional'] else "NO",b=True)
    r+=1
r+=1
c=ws.cell(r,2); c.value="Conclusión: "+pruebas['conclusion']; c.font=T(italic=True,size=9.5)
ws.merge_cells(start_row=r,start_column=2,end_row=r,end_column=8); ws.row_dimensions[r].height=60
c.alignment=Alignment(wrap_text=True,vertical="top")

# ---------- PRONOSTICO_2026 ----------
ws=wb.create_sheet("Pronostico_2026"); ws.sheet_view.showGridLines=False
for i,ww in enumerate([3,10,14,13,13,12,13,13],1): ws.column_dimensions[get_column_letter(i)].width=ww
r=2
ws.cell(r,2,"PRONÓSTICO abr-2026 → mar-2027 → UNIDADES → EMPAQUE → PALLETS → LOTE (por producto)").font=T(bold=True,size=13,color=NAVY); r+=1
ws.cell(r,2,"Litros = salida Holt-Winters (valores). Conversiones = fórmulas enlazadas a SKUs_Empaques. Lote estándar = ROUNDUP(pallets/corridas,0).").font=T(italic=True,size=9); r+=1
lbl(ws.cell(r,2),"Corridas/mes:"); val(ws.cell(r,3),20,"0",blue=True); ws.cell(r,3).fill=PatternFill("solid",fgColor="FFFF00")
CORR=f"$C${r}"; r+=2
blocks={}
for bi,(p,skurow,agr) in enumerate([('P1',SKU0,'Cajones'),('P2',SKU0+1,'Packs'),('P3',SKU0+2,'Racks')]):
    ws.cell(r,2,f"{p} — {datos[bi][1]}").font=T(bold=True,size=11,color=NAVY); r+=1
    cab=["Mes","Litros","Unidades",agr,"Capas","Pallets","Lote est. (pallets)","Lote est. (und)"]
    for j,t in enumerate(cab): hdr(ws.cell(r,2+j),t)
    r+=1; st=r
    sub=fc[fc.producto==p].reset_index(drop=True)
    for i in range(12):
        lbl(ws.cell(r,2),ETIQ[i])
        val(ws.cell(r,3),round(sub.litros[i]))                     # litros (valor HW)
        fx(ws.cell(r,4),f"=C{r}/SKUs_Empaques!$E${skurow}")        # unidades
        fx(ws.cell(r,5),f"=ROUNDUP(D{r}/SKUs_Empaques!$F${skurow},0)")
        fx(ws.cell(r,6),f"=ROUNDUP(D{r}/SKUs_Empaques!$I${skurow},0)")
        fx(ws.cell(r,7),f"=ROUNDUP(D{r}/SKUs_Empaques!$J${skurow},0)")
        fx(ws.cell(r,8),f"=MAX(1,ROUNDUP(G{r}/{CORR},0))")
        fx(ws.cell(r,9),f"=H{r}*SKUs_Empaques!$J${skurow}")
        if i%2: 
            for cc in range(2,10): ws.cell(r,cc).fill=GREY
        r+=1
    lbl(ws.cell(r,2),"TOTAL",b=True)
    for col in "CDEFG":
        fx(ws.cell(r,{'C':3,'D':4,'E':5,'F':6,'G':7}[col]),f"=SUM({col}{st}:{col}{r-1})")
    for cc in range(2,10): ws.cell(r,cc).fill=SUBF
    blocks[p]=(st,r); r+=2

import json as _json
_json.dump(blocks, open("data/pronostico2026_celdas.json","w"))

# ---------- BACKTEST_TS ----------
ws=wb.create_sheet("Backtest_TS"); ws.sheet_view.showGridLines=False
for i,ww in enumerate([3,8,10,13,13,12,13,12,9,11],1): ws.column_dimensions[get_column_letter(i)].width=ww
r=2
ws.cell(r,2,"EVALUACIÓN DEL ERROR Y SEÑAL DE RASTREO (backtest trimestral: entrena 2021T1–2024T4, prueba 2025T1–2026T1 reales)").font=T(bold=True,size=13,color=NAVY); r+=2
cab=["Prod.","Trim.","Real (L)","Pronóstico (L)","Error (L)","CFE","MAD","TS=CFE/MAD","|TS|≤4"]
for j,t in enumerate(cab): hdr(ws.cell(r,2+j),t)
r+=1
for p in ['P1','P2','P3']:
    sub=bt[bt.producto==p].reset_index(drop=True); st=r
    for i in range(len(sub)):
        lbl(ws.cell(r,2),p); lbl(ws.cell(r,3),str(sub.trimestre[i]))
        val(ws.cell(r,4),int(sub.real[i])); val(ws.cell(r,5),int(sub.pronostico[i]))
        fx(ws.cell(r,6),f"=D{r}-E{r}")
        fx(ws.cell(r,7),f"=SUM($F${st}:F{r})")
        fx(ws.cell(r,8),f"=SUMPRODUCT(ABS($F${st}:F{r}))/(ROW(F{r})-ROW($F${st})+1)")   # array-like; openpyxl ok, LO calc fine
        fx(ws.cell(r,9),f"=G{r}/H{r}","0.00")
        fx(ws.cell(r,10),f'=IF(ABS(I{r})<=4,"SI","NO")',"@")
        if not sub.dentro_limites[i]:
            for cc in range(2,11): ws.cell(r,cc).fill=RED
        r+=1
r+=1
cab2=["Prod.","MAD (L)","CFE (L)","MSE","RMSE (L)","MAPE %","TS final","α","φ"]
for j,t in enumerate(cab2): hdr(ws.cell(r,2+j),t)
r+=1
for p in [k for k in evr if not k.endswith("_MAPE")]:
    e=evr[p]; h=hwp[p]
    if 'alpha' not in h: h=h.get('directo',{'alpha':'','phi':''})
    lbl(ws.cell(r,2),p if p!='P3' else 'P3 (combo directo+agua)',b=True)
    val(ws.cell(r,3),e['MAD']); val(ws.cell(r,4),e['CFE']); val(ws.cell(r,5),e['MSE'])
    val(ws.cell(r,6),e['RMSE']); val(ws.cell(r,7),e['MAPE'],"0.00"); val(ws.cell(r,8),e['TS_final'],"0.00")
    val(ws.cell(r,9),h['alpha'],"0.000"); val(ws.cell(r,10),h['phi'],"0.000")
    r+=1
r+=1
c=ws.cell(r,2); c.value=("Lectura: MAPE 1,9–2,7% trimestral (excelente); validación un-paso 2026T1: +0,07% P1/P2, +0,47% P3. TS<−4 con causa asignable: "
 "quiebre estructural del impuesto saludable en 2025 no observable desde 2022–2024. El modelo de producción, "
 "reentrenado con 2025 (α≈0,98), parte del nivel corregido; la señal debe monitorearse mensualmente en operación.")
c.font=T(italic=True,size=9.5); ws.merge_cells(start_row=r,start_column=2,end_row=r,end_column=10)
c.alignment=Alignment(wrap_text=True,vertical="top"); ws.row_dimensions[r].height=44

# ---------- ROTACION ----------
ws=wb.create_sheet("Rotacion"); ws.sheet_view.showGridLines=False
for i,ww in enumerate([3,12,15,15,15,14,14,14,14,14,14],1): ws.column_dimensions[get_column_letter(i)].width=ww
r=2
ws.cell(r,2,"ROTACIÓN DE INVENTARIOS — lote base = producción de un TURNO").font=T(bold=True,size=13,color=NAVY); r+=1
ws.cell(r,2,"Rotación = Demanda anual ÷ (Lote/2). Cobertura = 365 ÷ Rotación. Escenarios: corrida diaria (≈20/mes), semanal (≈4/mes), mensual (1/mes).").font=T(italic=True,size=9); r+=2
cab=["Prod.","Und/pallet","Demanda anual (und)","Demanda (pallets)","Lote TURNO (pal)","Rot. turno","Cob. días","Lote día 2T (pal)","Rot. día","Lote semanal (pal)","Rot. semanal"]
for j,t in enumerate(cab): hdr(ws.cell(r,2+j),t)
r+=1
for i,p in enumerate(['P1','P2','P3']):
    q=rot[rot.producto==p].iloc[0]; skurow=SKU0+i
    lbl(ws.cell(r,2),p,b=True)
    fx(ws.cell(r,3),f"=SKUs_Empaques!$J${skurow}")
    val(ws.cell(r,4),int(q.demanda_anual_und)); val(ws.cell(r,5),int(q.demanda_anual_pallets))
    val(ws.cell(r,6),int(q.lote_turno_pallets))
    fx(ws.cell(r,7),f"=D{r}/((F{r}*C{r})/2)","0.0")
    fx(ws.cell(r,8),f"=365/G{r}","0.00")
    val(ws.cell(r,9),int(q.lote_dia_2turnos_pallets))
    fx(ws.cell(r,10),f"=D{r}/((I{r}*C{r})/2)","0.0")
    val(ws.cell(r,11),int(q.lote_semanal_pallets))
    fx(ws.cell(r,12),f"=D{r}/((K{r}*C{r})/2)","0.0")
    r+=1

wb.save("Modelo_Fontibon_Operativo.xlsx")
print("OK -> Modelo_Fontibon_Operativo.xlsx")
