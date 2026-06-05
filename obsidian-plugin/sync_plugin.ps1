$ErrorActionPreference = "Stop"

$root = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
$source = Join-Path $root "obsidian-plugin\paperbrain"
$target = Join-Path $root ".obsidian\plugins\paperbrain"

New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item -LiteralPath (Join-Path $source "manifest.json") -Destination (Join-Path $target "manifest.json") -Force
Copy-Item -LiteralPath (Join-Path $source "main.js") -Destination (Join-Path $target "main.js") -Force
Copy-Item -LiteralPath (Join-Path $source "styles.css") -Destination (Join-Path $target "styles.css") -Force

Write-Host "PaperBrain plugin synced to $target"
