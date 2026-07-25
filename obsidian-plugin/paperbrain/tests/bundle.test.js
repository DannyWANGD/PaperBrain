"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const Module = require("node:module");
const os = require("node:os");
const path = require("node:path");

class ObsidianBase {}
let openedModalDetails = null;

class ModalStub extends ObsidianBase {
  constructor(app) {
    super();
    this.app = app;
  }

  open() {
    openedModalDetails = this.details;
    if (typeof this.resolve === "function") {
      const resolve = this.resolve;
      this.resolve = null;
      resolve(true);
    }
  }

  close() {}
}

function loadPluginClass() {
  const originalLoad = Module._load;
  Module._load = function load(request, parent, isMain) {
    if (request === "obsidian") {
      return {
        ItemView: ObsidianBase,
        Modal: ModalStub,
        Notice: class Notice {},
        Plugin: ObsidianBase,
        PluginSettingTab: ObsidianBase,
        Setting: class Setting {},
        normalizePath: (value) => value,
        requireApiVersion: () => true,
        setIcon: () => {},
      };
    }
    return originalLoad.call(this, request, parent, isMain);
  };
  try {
    const bundlePath = path.resolve(__dirname, "..", "main.js");
    delete require.cache[bundlePath];
    return require(bundlePath);
  } finally {
    Module._load = originalLoad;
  }
}

test("built main.js exports an Obsidian plugin class", () => {
  assert.equal(typeof loadPluginClass(), "function");
  const bundle = fs.readFileSync(path.resolve(__dirname, "..", "main.js"), "utf8");
  const source = fs.readFileSync(path.resolve(__dirname, "..", "src", "main.js"), "utf8");
  const styles = fs.readFileSync(path.resolve(__dirname, "..", "styles.css"), "utf8");
  assert.match(bundle, /API key file/);
  assert.match(bundle, /Open \.env file/);
  for (const section of [
    "discovery",
    "runtime",
    "network",
    "advanced-section",
  ]) {
    assert.match(source, new RegExp(`createSection\\([\\s\\S]*?"${section}"`));
  }
  assert.match(styles, /\.paperbrain-settings-section/);
  assert.match(styles, /@media \(min-width: 1201px\)/);
  assert.match(styles, /flex-wrap: wrap/);
  assert.match(bundle, /Save discovery preferences/);
  assert.match(bundle, /Choose categories/);
});

test("discovery saves are blocked while runs, installs, or updates are active", () => {
  const PluginClass = loadPluginClass();
  const plugin = new PluginClass();
  let runActive = true;
  let installActive = false;
  plugin.processManager = { snapshot: () => ({ running: runActive }) };
  plugin.backendInstaller = { snapshot: () => ({ running: installActive }) };
  plugin.softwareUpdates = { checking: false, console: null, backend: null };

  assert.match(plugin.discoverySaveBlockReason(), /active PaperBrain run/);
  runActive = false;
  installActive = true;
  assert.match(plugin.discoverySaveBlockReason(), /backend installation/);
  installActive = false;
  plugin.softwareUpdates.checking = true;
  assert.match(plugin.discoverySaveBlockReason(), /software update/);
  plugin.softwareUpdates.checking = false;
  assert.equal(plugin.discoverySaveBlockReason(), "");
});

test("discovery config resolution follows explicit, source, and managed runtime modes", () => {
  const PluginClass = loadPluginClass();
  const plugin = new PluginClass();
  const custom = path.join(os.tmpdir(), "paperbrain-custom.yaml");
  plugin.settings = {
    configPath: custom,
    backendPath: "",
    vaultPath: os.tmpdir(),
    executionMode: "cli",
    cliPath: "paperbrain",
  };
  assert.equal(plugin.discoveryConfigPath(), custom);

  plugin.settings.configPath = "";
  assert.equal(plugin.discoveryConfigPath(), path.join(os.homedir(), ".paperbrain", "config", "config.yaml"));

  plugin.settings.executionMode = "python-script";
  plugin.settings.backendPath = path.join(os.tmpdir(), "paperbrain-source");
  assert.equal(plugin.discoveryConfigPath(), path.join(plugin.settings.backendPath, "script", "config", "config.yaml"));
});

test("backend installation passes the resolved automatic dependency source to the installer", async () => {
  const PluginClass = loadPluginClass();
  const plugin = new PluginClass();
  let installPlan = null;
  openedModalDetails = null;
  plugin.app = {};
  plugin.settings = {
    dependencySource: "auto",
    customDependencyIndex: "",
    vaultPath: "/tmp/paperbrain-vault",
    proxyMode: "manual",
    proxyUrl: "http://127.0.0.1:7890",
  };
  plugin.processManager = { snapshot: () => ({ running: false }) };
  plugin.backendInstaller = {
    snapshot: () => ({ running: false }),
    install: async (plan) => {
      installPlan = plan;
      return { ok: false };
    },
  };
  plugin.detectCondaExecutable = async () => "/tmp/conda";

  await plugin.installBackend();

  assert.equal(openedModalDetails.dependencyIndex.id, "auto");
  assert.ok(installPlan);
  assert.equal(installPlan.dependencyIndex.id, "auto");
  assert.equal(installPlan.dependencyIndex.candidates.length, 4);
  assert.ok(installPlan.environment);
  assert.equal(installPlan.proxyMode, "manual");
  assert.equal(installPlan.proxyUrl, "http://127.0.0.1:7890");
  assert.equal(installPlan.environment.HTTPS_PROXY, "http://127.0.0.1:7890");
});

