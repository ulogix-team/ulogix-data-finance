"""Ejecuta el pipeline completo en orden. Uso: python run_all.py"""
import subprocess, sys
PASOS=["00_extraer_kof","01_reconstruccion_datos","02_pruebas_estadisticas",
       "03_modelo_holt_winters","04_evaluacion_errores","05_inventario_lotes",
       "06_export_odoo","07_generar_excel","08_distribuciones","09_montecarlo",
       "10_multivariado","11_diagrama_flujo","12_verificacion","13_escenarios","14_excel_escenarios"]
for p in PASOS:
    print(f"\n{'='*60}\n>>> scripts/{p}.py\n{'='*60}")
    r=subprocess.run([sys.executable,f"scripts/{p}.py"])
    if r.returncode!=0: sys.exit(f"FALLO en {p}")
print("\nPIPELINE COMPLETO OK")
