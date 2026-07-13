"""
09_montecarlo.py
Paso del flujo: Simulacion Montecarlo.
Demanda simulada 2026 = pronostico HW x (1 + eps), eps ~ Normal(mu, sigma)
ajustada en 08 (validada con KS/AD/chi2). N=10.000 replicas por producto.
Salidas: data/montecarlo.csv (P5/P50/P95 mensual), figuras/fig_montecarlo.png
"""
import numpy as np, pandas as pd, json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.style.use('grayscale')
plt.rcParams.update({'font.family':'serif','font.size':9,'figure.dpi':150,
                     'axes.grid':True,'grid.alpha':.3})

N = 10_000; rng = np.random.default_rng(42)
fc = pd.read_csv("data/pronostico_2026.csv", parse_dates=['fecha'])
dist = json.load(open("data/distribuciones.json"))
meses = ['Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic','Ene','Feb','Mar']  # abr-26 a mar-27

rows=[]; fig,ax=plt.subplots(1,3,figsize=(11,3.2))
for k,p in enumerate(['P1','P2','P3']):
    base = fc[fc.producto==p].litros.values
    eps = rng.normal(dist[p]['mu'], dist[p]['sigma'], size=(N,12))
    sim = base*(1+eps)
    p5,p50,p95 = np.percentile(sim,[5,50,95],axis=0)
    for i in range(12):
        rows.append(dict(producto=p, mes=meses[i], P5=round(p5[i]),
                         P50=round(p50[i]), P95=round(p95[i]),
                         base_HW=round(base[i])))
    x=np.arange(1,13)
    ax[k].fill_between(x,p5,p95,color='0.85',label='P5–P95')
    ax[k].plot(x,p50,'k-',lw=1.5,label='Mediana')
    ax[k].plot(x,base,'k--',lw=1,label='HW base')
    ax[k].set_title(f"{p} — MC abr-26→mar-27 (N={N:,})".replace(","," "))
    ax[k].set_xticks(x); ax[k].set_xticklabels([m[0] for m in meses])
    ax[k].set_ylabel("Litros/mes")
ax[0].legend(fontsize=7)
fig.tight_layout(); fig.savefig("figuras/fig_montecarlo.png", bbox_inches='tight')
mc=pd.DataFrame(rows); mc.to_csv("data/montecarlo.csv",index=False)
tot=mc.groupby('producto')[['P5','P50','P95']].sum()/1e6
print("Totales anuales 2026 (millones L):\n", tot.round(2))
