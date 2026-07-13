"""
03_modelo_holt_winters.py  (v3 — P3 ligado a la demanda de AGUA)
P1/P2: Holt-Winters amortiguado sobre su serie (refrescos x empaque).
P3 (garrafon): el garrafon ES agua, pero el multivariado muestra que es un
segmento casi independiente (r=0,12-0,20 con agua personal). Se usan DOS modelos
y la COMBINACION de pronosticos (Bates & Granger, 1969) como oficial:
  (a) DIRECTO: HW amortiguado sobre la serie garrafon (mejor backtest);
  (b) LIGADO AL AGUA: W=Agua+Garrafon (HW m=4) x share garrafon (SES) —
      incorpora la tendencia/estacionalidad del mercado de agua;
  P3 oficial = (a+b)/2. Los tres se evaluan en el backtest (script 04).
Holt-Winters multiplicativo con tendencia amortiguada sobre la serie
trimestral REAL (2021T1-2026T1). Validacion adicional: el modelo entrenado
hasta 2025T4 predice 2026T1 y se compara contra el dato real observado.
Pronostico final: 4 trimestres (2026T2-2027T1), desagregado a 12 meses
(abr-2026 a mar-2027) con los pesos intra-trimestre W.
Salidas: data/pronostico_trimestral.csv, data/pronostico_2026.csv (mensual),
         data/hw_parametros.json, data/validacion_2026T1.json
"""
import numpy as np, pandas as pd, json
from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing

ENVASE={'P1':0.35,'P2':1.5,'P3':25.0}
W={int(k):v for k,v in json.load(open('data/parametros.json'))['W'].items()}
HORIZONTE=[(2026,2),(2026,3),(2026,4),(2027,1)]

def serieQ():
    dq=pd.read_csv("data/historico_trimestral_planta.csv")
    dq['t']=pd.PeriodIndex([f"{y}Q{q}" for y,q in zip(dq.anio,dq.trim)],freq='Q').to_timestamp()
    return dq.pivot_table(index='t',columns='producto',values='litros').asfreq('QS')

def modelo_P3_compuesto(hasta=None, horizonte=4):
    """Devuelve (fcst_litros_P3, fitted_litros_P3, params, series_reales_P3_litros)."""
    kof=json.load(open("data/kof_trimestral_colombia.json"))
    par=json.load(open("data/parametros.json"))
    esc=par['SHARE']['P3']*par['L_CU']*1e6           # MCU garrafon -> litros planta
    df=pd.DataFrame([dict(k=k,**v) for k,v in sorted(kof.items())])
    df['t']=pd.PeriodIndex(df.k,freq='Q').to_timestamp()
    df=df.set_index('t')
    if hasta is not None: df=df[:hasta]
    W=(df['agua']+df['garrafon']).asfreq('QS')       # agua TOTAL (MCU)
    s=(df['garrafon']/(df['agua']+df['garrafon'])).asfreq('QS')
    mW=ExponentialSmoothing(W,trend='add',damped_trend=True,seasonal='mul',
                            seasonal_periods=4,initialization_method='estimated').fit()
    mS=SimpleExpSmoothing(s,initialization_method='estimated').fit()
    fc=(mW.forecast(horizonte).values*float(mS.forecast(1).iloc[0]))*esc
    fitted=(mW.fittedvalues*mS.fittedvalues).values*esc
    pr=dict(alpha_W=round(mW.params['smoothing_level'],4),beta_W=round(mW.params['smoothing_trend'],4),
            gamma_W=round(mW.params['smoothing_seasonal'],4),phi_W=round(mW.params['damping_trend'],4),
            alpha_s=round(mS.params['smoothing_level'],4),share_fcst=round(float(mS.forecast(1).iloc[0]),4))
    return fc, fitted, pr, (df['garrafon'].values*esc)

