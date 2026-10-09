# Managed by BosskuAI (`bossku hooks install`). Codex Stop/SessionEnd wrapper.
# Curated one-way Obsidian export, then continue JSON required by Codex Stop.
$ErrorActionPreference = 'Continue'
# Read and pass the payload as UTF-8: the console code page would turn a non-ASCII project path into '?'.
$utf8 = New-Object System.Text.UTF8Encoding($false)
$OutputEncoding = $utf8
$inputJson = ''
try {
  $buffer = New-Object System.IO.MemoryStream
  [Console]::OpenStandardInput().CopyTo($buffer)
  $inputJson = $utf8.GetString($buffer.ToArray())
} catch {}
function Invoke-BosskuSyncHook {
  if (Get-Command bossku -ErrorAction SilentlyContinue) {
    if ($inputJson) { $inputJson | & bossku sync-hook | Out-Null }
    else { & bossku sync-hook | Out-Null }
    return
  }
  $py = Get-Command python -ErrorAction SilentlyContinue
  if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
  if ($py) {
    if ($inputJson) { $inputJson | & $py.Source -m bossku sync-hook | Out-Null }
    else { & $py.Source -m bossku sync-hook | Out-Null }
  }
}
try { Invoke-BosskuSyncHook } catch {}
Write-Output '{"continue": true}'
