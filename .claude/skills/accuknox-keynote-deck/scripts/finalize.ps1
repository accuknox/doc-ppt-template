# Re-save each TCTS deck through PowerPoint with TrueType fonts embedded, then export a PDF.
# Embedding keeps Space Grotesk on machines that do not have it installed.
param([string]$Dir = "D:\Atharva\AccuKnox\doc-ppt-template\output\tcts")
$pp = New-Object -ComObject PowerPoint.Application
try {
  Get-ChildItem -Path $Dir -Filter *.pptx | ForEach-Object {
    $src = $_.FullName
    $tmp = Join-Path $Dir ("_embed_" + $_.Name)
    $pres = $pp.Presentations.Open($src, $false, $false, $false)
    $pres.SaveAs($tmp, 24, -1)
    $pdf = [System.IO.Path]::ChangeExtension($src, ".pdf")
    $pres.SaveAs($pdf, 32)
    $pres.Close()
    Move-Item -Force $tmp $src
    Write-Output "embedded fonts and exported PDF: $($_.Name)"
  }
} finally {
  $pp.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($pp) | Out-Null
}
