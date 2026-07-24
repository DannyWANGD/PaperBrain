[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$VaultPath,
    [string]$IndexUrl = "auto"
)

$ErrorActionPreference = "Stop"
$BackendVersion = "0.3.6"
$BackendTag = "backend-0.3.6"
$BackendRepository = "DannyWANGD/PaperBrain"
$WheelName = "paperbrain-0.3.6-py3-none-any.whl"
$WheelSha256 = "d41cf6867b74fbef00cec3438fc12c13d1d74597634afc9ff93289ac5c0de986"
$RequirementsName = "requirements.lock"
$RequirementsSha256 = "2a7394540a7552cd1bbbb88e9c440ae3c493e25e5d30a7c8300281831d30de7c"
$ProbeRequirement = "openai==2.46.0"
$ProbeSha256 = "672381db55efb3a1e2610f29304c130cccdd0b319bace4d492b2443cb64c1e7c"
$MiniforgeVersion = "26.3.2-2"
$RuntimeRoot = Join-Path $HOME ".paperbrain\runtime\miniforge3"
$ConfigDir = Join-Path $HOME ".paperbrain\config"

function Invoke-Checked {
    param([string]$FilePath, [string[]]$Arguments)
    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$FilePath exited with code $LASTEXITCODE."
    }
}

function Download-File {
    param([string]$Url, [string]$Destination)
    $curl = Get-Command "curl.exe" -ErrorAction SilentlyContinue
    if ($curl) {
        Invoke-Checked -FilePath $curl.Source -Arguments @("--fail", "--location", "--retry", "2", "--connect-timeout", "20", "--output", $Destination, $Url)
        return
    }
    Invoke-WebRequest -UseBasicParsing -Uri $Url -OutFile $Destination
}

function Assert-Hash {
    param([string]$FilePath, [string]$Expected)
    $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $FilePath).Hash.ToLowerInvariant()
    if ($actual -ne $Expected) {
        throw "SHA-256 verification failed for $(Split-Path -Leaf $FilePath)."
    }
}

if (-not (Test-Path -LiteralPath $VaultPath -PathType Container)) {
    throw "Vault directory does not exist: $VaultPath"
}
if ($IndexUrl -ne "auto") {
    $index = $null
    if (-not [Uri]::TryCreate($IndexUrl, [UriKind]::Absolute, [ref]$index) -or
        $index.Scheme -ne "https" -or $index.UserInfo -or $index.Query -or $index.Fragment -or
        $index.AbsolutePath -notmatch "/simple/?$") {
        throw "The dependency index must be auto or a credential-free HTTPS URL ending in /simple."
    }
}

