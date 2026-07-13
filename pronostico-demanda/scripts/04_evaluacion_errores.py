"""
04_evaluacion_errores.py  (v2 — backtest trimestral)
Backtest: entrena 2021T1-2024T4 (16 trim.), prueba 2025T1-2026T1 (5 trim. REALES).
Metricas: MAD, CFE, MSE, RMSE, MAPE. Senal de rastreo TS=CFE/MAD, limites +/-4.
"""
import numpy as np, pandas as pd, json
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import importlib.util as _il
_spec=_il.spec_from_file_location("m03","scripts/03_modelo_holt_winters.py")
_m03=_il.module_from_spec(_spec); _spec.loader.exec_module(_m03)

def serieQ():
    dq=pd.read_csv("data/historico_trimestral_planta.csv")
    dq['t']=pd.PeriodIndex([f"{y}Q{q}" for y,q in zip(dq.anio,dq.trim)],freq='Q').to_timestamp()
    return dq.pivot_table(index='t',columns='producto',values='litros').asfreq('QS')

if __name__=="__main__":
    piv=serieQ(); filas=[]; resumen={}
    etiquetas=['2025T1','2025T2','2025T3','2025T4','2026T1']
    for p in ['P1','P2','P3']:
        tr,te=piv[p][:'2024-10-01'],piv[p]['2025-01-01':]
        if p=='P3':
            mDb=ExponentialSmoothing(tr,trend='add',damped_trend=True,seasonal='mul',
                                     seasonal_periods=4,initialization_method='estimated').fit()
            predD=mDb.forecast(len(te)).values
            fcA,_,_,_=_m03.modelo_P3_compuesto(hasta='2024-10-01',horizonte=len(te))
            comparacion={}
            for nom,pv in [('P3_directo',predD),('P3_ligado_agua',np.asarray(fcA)),
                           ('P3_combinado',(predD+np.asarray(fcA))/2)]:
                ee=te.values-pv
                comparacion[nom]=round(float((np.abs(ee)/te.values).mean()*100),2)
            resumen['P3_comparacion_MAPE']=comparacion
            pred=pd.Series((predD+np.asarray(fcA))/2,index=te.index)
        else:
            m=ExponentialSmoothing(tr,trend='add',damped_trend=True,seasonal='mul',
                                   seasonal_periods=4,initialization_method='estimated').fit()
            pred=m.forecast(len(te))
        e=te.values-pred.values; cfe=np.cumsum(e)
        mad=np.array([np.abs(e[:i+1]).mean() for i in range(len(e))])
        ts=cfe/mad
        for i in range(len(e)):
            filas.append(dict(producto=p,trimestre=etiquetas[i],real=round(te.values[i]),
                              pronostico=round(pred.values[i]),error=round(e[i]),
                              CFE=round(cfe[i]),MAD=round(mad[i]),TS=round(ts[i],2),
                              dentro_limites=bool(abs(ts[i])<=4)))
        resumen[p]=dict(MAD=round(float(np.abs(e).mean())),CFE=round(float(cfe[-1])),
                        MSE=round(float((e**2).mean())),RMSE=round(float(np.sqrt((e**2).mean()))),
                        MAPE=round(float((np.abs(e)/te.values).mean()*100),2),
                        TS_final=round(float(ts[-1]),2),TS_max_abs=round(float(np.abs(ts).max()),2),
                        senal_ok=bool(np.abs(ts).max()<=4))
    pd.DataFrame(filas).to_csv("data/evaluacion_backtest.csv",index=False)
    json.dump(resumen,open("data/evaluacion_resumen.json","w"),indent=1)
    for p,r in resumen.items():
        if 'MAPE' not in r:
            print(f"{p}: {r}"); continue
        print(f"{p}: MAPE={r['MAPE']}% MAD={r['MAD']:,}L CFE={r['CFE']:,}L "
              f"TSmax={r['TS_max_abs']} -> {'OK' if r['senal_ok'] else 'FUERA (causa asignable: impuesto 2025)'}")
