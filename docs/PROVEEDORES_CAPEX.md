# Proveedores y cotizaciones del CAPEX

Registro de procura publicado desde la hoja `Proveedores_CAPEX`. Los precios directos incluyen la logística indicada por el propietario; los listados públicos son benchmarks y requieren RFQ, inspección, seriales, FAT/SAT, confirmación eléctrica y validación de formato antes de adjudicar.

| Línea | Equipo | Proveedor / fuente | Precio | Estado |
|---|---|---|---:|---|
| L3 | Robot ABB para garrafones | EUROBOTS, cotización directa | GBP 13.500, envío y logística incluidos | Seleccionado; validar alcance del controlador |
| L1-L2 | Controlador ABB IRC5 del GANTRY | IGAM, cotización directa | USD 6.500, envío y logística incluidos | Seleccionado |
| L2 | KRONES Variopac 459 usada | [Machinio](https://www.machinio.com/cat/variopac) | USD 79.900, logística no confirmada | Benchmark; RFQ pendiente |
| L2 | KRONES Variopac Pro TFS-4-DS 2021 | [MachinePoint](https://www.machinepoint.com/machinepoint/inventory.nsf/idmaquina/300047107?ln=es&opendocument=) | Consultar | Alternativa RFQ |
| L1 | KRONES VODM usada 2012, 44.000 bph | [MachinePoint](https://www.machinepoint.com/machinepoint/inventory.nsf/idmaquina/300049529?ln=en&opendocument=) | Consultar | Alternativa con holgura; inspección pendiente |
| L1 | KRONES glass line 4.000 L/h | [Truck1](https://www.truck1.eu/industrial-equipment/liquid-filling-machines/used-krones-filling-line-for-flat-drinks-in-glass-a11361978.html) | EUR 138.000 | Descartada: ≈11.429 bph no cubre L1 |
| L1 | KRONES CSD vidrio 36.000 bph | [Used German Machines](https://used-german-machines.de/machines/99922681) | Consultar | Alternativa condicionada; menor holgura |
| L2 | KRONES PET CSD 18.000 bph | [Exapro](https://www.exapro.com/krones-ultra-clean-pet-p260108037/) | Consultar | Base técnica; RFQ pendiente |
| Común | Sensores, neumática, seguridad y tableros | ABB, Festo, ReeR, Satech e Interroll | Ver BOM de CAPEX | RFQ por paquete |
| Digital | SCADA, MES, UNS, simulación y gemelos | Inductive Automation, Coreflux, Siemens y ABB | Ver `Licencias` y `APU_Ingenieria` | Incluido en arquitectura |

## Criterios de selección

1. Cumplimiento de capacidad después de aplicar OEE y turnos reales.
2. Costo total instalado, no solo precio publicado.
3. Estado, horas, historial, repuestos y soporte regional.
4. Compatibilidad con envase, caja, pallet, tensión y normas de seguridad.
5. Prueba de aceptación, garantía y disponibilidad de documentación técnica.
6. Comparación contra conservar equipo existente: en L3 la llenadora permanece porque ya cubre la demanda.

Los enlaces son referencias de mercado fechadas; pueden cambiar o dejar de estar disponibles. La hoja viva conserva el estado de cada alternativa.
