"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const childProcess = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const root = path.resolve(__dirname, "..");

function readJson(name) {
  return JSON.parse(fs.readFileSync(path.join(root, name), "utf8"));
}

test("package, manifest, and compatibility versions stay aligned", () => {
  const packageJson = readJson("package.json");
  const packageLock = readJson("package-lock.json");
  const manifest = readJson("manifest.json");
  const versions = readJson("versions.json");
  assert.equal(packageJson.version, manifest.version);
  assert.equal(packageLock.version, manifest.version);
  assert.equal(packageLock.packages[""].version, manifest.version);
  assert.equal(versions[manifest.version], manifest.minAppVersion);
  assert.match(manifest.version, /^\d+\.\d+\.\d+$/);
  assert.match(manifest.id, /^[a-z][a-z-]*$/);
  assert.equal(manifest.id.includes("obsidian"), false);
  assert.equal(manifest.id.endsWith("plugin"), false);
  assert.equal(manifest.isDesktopOnly, true);
  assert.equal(manifest.author, "DannyWANGD");
  assert.equal(manifest.authorUrl, "https://github.com/DannyWANGD");
});

test("release runtime assets and canonical source files exist", () => {
  for (const name of [
    "main.js", "manifest.json", "styles.css", "src/main.js", "src/runtime.js", "src/process-manager.js",
    "src/backend-installer.js", "src/backend-release.js", "src/miniforge-release.js",
    "src/manual-install.js", "src/update-manager.js", "installers/install-backend.ps1", "installers/install-backend.sh",
    "README.md", "README_EN.md",
  ]) {
    assert.equal(fs.existsSync(path.join(root, name)), true, `${name} should exist`);
  }
});

test("backend installer assets are versioned, checksummed, and documented", () => {
  const { BACKEND_RELEASE } = require("../src/backend-release");
  const { MINIFORGE_RELEASE } = require("../src/miniforge-release");
  for (const asset of [
    ...Object.values(BACKEND_RELEASE.assets),
    ...Object.values(MINIFORGE_RELEASE.assets),
  ]) {
    assert.match(asset.sha256, /^[a-f0-9]{64}$/, `${asset.name} needs a fixed SHA-256`);
  }
  assert.match(BACKEND_RELEASE.dependencyProbe.requirement, /^[A-Za-z0-9][A-Za-z0-9._-]*==[A-Za-z0-9][A-Za-z0-9._+-]*$/);
  assert.match(BACKEND_RELEASE.dependencyProbe.sha256, /^[a-f0-9]{64}$/);
  const readme = fs.readFileSync(path.join(root, "README_EN.md"), "utf8");
  assert.match(readme, /Terminal install/);
  assert.match(readme, /Install inside Obsidian/);
  assert.match(readme, /Miniforge 26\.3\.2-2/);
  assert.match(readme, /does not modify\s+(?:the )?system PATH/i);
  assert.match(readme, /~\/\.paperbrain\/runtime\/miniforge3/);
  assert.match(readme, /backend-0\.3\.6/);
  assert.match(readme, /install-backend\.ps1/);
  assert.match(readme, /install-backend\.sh/);
});

test("Chinese and English setup guides are switchable and installation-complete", () => {
  const chinese = fs.readFileSync(path.join(root, "README.md"), "utf8");
  const english = fs.readFileSync(path.join(root, "README_EN.md"), "utf8");
  assert.match(chinese, /\[English\]\(README_EN\.md\)/);
  assert.match(english, /\[简体中文\]\(README\.md\)/);
  for (const readme of [chinese, english]) {
    assert.match(readme, /https:\/\/github\.com\/DannyWANGD\/obsidian-paperbrain/);
    for (const asset of ["main.js", "manifest.json", "styles.css", "install-backend.ps1", "install-backend.sh", "checksums.txt"]) {
      assert.equal(readme.includes(`\`${asset}\``), true, `${asset} should be explained in both READMEs`);
    }
    assert.match(readme, /backend-0\.3\.6/);
    assert.match(readme, /Miniforge 26\.3\.2-2/);
    assert.match(readme, /\.paperbrain[\\/]runtime[\\/]miniforge3/);
    assert.match(readme, /\.paperbrain[\\/]config/);
  }
});

test("optional companion plugin snapshot stays versioned and dependency-free", () => {
  const manifest = readJson("manifest.json");
  const companions = readJson(path.join("docs", "companion-plugins.json"));
  assert.equal(companions.paperbrainVersion, manifest.version);
  assert.deepEqual(companions.required, []);
  const enabledIds = companions.testedOptional.map((item) => item.id);
  const installedIds = companions.installedOptional.map((item) => item.id);
  const expectedEnabledIds = [
    "obsidian42-brat", "dataview", "obsidian-audio-player", "floating-toc",
    "highlightr-plugin", "obsidian-style-settings", "immersive-translate",
    "smart-connections", "copilot", "realclaudian",
  ];
  assert.deepEqual(enabledIds, expectedEnabledIds);
  assert.deepEqual(installedIds, ["aqu-translay-translator", "components"]);
  const allIds = [...enabledIds, ...installedIds];
  assert.equal(new Set(allIds).size, allIds.length);
  const docs = ["README.md", "README_EN.md", path.join("docs", "COMPANION_PLUGINS.md")]
    .map((name) => ({ name, text: fs.readFileSync(path.join(root, name), "utf8") }));
  for (const id of allIds) {
    for (const doc of docs) {
      assert.equal(doc.text.includes(`\`${id}\``), true, `${id} should be documented in ${doc.name}`);
    }
  }
});

test("release workflow publishes the stable release assets", () => {
  const workflow = fs.readFileSync(path.join(root, ".github", "workflows", "release.yml"), "utf8");
  assert.match(workflow, /gh release create/);
  assert.match(workflow, /installers\/install-backend\.ps1 installers\/install-backend\.sh checksums\.txt/);
  assert.match(workflow, /bash -n installers\/install-backend\.sh/);
  assert.match(workflow, /Language\.Parser/);
  assert.doesNotMatch(workflow, /--prerelease/);
});

test("generated and local-only files stay outside source commits", () => {
  const ignore = fs.readFileSync(path.join(root, ".gitignore"), "utf8").split(/\r?\n/);
  for (const name of ["/main.js", "node_modules/", "data.json"]) {
    assert.equal(ignore.includes(name), true, `${name} should be ignored`);
  }

  const isIgnored = (name) => childProcess.spawnSync(
    "git",
    ["check-ignore", "--no-index", "--quiet", "--", name],
    { cwd: root },
  ).status === 0;
  assert.equal(isIgnored("main.js"), true, "the generated root bundle should be ignored");
  assert.equal(isIgnored("src/main.js"), false, "the canonical plugin source must be tracked");
});
