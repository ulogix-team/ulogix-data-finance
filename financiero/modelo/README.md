# Publicación del modelo vivo

Esta carpeta contiene el snapshot XLSX del Google Sheet que gobierna el caso financiero. El archivo preserva fórmulas, estructura y formato para revisión fuera de línea.

Para regenerarlo:

```bash
python tools/exportar_modelo_sheets.py --env-file ../ulogix-fontibon-suite/.env
```

Verifique siempre `modelo.manifest.json`: identifica fecha de publicación, tamaño y SHA-256. No edite el XLSX esperando que el ERP adopte esos cambios; las modificaciones operativas se realizan en Sheets.
