# Launch a console for the project.
param(
    [switch]$Quick,
    [switch]$Verbose
)

$project_root = Split-Path $PSScriptRoot
. $PSScriptRoot\Write-Status.ps1

Write-Status "MKVtoMP4 console"

$venv = Join-Path $project_root "venv\scripts\Activate.ps1"
if (Test-Path $venv) {
    if (-Not($Quick)) {
        . $PSScriptRoot\Update.ps1 -DevRequirements -Verbose:$Verbose
    }
}
else {
    if ($Quick) {
        Write-Warning "No virtual env detected, -Quick will be ignored"
    }
    . $PSScriptRoot\Setup.ps1 -DevRequirements
}

. $PSScriptRoot\Ensure-Venv.ps1 | Out-Null

# Register helper functions
Set-Item function:global:Update-DevEnvironment {
    param([switch]$Verbose)
    . $PSScriptRoot\Update.ps1 -DevRequirements -Verbose:$Verbose
} -Force

Write-Status "MKVtoMP4 ready"
