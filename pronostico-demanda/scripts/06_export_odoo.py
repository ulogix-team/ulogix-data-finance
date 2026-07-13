"""
06_export_odoo.py  (v3 — bases completas para Odoo SaaS)
Genera en erp_odoo/ los archivos de importacion con IDs externos, alineados
con los modulos del cliente (Inventario, Manufactura+Planeacion/MPS, Ventas,
Codigo de barras). ALCANCE ACTUAL: solo bases de productos y pronostico;
finanzas/precios/compras se abordaran despues (list_price=0, purchase_ok=False
en terminados).

Archivos:
  01_uom_category.csv        categorias de UdM (una por jerarquia de producto)
  02_uom_uom.csv             UdM: botella/cajon/pack/rack/capa/pallet (ratios)
  03_product_category.csv    categorias de producto
  04_product_template.csv    3 productos TERMINADOS (SKU, EAN-13, ruta Fabricar)
  05_componentes.csv         componentes base para las LdM (agua, concentrado,
                             envases, tapas, etiqueta; casco retornable)
  06_product_packaging.csv   empaques: cajon/pack/rack, capa, pallet
  07_mrp_bom.csv             cabeceras de LdM (1 por terminado)
  08_mrp_bom_line.csv        lineas de LdM (componentes por unidad)
  09_mps_pronostico.csv      demanda mensual abr-2026->mar-2027 en unidades,
                             para la Planeacion Maestra (MPS) de Manufactura
Guia de configuracion e importacion: erp_odoo/00_LEEME_ODOO.md
"""
import pandas as pd, os

def ean13(base12):
    d=[int(c) for c in base12]
    return base12+str((10-(sum(d[0::2])+3*sum(d[1::2]))%10)%10)

X="__import__."   # prefijo de ID externo

UOM_CAT=[("uomcat_cc350","Empaque CC 350 ml"),
         ("uomcat_qt15","Empaque QuAtro 1.5 L"),
         ("uomcat_gf25","Empaque Garrafon 25 L"),
         ("uomcat_liq","Liquidos proceso")]

UOM=[  # (id, nombre, categoria, tipo, ratio unidades base)
 ("uom_bot350","Botella 350 ml","uomcat_cc350","reference",1),
 ("uom_cajon30","Cajon x30 (CC350)","uomcat_cc350","bigger",30),
 ("uom_capa_cc","Capa 9 cajones (CC350)","uomcat_cc350","bigger",270),
 ("uom_pallet_cc","Pallet 54 cajones (CC350)","uomcat_cc350","bigger",1620),
 ("uom_bot15","Botella 1.5 L","uomcat_qt15","reference",1),
 ("uom_pack6","Pack x6 (QT1.5)","uomcat_qt15","bigger",6),
 ("uom_capa_qt","Capa 28 packs (QT1.5)","uomcat_qt15","bigger",168),
 ("uom_pallet_qt","Pallet 140 packs (QT1.5)","uomcat_qt15","bigger",840),
 ("uom_gfn","Garrafon 25 L","uomcat_gf25","reference",1),
 ("uom_rack6","Rack x6 (=capa)","uomcat_gf25","bigger",6),
 ("uom_pallet_gf","Pallet 5 racks (Garrafon)","uomcat_gf25","bigger",30),
 ("uom_litro","Litro (proceso)","uomcat_liq","reference",1),
 ("uom_ml","Mililitro (proceso)","uomcat_liq","smaller",1000),
]

PCAT=[("pcat_bebidas","Bebidas"),
      ("pcat_carb_ret","Bebidas / Carbonatadas / Retornable"),
      ("pcat_carb_nr","Bebidas / Carbonatadas / No retornable"),
      ("pcat_agua","Bebidas / Agua / Garrafon"),
      ("pcat_mp","Materias primas y empaques")]

TERMINADOS=[
 dict(id="prod_cc_ret_350",default_code="CC-RET-350",
      name="Coca-Cola 350 ml Vidrio Retornable",barcode=ean13("770100000001"),
      categ="pcat_carb_ret",uom="uom_bot350",
      desc="Retornable vidrio 0,35 L. Pallet=54 cajones=1.620 bot=567 L. Ref. catalogo: 75005771 'Cocacola 355 Ml Ret.' (MX)."),
 dict(id="prod_qt_nr_1500",default_code="QT-NR-1500",
      name="QuAtro Toronja 1.5 L PET No Retornable",barcode=ean13("770100000002"),
      categ="pcat_carb_nr",uom="uom_bot15",
      desc="PET NR 1,5 L. Pallet=140 packs=840 bot=1.260 L. Carbonatada sabor #1 de Colombia (KOF 2025)."),
 dict(id="prod_ag_gf_25",default_code="AG-GF-25000",
      name="Garrafon Agua 25 L Retornable",barcode=ean13("770100000003"),
      categ="pcat_agua",uom="uom_gfn",
      desc="Garrafon retornable 25 L. Pallet=5 racks=30 gfn=750 L. Ref. catalogo: 7501032401917 'Agua Cristal 20lt' (MX)."),
]

