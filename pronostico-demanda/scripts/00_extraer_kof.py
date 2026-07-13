"""
00_extraer_kof.py
Extraccion REPRODUCIBLE de la tabla "Volumen" (fila Colombia) de los 17
Reportes de Resultados Trimestrales de Coca-Cola FEMSA incluidos en
referencias/descargas/ (fuente: portal oficial de inversionistas KOF,
https://investors.coca-colafemsa.com/informacion-financiera/reportes-trimestrales/).

Estructura de la tabla en cada reporte (millones de cajas unidad, MCU):
  Pais | Refrescos | Agua | Garrafon | Otros | Total || (mismo, anio previo) || Δ%
La fila Colombia con >=11 campos numericos es la fila de volumen. Las columnas
comparativas del anio previo permiten extender la serie: los reportes de 2022
aportan los cuatro trimestres de 2021 -> 21 trimestres (2021T1-2026T1).

Salida: data/kof_trimestral_colombia.json
Verificacion posterior: scripts/12_verificacion.py
"""
import re, glob, json, os
from pypdf import PdfReader

def texto_pdf(path):
    return "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)

def extraer():
    data={}
    archivos=sorted(glob.glob("referencias/descargas/20??-T-?.pdf"))
    if not archivos:
        raise SystemExit("No se encontraron PDFs en referencias/descargas/")
    for f in archivos:
        nombre=os.path.basename(f); y,q=int(nombre[:4]),int(nombre[7])
        lineas=texto_pdf(f).splitlines()
        candidatos=[]
        for i,line in enumerate(lineas):
            if 'Colombia' in line:
                candidatos.append(line)
                candidatos.append(line+" "+(lineas[i+1] if i+1<len(lineas) else ""))
        for line in candidatos:
                # tomar SOLO los numeros que siguen a la palabra 'Colombia'
                seg=line.split('Colombia',1)[1]
                nums=re.findall(r'-?\d+[\d,]*\.?\d*', seg.replace(',',''))
                if len(nums)>=10:
                    v=[float(x) for x in nums[:10]]
                    cur=dict(refrescos=v[0],agua=v[1],garrafon=v[2],otros=v[3],total=v[4])
                    pri=dict(refrescos=v[5],agua=v[6],garrafon=v[7],otros=v[8],total=v[9])
                    # sanidad: categorias deben sumar el total (tolerancia 0.15 MCU)
                    if abs(cur['total']-sum([cur['refrescos'],cur['agua'],cur['garrafon'],cur['otros']]))<0.15:
                        data[(y,q)]=cur
                        data.setdefault((y-1,q),pri)
                        break
    return dict(sorted(data.items()))

if __name__=="__main__":
    data=extraer()
    os.makedirs("data",exist_ok=True)
    json.dump({f"{y}Q{q}":d for (y,q),d in data.items()},
              open("data/kof_trimestral_colombia.json","w"),indent=1)
    print(f"{len(data)} trimestres extraidos ({min(data)} a {max(data)})")
    for (y,q),d in data.items():
        print(f"  {y}T{q}: R={d['refrescos']:5.1f} A={d['agua']:4.1f} "
              f"G={d['garrafon']:3.1f} O={d['otros']:3.1f} T={d['total']:5.1f}")
