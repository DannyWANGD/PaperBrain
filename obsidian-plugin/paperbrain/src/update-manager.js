"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

const CONSOLE_REPOSITORY = "DannyWANGD/obsidian-paperbrain";
const BACKEND_REPOSITORY = "DannyWANGD/PaperBrain";
const CONSOLE_ASSET_NAMES = Object.freeze(["main.js", "manifest.json", "styles.css"]);
const ASSET_NAME_PATTERN = /^[A-Za-z0-9][A-Za-z0-9._-]*$/;
const VERSION_PATTERN = /^(\d+)\.(\d+)\.(\d+)$/;

function parseVersion(value) {
  const match = String(value || "").trim().match(VERSION_PATTERN);
  return match ? match.slice(1).map(Number) : null;
}

function compareVersions(left, right) {
  const leftVersion = parseVersion(left);
  const rightVersion = parseVersion(right);
  if (!leftVersion || !rightVersion) throw new Error("Versions must use x.y.z format.");
  for (let index = 0; index < 3; index += 1) {
    if (leftVersion[index] !== rightVersion[index]) return leftVersion[index] - rightVersion[index];
  }
  return 0;
}

function releaseAssetUrl(repository, tag, name) {
  if (![CONSOLE_REPOSITORY, BACKEND_REPOSITORY].includes(repository)
      || !ASSET_NAME_PATTERN.test(String(name || ""))
      || !String(tag || "").trim()) {
    throw new Error("The release asset reference is invalid.");
  }
  return `https://github.com/${repository}/releases/download/${encodeURIComponent(tag)}/${name}`;
}

function latestAssetUrl(repository, name) {
  if (![CONSOLE_REPOSITORY, BACKEND_REPOSITORY].includes(repository)
      || !ASSET_NAME_PATTERN.test(String(name || ""))) {
    throw new Error("The latest release asset reference is invalid.");
  }
  return `https://github.com/${repository}/releases/latest/download/${name}`;
}

function sha256(bytes) {
  return crypto.createHash("sha256").update(bytes).digest("hex");
}

function parseChecksums(value) {
  const result = new Map();
  const lines = String(value || "").split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  if (!lines.length) throw new Error("The release checksum file is empty.");
  for (const line of lines) {
    const match = line.match(/^([a-f0-9]{64})\s+\*?(.+)$/i);
    if (!match) throw new Error("The release checksum file contains an invalid line.");
    const name = match[2].trim();
    if (!ASSET_NAME_PATTERN.test(name)) throw new Error("The release checksum file contains an unsafe asset name.");
    if (result.has(name)) throw new Error(`The release checksum file repeats ${name}.`);
    result.set(name, match[1].toLowerCase());
  }
  return result;
}

function requiredChecksum(checksums, name) {
  const value = checksums.get(name);
  if (!value) throw new Error(`The release checksum file does not include ${name}.`);
  return value;
}

function parseConsoleManifest(bytes) {
  let manifest;
  try {
    manifest = JSON.parse(Buffer.from(bytes).toString("utf8").replace(/^\uFEFF/, ""));
  } catch (_) {
    throw new Error("The latest Console manifest is not valid JSON.");
  }
  if (!manifest || manifest.id !== "paperbrain" || !parseVersion(manifest.version)
      || !parseVersion(manifest.minAppVersion)) {
    throw new Error("The latest Console manifest is not a compatible PaperBrain manifest.");
  }
  return manifest;
}

async function discoverConsoleRelease(download, options = {}) {
  const manifestBytes = await download(
    latestAssetUrl(CONSOLE_REPOSITORY, "manifest.json"),
    { ...options, maxBytes: 64 * 1024 },
  );
  const manifest = parseConsoleManifest(manifestBytes);
  const tag = manifest.version;
  const checksumBytes = await download(
    releaseAssetUrl(CONSOLE_REPOSITORY, tag, "checksums.txt"),
    { ...options, maxBytes: 128 * 1024 },
  );
  const checksums = parseChecksums(checksumBytes.toString("utf8"));
  if (sha256(manifestBytes) !== requiredChecksum(checksums, "manifest.json")) {
    throw new Error("The latest Console manifest failed SHA-256 verification.");
  }
  const assets = {};
  for (const name of CONSOLE_ASSET_NAMES) {
    assets[name] = Object.freeze({ name, sha256: requiredChecksum(checksums, name) });
  }
  return Object.freeze({
    repository: CONSOLE_REPOSITORY,
    version: manifest.version,
    tag,
    manifest: Object.freeze({ ...manifest }),
    assets: Object.freeze(assets),
  });
}