COMPONENTES=[  # (id, codigo, nombre, uom, tipo, categ)
 ("comp_agua","MP-AGUA","Agua tratada (proceso)","uom_litro","product","pcat_mp"),
 ("comp_conc_cc","MP-CONC-CC","Concentrado Coca-Cola","uom_ml","product","pcat_mp"),
 ("comp_conc_qt","MP-CONC-QT","Concentrado QuAtro toronja","uom_ml","product","pcat_mp"),
 ("comp_co2","MP-CO2","CO2 carbonatacion (g)","uom_ml","product","pcat_mp"),
 ("comp_casco_350","EMP-CASCO-350","Casco vidrio retornable 350 ml","uom_bot350","product","pcat_mp"),
 ("comp_pet_15","EMP-PET-15","Botella PET 1.5 L","uom_bot15","product","pcat_mp"),
 ("comp_casco_gf","EMP-CASCO-GF","Casco garrafon retornable 25 L","uom_gfn","product","pcat_mp"),
 ("comp_tapa_cc","EMP-TAPA-CC","Tapa corona (CC350)","uom_bot350","product","pcat_mp"),
 ("comp_tapa_pet","EMP-TAPA-PET","Tapa rosca PET","uom_bot15","product","pcat_mp"),
 ("comp_tapa_gf","EMP-TAPA-GF","Tapa garrafon","uom_gfn","product","pcat_mp"),
 ("comp_etiq_qt","EMP-ETIQ-QT","Etiqueta QuAtro 1.5 L","uom_bot15","product","pcat_mp"),
]

# LdM por 1 unidad de terminado (bases; ajustar mermas despues)
BOM_LINES={
 "prod_cc_ret_350":[("comp_agua",0.315),("comp_conc_cc",35.0),("comp_co2",3.0),
                    ("comp_casco_350",1),("comp_tapa_cc",1)],
 "prod_qt_nr_1500":[("comp_agua",1.35),("comp_conc_qt",150.0),("comp_co2",12.0),
                    ("comp_pet_15",1),("comp_tapa_pet",1),("comp_etiq_qt",1)],
 "prod_ag_gf_25":[("comp_agua",25.0),("comp_casco_gf",1),("comp_tapa_gf",1)],
}

if __name__=="__main__":
    os.makedirs("erp_odoo",exist_ok=True)
    pd.DataFrame([{"id":X+i,"name":n} for i,n in UOM_CAT]
        ).to_csv("erp_odoo/01_uom_category.csv",index=False)
    pd.DataFrame([{"id":X+i,"name":n,"category_id/id":X+c,"uom_type":t,
                   "factor_inv":r if t=="bigger" else "","factor":r if t=="smaller" else ("1" if t=="reference" else "")}
                  for i,n,c,t,r in UOM]).to_csv("erp_odoo/02_uom_uom.csv",index=False)
    pd.DataFrame([{"id":X+i,"name":n} for i,n in PCAT]
        ).to_csv("erp_odoo/03_product_category.csv",index=False)
    pd.DataFrame([{"id":X+p["id"],"name":p["name"],"default_code":p["default_code"],
                   "barcode":p["barcode"],"detailed_type":"product",
                   "categ_id/id":X+p["categ"],"uom_id/id":X+p["uom"],"uom_po_id/id":X+p["uom"],
                   "sale_ok":"True","purchase_ok":"False","list_price":0,
                   "route_ids/id":"mrp.route_warehouse0_manufacture",
                   "description_sale":p["desc"]} for p in TERMINADOS]
        ).to_csv("erp_odoo/04_product_template.csv",index=False)
    pd.DataFrame([{"id":X+i,"name":n,"default_code":c,"detailed_type":t,
                   "categ_id/id":X+g,"uom_id/id":X+u,"uom_po_id/id":X+u,
                   "sale_ok":"False","purchase_ok":"True","list_price":0}
                  for i,c,n,u,t,g in COMPONENTES]
        ).to_csv("erp_odoo/05_componentes.csv",index=False)
    PACK=[("prod_cc_ret_350","Cajon x30",30),("prod_cc_ret_350","Capa (9 cajones)",270),
          ("prod_cc_ret_350","Pallet (54 cajones)",1620),
          ("prod_qt_nr_1500","Pack x6",6),("prod_qt_nr_1500","Capa (28 packs)",168),
          ("prod_qt_nr_1500","Pallet (140 packs)",840),
          ("prod_ag_gf_25","Rack x6 (=capa)",6),("prod_ag_gf_25","Pallet (5 racks)",30)]
    pd.DataFrame([{"id":X+f"pack_{p}_{q}","name":n,"product_id/id":X+p,
                   "qty":q,"sales":"True","purchase":"False"} for p,n,q in PACK]
        ).to_csv("erp_odoo/06_product_packaging.csv",index=False)
    pd.DataFrame([{"id":X+f"bom_{p['id']}","product_tmpl_id/id":X+p["id"],
                   "product_qty":1,"type":"normal",
                   "code":f"LdM-{p['default_code']}"} for p in TERMINADOS]
        ).to_csv("erp_odoo/07_mrp_bom.csv",index=False)
    lines=[]
    for prod,ls in BOM_LINES.items():
        for comp,qty in ls:
            lines.append({"id":X+f"boml_{prod}_{comp}",
                          "bom_id/id":X+f"bom_{prod}",
                          "product_id/id":X+comp,"product_qty":qty})
    pd.DataFrame(lines).to_csv("erp_odoo/08_mrp_bom_line.csv",index=False)
    # MPS: demanda mensual pronosticada en unidades por SKU
    fc=pd.read_csv("data/pronostico_2026.csv",parse_dates=['fecha'])
    code={'P1':'CC-RET-350','P2':'QT-NR-1500','P3':'AG-GF-25000'}
    xid={'P1':'prod_cc_ret_350','P2':'prod_qt_nr_1500','P3':'prod_ag_gf_25'}
    fc['default_code']=fc.producto.map(code)
    fc['product_id/id']=X+fc.producto.map(xid)
    fc['fecha']=fc.fecha.dt.strftime('%Y-%m-%d')
    fc[['product_id/id','default_code','fecha','unidades','litros']]\
        .rename(columns={'fecha':'date','unidades':'forecast_qty'})\
        .to_csv("erp_odoo/09_mps_pronostico.csv",index=False)
    print("OK -> erp_odoo/: 9 archivos de importacion generados")
