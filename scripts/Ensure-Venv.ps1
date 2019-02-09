# Ensures this console or script has activated the correct venv for this project
# Return $True if it already was, $False if this script needed to activate it,
# and throws if no venv could be activated.

$project_root = Split-Path $PSScriptRoot
$expected_venv = Join-Path $project_root "venv"

if ($ENV:VIRTUAL_ENV -eq $expected_venv) {
    return $True
}
else {
    $activate = Join-Path $expected_venv "Scripts\Activate.ps1"
    . $activate
    if ($ENV:VIRTUAL_ENV -eq $expected_venv) {
        return $False
    }
    else {
        throw "Unable to activate $expected_venv"
    }
}
