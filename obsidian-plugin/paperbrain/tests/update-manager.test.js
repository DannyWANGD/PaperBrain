"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");

const {
  UpdateManager,
  compareVersions,
  discoverBackendRelease,
  discoverConsoleRelease,
  latestAssetUrl,
  parseChecksums,
  releaseAssetUrl,
  sha256,
} = require("../src/update-manager");

const CONSOLE_REPOSITORY = "DannyWANGD/obsidian-paperbrain";
const BACKEND_REPOSITORY = "DannyWANGD/PaperBrain";

function consoleFixture(version = "0.5.1") {
  const files = {
    "main.js": Buffer.from(`console ${version}`),
    "manifest.json": Buffer.from(JSON.stringify({
      id: "paperbrain",
      name: "PaperBrain Console",
      version,
      minAppVersion: "1.5.0",
      isDesktopOnly: true,
    })),
    "styles.css": Buffer.from(`styles ${version}`),
  };
  const checksums = Buffer.from(Object.entries(files)
    .map(([name, bytes]) => `${sha256(bytes)}  ${name}`)
    .join("\n") + "\n");
  const responses = new Map([
    [latestAssetUrl(CONSOLE_REPOSITORY, "manifest.json"), files["manifest.json"]],
    [releaseAssetUrl(CONSOLE_REPOSITORY, version, "checksums.txt"), checksums],
    ...Object.entries(files).map(([name, bytes]) => [releaseAssetUrl(CONSOLE_REPOSITORY, version, name), bytes]),
  ]);
  const download = async (url) => {
    if (!responses.has(url)) throw new Error(`Unexpected download: ${url}`);
    return responses.get(url);
  };
  return { files, checksums, download };
}

async function temporaryPlugin(t) {
  const root = await fs.promises.mkdtemp(path.join(os.tmpdir(), "paperbrain-update-test-"));
  t.after(() => fs.promises.rm(root, { recursive: true, force: true }));
  const original = {
    "main.js": Buffer.from("old main"),
    "manifest.json": Buffer.from(JSON.stringify({
      id: "paperbrain",
      name: "PaperBrain Console",
      version: "0.5.0",
      minAppVersion: "1.5.0",
    })),
    "styles.css": Buffer.from("old styles"),
  };
  for (const [name, bytes] of Object.entries(original)) await fs.promises.writeFile(path.join(root, name), bytes);
  return { root, original };
}

test("semantic versions compare without lexical ordering errors", () => {
  assert.equal(compareVersions("0.5.1", "0.5.0") > 0, true);
  assert.equal(compareVersions("0.10.0", "0.9.9") > 0, true);
  assert.equal(compareVersions("1.2.3", "1.2.3"), 0);
  assert.throws(() => compareVersions("1.2", "1.2.0"), /x\.y\.z/);
});

test("checksum parsing rejects duplicate and unsafe asset names", () => {
  const hash = "a".repeat(64);
  assert.equal(parseChecksums(`${hash}  main.js`).get("main.js"), hash);
  assert.throws(() => parseChecksums(`${hash}  ../main.js`), /unsafe asset name/);
  assert.throws(() => parseChecksums(`${hash}  main.js\n${hash}  main.js`), /repeats main\.js/);
});

test("Console discovery uses the stable manifest and exact tagged checksums", async () => {
  const fixture = consoleFixture();
  const release = await discoverConsoleRelease(fixture.download);
  assert.equal(release.version, "0.5.1");
  assert.equal(release.tag, "0.5.1");
  assert.deepEqual(Object.keys(release.assets).sort(), ["main.js", "manifest.json", "styles.css"]);
  assert.equal(release.assets["main.js"].sha256, sha256(fixture.files["main.js"]));
});

test("Console discovery rejects a manifest that is not checksummed", async () => {
  const fixture = consoleFixture();
  const badChecksums = Buffer.from(fixture.checksums.toString("utf8").replace(sha256(fixture.files["manifest.json"]), "0".repeat(64)));
  const download = async (url) => url.endsWith("checksums.txt") ? badChecksums : fixture.download(url);
  await assert.rejects(discoverConsoleRelease(download), /manifest failed SHA-256/);
});

test("backend discovery derives a fixed tagged wheel release", async () => {
  const wheel = "paperbrain-0.3.7-py3-none-any.whl";
  const checksums = Buffer.from(`${"a".repeat(64)}  ${wheel}\n${"b".repeat(64)}  requirements.lock\n`);
  const release = await discoverBackendRelease(
    async (url) => {
      assert.equal(url, latestAssetUrl(BACKEND_REPOSITORY, "backend-checksums.txt"));
      return checksums;
    },
    { dependencyProbe: { requirement: "openai==2.46.0", sha256: "c".repeat(64) } },
  );
  assert.equal(release.version, "0.3.7");
  assert.equal(release.tag, "backend-0.3.7");
  assert.equal(release.assets.wheel.name, wheel);
  assert.equal(release.assets.requirements.sha256, "b".repeat(64));
});

