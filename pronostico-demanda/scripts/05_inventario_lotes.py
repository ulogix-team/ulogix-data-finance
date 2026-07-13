"""
05_inventario_lotes.py
Conversion del pronostico a la jerarquia real de empaque de la planta,
definicion del lote de produccion y rotacion de inventarios.

JERARQUIA DE EMPAQUE (dato de planta):
  P1 Coca-Cola 350 ml retornable (vidrio):
     cajon = 30 botellas | capa = 9 cajones (270 bot) | pallet = 6 capas
     = 54 cajones = 1.620 botellas = 567,0 L
  P2 QuAtro 1.5 L PET no retornable:
     pack = 6 botellas | capa = 28 packs (168 bot) | pallet = 5 capas
     = 140 packs = 840 botellas = 1.260,0 L
  P3 Garrafon 25 L retornable:
     rack = 6 garrafones = 1 capa | pallet = 5 capas = 30 garrafones = 750,0 L

LOTE DE PRODUCCION: la linea libera producto en pallets completos ->
  lote minimo = 1 pallet; incremento = 1 pallet.
  Lote estandar sugerido = demanda mensual / CORRIDAS_MES, redondeado hacia
  arriba a pallets completos (CORRIDAS_MES es un parametro de planeacion,
  no un estudio de tiempos; por defecto 20 corridas/mes ~ 1 por dia habil).

ROTACION DE INVENTARIOS (sin lead times, fase posterior):
  Inventario de ciclo promedio = Lote/2 (modelo de dientes de sierra).
  Rotacion = Demanda anual / Inventario promedio   [veces/anio]
  Cobertura = 365 / Rotacion                        [dias]
Salida: data/plan_unidades_lotes.csv, data/rotacion_inventarios.csv
"""
import numpy as np, pandas as pd, json, math

EMPAQUE = {
 'P1': dict(nombre='Coca-Cola 350 ml Vidrio Retornable', envase_L=0.35,
            agrupacion='cajon', und_por_agrup=30, agrup_por_capa=9,
            capas_por_pallet=6),
 'P2': dict(nombre='QuAtro Toronja 1.5 L PET NR', envase_L=1.5,
            agrupacion='pack', und_por_agrup=6, agrup_por_capa=28,
            capas_por_pallet=5),
 'P3': dict(nombre='Garrafon Agua 25 L Retornable', envase_L=25.0,
            agrupacion='rack', und_por_agrup=6, agrup_por_capa=1,
            capas_por_pallet=5),
}
# LOTE = PRODUCCION DE UN TURNO DE 8 h (definicion del proyecto, fase de tiempos):
# Q_turno = Rp_real x 8 h x OEE_linea, redondeado a pallets. Fuente: Tiempos_Fontibon_Corregido.xlsx
# L1: 42.500 bph x 8 x 0,771 -> 162 pallets = 262.440 und
# L2: 12.000 bph x 8 x 0,765 ->  87 pallets =  73.080 und
# L3:    480 gfn/h x 8 x 0,754 (paletizado manual 2 operarios) -> 96 pallets = 2.880 und
LOTE_TURNO_PALLETS = {'P1': 162, 'P2': 87, 'P3': 96}

def derivados(e):
    und_capa   = e['und_por_agrup']*e['agrup_por_capa']
    und_pallet = und_capa*e['capas_por_pallet']
    return und_capa, und_pallet, und_pallet*e['envase_L']

def plan(df_fc):
    filas, rot = [], []
    for p, e in EMPAQUE.items():
        und_capa, und_pallet, L_pallet = derivados(e)
        sub = df_fc[df_fc.producto==p].copy()
        sub['agrupaciones'] = np.ceil(sub.unidades/e['und_por_agrup']).astype(int)
        sub['pallets'] = np.ceil(sub.unidades/und_pallet).astype(int)
        sub['lote_estandar_pallets'] = LOTE_TURNO_PALLETS[p]
        sub['lote_estandar_unidades'] = sub.lote_estandar_pallets*und_pallet
        filas.append(sub)

        # Rotacion bajo escenarios de tamano de lote (corridas por mes):
        #   turno (definicion base) | dia 2 turnos | semanal (~12 turnos)
        D_und = int(sub.unidades.sum())
        fila = dict(producto=p, nombre=e['nombre'],
                    unidades_por_pallet=und_pallet,
                    litros_por_pallet=round(L_pallet,1),
                    demanda_anual_und=D_und,
                    demanda_anual_pallets=int(sub.pallets.sum()))
        for esc, mult in [('turno',1), ('dia_2turnos',2), ('semanal',12)]:
            Q_pal = LOTE_TURNO_PALLETS[p]*mult
            Q_und = Q_pal*und_pallet
            rotacion = D_und/(Q_und/2)
            fila[f'lote_{esc}_pallets'] = Q_pal
            fila[f'rotacion_{esc}'] = round(rotacion,1)
            fila[f'cobertura_{esc}_dias'] = round(365/rotacion,2)
        rot.append(fila)
    return pd.concat(filas), pd.DataFrame(rot)

if __name__ == "__main__":
    fc = pd.read_csv("data/pronostico_2026.csv", parse_dates=['fecha'])
    plan_df, rot_df = plan(fc)
    plan_df.to_csv("data/plan_unidades_lotes.csv", index=False)
    rot_df.to_csv("data/rotacion_inventarios.csv", index=False)
    print(rot_df.to_string(index=False))
    print("\nOK -> plan_unidades_lotes.csv, rotacion_inventarios.csv")