if __name__=="__main__":
    piv=serieQ(); params={}; fcQ={}; val={}
    for p in ['P1','P2']:
        # validacion un paso: entrena hasta 2025T4, predice 2026T1 real
        tr=piv[p][:'2025-10-01']
        m1=ExponentialSmoothing(tr,trend='add',damped_trend=True,seasonal='mul',
                                seasonal_periods=4,initialization_method='estimated').fit()
        pred1=float(m1.forecast(1).iloc[0]); real1=float(piv[p].iloc[-1])
        val[p]=dict(pred_2026T1=round(pred1),real_2026T1=round(real1),
                    error_pct=round((pred1/real1-1)*100,2))
        # modelo final con toda la serie
        m=ExponentialSmoothing(piv[p],trend='add',damped_trend=True,seasonal='mul',
                               seasonal_periods=4,initialization_method='estimated').fit()
        params[p]=dict(alpha=round(m.params['smoothing_level'],4),
                       beta=round(m.params['smoothing_trend'],4),
                       gamma=round(m.params['smoothing_seasonal'],4),
                       phi=round(m.params['damping_trend'],4),AIC=round(m.aic,1))
        fcQ[p]=m.forecast(4).values
        fitted=m.fittedvalues
        resid=(piv[p]-fitted)/fitted
        pd.DataFrame({'resid_rel':resid}).to_csv(f"data/residuos_{p}.csv")
    # ---- P3: directo + ligado-al-agua + COMBINACION oficial ----
    ser3=piv['P3']
    # (a) directo
    trD=ser3[:'2025-10-01']
    mD1=ExponentialSmoothing(trD,trend='add',damped_trend=True,seasonal='mul',
                             seasonal_periods=4,initialization_method='estimated').fit()
    predD1=float(mD1.forecast(1).iloc[0])
    mD=ExponentialSmoothing(ser3,trend='add',damped_trend=True,seasonal='mul',
                            seasonal_periods=4,initialization_method='estimated').fit()
    fcD=mD.forecast(4).values; fitD=mD.fittedvalues.values
    # (b) ligado al agua
    fcA1,_,_,_ = modelo_P3_compuesto(hasta='2025-10-01',horizonte=1)
    fcA,fitA,prA,realL = modelo_P3_compuesto()
    # combinacion 50/50
    real1=float(ser3.iloc[-1]); pred1=(predD1+float(fcA1[0]))/2
    val['P3']=dict(pred_2026T1=round(pred1),real_2026T1=round(real1),
                   error_pct=round((pred1/real1-1)*100,2),
                   detalle=dict(directo_pct=round((predD1/real1-1)*100,2),
                                agua_pct=round((float(fcA1[0])/real1-1)*100,2)))
    fcQ['P3']=(fcD+fcA)/2
    params['P3']=dict(metodo="combinacion 50/50 (Bates-Granger)",
                      directo=dict(alpha=round(mD.params['smoothing_level'],4),
                                   phi=round(mD.params['damping_trend'],4)),
                      ligado_agua=prA)
    fit3=(fitD+fitA)/2; resid3=(realL-fit3)/fit3
    pd.DataFrame({'resid_rel':resid3}).to_csv("data/residuos_P3.csv")
    # trimestral
    rowsQ=[]
    for i,(y,q) in enumerate(HORIZONTE):
        for p in ['P1','P2','P3']:
            rowsQ.append(dict(anio=y,trim=q,producto=p,litros=round(fcQ[p][i],1)))
    pd.DataFrame(rowsQ).to_csv("data/pronostico_trimestral.csv",index=False)
    # mensual abr26-mar27
    rowsM=[]
    for i,(y,q) in enumerate(HORIZONTE):
        for j,w in enumerate(W[q]):
            mes=(q-1)*3+j+1
            for p in ['P1','P2','P3']:
                lit=fcQ[p][i]*w
                rowsM.append(dict(fecha=f"{y}-{mes:02d}-01",producto=p,
                                  litros=round(lit,1),
                                  unidades=round(lit/ENVASE[p])))
    fm=pd.DataFrame(rowsM); fm.to_csv("data/pronostico_2026.csv",index=False)
    json.dump(params,open("data/hw_parametros.json","w"),indent=1)
    json.dump(val,open("data/validacion_2026T1.json","w"),indent=1)
    print("P3 compuesto: agua total (HW) x share garrafon (SES) — garrafon ligado a demanda de agua")
    print("Validacion un-paso (train<=2025T4 -> 2026T1 real):")
    for p,v in val.items(): print(f"  {p}: pred={v['pred_2026T1']:,} vs real={v['real_2026T1']:,}  ({v['error_pct']:+.2f}%)")
    print("\nParametros:",json.dumps(params))
    tot=fm.groupby('producto').litros.sum()/1e6
    print("\nTotal abr-2026→mar-2027 (M L):",tot.round(2).to_dict())
