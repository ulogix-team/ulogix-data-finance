"""
13_escenarios.py
Motor de escenarios de demanda: aplica FACTORES multiplicativos, documentados
y con fuente, al pronostico base (Holt-Winters, abr-2026->mar-2027) para
simular momentos en que la demanda debe subir o bajar. Cada escenario es
100% reproducible (no aleatorio) salvo las bandas Monte Carlo, que reusan
sigma de data/distribuciones.json centradas en la demanda YA ajustada.

Uso:
  python scripts/13_escenarios.py                  -> corre todos los escenarios
  python scripts/13_escenarios.py "Mundial 2026"    -> corre solo uno (opcional)

Salidas:
  data/escenarios_demanda.csv   (mensual, litros y unidades, por escenario)
  data/escenarios_resumen.csv   (totales anuales y variacion % vs Base)
  figuras/fig_escenarios.png    (comparacion visual por producto)

Como agregar un escenario propio: añadir una entrada al diccionario ESCENARIOS
con un factor por mes y producto (1.00 = sin cambio) y una fuente/justificacion.
Los meses siguen el orden del pronostico: Abr-26 ... Mar-27 (indices 0..11).
"""
import sys, json, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.style.use('grayscale')
plt.rcParams.update({'font.family':'serif','font.size':9,'figure.dpi':150,
                     'axes.grid':True,'grid.alpha':.3})

MESES = ['Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic','Ene','Feb','Mar']
UNO = [1.00]*12

def f(base=1.0, overrides=None):
    """Crea un vector de 12 factores; overrides = dict {indice_mes(0=Abr): factor}."""
    v = [base]*12
    for k, val in (overrides or {}).items():
        v[int(k)] = val
    return v

# ============================================================================
# ESCENARIOS (documentados). Indices de mes: 0=Abr-26 ... 11=Mar-27.
# ============================================================================
ESCENARIOS = {
 "Base": {
   "descripcion": "Pronostico oficial del proyecto, sin ajuste.",
   "P1": UNO, "P2": UNO, "P3": UNO,
 },
 "Mundial 2026": {
   "descripcion": ("Upside NO incluido en el escenario base (ver S6, reporte v3): "
     "KOF definio un plan comercial explicito para el Mundial FIFA (11-jun al 19-jul-2026) [12],[13],[20]. "
     "Se modela un incremento en jun (idx2) y jul (idx3) para las gaseosas; el garrafon casi no participa "
     "de este efecto (r=0,12 con refrescos, Sec. VI del reporte)."),
   "P1": f(1.00, {2:1.06, 3:1.10, 4:1.02}),
   "P2": f(1.00, {2:1.06, 3:1.10, 4:1.02}),
   "P3": f(1.00, {2:1.01, 3:1.02}),
 },
 "Paro nacional / choque logistico": {
   "descripcion": ("Disrupcion de transporte de ~2 semanas (paro camionero o de orden publico, "
     "recurrentes en Colombia) que impide despachar en un mes cualquiera del horizonte. "
     "Se ilustra en agosto (idx4): -18% en las tres lineas por perdida de dias habiles de despacho; "
     "octubre (idx6) recupera parcialmente (+4%) por recuperacion de pedidos representados."),
   "P1": f(1.00, {4:0.82, 6:1.04}),
   "P2": f(1.00, {4:0.82, 6:1.04}),
   "P3": f(1.00, {4:0.82, 6:1.04}),
 },
 "Recesion moderada": {
   "descripcion": ("Desaceleracion economica sostenida (caida de ingreso disponible): elasticidad-ingreso "
     "positiva de bebidas no esenciales. Se aplica -5% sostenido en gaseosas desde jun (idx2) en adelante; "
     "el garrafon (bien mas inelastico, consumo basico de agua) se reduce solo -2%."),
   "P1": f(1.00, {i:0.95 for i in range(2,12)}),
   "P2": f(1.00, {i:0.95 for i in range(2,12)}),
   "P3": f(1.00, {i:0.98 for i in range(2,12)}),
 },
 "Restriccion hidrica adicional (CAR)": {
   "descripcion": ("Endurecimiento de la Resolucion CAR 347/2026 sobre concesion de aguas en La Calera "
     "[Ref 12, reporte]: reduccion adicional de suministro que golpea especificamente al garrafon. "
     "-15% sostenido en P3 desde el mes de vigencia estimado (jul, idx3); P1/P2 no afectados "
     "(abastecimiento de acueducto, no de manantial)."),
   "P1": UNO, "P2": UNO,
   "P3": f(1.00, {i:0.85 for i in range(3,12)}),
 },
 "Repunte agresivo post-impuesto": {
   "descripcion": ("Escenario optimista alterno: la recuperacion de refrescos tras el impuesto saludable "
     "(Sec. V.C, +9,2% interanual real en 1T-2026 [21]) se sostiene mas alla de lo asumido en el modelo "
     "base (que ya es conservador, phi<1). +5% sostenido en gaseosas todo el horizonte."),
   "P1": f(1.05), "P2": f(1.05), "P3": list(UNO),
 },
}