$tempDir = Join-Path ([IO.Path]::GetTempPath()) ("paperbrain-install-" + [Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $tempDir | Out-Null
$managedRuntimeIncomplete = $false
try {
    $condaPath = ""
    $condaCommand = Get-Command "conda.exe" -ErrorAction SilentlyContinue
    if ($condaCommand) {
        $condaPath = $condaCommand.Source
    } else {
        foreach ($candidate in @(
            (Join-Path $HOME "miniforge3\Scripts\conda.exe"),
            (Join-Path $HOME "mambaforge\Scripts\conda.exe"),
            (Join-Path $HOME "anaconda3\Scripts\conda.exe"),
            (Join-Path $HOME "miniconda3\Scripts\conda.exe"),
            (Join-Path $RuntimeRoot "Scripts\conda.exe")
        )) {
            if (Test-Path -LiteralPath $candidate -PathType Leaf) {
                $condaPath = $candidate
                break
            }
        }
    }

    if (-not $condaPath) {
        if ($env:PROCESSOR_ARCHITECTURE -notin @("AMD64", "x86_64")) {
            throw "Automatic Miniforge installation is available only for Windows x64."
        }
        if (Test-Path -LiteralPath $RuntimeRoot) {
            throw "The managed runtime path exists but does not contain Conda: $RuntimeRoot"
        }
        $miniforgeName = "Miniforge3-26.3.2-2-Windows-x86_64.exe"
        $miniforgeSha256 = "088884aafcbf2e3355671d4e9b227b0d1cfb278e3bbe74ba2ad213c553874d70"
        $miniforgeInstaller = Join-Path $tempDir $miniforgeName
        $miniforgeUrl = "https://github.com/conda-forge/miniforge/releases/download/$MiniforgeVersion/$miniforgeName"
        Write-Host "Downloading Miniforge $MiniforgeVersion..."
        Download-File $miniforgeUrl $miniforgeInstaller
        Assert-Hash $miniforgeInstaller $miniforgeSha256
        New-Item -ItemType Directory -Path (Split-Path -Parent $RuntimeRoot) -Force | Out-Null
        $managedRuntimeIncomplete = $true
        Invoke-Checked -FilePath $miniforgeInstaller -Arguments @("/InstallationType=JustMe", "/RegisterPython=0", "/S", "/D=$RuntimeRoot")
        $condaPath = Join-Path $RuntimeRoot "Scripts\conda.exe"
        Invoke-Checked -FilePath $condaPath -Arguments @("--version")
        @{
            owner = "PaperBrain"
            miniforgeVersion = $MiniforgeVersion
            platform = "win32"
            arch = "x64"
        } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $RuntimeRoot ".paperbrain-managed.json") -Encoding UTF8
        $managedRuntimeIncomplete = $false
    }

    Invoke-Checked -FilePath $condaPath -Arguments @("--version")
    $environments = (& $condaPath "env" "list" "--json" | Out-String | ConvertFrom-Json).envs
    if ($LASTEXITCODE -ne 0) { throw "Could not list Conda environments." }
    $envPath = $environments | Where-Object { (Split-Path -Leaf $_) -ieq "wd" } | Select-Object -First 1
    if (-not $envPath) {
        Write-Host "Creating wd with Python 3.10 and pip 24 or later..."
        Invoke-Checked -FilePath $condaPath -Arguments @("create", "--yes", "--name", "wd", "--override-channels", "--channel", "https://conda.anaconda.org/conda-forge", "python=3.10", "pip>=24")
        $environments = (& $condaPath "env" "list" "--json" | Out-String | ConvertFrom-Json).envs
        if ($LASTEXITCODE -ne 0) { throw "Could not list Conda environments after creation." }
        $envPath = $environments | Where-Object { (Split-Path -Leaf $_) -ieq "wd" } | Select-Object -First 1
    }
    if (-not $envPath) { throw "Conda did not report a wd environment." }
    $pythonPath = Join-Path $envPath "python.exe"
    $paperbrainPath = Join-Path $envPath "Scripts\paperbrain.exe"
    Invoke-Checked -FilePath $pythonPath -Arguments @("-c", 'import pip, sys; assert sys.version_info >= (3, 9), "PaperBrain requires Python 3.9 or later"; major = int(pip.__version__.split(".")[0]); assert major >= 24, "PaperBrain requires pip 24 or later"; print(f"Using Python {sys.version.split()[0]} and pip {pip.__version__}")')

    $releaseBase = "https://github.com/$BackendRepository/releases/download/$BackendTag"
    $wheelPath = Join-Path $tempDir $WheelName
    $requirementsPath = Join-Path $tempDir $RequirementsName
    Write-Host "Downloading and verifying PaperBrain backend $BackendVersion..."
    Download-File "$releaseBase/$WheelName" $wheelPath
    Assert-Hash $wheelPath $WheelSha256
    Download-File "$releaseBase/$RequirementsName" $requirementsPath
    Assert-Hash $requirementsPath $RequirementsSha256

    if ($IndexUrl -eq "auto") {
        $sources = @(
            @{ Label = "Official PyPI"; Url = "https://pypi.org/simple" },
            @{ Label = "Alibaba Cloud"; Url = "https://mirrors.aliyun.com/pypi/simple" },
            @{ Label = "USTC"; Url = "https://mirrors.ustc.edu.cn/pypi/simple" },
            @{ Label = "Tsinghua TUNA"; Url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple" }
        )
        $successful = @()
        foreach ($source in $sources) {
            $probeDir = Join-Path $tempDir ("probe-" + [Guid]::NewGuid().ToString("N"))
            New-Item -ItemType Directory -Path $probeDir | Out-Null
            Write-Host "Testing $($source.Label)..."
            $timer = [Diagnostics.Stopwatch]::StartNew()
            & $pythonPath -m pip download --disable-pip-version-check --no-deps "--only-binary=:all:" --no-cache-dir --timeout 20 --retries 1 --dest $probeDir --index-url $source.Url $ProbeRequirement
            $code = $LASTEXITCODE
            $timer.Stop()
            $files = @(Get-ChildItem -LiteralPath $probeDir -File)
            if ($code -eq 0 -and $files.Count -eq 1 -and (Get-FileHash -Algorithm SHA256 -LiteralPath $files[0].FullName).Hash.ToLowerInvariant() -eq $ProbeSha256) {
                $successful += [PSCustomObject]@{ Label = $source.Label; Url = $source.Url; Elapsed = $timer.ElapsedMilliseconds }
            } else {
                Write-Warning "$($source.Label) did not pass the wheel download and SHA-256 probe."
            }
        }
        $selected = $successful | Sort-Object Elapsed | Select-Object -First 1
        if (-not $selected) { throw "No dependency source passed the download and SHA-256 probe." }
        $IndexUrl = $selected.Url
        Write-Host "Selected $($selected.Label) for dependency installation."
    }

    Invoke-Checked -FilePath $pythonPath -Arguments @("-m", "pip", "install", "--disable-pip-version-check", "--index-url", $IndexUrl, "--require-hashes", "-r", $requirementsPath)
    Invoke-Checked -FilePath $pythonPath -Arguments @("-m", "pip", "install", "--disable-pip-version-check", "--no-deps", "--force-reinstall", $wheelPath)
    New-Item -ItemType Directory -Path $ConfigDir -Force | Out-Null
    $bootstrapOutput = & $paperbrainPath "bootstrap" "--config-dir" $ConfigDir "--vault" $VaultPath | Out-String
    if ($LASTEXITCODE -ne 0) { throw "PaperBrain bootstrap failed with code $LASTEXITCODE." }
    Write-Host $bootstrapOutput
    $bootstrap = $bootstrapOutput | ConvertFrom-Json
    if (-not $bootstrap.ok -or $bootstrap.command -ne "bootstrap" -or -not $bootstrap.config_path) {
        throw "The installed backend did not return a valid bootstrap result."
    }
    $receiptPath = Join-Path $HOME ".paperbrain\runtime\terminal-install.json"
    New-Item -ItemType Directory -Path (Split-Path -Parent $receiptPath) -Force | Out-Null
    $runtimePrefix = $RuntimeRoot.TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    $managedRuntimePath = if ($condaPath.StartsWith($runtimePrefix, [StringComparison]::OrdinalIgnoreCase)) { $RuntimeRoot } else { "" }
    @{
        backendVersion = $BackendVersion
        condaPath = $condaPath
        envPath = $envPath
        pythonPath = $pythonPath
        cliPath = $paperbrainPath
        configPath = [string]$bootstrap.config_path
        managedRuntimePath = $managedRuntimePath
    } | ConvertTo-Json | Set-Content -LiteralPath $receiptPath -Encoding UTF8
    Write-Host "`nPaperBrain backend $BackendVersion is ready. Return to Obsidian and select Detect again."
} finally {
    Remove-Item -LiteralPath $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    if ($managedRuntimeIncomplete) {
        Remove-Item -LiteralPath $RuntimeRoot -Recurse -Force -ErrorAction SilentlyContinue
    }
}
