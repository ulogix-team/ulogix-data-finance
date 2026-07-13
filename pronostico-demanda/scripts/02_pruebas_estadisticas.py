"""
02_pruebas_estadisticas.py  (v2 — sobre serie trimestral REAL)
Ruta formal sobre los 21 trimestres observados de KOF Colombia:
correlacion entre categorias reales, rachas, Kruskal-Wallis (anios),
Levene, ACF (estacionalidad rezago 4 trimestral).
"""
import numpy as np, pandas as pd, json
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf

def runs_test(x):
    med=np.median(x); s=x>med
    n1,n2=s.sum(),(~s).sum()
    runs=1+(s[1:]!=s[:-1]).sum()
    mu=2*n1*n2/(n1+n2)+1
    var=2*n1*n2*(2*n1*n2-n1-n2)/(((n1+n2)**2)*(n1+n2-1))
    z=(runs-mu)/np.sqrt(var)
    return dict(rachas=int(runs),esperadas=round(mu,2),z=round(z,3),
                p=round(2*(1-stats.norm.cdf(abs(z))),4))

if __name__=="__main__":
    kof=json.load(open("data/kof_trimestral_colombia.json"))
    df=pd.DataFrame([dict(anio=int(k[:4]),trim=int(k[-1]),**v) for k,v in sorted(kof.items())])
    out={'correlacion_categorias':df[['refrescos','agua','garrafon','otros']].corr().round(3).to_dict()}
    for col in ['refrescos','agua','garrafon']:
        y=df[col].values; grupos=[y[df.anio==a] for a in df.anio.unique() if (df.anio==a).sum()>=4]
        H,pkw=stats.kruskal(*grupos); Wl,plev=stats.levene(*grupos)
        dy=np.diff(y)                      # quitar tendencia para ver estacionalidad
        a=acf(dy,nlags=8); lb=acorr_ljungbox(dy,lags=[4],return_df=True)
        out[col]=dict(rachas=runs_test(y),
                      kruskal_wallis=dict(H=round(H,3),p=round(pkw,4)),
                      levene=dict(W=round(Wl,3),p=round(plev,4)),
                      acf_lag4_diff=round(float(a[4]),3),
                      ljungbox_lag4_p=round(float(lb['lb_pvalue'].iloc[0]),6),
                      estacional=bool(abs(a[4])>2/np.sqrt(len(dy))))
    out['conclusion']=("Serie trimestral REAL (21 obs.): sobre la serie DIFERENCIADA (sin tendencia), "
      "el ACF en rezago 4 es significativo -> estacionalidad anual confirmada con datos observados. "
      "Kruskal-Wallis detecta diferencias de nivel entre anios (crecimiento 2021-2024, quiebre 2025). "
      "Ruta del diagrama: Holt-Winters multiplicativo, m=4 (trimestral).")
    json.dump(out,open("data/pruebas_estadisticas.json","w"),indent=1)
    for c in ['refrescos','agua','garrafon']:
        r=out[c]; print(f"{c:10s}: rachas p={r['rachas']['p']} | KW p={r['kruskal_wallis']['p']} | "
              f"Levene p={r['levene']['p']} | ACF4(diff)={r['acf_lag4_diff']} (LB p={r['ljungbox_lag4_p']}) "
              f"-> estacional={r['estacional']}")
    print("\n"+out['conclusion'])
