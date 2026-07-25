"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");

const {
  MANUAL_INSTALL_RELEASE,
  buildManualInstallCommand,
  installerAssetUrl,
  manualInstallReceiptPath,
  normalizeManualInstallReceipt,
  platformForManualInstall,
} = require("../src/manual-install");

const root = path.resolve(__dirname, "..");
const AUTO_INDEX = { id: "auto", label: "Automatic", candidates: [] };

function fileSha256(name) {
  return crypto.createHash("sha256").update(fs.readFileSync(path.join(root, "installers", name))).digest("hex");
}

test("manual installer assets have the hashes embedded in generated commands", () => {
  for (const asset of Object.values(MANUAL_INSTALL_RELEASE.assets)) {
    assert.equal(fileSha256(asset.name), asset.sha256);
    assert.match(installerAssetUrl(asset), new RegExp(`/releases/download/${MANUAL_INSTALL_RELEASE.tag}/${asset.name}$`));
  }
});

test("the Unix installer resolves wd without parsing conda-run trailing output", () => {
  const installer = fs.readFileSync(path.join(root, "installers", "install-backend.sh"), "utf8");
  assert.match(installer, /cd "\$HOME"/);
  assert.match(installer, /"\$CONDA_PATH" info --base/);
  assert.match(installer, /sys\.stdout\.write/);
  assert.doesNotMatch(installer, /run -n base python/);
  assert.doesNotMatch(installer, /tail -n 1/);
});

test("Windows command downloads, verifies, and runs the PowerShell installer", () => {
  const command = buildManualInstallCommand("win32", {
    vaultPath: "C:\\Researcher's Vault",
    dependencyIndex: AUTO_INDEX,
  });
  assert.match(command, /Invoke-WebRequest/);
  assert.match(command, /Get-FileHash -Algorithm SHA256/);
  assert.match(command, /install-backend\.ps1/);
  assert.match(command, /C:\\Researcher''s Vault/);
  assert.match(command, /-IndexUrl 'auto'/);
  assert.match(command, /-ExecutionPolicy Bypass/);
});

test("macOS and Linux commands use native SHA-256 checks and preserve shell-safe paths", () => {
  const options = {
    vaultPath: "/Users/demo/Researcher's Vault",
    dependencyIndex: { id: "custom", url: "https://packages.example.org/pypi/simple" },
  };
  const mac = buildManualInstallCommand("darwin", options);
  const linux = buildManualInstallCommand("linux", options);
  for (const command of [mac, linux]) {
    assert.match(command, /curl --fail --location/);
    assert.match(command, /install-backend\.sh/);
    assert.equal(command.includes(`Researcher'"'"'s Vault`), true);
    assert.match(command, /https:\/\/packages\.example\.org\/pypi\/simple/);
    assert.match(command, /bash \"\$tmp\"/);
  }
  assert.match(mac, /shasum -a 256 -c -/);
  assert.match(linux, /sha256sum -c -/);
});

test("unsupported command targets and incomplete settings fail before copying", () => {
  assert.throws(() => buildManualInstallCommand("freebsd", { vaultPath: "/tmp/vault", dependencyIndex: AUTO_INDEX }), /not available/);
  assert.throws(() => buildManualInstallCommand("linux", { vaultPath: "", dependencyIndex: AUTO_INDEX }), /vault path/);
  assert.throws(() => buildManualInstallCommand("linux", { vaultPath: "/tmp/vault", dependencyIndex: {} }), /dependency source/);
  assert.equal(platformForManualInstall("darwin"), "darwin");
  assert.equal(platformForManualInstall("freebsd"), "linux");
});

test("terminal installation receipts are accepted only when every required path exists", () => {
  const raw = {
    backendVersion: "0.3.7",
    condaPath: "/opt/conda/bin/conda",
    envPath: "/opt/conda/envs/wd",
    pythonPath: "/opt/conda/envs/wd/bin/python",
    cliPath: "/opt/conda/envs/wd/bin/paperbrain",
    configPath: "/home/demo/.paperbrain/config/config.yaml",
    managedRuntimePath: "",
  };
  const existing = new Set(Object.values(raw));
  const receipt = normalizeManualInstallReceipt(raw, (value) => existing.has(value));
  assert.equal(receipt.cliPath, raw.cliPath);
  assert.equal(normalizeManualInstallReceipt({ ...raw, cliPath: "/missing" }, (value) => existing.has(value)), null);
  assert.equal(manualInstallReceiptPath("/home/demo"), path.join("/home/demo", ".paperbrain", "runtime", "terminal-install.json"));
});