test("terminal installation exposes verified commands for Windows, macOS, and Linux", () => {
  const PluginClass = loadPluginClass();
  const plugin = new PluginClass();
  openedModalDetails = null;
  plugin.app = {};
  plugin.settings = {
    dependencySource: "auto",
    customDependencyIndex: "",
    vaultPath: "/tmp/paperbrain-vault",
  };

  assert.equal(plugin.showManualBackendInstall(), true);
  assert.ok(openedModalDetails);
  assert.equal(openedModalDetails.backendVersion, "0.3.7");
  assert.deepEqual(Object.keys(openedModalDetails.commands).sort(), ["darwin", "linux", "win32"]);
  assert.match(openedModalDetails.commands.win32, /install-backend\.ps1/);
  assert.match(openedModalDetails.commands.darwin, /install-backend\.sh/);
  assert.match(openedModalDetails.commands.linux, /sha256sum -c -/);
  for (const command of Object.values(openedModalDetails.commands)) {
    assert.match(command, /releases\/download\/0\.6\.0/);
    assert.match(command, /auto/);
  }
});

test("software update checks keep Console and backend results independent", async () => {
  const PluginClass = loadPluginClass();
  const plugin = new PluginClass();
  plugin.manifest = { version: "0.6.0" };
  plugin.settings = { installedBackendVersion: "0.3.7" };
  plugin.softwareUpdates = { checking: false, checked: false, console: null, backend: null, pendingConsoleVersion: "" };
  plugin.processManager = { snapshot: () => ({ running: false }) };
  plugin.backendInstaller = { snapshot: () => ({ running: false }) };
  plugin.detectSetup = async () => {};
  plugin.detectInstalledBackendVersion = async () => ({
    version: "0.3.7",
    source: "runtime",
    mode: "python-script",
    managed: false,
  });
  plugin.updateNetworkOptions = () => ({});
  plugin.updateManager = {
    checkConsole: async () => { throw new Error("Console network unavailable"); },
    checkBackend: async () => ({ version: "0.3.7", tag: "backend-0.3.7" }),
  };

  assert.equal(await plugin.checkSoftwareUpdates(), true);
  assert.match(plugin.softwareUpdates.console.status, /Console update check failed/);
  assert.match(plugin.softwareUpdates.backend.status, /source mode and is developer-managed/);
  assert.equal(plugin.softwareUpdates.backend.available, false);
});

test("managed backend update reuses the discovered release without another confirmation", async () => {
  const PluginClass = loadPluginClass();
  const plugin = new PluginClass();
  const release = { version: "0.3.7", tag: "backend-0.3.7" };
  let installOptions = null;
  plugin.softwareUpdates = {
    checking: false,
    console: null,
    backend: { available: true, managed: true, release, updating: false },
  };
  plugin.processManager = { snapshot: () => ({ running: false }) };
  plugin.backendInstaller = { snapshot: () => ({ running: false }) };
  plugin.activateView = async () => {};
  plugin.installBackend = async (options) => {
    installOptions = options;
    return true;
  };

  assert.equal(await plugin.updateBackend(), true);
  assert.deepEqual(installOptions, { release, skipConfirmation: true });
  assert.equal(plugin.softwareUpdates.backend.available, false);
  assert.match(plugin.softwareUpdates.backend.status, /0\.3\.7 is up to date/);
});

test("backend update failures restore the settings action", async () => {
  const PluginClass = loadPluginClass();
  const plugin = new PluginClass();
  plugin.softwareUpdates = {
    checking: false,
    console: null,
    backend: {
      available: true,
      managed: true,
      release: { version: "0.3.7", tag: "backend-0.3.7" },
      updating: false,
    },
  };
  plugin.processManager = { snapshot: () => ({ running: false }) };
  plugin.backendInstaller = { snapshot: () => ({ running: false }) };
  plugin.activateView = async () => {};
  plugin.installBackend = async () => { throw new Error("simulated update failure"); };

  assert.equal(await plugin.updateBackend(), false);
  assert.equal(plugin.softwareUpdates.backend.updating, false);
  assert.match(plugin.softwareUpdates.backend.status, /simulated update failure/);
});

test("setup detection wires a manually installed wd CLI into plugin settings", async (t) => {
  const PluginClass = loadPluginClass();
  const plugin = new PluginClass();
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "paperbrain-manual-detect-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const envPath = path.join(root, "wd");
  const pythonPath = process.platform === "win32"
    ? path.join(envPath, "python.exe")
    : path.join(envPath, "bin", "python");
  const cliPath = process.platform === "win32"
    ? path.join(envPath, "Scripts", "paperbrain.exe")
    : path.join(envPath, "bin", "paperbrain");
  fs.mkdirSync(path.dirname(pythonPath), { recursive: true });
  fs.mkdirSync(path.dirname(cliPath), { recursive: true });
  fs.writeFileSync(pythonPath, "");
  fs.writeFileSync(cliPath, "");
  plugin.settings = {
    backendPath: "",
    vaultPath: root,
    pythonPath,
    condaPath: "",
    executionMode: "auto",
  };
  plugin.detectCondaExecutable = async () => "";
  plugin.saveSettings = async () => {};

  const result = await plugin.detectSetup();

  assert.equal(result.pythonPath, pythonPath);
  assert.equal(plugin.settings.cliPath, cliPath);
  assert.equal(plugin.settings.executionMode, "cli");
});

test("the API key file remains addressable without the setup guide", () => {
  const PluginClass = loadPluginClass();
  const plugin = new PluginClass();
  plugin.settings = { configPath: "" };
  assert.equal(plugin.managedEnvFilePath(), path.join(os.homedir(), ".paperbrain", "config", ".env"));

  const customConfig = path.join(os.tmpdir(), "paperbrain-custom-config", "config.yaml");
  plugin.settings.configPath = customConfig;
  assert.equal(plugin.managedEnvFilePath(), path.join(path.dirname(customConfig), ".env"));
});
