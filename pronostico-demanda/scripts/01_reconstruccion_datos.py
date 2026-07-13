"""
01_reconstruccion_datos.py  (v2 — datos trimestrales REALES)
Serie trimestral de volumen de Colombia extraida de los 17 Reportes de
Resultados Trimestrales de Coca-Cola FEMSA (1T-2022 a 1T-2026), tabla
"Volumen" por pais: Refrescos | Agua | Garrafon | Otros | Total (MCU).
Las columnas comparativas de los reportes 2022 extienden la serie a 2021.
Total: 21 trimestres reales (2021T1-2026T1).
Escala planta Fontibon: P1=Refrescos*34%*share, P2=Refrescos*66%*share,
P3=Garrafon*share. Desagregacion mensual con pesos intra-trimestre
documentados (patron de consumo; supuesto S4').
Salidas: data/historico_trimestral_planta.csv, data/historico_planta.csv (mensual)
"""
import numpy as np, pandas as pd, json, os

L_CU = 24*8*0.0295735
RET, NR = 0.34, 0.66                      # mezcla empaque carbonatadas (Informe Integrado 2025)
BOG_SHARE = 0.17
CAPT = {'P1':.70,'P2':.45,'P3':.50}
SHARE = {p: BOG_SHARE*c for p,c in CAPT.items()}
ENVASE = {'P1':0.35,'P2':1.5,'P3':25.0}
# pesos intra-trimestre (normalizados por trimestre; patron doc. consumo)
W = {1:[.337,.315,.348], 2:[.323,.333,.343], 3:[.349,.329,.322], 4:[.309,.325,.366]}
W = {q:[x/sum(w) for x in w] for q,w in W.items()}   # normalizados a suma exacta 1

def construir():
    kof = json.load(open("data/kof_trimestral_colombia.json"))
    rowsQ, rowsM = [], []
    for key,d in sorted(kof.items()):
        y,q = int(key[:4]), int(key[-1])
        univ = {'P1': d['refrescos']*RET, 'P2': d['refrescos']*NR, 'P3': d['garrafon']}  # MCU
        for p,mcu in univ.items():
            litQ = mcu*1e6*L_CU*SHARE[p]
            rowsQ.append(dict(anio=y,trim=q,producto=p,MCU_universo=round(mcu,2),
                              litros=round(litQ,1),
                              unidades=round(litQ/ENVASE[p])))
            for j,w in enumerate(W[q]):
                mes=(q-1)*3+j+1
                litM=litQ*w
                rowsM.append(dict(fecha=f"{y}-{mes:02d}-01",producto=p,
                                  litros=round(litM,1),
                                  unidades=round(litM/ENVASE[p])))
    dq=pd.DataFrame(rowsQ); dm=pd.DataFrame(rowsM)
    dm['fecha']=pd.to_datetime(dm['fecha'])
    return dq,dm

if __name__=="__main__":
    os.makedirs("data",exist_ok=True)
    dq,dm=construir()
    dq.to_csv("data/historico_trimestral_planta.csv",index=False)
    dm.to_csv("data/historico_planta.csv",index=False)
    json.dump(dict(SHARE=SHARE,ENVASE=ENVASE,L_CU=L_CU,RET=RET,NR=NR,W=W),
              open("data/parametros.json","w"),indent=1)
    print(dq.pivot_table(index=['anio'],columns='producto',values='litros',aggfunc='sum').round(0))
    print(f"\n{dq.anio.nunique()} anios, {len(dq)//3} trimestres reales. OK")