def cargar_base():
    fc = pd.read_csv("data/pronostico_2026.csv", parse_dates=['fecha'])
    envase = {'P1':0.35,'P2':1.5,'P3':25.0}
    return fc, envase

def aplicar_escenarios():
    fc, envase = cargar_base()
    dist = json.load(open("data/distribuciones.json"))
    rng = np.random.default_rng(42)
    N = 10_000

    filas, resumen = [], []
    for nombre, esc in ESCENARIOS.items():
        for p in ['P1','P2','P3']:
            base = fc[fc.producto==p].sort_values('fecha').reset_index(drop=True)
            factor = esc[p]
            lit_aj = base.litros.values * np.array(factor)
            und_aj = lit_aj / envase[p]
            for i in range(12):
                filas.append(dict(escenario=nombre, producto=p, mes=MESES[i],
                                  fecha=base.fecha[i].date().isoformat(),
                                  factor=factor[i], litros_base=round(base.litros[i]),
                                  litros_escenario=round(lit_aj[i]),
                                  unidades_escenario=round(und_aj[i])))
            tot_base = base.litros.sum(); tot_esc = lit_aj.sum()
            # Monte Carlo del escenario (misma sigma, centrado en la demanda ajustada)
            eps = rng.normal(dist[p]['mu'], dist[p]['sigma'], size=(N,12))
            sim = lit_aj*(1+eps)
            p5, p50, p95 = np.percentile(sim.sum(axis=1), [5,50,95])
            resumen.append(dict(escenario=nombre, producto=p,
                                total_anual_base_L=round(tot_base),
                                total_anual_escenario_L=round(tot_esc),
                                delta_pct=round((tot_esc/tot_base-1)*100,2),
                                MC_P5_L=round(p5), MC_P50_L=round(p50), MC_P95_L=round(p95),
                                descripcion=esc["descripcion"]))
    return pd.DataFrame(filas), pd.DataFrame(resumen)

def graficar(df):
    fig, ax = plt.subplots(1,3, figsize=(12,3.4))
    estilos = ['-','--','-.',':','-','--']
    for k,p in enumerate(['P1','P2','P3']):
        for i,esc in enumerate(ESCENARIOS):
            sub = df[(df.producto==p)&(df.escenario==esc)]
            ax[k].plot(range(1,13), sub.litros_escenario.values/1e6,
                      estilos[i%len(estilos)], lw=1.3 if esc=="Base" else 1.0,
                      color='black' if esc=="Base" else str(0.15+0.13*i),
                      label=esc)
        ax[k].set_xticks(range(1,13)); ax[k].set_xticklabels([m[0] for m in MESES])
        ax[k].set_title(p); ax[k].set_ylabel("Litros/mes (M)")
    ax[0].legend(fontsize=6, loc='upper left')
    fig.suptitle("Escenarios de demanda — factores aplicados al pronóstico base", y=1.04)
    fig.tight_layout()
    fig.savefig("figuras/fig_escenarios.png", bbox_inches='tight')

if __name__ == "__main__":
    solo = sys.argv[1] if len(sys.argv) > 1 else None
    if solo:
        if solo not in ESCENARIOS:
            sys.exit(f"Escenario no encontrado. Opciones: {list(ESCENARIOS)}")
        ESCENARIOS_ORIG = dict(ESCENARIOS)
        for k in list(ESCENARIOS):
            if k not in ("Base", solo): del ESCENARIOS[k]

    dfm, dfr = aplicar_escenarios()
    dfm.to_csv("data/escenarios_demanda.csv", index=False)
    dfr.to_csv("data/escenarios_resumen.csv", index=False)
    graficar(dfm)

    print(f"{len(ESCENARIOS)} escenarios calculados: {list(ESCENARIOS)}\n")
    piv = dfr.pivot_table(index='escenario', columns='producto', values='delta_pct')
    print("Variación % vs Base (litros/año) por producto:")
    print(piv.round(1).to_string())
    print("\nOK -> data/escenarios_demanda.csv, data/escenarios_resumen.csv, figuras/fig_escenarios.png")
