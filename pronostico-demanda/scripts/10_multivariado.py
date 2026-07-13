"""
10_multivariado.py  (v2 — sobre categorias trimestrales REALES de KOF Colombia)
Box-Plot por trimestre, correlacion entre categorias, ACF de la serie
diferenciada, descomposicion, PCA. Figuras B/N.
"""
import numpy as np, pandas as pd, json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
plt.style.use('grayscale')
plt.rcParams.update({'font.family':'serif','font.size':9,'figure.dpi':150,
                     'axes.grid':True,'grid.alpha':.3})

kof=json.load(open("data/kof_trimestral_colombia.json"))
df=pd.DataFrame([dict(anio=int(k[:4]),trim=int(k[-1]),**v) for k,v in sorted(kof.items())])
df['t']=pd.PeriodIndex([f"{y}Q{q}" for y,q in zip(df.anio,df.trim)],freq='Q').to_timestamp()
df=df.set_index('t')
fcq=pd.read_csv("data/pronostico_trimestral.csv")
fcq['t']=pd.PeriodIndex([f"{y}Q{q}" for y,q in zip(fcq.anio,fcq.trim)],freq='Q').to_timestamp()
hq=pd.read_csv("data/historico_trimestral_planta.csv")
hq['t']=pd.PeriodIndex([f"{y}Q{q}" for y,q in zip(hq.anio,hq.trim)],freq='Q').to_timestamp()
pivP=hq.pivot_table(index='t',columns='producto',values='litros')

# Serie planta trimestral + pronostico
fig,ax=plt.subplots(3,1,figsize=(9,7))
for k,p in enumerate(['P1','P2','P3']):
    ax[k].plot(pivP.index,pivP[p]/1e6,'k-o',ms=3,lw=1.2,label='Trimestral real (KOF)')
    f=fcq[fcq.producto==p]
    ax[k].plot(f.t,f.litros/1e6,'k--s',ms=3,lw=1.2,label='Pronóstico 2026T2–2027T1')
    ax[k].set_ylabel(f"{p} (M L/trim)"); ax[k].legend(fontsize=7,loc='upper left')
fig.suptitle("Demanda trimestral — planta Fontibón (2021T1–2027T1)")
fig.tight_layout(); fig.savefig("figuras/fig_series.png",bbox_inches='tight')

# Box-Plot por trimestre (universo refrescos, dato real)
fig,ax=plt.subplots(figsize=(7,3))
df.boxplot(column='refrescos',by='trim',ax=ax,grid=True,
           boxprops=dict(color='black'),medianprops=dict(color='black'))
ax.set_title("Box-Plot por trimestre — Refrescos Colombia (MCU, 2021–2026)")
plt.suptitle(""); ax.set_xlabel("Trimestre"); ax.set_ylabel("MCU")
fig.tight_layout(); fig.savefig("figuras/fig_boxplot_mes.png",bbox_inches='tight')

# Correlacion categorias reales
cats=['refrescos','agua','garrafon','otros']
corr=df[cats].corr()
fig,ax=plt.subplots(figsize=(4.2,3.4))
im=ax.imshow(corr,cmap='gray_r',vmin=0,vmax=1)
ax.set_xticks(range(4),cats,rotation=30); ax.set_yticks(range(4),cats)
for i in range(4):
    for j in range(4):
        ax.text(j,i,f"{corr.iloc[i,j]:.2f}",ha='center',va='center',
                color='white' if corr.iloc[i,j]>.55 else 'black',fontsize=8)
ax.set_title("Correlación entre categorías (datos reales)")
fig.colorbar(im,fraction=.046); fig.tight_layout()
fig.savefig("figuras/fig_corr.png",bbox_inches='tight')

# ACF de la serie diferenciada (refrescos)
d=np.diff(df['refrescos'].values)
fig,ax=plt.subplots(1,2,figsize=(9,3))
plot_acf(d,lags=8,ax=ax[0],color='black',vlines_kwargs={'colors':'black'})
plot_pacf(d,lags=8,ax=ax[1],color='black',method='ywm',vlines_kwargs={'colors':'black'})
ax[0].set_title("ACF Δrefrescos (pico rezago 4 → estacionalidad)")
ax[1].set_title("PACF Δrefrescos")
fig.tight_layout(); fig.savefig("figuras/fig_acf.png",bbox_inches='tight')

# Descomposicion trimestral refrescos
dec=seasonal_decompose(df['refrescos'],model='multiplicative',period=4)
fig=dec.plot(); fig.set_size_inches(8,6)
for a in fig.axes:
    for l in a.get_lines(): l.set_color('black')
fig.suptitle("Descomposición multiplicativa — Refrescos Colombia (trimestral)",y=1.01)
fig.tight_layout(); fig.savefig("figuras/fig_descomposicion.png",bbox_inches='tight')

# PCA categorias reales
X=StandardScaler().fit_transform(df[cats].values)
pca=PCA().fit(X); evr=pca.explained_variance_ratio_; Z=pca.transform(X)
fig,ax=plt.subplots(1,2,figsize=(9,3))
ax[0].bar(range(1,5),evr*100,color='0.6',edgecolor='black')
ax[0].set_xticks(range(1,5)); ax[0].set_xlabel("Componente"); ax[0].set_ylabel("% varianza")
ax[0].set_title(f"Scree: PC1 explica {evr[0]*100:.1f}%")
ax[1].scatter(Z[:,0],Z[:,1],c='black',s=14)
for i,c in enumerate(cats):
    ax[1].arrow(0,0,pca.components_[0,i]*2.6,pca.components_[1,i]*2.6,head_width=.07,color='black')
    ax[1].text(pca.components_[0,i]*3.0,pca.components_[1,i]*3.0,c,fontsize=8)
ax[1].set_xlabel("PC1"); ax[1].set_ylabel("PC2"); ax[1].set_title("Biplot PCA (categorías)")
fig.tight_layout(); fig.savefig("figuras/fig_pca.png",bbox_inches='tight')
json.dump(dict(varianza_explicada=[round(float(v),4) for v in evr],
               correlacion=corr.round(3).to_dict()),open("data/pca.json","w"),indent=1)
print("Corr:\n",corr.round(2)); print("PCA:",[f"{v*100:.1f}%" for v in evr]); print("Figuras OK")
