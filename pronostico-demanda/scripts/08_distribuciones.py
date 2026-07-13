"""
08_distribuciones.py
Paso del flujo: ¿Cual funcion de distribucion de probabilidad?
Ajuste de distribuciones a los ERRORES RELATIVOS del backtest (real vs
pronostico 2025) y contraste con: Kolmogorov-Smirnov, Anderson-Darling y
Chi-cuadrado. La distribucion elegida alimenta la simulacion Monte Carlo (09).
Salidas: data/distribuciones.json, figuras/fig_hist_dist.png, figuras/fig_qq.png
"""
import numpy as np, pandas as pd, json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

plt.style.use('grayscale')
plt.rcParams.update({'font.family':'serif','font.size':9,'figure.dpi':150,
                     'axes.grid':True,'grid.alpha':.3})

res = {}
fig1, ax1 = plt.subplots(1,3, figsize=(10,3))
fig2, ax2 = plt.subplots(1,3, figsize=(10,3))
for k,p in enumerate(['P1','P2','P3']):
    e = pd.read_csv(f"data/residuos_{p}.csv")['resid_rel'].dropna().values  # n=21 in-sample
    mu, sd = e.mean(), e.std(ddof=1)
    ks = stats.kstest(e, 'norm', args=(mu, sd))
    ad = stats.anderson(e, dist='norm')
    # chi-cuadrado con 4 clases equiprobables (n=12 pequeno)
    edges = stats.norm.ppf(np.linspace(0,1,6)[1:-1], mu, sd)  # 5 clases (n=21)
    obs, _ = np.histogram(e, bins=np.concatenate(([-np.inf], edges, [np.inf])))
    chi2 = stats.chisquare(obs, f_exp=[len(e)/5]*5)
    res[p] = dict(mu=round(float(mu),5), sigma=round(float(sd),5),
                  KS_D=round(float(ks.statistic),4), KS_p=round(float(ks.pvalue),4),
                  AD_A2=round(float(ad.statistic),4),
                  AD_crit_5pct=round(float(ad.critical_values[2]),4),
                  chi2=round(float(chi2.statistic),4), chi2_p=round(float(chi2.pvalue),4),
                  normal_aceptada=bool(ks.pvalue>0.05 and ad.statistic<ad.critical_values[2]))
    # histograma + normal ajustada
    ax1[k].hist(e, bins=6, density=True, edgecolor='black', color='0.8')
    xs = np.linspace(e.min()-.01, e.max()+.01, 200)
    ax1[k].plot(xs, stats.norm.pdf(xs, mu, sd), 'k-', lw=1.5)
    ax1[k].set_title(f"{p}: residuo relativo HW (n=21)\nN(μ={mu:.3f}, σ={sd:.3f})")
    # QQ
    stats.probplot(e, dist="norm", sparams=(mu,sd), plot=ax2[k])
    ax2[k].get_lines()[0].set(marker='o', color='black', ms=4)
    ax2[k].get_lines()[1].set(color='black', ls='--')
    ax2[k].set_title(f"Q-Q {p}")
fig1.tight_layout(); fig1.savefig("figuras/fig_hist_dist.png", bbox_inches='tight')
fig2.tight_layout(); fig2.savefig("figuras/fig_qq.png", bbox_inches='tight')
json.dump(res, open("data/distribuciones.json","w"), indent=1)
for p,r in res.items():
    print(f"{p}: KS p={r['KS_p']} | AD A2={r['AD_A2']} (crit5%={r['AD_crit_5pct']}) | "
          f"chi2 p={r['chi2_p']} -> Normal {'ACEPTADA' if r['normal_aceptada'] else 'RECHAZADA'}")