async function discoverBackendRelease(download, baseRelease, options = {}) {
  if (!baseRelease || !baseRelease.dependencyProbe) throw new Error("The embedded backend release is incomplete.");
  const checksumBytes = await download(
    latestAssetUrl(BACKEND_REPOSITORY, "backend-checksums.txt"),
    { ...options, maxBytes: 128 * 1024 },
  );
  const checksums = parseChecksums(checksumBytes.toString("utf8"));
  const wheels = [...checksums.keys()].filter((name) => /^paperbrain-\d+\.\d+\.\d+-py3-none-any\.whl$/.test(name));
  if (wheels.length !== 1) throw new Error("The backend release must contain exactly one universal PaperBrain wheel.");
  const wheelName = wheels[0];
  const versionMatch = wheelName.match(/^paperbrain-(\d+\.\d+\.\d+)-py3-none-any\.whl$/);
  const version = versionMatch && versionMatch[1];
  if (!parseVersion(version)) throw new Error("The backend wheel version is invalid.");
  return Object.freeze({
    repository: BACKEND_REPOSITORY,
    version,
    tag: `backend-${version}`,
    dependencyProbe: baseRelease.dependencyProbe,
    assets: Object.freeze({
      wheel: Object.freeze({ name: wheelName, sha256: requiredChecksum(checksums, wheelName) }),
      requirements: Object.freeze({
        name: "requirements.lock",
        sha256: requiredChecksum(checksums, "requirements.lock"),
      }),
    }),
  });
}

class UpdateManager {
  constructor(options = {}) {
    this.download = options.download;
    this.fs = options.fs || fs.promises;
    this.path = options.pathApi || path;
    this.pluginDir = options.pluginDir || __dirname;
    this.supportsAppVersion = options.supportsAppVersion || (() => true);
  }

  async checkConsole(options = {}) {
    const release = await discoverConsoleRelease(this.download, options);
    if (!this.supportsAppVersion(release.manifest.minAppVersion)) {
      throw new Error(`Console ${release.version} requires Obsidian ${release.manifest.minAppVersion} or later.`);
    }
    return release;
  }

  checkBackend(baseRelease, options = {}) {
    return discoverBackendRelease(this.download, baseRelease, options);
  }

  async installConsole(release, options = {}) {
    if (!release || release.repository !== CONSOLE_REPOSITORY || !parseVersion(release.version)
        || release.tag !== release.version) {
      throw new Error("The Console update release is invalid.");
    }
    if (!release.manifest || !this.supportsAppVersion(release.manifest.minAppVersion)) {
      throw new Error(`Console ${release.version} is not compatible with this Obsidian version.`);
    }
    const root = await this.fs.realpath(this.pluginDir);
    const currentManifest = parseConsoleManifest(await this.fs.readFile(this.path.join(root, "manifest.json")));
    if (currentManifest.id !== release.manifest.id) throw new Error("The current plugin directory is not PaperBrain Console.");

    const temporaryRoot = await this.fs.mkdtemp(this.path.join(root, ".paperbrain-update-"));
    const stagedRoot = this.path.join(temporaryRoot, "staged");
    const backupRoot = this.path.join(temporaryRoot, "backup");
    const replacements = [];
    try {
      await this.fs.mkdir(stagedRoot);
      await this.fs.mkdir(backupRoot);
      for (const name of CONSOLE_ASSET_NAMES) {
        const asset = release.assets && release.assets[name];
        if (!asset || asset.name !== name || !/^[a-f0-9]{64}$/.test(asset.sha256 || "")) {
          throw new Error(`The Console update metadata is incomplete for ${name}.`);
        }
        const maxBytes = name === "main.js" ? 16 * 1024 * 1024 : name === "styles.css" ? 2 * 1024 * 1024 : 64 * 1024;
        const bytes = await this.download(
          releaseAssetUrl(CONSOLE_REPOSITORY, release.tag, name),
          { ...options, maxBytes },
        );
        if (sha256(bytes) !== asset.sha256) throw new Error(`${name} failed SHA-256 verification.`);
        if (name === "manifest.json") {
          const manifest = parseConsoleManifest(bytes);
          if (manifest.version !== release.version || manifest.id !== "paperbrain") {
            throw new Error("The downloaded Console manifest does not match the selected release.");
          }
        }
        await this.fs.writeFile(this.path.join(stagedRoot, name), bytes, { flag: "wx" });
      }

      for (const name of CONSOLE_ASSET_NAMES) {
        const destination = this.path.join(root, name);
        const backup = this.path.join(backupRoot, name);
        const staged = this.path.join(stagedRoot, name);
        await this.fs.rename(destination, backup);
        const replacement = { destination, backup, installed: false };
        replacements.push(replacement);
        await this.fs.rename(staged, destination);
        replacement.installed = true;
      }
      return { ok: true, version: release.version, restartRequired: true };
    } catch (error) {
      const rollbackErrors = [];
      for (const replacement of [...replacements].reverse()) {
        try {
          if (replacement.installed) await this.fs.rm(replacement.destination, { force: true });
          await this.fs.rename(replacement.backup, replacement.destination);
        } catch (rollbackError) {
          rollbackErrors.push(rollbackError.message);
        }
      }
      if (rollbackErrors.length) {
        throw new Error(`${error.message} Rollback also failed: ${rollbackErrors.join(" ")}`);
      }
      throw error;
    } finally {
      try {
        await this.fs.rm(temporaryRoot, { recursive: true, force: true });
      } catch (_) {
        // Runtime files are already committed or rolled back; stale temporary files are harmless.
      }
    }
  }
}

module.exports = {
  BACKEND_REPOSITORY,
  CONSOLE_ASSET_NAMES,
  CONSOLE_REPOSITORY,
  UpdateManager,
  compareVersions,
  discoverBackendRelease,
  discoverConsoleRelease,
  latestAssetUrl,
  parseChecksums,
  parseConsoleManifest,
  parseVersion,
  releaseAssetUrl,
  sha256,
};
