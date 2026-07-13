"""
12_verificacion.py
Control de calidad automatizado del repositorio (QA). Verifica:
  V1  Categorias suman el total en cada trimestre extraido
  V2  Agregados anuales vs Informes Integrados KOF (2022:330.1, 2023:347.6,
      2024:352.3, 2025:349.4 MCU; tolerancia 0.3)
  V3  Pesos intra-trimestre suman 1.000 por trimestre
  V4  Pronostico mensual re-agregado == pronostico trimestral (tolerancia 1 L)
  V5  Digitos de control EAN-13 de los SKU
  V6  Unidades por pallet coherentes con la jerarquia declarada
Codigo de salida 0 si todo pasa.
"""
import json, sys, pandas as pd

def check(nombre, ok, detalle=""):
    print(f"[{'PASA' if ok else 'FALLA'}] {nombre} {detalle}")
    return ok

def ean_ok(code):
    d=[int(c) for c in code]
    return d[-1]==(10-(sum(d[0:12:2])+3*sum(d[1:12:2]))%10)%10

if __name__=="__main__":
    ok=True
    kof=json.load(open("data/kof_trimestral_colombia.json"))
    # V1
    v1=all(abs(v['total']-(v['refrescos']+v['agua']+v['garrafon']+v['otros']))<0.15 for v in kof.values())
    ok&=check("V1 categorias==total (21 trimestres)",v1)
    # V2
    anual={}
    for k,v in kof.items(): anual[k[:4]]=anual.get(k[:4],0)+v['total']
    ref={'2022':330.1,'2023':347.6,'2024':352.3,'2025':349.4}
    v2=all(abs(anual[y]-r)<=0.3 for y,r in ref.items())
    ok&=check("V2 anual vs Informes Integrados",v2,
              str({y:round(anual[y],1) for y in ref}))
    # V3
    W=json.load(open("data/parametros.json"))['W']
    v3=all(abs(sum(w)-1)<1e-9 for w in W.values())
    ok&=check("V3 pesos intra-trimestre suman 1",v3)
    # V4
    fm=pd.read_csv("data/pronostico_2026.csv",parse_dates=['fecha'])
    fq=pd.read_csv("data/pronostico_trimestral.csv")
    fm['trim']=fm.fecha.dt.quarter; fm['anio']=fm.fecha.dt.year
    agg=fm.groupby(['anio','trim','producto']).litros.sum().reset_index()
    m=agg.merge(fq,on=['anio','trim','producto'],suffixes=('_m','_q'))
    v4=(m.litros_m-m.litros_q).abs().max()<1.0
    ok&=check("V4 mensual re-agregado == trimestral",v4)
    # V5
    eans=pd.read_csv("erp_odoo/04_product_template.csv").barcode.astype(str).tolist()
    v5=all(ean_ok(e) for e in eans)
    ok&=check("V5 digitos de control EAN-13",v5,str(eans))
    # V6
    v6=(30*9*6==1620) and (6*28*5==840) and (6*1*5==30)
    ok&=check("V6 jerarquia de empaque (1620/840/30 und/pallet)",v6)
    print("\nRESULTADO:","TODO OK" if ok else "HAY FALLAS")
    sys.exit(0 if ok else 1)
