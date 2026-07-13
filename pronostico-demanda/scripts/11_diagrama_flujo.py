"""
11_diagrama_flujo.py  (v3 — diagrama corregido)
Diagrama de flujo metodologico en B/N: rectangulos = procesos,
rombos = decisiones, con la respuesta tomada anotada en la flecha.
Salida: figuras/fig_metodologia.png
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch
plt.rcParams.update({'font.family':'serif','figure.dpi':170})

fig,ax=plt.subplots(figsize=(8.2,11.8)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')

def caja(y,txt,h=0.058,w=0.62,fc='0.95'):
    ax.add_patch(FancyBboxPatch((0.5-w/2,y-h/2),w,h,boxstyle="round,pad=0.008",
                 fc=fc,ec='black',lw=1.3))
    ax.text(0.5,y,txt,ha='center',va='center',fontsize=9.2)
def rombo(y,txt,h=0.072,w=0.66):
    ax.add_patch(Polygon([(0.5,y+h/2),(0.5+w/2,y),(0.5,y-h/2),(0.5-w/2,y)],
                 closed=True,fc='0.85',ec='black',lw=1.3))
    ax.text(0.5,y,txt,ha='center',va='center',fontsize=8.8)
def flecha(y1,y2,lbl=None):
    ax.add_patch(FancyArrowPatch((0.5,y1),(0.5,y2),arrowstyle='-|>',
                 mutation_scale=15,color='black',lw=1.2))
    if lbl: ax.text(0.515,(y1+y2)/2,lbl,fontsize=8.4,style='italic',ha='left',va='center')

pasos=[
 ('caja',"1. Necesidad del pronóstico\nPlan de producción abr-2026 → mar-2027 (3 SKU, planta Fontibón)"),
 ('rombo',"2. ¿Existen datos históricos?"),
 ('caja',"3. Datos REALES: 21 trimestres KOF Colombia (2021T1–2026T1)\nTabla «Volumen» por categoría de los 17 reportes trimestrales"),
 ('caja',"4. Análisis de datos\nCorrelación entre categorías · Rachas (aleatoriedad) ·\nKruskal-Wallis (medias) · Levene (varianzas) · Box-Plot"),
 ('rombo',"5. Autocorrelación (serie Δ): ¿constante? ¿tendencia?\n¿ESTACIONALIDAD?"),
 ('caja',"6. Método seleccionado: HOLT-WINTERS multiplicativo (m=4)\ncon tendencia amortiguada φ<1 (conservador)"),
 ('rombo',"7. ¿Cuál distribución del error?\nKolmogorov-Smirnov · Anderson-Darling · χ²"),
 ('caja',"8. Simulación Monte Carlo\nN = 10.000 réplicas → bandas P5–P95"),
 ('caja',"9. Medición del error (backtest 5 trimestres)\nMAD · CFE · MSE · MAPE"),
 ('caja',"10. Señal de rastreo  TS = CFE / MAD, límites ±4\nDetecta el quiebre del impuesto (2025) — causa asignable"),
 ('caja',"11. Validación final: modelo (≤2025T4) vs 1T-2026 REAL\nError +0,07 % (P1, P2) · +0,47 % (P3)"),
 ('caja',"12. PRONÓSTICO abr-2026 → mar-2027\n+ plan en unidades, pallets y lotes"),
]
lbls={1:"Sí (datos reales)",4:"Sí → rezago 4 significativo",6:"Normal aceptada"}
n=len(pasos); ys=[0.965-i*(0.93/(n-1))-0.02 for i in range(n)]
for i,(k,t) in enumerate(pasos):
    (rombo if k=='rombo' else caja)(ys[i],t)
    if i<n-1:
        gap=0.036 if k=='rombo' or pasos[i+1][0]=='rombo' else 0.030
        flecha(ys[i]-gap,ys[i+1]+gap,lbls.get(i))
ax.set_title("Procedimiento formal de selección y validación del método de pronóstico",
             fontsize=11.5,pad=14)
fig.savefig("figuras/fig_metodologia.png",bbox_inches='tight')
print("OK -> figuras/fig_metodologia.png")
