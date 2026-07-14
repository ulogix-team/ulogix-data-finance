param(
    [string]$WorkbookPath = "",
    [string]$OutputDir = ""
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
if (-not $WorkbookPath) {
    $WorkbookPath = Join-Path $root "financiero\modelo\Modelo_FEMSA_Ulogix_2026.xlsx"
}
if (-not $OutputDir) {
    $OutputDir = Join-Path $root ".qa\modelo"
}
$WorkbookPath = (Resolve-Path -LiteralPath $WorkbookPath).Path
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$OutputDir = (Resolve-Path -LiteralPath $OutputDir).Path

$excel = $null
$book = $null
$reporte = @()
try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $excel.AskToUpdateLinks = $false
    $excel.AutomationSecurity = 3
    $book = $excel.Workbooks.Open($WorkbookPath, 0, $true)
    $excel.CalculateFullRebuild()

    foreach ($sheet in $book.Worksheets) {
        $used = $sheet.UsedRange
        $formulas = 0
        $errors = 0
        try { $formulas = [int64]$used.SpecialCells(-4123).CountLarge } catch {}
        try { $errors = [int64]$used.SpecialCells(-4123, 16).CountLarge } catch {}
        $reporte += [pscustomobject]@{
            hoja = $sheet.Name
            visible = ($sheet.Visible -eq -1)
            filas = [int]$used.Rows.Count
            columnas = [int]$used.Columns.Count
            formulas = $formulas
            errores_formula = $errors
        }
    }

    $dashboard = $book.Worksheets | Where-Object { $_.Name -eq "Dashboard" } | Select-Object -First 1
    if ($dashboard) {
        $dashboard.Activate()
        $rango = $dashboard.UsedRange
        $dashboard.PageSetup.PrintArea = $rango.Address()
        $dashboard.PageSetup.Orientation = 2
        $dashboard.PageSetup.Zoom = $false
        $dashboard.PageSetup.FitToPagesWide = 1
        $dashboard.PageSetup.FitToPagesTall = 1
        $dashboard.ExportAsFixedFormat(0, (Join-Path $OutputDir "Dashboard.pdf"), 0, $true, $false)
    }

    $resumen = [pscustomobject]@{
        archivo = $WorkbookPath
        hojas = $reporte.Count
        formulas = ($reporte | Measure-Object -Property formulas -Sum).Sum
        errores_formula = ($reporte | Measure-Object -Property errores_formula -Sum).Sum
        detalle = $reporte
    }
    $resumen | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $OutputDir "verificacion.json") -Encoding UTF8
    $resumen | Select-Object archivo, hojas, formulas, errores_formula | Format-List
}
finally {
    if ($book) { $book.Close($false) }
    if ($excel) { $excel.Quit() }
    if ($dashboard) { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($dashboard) }
    if ($book) { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($book) }
    if ($excel) { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($excel) }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
