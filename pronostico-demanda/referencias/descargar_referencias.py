"""
descargar_referencias.py
Descarga las fuentes primarias (PDF/HTML) del proyecto a referencias/descargas/.
Ejecutar con el entorno conda activo:  python referencias/descargar_referencias.py
Nota: el sandbox donde se construyo el repo no tiene salida a estos dominios,
por eso los archivos se descargan en la maquina del usuario.
"""
import os, requests

FUENTES = {
 # --- Coca-Cola FEMSA (fuentes primarias de volumen) ---
 "KOF_Informe_Integrado_2025.pdf":
   "https://investors.coca-colafemsa.com/assets/files/reportes_resultados_esp/2026/2025-KOF-II-ESP.pdf",
 "KOF_Informe_Integrado_2024.pdf":
   "https://investors.coca-colafemsa.com/assets/files/reportes_resultados_esp/2024/kof-ii-2024-esp.pdf",
 "KOF_Reporte_Anual_2023.pdf":
   "https://investors.coca-colafemsa.com/assets/files/reportes_resultados_esp/2023/24-04-11-reporte-anual-2023.pdf",
 # --- DANE (fuente oficial: estacionalidad y sector) ---
 "DANE_EMMET_metodologia.pdf":
   "https://www.dane.gov.co/files/operaciones/EMMET/met-EMMET.pdf",
 "DANE_EMMET_boletin_ago2025.pdf":
   "https://www.dane.gov.co/files/operaciones/EMMET/bol-EMMET-ago2025.pdf",
 "DANE_EMMET_boletin_ene2025.pdf":
   "https://www.dane.gov.co/files/operaciones/EMMET/bol-EMMET-ene2025.pdf",
 "DANE_IPI_boletin_dic2025.pdf":
   "https://www.dane.gov.co/files/operaciones/IPI/bol-IPI-dic2025.pdf",
}
PAGINAS = {  # HTML de referencia (guardar como .html)
 "KOF_portal_reportes.html":
   "https://investors.coca-colafemsa.com/informacion-financiera/reportes-y-resultados/",
 "KOF_informe_integrado_portal.html":
   "https://coca-colafemsa.com/sostenibilidad/informe-integrado.html",
 "DANE_EMMET_historicos.html":
   "https://www.dane.gov.co/index.php/estadisticas-por-tema/industria/encuesta-mensual-manufacturera-con-enfoque-territorial-emmet/emmet-historicos",
}

def bajar(nombre, url, carpeta="referencias/descargas"):
    os.makedirs(carpeta, exist_ok=True)
    destino = os.path.join(carpeta, nombre)
    try:
        r = requests.get(url, timeout=60,
                         headers={"User-Agent": "Mozilla/5.0 (proyecto-ingenieria)"})
        r.raise_for_status()
        open(destino, "wb").write(r.content)
        print(f"OK  {nombre}  ({len(r.content)/1e6:.1f} MB)")
    except Exception as e:
        print(f"FALLO {nombre}: {e}")

if __name__ == "__main__":
    for n, u in {**FUENTES, **PAGINAS}.items():
        bajar(n, u)
    print("\nListo. Archivos en referencias/descargas/")
