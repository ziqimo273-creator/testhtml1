# Windows PowerShell 5.1+
# Mirrors three sites into separate folders. Install GNU Wget first:
# winget install GnuWin32.Wget  (or install Wget from https://www.gnu.org/software/wget/)
$ErrorActionPreference = "Stop"
$sites = @(
  @{ Name = "namestyles"; Url = "https://namestyles.net/" },
  @{ Name = "diagonalcalculator"; Url = "https://diagonalcalculator.com/" },
  @{ Name = "stylenamegenerator"; Url = "https://stylenamegenerator.com/" }
)
$root = Join-Path $PSScriptRoot "offline-sites"
New-Item -ItemType Directory -Force -Path $root | Out-Null
$wget = Get-Command wget.exe -ErrorAction SilentlyContinue
if (-not $wget) { $wget = Get-Command wget -ErrorAction SilentlyContinue }
if (-not $wget) {
  throw "GNU Wget was not found. Install GNU Wget, reopen PowerShell, and run this script again."
}
foreach ($site in $sites) {
  $dest = Join-Path $root $site.Name
  New-Item -ItemType Directory -Force -Path $dest | Out-Null
  Write-Host "`n=== Mirroring $($site.Url) to $dest ===" -ForegroundColor Cyan
  # Keep requests polite; same-host pages and required resources are downloaded recursively.
  & $wget.Source --mirror --page-requisites --adjust-extension --convert-links --backup-converted --no-parent --wait=1 --random-wait --timeout=25 --tries=2 --directory-prefix="$dest" "$($site.Url)"
  if ($LASTEXITCODE -ne 0) {
    Write-Warning "Wget reported errors for $($site.Name). Review its output and retry after checking robots.txt / site access."
  }
}
Write-Host "`nFinished crawl attempt. Files are under: $root" -ForegroundColor Green
Write-Host "This is a crawl attempt, not a guarantee of completeness. Run check-links.py next."
