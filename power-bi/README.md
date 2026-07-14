<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/header-dark.svg" width="100%"/>

# Capa analítica MES

Contrato de visualización para OEE, producción, alarmas, paros, mantenimiento y resultados ejecutivos. La arquitectura vigente usa **Ignition + Coreflux MQTT/UNS + ERP Streamlit/Odoo**; Power BI puede consumir históricos exportados, pero no es la fuente de los KPI.

| Vista | KPI | Fuente autorizada |
|---|---|---|
| Producción por línea | `AvailableQuantity`, orden activa y cumplimiento | UNS MQTT + `po_tracking` |
| OEE | disponibilidad, rendimiento, calidad, OEE y MLT | `kpi_uns` |
| Paros y alarmas | estado, duración y mantenimiento | UNS `MES/Maintance/#` y SCADA |
| Inventario | terminado y componentes | ERP local + Odoo |
| Finanzas | CAPEX, VPN, TIR, ROI y payback | Google Sheets vivo |

`AvailableQuantity` es el valor absoluto producido de la orden activa y constituye el camino principal de manufactura. `GoodCount` permanece como contrato legado para simulaciones.

Licencias vigentes: CAPEX software **COP 112.086.015** y OPEX mensual de licencias/hosting **COP 8.262.150**. El desglose está en la hoja `Licencias`; no se replica manualmente aquí.

<img src="https://raw.githubusercontent.com/ulogix-team/assets/main/banners/footer-dark.svg" width="100%"/>