test("backend discovery rejects ambiguous wheels", async () => {
  const checksums = Buffer.from([
    `${"a".repeat(64)}  paperbrain-0.3.7-py3-none-any.whl`,
    `${"b".repeat(64)}  paperbrain-0.3.8-py3-none-any.whl`,
    `${"c".repeat(64)}  requirements.lock`,
  ].join("\n"));
  await assert.rejects(
    discoverBackendRelease(async () => checksums, { dependencyProbe: {} }),
    /exactly one universal PaperBrain wheel/,
  );
});

test("Console installation replaces only release runtime assets", async (t) => {
  const { root } = await temporaryPlugin(t);
  const fixture = consoleFixture();
  await fs.promises.writeFile(path.join(root, "data.json"), "preserved");
  const manager = new UpdateManager({ download: fixture.download, pluginDir: root });
  const release = await manager.checkConsole();
  const result = await manager.installConsole(release);

  assert.deepEqual(result, { ok: true, version: "0.5.1", restartRequired: true });
  for (const [name, bytes] of Object.entries(fixture.files)) {
    assert.deepEqual(await fs.promises.readFile(path.join(root, name)), bytes);
  }
  assert.equal(await fs.promises.readFile(path.join(root, "data.json"), "utf8"), "preserved");
  assert.deepEqual((await fs.promises.readdir(root)).sort(), ["data.json", "main.js", "manifest.json", "styles.css"]);
});

test("Console installation verifies every download before changing files", async (t) => {
  const { root, original } = await temporaryPlugin(t);
  const fixture = consoleFixture();
  const download = async (url) => url.endsWith("styles.css") ? Buffer.from("tampered") : fixture.download(url);
  const manager = new UpdateManager({ download, pluginDir: root });
  const release = await manager.checkConsole();
  await assert.rejects(manager.installConsole(release), /styles\.css failed SHA-256/);
  for (const [name, bytes] of Object.entries(original)) {
    assert.deepEqual(await fs.promises.readFile(path.join(root, name)), bytes);
  }
});

test("Console installation rolls back all files when replacement fails", async (t) => {
  const { root, original } = await temporaryPlugin(t);
  const fixture = consoleFixture();
  const failingFs = Object.create(fs.promises);
  failingFs.rename = async (source, destination) => {
    if (source.includes(`${path.sep}staged${path.sep}`) && path.basename(source) === "styles.css") {
      throw new Error("simulated replacement failure");
    }
    return fs.promises.rename(source, destination);
  };
  const manager = new UpdateManager({ download: fixture.download, pluginDir: root, fs: failingFs });
  const release = await manager.checkConsole();
  await assert.rejects(manager.installConsole(release), /simulated replacement failure/);
  for (const [name, bytes] of Object.entries(original)) {
    assert.deepEqual(await fs.promises.readFile(path.join(root, name)), bytes);
  }
});

test("Console discovery enforces the running Obsidian compatibility check", async () => {
  const fixture = consoleFixture();
  const manager = new UpdateManager({
    download: fixture.download,
    supportsAppVersion: () => false,
  });
  await assert.rejects(manager.checkConsole(), /requires Obsidian 1\.5\.0 or later/);
});

test("Console installation rechecks Obsidian compatibility before writing", async (t) => {
  const { root, original } = await temporaryPlugin(t);
  const fixture = consoleFixture();
  const release = await discoverConsoleRelease(fixture.download);
  const manager = new UpdateManager({
    download: fixture.download,
    pluginDir: root,
    supportsAppVersion: () => false,
  });
  await assert.rejects(manager.installConsole(release), /not compatible with this Obsidian version/);
  for (const [name, bytes] of Object.entries(original)) {
    assert.deepEqual(await fs.promises.readFile(path.join(root, name)), bytes);
  }
});

test("Console installation rejects unresolved or packaged application directories", async () => {
  const fixture = consoleFixture();
  const release = await discoverConsoleRelease(fixture.download);
  for (const pluginDir of ["", "/opt/Obsidian/resources/electron.asar"]) {
    const manager = new UpdateManager({ download: fixture.download, pluginDir });
    await assert.rejects(manager.installConsole(release), /plugin directory could not be resolved safely/);
  }
});
