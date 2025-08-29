Param(
    [switch] $IncludeDev
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot
try {
    if (-not (Test-Path ".\tools\pyproject_to_requirements.py")) {
        Write-Error "Tool not found: .\tools\pyproject_to_requirements.py"
        exit 1
    }

    $pyproject = Join-Path $PSScriptRoot "pyproject.toml"
    if (-not (Test-Path $pyproject)) {
        Write-Error "pyproject.toml not found in backend folder."
        exit 1
    }

    $args = @("--pyproject", $pyproject, "--out", "requirements.txt")
    if ($IncludeDev) { $args += @("--include-dev", "--dev-out", "requirements-dev.txt") }

    Write-Output "Generating requirements.txt from pyproject.toml..."
    python .\tools\pyproject_to_requirements.py $args
    Write-Output "Done. Check requirements.txt (and requirements-dev.txt if requested)."

} finally {
    Pop-Location
}