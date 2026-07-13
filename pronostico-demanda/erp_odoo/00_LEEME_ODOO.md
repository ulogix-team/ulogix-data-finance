# Guía de configuración Odoo — Bases de productos y pronóstico
**Alcance actual:** solo productos, empaques, LdM y demanda pronosticada (MPS).
Precios, costos, compras y contabilidad se configurarán en la fase financiera
(por eso `list_price=0` y los terminados tienen `purchase_ok=False`).

Instancia de referencia: Odoo SaaS con **Inventario, Manufactura, Taller y
Código de barras** ya instalados (captura del cliente).

## 1. Apps y ajustes previos (una sola vez)
1. **Instalar Ventas** (Aplicaciones → "Ventas") — necesario para pedidos y
   para que el MPS lea demanda de ventas más adelante.
2. **Ajustes → Inventario**: activar
   - ☑ *Unidades de medida*
   - ☑ *Empaques de producto* (Packages/Packagings)
   - ☑ *Código de barras* ya instalado: los EAN-13 importados funcionan directo.
   - (Dejar rutas multietapa y lotes/series para la fase siguiente.)
3. **Ajustes → Manufactura**: activar
   - ☑ *Planeación Maestra de Producción (MPS)*
   - Rango de tiempo del MPS: **Mensual**; horizonte: **12 meses**.
   - (Órdenes de trabajo/Taller quedan para la fase de tiempos.)

## 2. Orden de importación (Favoritos → Importar registros)
Importar los CSV **en este orden** (los `id` son IDs externos: re-importar
actualiza en lugar de duplicar):

| # | Archivo | Modelo Odoo destino |
|---|---|---|
| 1 | 01_uom_category.csv | Categorías de unidades de medida (`uom.category`) |
| 2 | 02_uom_uom.csv | Unidades de medida (`uom.uom`) |
| 3 | 03_product_category.csv | Categorías de producto (`product.category`) |
| 4 | 04_product_template.csv | Productos (terminados) (`product.template`) |
| 5 | 05_componentes.csv | Productos (materias primas/empaques) |
| 6 | 06_product_packaging.csv | Empaques (`product.packaging`) |
| 7 | 07_mrp_bom.csv | Listas de materiales (`mrp.bom`) |
| 8 | 08_mrp_bom_line.csv | Líneas de LdM (`mrp.bom.line`) |
| 9 | 09_mps_pronostico.csv | ver §4 (MPS) |

Notas de mapeo al importar:
- Columnas `algo/id` deben mapearse al campo con sufijo **/ID externo**.
- `route_ids/id = mrp.route_warehouse0_manufacture` marca la ruta **Fabricar**
  en los 3 terminados (ID externo estándar de Odoo).
- En `02_uom_uom.csv`, `factor_inv` = cuántas unidades base contiene la UdM
  mayor (p. ej. Pallet CC350 = 1.620 botellas).

## 3. Productos terminados (resumen)
| SKU | EAN-13 | UdM base | Empaques (venta) | Lote de producción |
|---|---|---|---|---|
| CC-RET-350 | 7701000000016 | Botella 350 ml | cajón×30 · capa 270 · pallet 1.620 | múltiplos de pallet (mín. 1) |
| QT-NR-1500 | 7701000000023 | Botella 1.5 L | pack×6 · capa 168 · pallet 840 | múltiplos de pallet (mín. 1) |
| AG-GF-25000 | 7701000000030 | Garrafón 25 L | rack×6 · pallet 30 | múltiplos de pallet (mín. 1) |

El lote se materializa en Odoo así (fase actual, sin tiempos):
**Inventario → Productos → pestaña Compras/Fabricación → Reglas de reorden**
o directamente en la Orden de fabricación usando la UdM *Pallet* — la cantidad
queda en múltiplos exactos del pallet. En la fase de tiempos se fijará
`Cantidad múltiplo` en reglas de abastecimiento.

## 4. Cargar el pronóstico en la Planeación (MPS)
`09_mps_pronostico.csv` trae la demanda mensual **abr-2026 → mar-2027** en
unidades por SKU (columnas: product_id/id, default_code, date, forecast_qty,
litros). Dos formas de usarlo:
- **Manual (recomendado en SaaS):** Manufactura → Planeación → añadir los 3
  productos → digitar `forecast_qty` de cada mes en la fila *Demanda
  pronosticada*. Son 36 celdas (3 SKU × 12 meses).
- **Importación (modo desarrollador):** modelo `mrp.production.schedule` +
  `mrp.product.forecast` usando los IDs externos del CSV.

Con la demanda cargada, el MPS calculará las cantidades **a reabastecer** y,
con la ruta Fabricar + LdM, generará las **órdenes de fabricación** sugeridas
por mes; los componentes (05) quedarán como necesidades de compra para la fase
financiera.

## 5. Órdenes de venta de prueba (opcional, para validar flujo)
Crear 1 pedido por SKU con el empaque *Pallet* (p. ej. 2 pallets de CC-RET-350
= 3.240 botellas) y confirmar: debe reservar de inventario y, al no haber
stock, el MPS/reabastecimiento propondrá la orden de fabricación.

## 6. Qué NO se configura todavía (fase financiera posterior)
Precios de venta y costos estándar, proveedores y órdenes de compra reales,
contabilidad, lotes/series y caducidades, rutas multietapa, centros de trabajo
y tiempos de Taller.
