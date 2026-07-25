"use strict";

const path = require("path");

const MANUAL_INSTALL_RELEASE = Object.freeze({
  repository: "DannyWANGD/obsidian-paperbrain",
  tag: "0.6.0",
  assets: Object.freeze({
    windows: Object.freeze({
      name: "install-backend.ps1",
      sha256: "2d74b5a460a86c470ddbd86de70b83f3e7f45b9e0b7cd428e1049c9683a0f3e6",
    }),
    unix: Object.freeze({
      name: "install-backend.sh",
      sha256: "5112f29488be8020392a39f675fe4248042144bb6a52991059bcd73a3cf126c0",
    }),
  }),
});

const MANUAL_PLATFORMS = Object.freeze([
  Object.freeze({ id: "win32", label: "Windows (PowerShell)" }),
  Object.freeze({ id: "darwin", label: "macOS (Terminal)" }),
  Object.freeze({ id: "linux", label: "Linux (Terminal)" }),
]);

function installerAssetUrl(asset, release = MANUAL_INSTALL_RELEASE) {
  return `https://github.com/${release.repository}/releases/download/${release.tag}/${asset.name}`;
}

function powershellQuote(value) {
  return `'${String(value || "").replace(/'/g, "''")}'`;
}

function shellQuote(value) {
  return `'${String(value || "").replace(/'/g, `'"'"'`)}'`;
}

function manualIndexArgument(dependencyIndex) {
  if (dependencyIndex && dependencyIndex.id === "auto") return "auto";
  const url = dependencyIndex && dependencyIndex.url ? String(dependencyIndex.url) : "";
  if (!url) throw new Error("A valid dependency source is required before generating the terminal command.");
  return url;
}

function buildManualInstallCommand(platform, options = {}) {
  const vaultPath = String(options.vaultPath || "").trim();
  if (!vaultPath) throw new Error("A vault path is required before generating the terminal command.");
  const indexUrl = manualIndexArgument(options.dependencyIndex);
  const release = options.release || MANUAL_INSTALL_RELEASE;
  if (platform === "win32") {
    const asset = release.assets.windows;
    const url = installerAssetUrl(asset, release);
    const tempName = `paperbrain-install-backend-${release.tag}.ps1`;
    return [
      `$url=${powershellQuote(url)}`,
      `$file=Join-Path ([IO.Path]::GetTempPath()) ${powershellQuote(tempName)}`,
      "$curl=Get-Command curl.exe -ErrorAction SilentlyContinue",
      "if ($curl) { & $curl.Source --fail --location --retry 2 --output $file $url; if ($LASTEXITCODE -ne 0) { throw 'PaperBrain installer download failed.' } } else { Invoke-WebRequest -UseBasicParsing -Uri $url -OutFile $file }",
      `$expected=${powershellQuote(asset.sha256)}`,
      "$actual=(Get-FileHash -Algorithm SHA256 -LiteralPath $file).Hash.ToLowerInvariant()",
      "if ($actual -ne $expected) { Remove-Item -LiteralPath $file -Force; throw 'PaperBrain installer SHA-256 verification failed.' }",
      `& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $file -VaultPath ${powershellQuote(vaultPath)} -IndexUrl ${powershellQuote(indexUrl)}`,
      "$code=$LASTEXITCODE",
      "Remove-Item -LiteralPath $file -Force -ErrorAction SilentlyContinue",
      "if ($code -ne 0) { throw \"PaperBrain installation failed with exit code $code.\" }",
    ].join("; ");
  }
  if (platform !== "darwin" && platform !== "linux") {
    throw new Error(`Terminal installation is not available for ${platform}.`);
  }
  const asset = release.assets.unix;
  const url = installerAssetUrl(asset, release);
  const checker = platform === "darwin" ? "shasum -a 256 -c -" : "sha256sum -c -";
  const download = `if command -v curl >/dev/null 2>&1; then curl --fail --location --retry 2 ${shellQuote(url)} --output "$tmp"; elif command -v wget >/dev/null 2>&1; then wget --tries=3 --timeout=20 --output-document="$tmp" ${shellQuote(url)}; else echo 'curl or wget is required.' >&2; false; fi`;
  const guarded = [
    "status=0",
    `{ ${download}; } && ${`printf '%s  %s\\n' ${shellQuote(asset.sha256)} "$tmp" | ${checker}`} && ${`bash "$tmp" --vault ${shellQuote(vaultPath)} --index-url ${shellQuote(indexUrl)}`} || status=$?`,
    'rm -f "$tmp"',
    '(exit "$status")',
  ].join("; ");
  return `tmp="$(mktemp "${"${TMPDIR:-/tmp}"}/paperbrain-install.XXXXXX")" && { ${guarded}; }`;
}

function platformForManualInstall(platform = process.platform) {
  return MANUAL_PLATFORMS.some((item) => item.id === platform) ? platform : "linux";
}

function manualInstallReceiptPath(home, pathApi = path) {
  return pathApi.join(String(home || ""), ".paperbrain", "runtime", "terminal-install.json");
}

function normalizeManualInstallReceipt(raw, existsSync) {
  if (!raw || typeof raw !== "object" || typeof existsSync !== "function") return null;
  const receipt = {};
  for (const key of ["backendVersion", "condaPath", "envPath", "pythonPath", "cliPath", "configPath", "managedRuntimePath"]) {
    receipt[key] = typeof raw[key] === "string" ? raw[key].trim() : "";
  }
  if (!/^\d+\.\d+\.\d+$/.test(receipt.backendVersion)
      || !receipt.condaPath || !receipt.envPath || !receipt.pythonPath || !receipt.cliPath || !receipt.configPath) return null;
  for (const key of ["condaPath", "envPath", "pythonPath", "cliPath", "configPath"]) {
    try {
      if (!existsSync(receipt[key])) return null;
    } catch (_) {
      return null;
    }
  }
  if (receipt.managedRuntimePath) {
    try {
      if (!existsSync(receipt.managedRuntimePath)) receipt.managedRuntimePath = "";
    } catch (_) {
      receipt.managedRuntimePath = "";
    }
  }
  return receipt;
}

module.exports = {
  MANUAL_INSTALL_RELEASE,
  MANUAL_PLATFORMS,
  buildManualInstallCommand,
  installerAssetUrl,
  manualInstallReceiptPath,
  manualIndexArgument,
  normalizeManualInstallReceipt,
  platformForManualInstall,
  powershellQuote,
  shellQuote,
};
