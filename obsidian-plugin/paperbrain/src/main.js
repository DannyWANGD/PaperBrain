const { ItemView, Modal, Notice, Plugin, PluginSettingTab, Setting, normalizePath, requireApiVersion, setIcon } = require("obsidian");
const childProcess = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");
const {
  buildInvocation,
  buildManagedEnvironment,
  buildSpawnOptions,
  cliExecutableForEnv,
  condaExecutableCandidates,
  detectBackendPath,
  detectVaultPath,
  detectWdPython,
  isCompatibleBackendVersion,
  normalizeRuntimeSettings,
  parsePayload,
  redactDiagnostics,
  resolveRuntimePath,
  resolveDependencyIndex,
  runConfirmationRequirements,
  safeExternalHttpUrl,
  toVaultRelativePath,
  validateRuntimeSettings,
  yesterday,
} = require("./runtime");
const { ProcessManager } = require("./process-manager");
const { BackendInstaller } = require("./backend-installer");
const { downloadHttpsBuffer } = require("./proxy-download");
const { BACKEND_RELEASE } = require("./backend-release");
const { MINIFORGE_RELEASE, resolveMiniforgeAsset } = require("./miniforge-release");
const { UpdateManager, compareVersions, parseVersion } = require("./update-manager");
const {
  ARXIV_CATEGORY_GROUPS,
  DEFAULT_CATEGORIES,
  filterCategoryGroups,
  updateCategoryGroupSelection,
} = require("./arxiv-categories");
const {
  defaultConfigPath,
  normalizeKeywords,
  parseKeywordBatch,
  readDiscoverySettings,
  validateDiscoverySettings,
  writeDiscoverySettings,
} = require("./discovery-settings");
const {
  MANUAL_PLATFORMS,
  buildManualInstallCommand,
  manualInstallReceiptPath,
  normalizeManualInstallReceipt,
  platformForManualInstall,
} = require("./manual-install");

const VIEW_TYPE = "paperbrain-console-view";
const CONSOLE_VERSION = "0.6.2";

const DEFAULT_SETTINGS = {
  settingsVersion: 6,
  executionMode: "auto",
  cliPath: "",
  pythonPath: "",
  backendPath: "",
  configPath: "",
  vaultPath: "",
  provider: "openrouter",
  generatePodcast: false,
  cancelTimeoutSeconds: 20,
  lastPreset: "daily",
  paidRunDisclosureAccepted: false,
  condaPath: "",
  installerManaged: false,
  installedBackendVersion: "",
  managedRuntimePath: "",
  dependencySource: "auto",
  customDependencyIndex: "",
  proxyMode: "inherit",
  proxyUrl: "",
};

const PANELS = [
  { id: "run", label: "Run" },
  { id: "timeline", label: "Timeline" },
  { id: "briefs", label: "Briefs" },
  { id: "artifacts", label: "Artifacts" },
];

const PRESETS = [
  { id: "daily", label: "Daily full", mode: "run", generatePodcast: null, clearArxiv: true },
  { id: "quick", label: "Quick no podcast", mode: "run", generatePodcast: false, clearArxiv: true },
  { id: "fetch", label: "Fetch only", mode: "fetch", generatePodcast: false, clearArxiv: true },
  { id: "screen", label: "Screen only", mode: "screen", generatePodcast: false, clearArxiv: true },
  { id: "digest", label: "Digest only", mode: "digest", generatePodcast: false, clearArxiv: true },
  { id: "single-deep", label: "Single deep", mode: "deep", generatePodcast: false, clearArxiv: false },
  { id: "index", label: "Rebuild index", mode: "index", generatePodcast: false, clearArxiv: false },
];

const STAGES = [
  "fetch",
  "coarse",
  "screen",
  "deep",
  "digest",
  "index",
  "podcast",
];

const STAGE_DETAILS = {
  fetch: {
    label: "Fetch",
    detail: "Collect candidates",
    queue: "Waiting for fetched candidates to be written into state.json.",
  },
  coarse: {
    label: "Coarse",
    detail: "Fast triage",
    queue: "Fetched papers are visible; coarse scores and re-screen flags fill in as papers update.",
  },
  screen: {
    label: "Screen",
    detail: "Rigorous review",
    queue: "The queue shows final score, screening stage, quality bars, digest and deep-analysis decisions.",
  },
  deep: {
    label: "Deep",
    detail: "PDF and note work",
    queue: "PDF and Note columns update as local PDFs and detailed notes become available.",
  },
  digest: {
    label: "Digest",
    detail: "Daily digest",
    queue: "Digest badges identify papers selected for the daily digest.",
  },
  index: {
    label: "Index",
    detail: "Research index",
    queue: "Queue data stays visible while index and review files are refreshed.",
  },
  podcast: {
    label: "Podcast",
    detail: "Audio artifact",
    queue: "Podcast status appears in artifacts when audio generation is enabled.",
  },
};

const STAGE_TO_INDEX = {
  initialized: -1,
  fetch: 0,
  fetched: 0,
  coarse: 1,
  coarse_screened: 1,
  screen: 2,
  screened: 2,
  deep: 3,
  deep_analyzed: 3,
  digest: 4,
  digest_written: 4,
  index: 5,
  podcast: 6,
  completed: 6,
  failed: 6,
  cancelled: 6,
};

const OUTPUT_STAGE_HINTS = [
  { pattern: /searching arxiv|fetching from|fetched|target date/i, stage: "fetch" },
  { pattern: /coarse screening|stage-1|coarse-screen/i, stage: "coarse" },
  { pattern: /rigorous|stage-2|screening complete|screen_paper/i, stage: "screen" },
  { pattern: /deep analysis|analyzing:|extracting architecture|performing deep/i, stage: "deep" },
  { pattern: /daily digest|paperdigest|digest written/i, stage: "digest" },
  { pattern: /research index|knowledge gardening|rebuild index|index written/i, stage: "index" },
  { pattern: /podcast|audio/i, stage: "podcast" },
];

module.exports = class PaperBrainPlugin extends Plugin {
  async onload() {
    const stored = (await this.loadData()) || {};
    const detectedVaultPath = detectVaultPath(this.app);
    this.settings = normalizeRuntimeSettings(Object.assign({}, DEFAULT_SETTINGS, stored), {
      detectedVaultPath,
      existsSync: fs.existsSync,
    });
    this.views = new Set();
    this.processManager = new ProcessManager({
      spawn: childProcess.spawn,
      inferStage: inferStageFromOutput,
      onNotice: ({ ok, message }) => new Notice(message, ok ? 5000 : 8000),
    });
    this.backendInstaller = new BackendInstaller({
      spawn: childProcess.spawn,
      download: downloadHttpsBuffer,
    });
    this.updateManager = new UpdateManager({
      download: downloadHttpsBuffer,
      pluginDir: __dirname,
      supportsAppVersion: (version) => typeof requireApiVersion !== "function" || requireApiVersion(version),
    });
    this.softwareUpdates = {
      checking: false,
      checked: false,
      console: null,
      backend: null,
      pendingConsoleVersion: "",
    };
    const firstStart = !stored.settingsVersion;
    const migratedLegacyPath = Boolean(stored.repoPath && !stored.backendPath);
    const migratedSettings = stored.settingsVersion !== DEFAULT_SETTINGS.settingsVersion;
    if (firstStart || migratedLegacyPath || migratedSettings) await this.saveSettings();
    this.addSettingTab(new PaperBrainSettingTab(this.app, this));
    this.registerView(VIEW_TYPE, (leaf) => {
      const view = new PaperBrainConsoleView(leaf, this);
      this.views.add(view);
      return view;
    });
    this.addRibbonIcon("brain-circuit", "PaperBrain console", () => this.activateView());
    this.addCommand({
      id: "open-paperbrain-console",
      name: "Open console",
      callback: () => this.activateView(),
    });
    this.addCommand({
      id: "validate-paperbrain-configuration",
      name: "Validate configuration",
      callback: () => this.validateConfiguration(true),
    });
    this.addCommand({
      id: "show-paperbrain-backend-terminal-command",
      name: "Show backend terminal command",
      callback: () => this.showManualBackendInstall(),
    });
    const validation = this.validateConfiguration(false);
    if (firstStart) {
      if (validation.ok) {
        const mode = validation.invocation.mode === "cli" ? "CLI lookup from PATH" : "local Python backend";
        new Notice(`PaperBrain setup initialized with the current vault and ${mode}. Review plugin settings before the first run.`, 8000);
      } else {
        new Notice("PaperBrain setup is incomplete. Open the console to finish setup.", 8000);
      }
    } else if (!validation.ok) {
      new Notice("PaperBrain setup needs attention. Open the console for details.", 8000);
    }
  }

  async onunload() {
    if (this.backendInstaller) this.backendInstaller.dispose();
    if (this.processManager) this.processManager.dispose("plugin unload");
    for (const view of this.views || []) view.dispose();
    if (this.views) this.views.clear();
    this.app.workspace.detachLeavesOfType(VIEW_TYPE);
  }

  async activateView() {
    const leaves = this.app.workspace.getLeavesOfType(VIEW_TYPE);
    if (leaves.length) {
      this.app.workspace.revealLeaf(leaves[0]);
      return;
    }
    const leaf = this.app.workspace.getRightLeaf(false);
    await leaf.setViewState({ type: VIEW_TYPE, active: true });
    this.app.workspace.revealLeaf(leaf);
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }

  validateConfiguration(showNotice = false) {
    const validation = validateRuntimeSettings(this.settings, { existsSync: fs.existsSync });
    if (showNotice) {
      if (validation.ok) {
        const warning = validation.warnings[0] ? ` ${validation.warnings[0]}` : "";
        new Notice(`PaperBrain configuration is valid.${warning}`, 7000);
      } else {
        new Notice("PaperBrain setup needs attention. Open the console for details.", 8000);
      }
    }
    return validation;
  }

  async detectSetup() {
    const receiptPath = manualInstallReceiptPath(os.homedir());
    try {
      const rawReceipt = JSON.parse(fs.readFileSync(receiptPath, "utf8").replace(/^\uFEFF/, ""));
      const receipt = normalizeManualInstallReceipt(rawReceipt, fs.existsSync);
      if (receipt) {
        Object.assign(this.settings, {
          executionMode: "cli",
          cliPath: receipt.cliPath,
          pythonPath: receipt.pythonPath,
          configPath: receipt.configPath,
          condaPath: receipt.condaPath,
          installerManaged: true,
          installedBackendVersion: receipt.backendVersion,
          managedRuntimePath: receipt.managedRuntimePath,
        });
      }
    } catch (_) {
      // A missing or stale receipt falls back to the normal constrained detection.
    }
    const condaPath = await this.detectCondaExecutable();
    let condaJson = "";
    try {
      condaJson = await execFileText(condaPath || "conda", ["env", "list", "--json"]);
    } catch (_) {
      // A saved or currently active wd environment can still be detected without conda on PATH.
    }
    const backendPath = detectBackendPath({
      savedPath: this.settings.backendPath,
      vaultPath: this.settings.vaultPath,
      existsSync: fs.existsSync,
    });
    const python = detectWdPython({
      savedPath: this.settings.pythonPath,
      env: process.env,
      condaJson,
      existsSync: fs.existsSync,
    });
    if (backendPath) this.settings.backendPath = backendPath;
    if (python.path) {
      this.settings.pythonPath = python.path;
      const envPath = process.platform === "win32"
        ? path.dirname(python.path)
        : path.dirname(path.dirname(python.path));
      const cliPath = cliExecutableForEnv(envPath);
      const defaultConfigPath = path.join(os.homedir(), ".paperbrain", "config", "config.yaml");
      if (fs.existsSync(cliPath)) {
        this.settings.cliPath = cliPath;
        if (!backendPath) this.settings.executionMode = "cli";
      }
      if (fs.existsSync(defaultConfigPath)) {
        this.settings.configPath = defaultConfigPath;
      }
    }
    if (condaPath) this.settings.condaPath = condaPath;
    this.settings.executionMode = backendPath ? "python-script" : this.settings.executionMode;
    await this.saveSettings();
    return { backendPath, pythonPath: python.path, pythonSource: python.source, condaPath };
  }

  async detectCondaExecutable() {
    const candidates = condaExecutableCandidates({
      savedPath: this.settings.condaPath,
      pythonPath: this.settings.pythonPath,
      env: process.env,
      home: os.homedir(),
    });
    for (const candidate of candidates) {
      try {
        await execFileText(candidate, ["--version"]);
        const payload = JSON.parse(await execFileText(candidate, ["env", "list", "--json"]));
        if (!payload || !Array.isArray(payload.envs)) continue;
        return candidate;
      } catch (_) {
        // Continue through explicit, environment, PATH, inferred, and common locations.
      }
    }
    return "";
  }

  softwareUpdatesBusy() {
    return Boolean(
      this.softwareUpdates && (
        this.softwareUpdates.checking
        || (this.softwareUpdates.console && this.softwareUpdates.console.updating)
        || (this.softwareUpdates.backend && this.softwareUpdates.backend.updating)
      ),
    ) || this.backendInstaller.snapshot().running || this.processManager.snapshot().running;
  }

  discoveryConfigPath() {
    const invocation = buildInvocation(this.settings, [], { existsSync: fs.existsSync });
    if (String(this.settings.configPath || "").trim()) {
      return resolveRuntimePath(this.settings.configPath, invocation.cwd);
    }
    if (invocation.mode === "python-script" && this.settings.backendPath) {
      return path.join(this.settings.backendPath, "script", "config", "config.yaml");
    }
    return defaultConfigPath();
  }

  discoverySaveBlockReason() {
    if (this.processManager.snapshot().running) return "Stop the active PaperBrain run before saving discovery preferences.";
    if (this.backendInstaller.snapshot().running) return "Wait for backend installation to finish before saving discovery preferences.";
    if (this.softwareUpdatesBusy()) return "Wait for the active software update before saving discovery preferences.";
    return "";
  }

  updateNetworkOptions() {
    return {
      proxyMode: this.settings.proxyMode,
      proxyUrl: this.settings.proxyUrl,
      env: buildManagedEnvironment(this.settings, process.env),
    };
  }

  async detectInstalledBackendVersion() {
    const invocation = buildInvocation(this.settings, ["doctor", "config"], { existsSync: fs.existsSync });
    let version = "";
    let source = "unknown";
    try {
      const result = await execFileResult(
        invocation.executable,
        invocation.args,
        { ...buildSpawnOptions(this.settings, invocation), timeout: 15000 },
      );
      const payload = parsePayload(result.stdout);
      if (payload && parseVersion(payload.backend_version)) {
        version = payload.backend_version;
        source = "runtime";
      }
    } catch (_) {
      // A valid installer receipt is the constrained fallback when the CLI cannot start.
    }
    if (!version && parseVersion(this.settings.installedBackendVersion)) {
      version = this.settings.installedBackendVersion;
      source = "receipt";
    }
    return {
      version,
      source,
      mode: invocation.mode,
      managed: invocation.mode === "cli" && Boolean(this.settings.installerManaged),
    };
  }

  async checkSoftwareUpdates() {
    if (this.softwareUpdatesBusy()) {
      new Notice("Wait for the active PaperBrain task before checking for updates.");
      return false;
    }
    this.softwareUpdates.checking = true;
    try {
      await this.detectSetup();
      const installedBackend = await this.detectInstalledBackendVersion();
      const network = this.updateNetworkOptions();
      const [consoleResult, backendResult] = await Promise.allSettled([
        this.updateManager.checkConsole(network),
        this.updateManager.checkBackend(BACKEND_RELEASE, network),
      ]);
      const currentConsole = this.softwareUpdates.pendingConsoleVersion
        || (this.manifest && this.manifest.version)
        || CONSOLE_VERSION;
      const console = {
        current: currentConsole,
        latest: "",
        available: false,
        release: null,
        error: "",
        updating: false,
        restartRequired: Boolean(this.softwareUpdates.pendingConsoleVersion),
      };
      if (consoleResult.status === "fulfilled") {
        console.release = consoleResult.value;
        console.latest = consoleResult.value.version;
        const comparison = compareVersions(console.latest, console.current);
        console.available = comparison > 0 && !console.restartRequired;
        console.status = console.restartRequired
          ? `Console ${console.current} is installed; restart Obsidian to load it.`
          : comparison > 0
            ? `Console ${console.latest} is available; installed ${console.current}.`
            : comparison === 0
              ? `Console ${console.current} is up to date.`
              : `Console ${console.current} is newer than the published stable release ${console.latest}.`;
      } else {
        console.error = consoleResult.reason && consoleResult.reason.message
          ? consoleResult.reason.message
          : String(consoleResult.reason || "Console update check failed.");
        console.status = `Console update check failed: ${console.error}`;
      }

      const backend = {
        current: installedBackend.version,
        currentSource: installedBackend.source,
        mode: installedBackend.mode,
        managed: installedBackend.managed,
        latest: "",
        available: false,
        release: null,
        error: "",
        updating: false,
      };
      if (backendResult.status === "fulfilled") {
        backend.release = backendResult.value;
        backend.latest = backendResult.value.version;
        if (!isCompatibleBackendVersion(backend.latest)) {
          backend.status = `Backend ${backend.latest} requires a compatible Console update.`;
        } else if (!backend.current) {
          backend.status = `Backend version was not detected; latest stable is ${backend.latest}.`;
        } else if (backend.mode === "python-script") {
          backend.status = `Backend ${backend.current} uses source mode and is developer-managed.`;
        } else if (!backend.managed) {
          backend.status = `Backend ${backend.current} is not managed by the Console updater.`;
        } else {
          const comparison = compareVersions(backend.latest, backend.current);
          backend.available = comparison > 0;
          backend.status = comparison > 0
            ? `Backend ${backend.latest} is available; installed ${backend.current}.`
            : comparison === 0
              ? `Backend ${backend.current} is up to date.`
              : `Backend ${backend.current} is newer than the published stable release ${backend.latest}.`;
        }
      } else {
        backend.error = backendResult.reason && backendResult.reason.message
          ? backendResult.reason.message
          : String(backendResult.reason || "Backend update check failed.");
        backend.status = `Backend update check failed: ${backend.error}`;
      }
      this.softwareUpdates.console = console;
      this.softwareUpdates.backend = backend;
      this.softwareUpdates.checked = true;
      const successes = [consoleResult, backendResult].filter((result) => result.status === "fulfilled").length;
      new Notice(successes ? "PaperBrain update check completed." : "PaperBrain update check failed.", successes ? 5000 : 9000);
      return successes > 0;
    } catch (error) {
      this.softwareUpdates.checked = true;
      this.softwareUpdates.console = { status: `Update check failed: ${error.message}`, error: error.message };
      this.softwareUpdates.backend = { status: `Update check failed: ${error.message}`, error: error.message };
      new Notice(`PaperBrain update check failed: ${error.message}`, 9000);
      return false;
    } finally {
      this.softwareUpdates.checking = false;
    }
  }

  softwareUpdateDescription() {
    if (!this.softwareUpdates || !this.softwareUpdates.checked) {
      const currentConsole = (this.manifest && this.manifest.version) || CONSOLE_VERSION;
      const backend = parseVersion(this.settings.installedBackendVersion)
        ? this.settings.installedBackendVersion
        : "not detected";
      return `Console ${currentConsole}; backend ${backend}. Check the latest stable releases.`;
    }
    return [this.softwareUpdates.console, this.softwareUpdates.backend]
      .map((item) => item && item.status)
      .filter(Boolean)
      .join(" ");
  }

  async updateConsole() {
    const state = this.softwareUpdates && this.softwareUpdates.console;
    if (this.softwareUpdatesBusy() || !state || !state.available || !state.release) return false;
    state.updating = true;
    try {
      const result = await this.updateManager.installConsole(state.release, this.updateNetworkOptions());
      this.softwareUpdates.pendingConsoleVersion = result.version;
      Object.assign(state, {
        current: result.version,
        available: false,
        updating: false,
        restartRequired: true,
        status: `Console ${result.version} is installed; restart Obsidian to load it.`,
      });
      new Notice(`PaperBrain Console ${result.version} is installed. Restart Obsidian to load it.`, 10000);
      return true;
    } catch (error) {
      state.updating = false;
      state.error = error.message;
      state.status = `Console update failed: ${error.message}`;
      new Notice(state.status, 10000);
      return false;
    }
  }

  async updateBackend() {
    const state = this.softwareUpdates && this.softwareUpdates.backend;
    if (this.softwareUpdatesBusy() || !state || !state.available || !state.release || !state.managed) return false;
    state.updating = true;
    try {
      await this.activateView();
      const updated = await this.installBackend({ release: state.release, skipConfirmation: true });
      if (!updated) {
        state.status = "Backend update failed. See the Console installation log.";
        return false;
      }
      Object.assign(state, {
        current: state.release.version,
        latest: state.release.version,
        available: false,
        status: `Backend ${state.release.version} is up to date.`,
      });
      return true;
    } catch (error) {
      state.error = error.message;
      state.status = `Backend update failed: ${error.message}`;
      new Notice(state.status, 10000);
      return false;
    } finally {
      state.updating = false;
    }
  }

  async installBackend(options = {}) {
    if (this.processManager.snapshot().running) {
      new Notice("Stop the active PaperBrain run before installing the backend.");
      return false;
    }
    if (this.backendInstaller.snapshot().running) {
      new Notice("PaperBrain backend installation is already running.");
      return false;
    }
    const release = options.release || BACKEND_RELEASE;
    const condaPath = await this.detectCondaExecutable();
    let dependencyIndex;
    let environment;
    try {
      dependencyIndex = resolveDependencyIndex(this.settings);
      environment = buildManagedEnvironment(this.settings, process.env);
    } catch (error) {
      new Notice(error.message, 9000);
      return false;
    }
    const miniforgeAsset = resolveMiniforgeAsset(process.platform, process.arch);
    if (!condaPath && !miniforgeAsset) {
      new Notice(`Automatic runtime installation is not available for ${process.platform}/${process.arch}.`, 9000);
      return false;
    }
    const configDir = path.join(os.homedir(), ".paperbrain", "config");
    const managedRuntimePath = path.join(os.homedir(), ".paperbrain", "runtime", "miniforge3");
    const accepted = options.skipConfirmation || await confirmBackendInstall(this.app, {
      condaPath,
      configDir,
      managedRuntimePath,
      miniforgeRelease: MINIFORGE_RELEASE,
      miniforgeAsset,
      vaultPath: this.settings.vaultPath,
      release,
      dependencyIndex,
      environment,
      proxyMode: this.settings.proxyMode,
      proxyUrl: this.settings.proxyUrl,
    });
    if (!accepted) return false;
    const result = await this.backendInstaller.install({
      condaExecutable: condaPath,
      configDir,
      vaultPath: this.settings.vaultPath,
      release,
      dependencyIndex,
      environment,
      proxyMode: this.settings.proxyMode,
      proxyUrl: this.settings.proxyUrl,
      miniforge: {
        release: MINIFORGE_RELEASE,
        asset: miniforgeAsset,
        installDir: managedRuntimePath,
      },
    });
    if (!result.ok) {
      new Notice("PaperBrain backend installation failed. See the console log for details.", 9000);
      return false;
    }
    Object.assign(this.settings, {
      settingsVersion: 6,
      executionMode: "cli",
      cliPath: result.cliPath,
      pythonPath: result.pythonPath,
      backendPath: "",
      configPath: result.configPath,
      condaPath: result.condaPath,
      installerManaged: true,
      installedBackendVersion: result.version,
      managedRuntimePath: result.managedRuntimePath,
    });
    await this.saveSettings();
    new Notice(`PaperBrain backend ${result.version} is ready.`, 9000);
    return true;
  }

  async testNetworkConnection() {
    if (this.backendInstaller.snapshot().running || this.processManager.snapshot().running) {
      new Notice("Wait for the active PaperBrain task before testing the connection.");
      return false;
    }
    let environment;
    try {
      environment = buildManagedEnvironment(this.settings, process.env);
      const url = `https://huggingface.co/api/daily_papers?date=${encodeURIComponent(yesterday())}`;
      const started = Date.now();
      const bytes = await downloadHttpsBuffer(url, {
        proxyMode: this.settings.proxyMode,
        proxyUrl: this.settings.proxyUrl,
        env: environment,
        timeoutMs: 30000,
        maxBytes: 8 * 1024 * 1024,
      });
      let payload = JSON.parse(bytes.toString("utf8"));
      if (payload && !Array.isArray(payload) && typeof payload === "object") {
        payload = payload.papers || payload.daily_papers || payload.results;
      }
      if (!Array.isArray(payload)) throw new Error("Hugging Face returned an unexpected payload.");
      this.processManager.appendLog(`network test: Hugging Face passed in ${Date.now() - started} ms`);
    } catch (error) {
      this.processManager.appendLog(`network test failed: ${error && error.name ? error.name : "Error"}`);
      new Notice("PaperBrain connection test failed. Check the proxy mode and URL.", 9000);
      return false;
    }

    const validation = this.validateConfiguration(false);
    if (!validation.ok) {
      new Notice("Plugin download connection passed. Install or detect the backend to run full diagnostics.", 8000);
      return true;
    }
    const commandArgs = ["doctor", "network", "--live"];
    const invocation = buildInvocation(this.settings, commandArgs, { existsSync: fs.existsSync });
    const result = this.processManager.start({
      invocation,
      commandArgs,
      spawnOptions: buildSpawnOptions(this.settings, invocation, environment),
      timeoutMs: Math.max(3, Number(this.settings.cancelTimeoutSeconds || 20)) * 1000,
      context: { date: yesterday(), provider: this.settings.provider, mode: "doctor", doctorScope: "network" },
      notify: false,
    });
    if (!result.started) return false;
    const outcome = await result.completion;
    if (!outcome.ok) {
      new Notice("Plugin download passed, but backend network diagnostics failed.", 9000);
      return false;
    }
    new Notice("PaperBrain network connection passed.");
    return true;
  }

  showManualBackendInstall() {
    let dependencyIndex;
    try {
      dependencyIndex = resolveDependencyIndex(this.settings);
    } catch (error) {
      new Notice(error.message, 9000);
      return false;
    }
    if (!this.settings.vaultPath) {
      new Notice("Set a valid vault path before generating a terminal installation command.", 9000);
      return false;
    }
    const commands = {};
    try {
      for (const platform of MANUAL_PLATFORMS) {
        commands[platform.id] = buildManualInstallCommand(platform.id, {
          vaultPath: this.settings.vaultPath,
          dependencyIndex,
        });
      }
    } catch (error) {
      new Notice(error.message, 9000);
      return false;
    }
    new ManualBackendInstallModal(this.app, {
      commands,
      dependencyIndex,
      platforms: MANUAL_PLATFORMS,
      selectedPlatform: platformForManualInstall(process.platform),
      backendVersion: BACKEND_RELEASE.version,
    }).open();
    return true;
  }

  openManagedEnvFile() {
    const envPath = this.managedEnvFilePath();
    if (!fs.existsSync(envPath)) {
      new Notice(`The API key file does not exist at ${envPath}. Complete backend installation first.`, 9000);
      return;
    }
    if (process.platform === "win32") {
      const editor = childProcess.spawn("notepad.exe", [envPath], { detached: true, windowsHide: false, stdio: "ignore" });
      editor.once("error", () => new Notice("Unable to open the PaperBrain .env file in Notepad."));
      editor.unref();
      return;
    }
    require("electron").shell.openPath(envPath).then((error) => {
      if (error) new Notice("Unable to open the PaperBrain .env file.");
    });
  }

  managedEnvFilePath() {
    const configPath = String(this.settings.configPath || "").trim();
    const configDir = configPath
      ? path.dirname(configPath)
      : path.join(os.homedir(), ".paperbrain", "config");
    return path.join(configDir, ".env");
  }

  openSettings() {
    this.app.setting.open();
    this.app.setting.openTabById(this.manifest.id);
  }

  async validateSetup() {
    if (this.backendInstaller.snapshot().running) {
      new Notice("Wait for backend installation to finish before validating setup.");
      return false;
    }
    await this.detectSetup();
    const validation = this.validateConfiguration(false);
    if (!validation.ok) {
      this.processManager.appendLog(`setup validation failed: ${validation.errors.join(" ")}`);
      new Notice("PaperBrain setup is incomplete. Open the console for details.", 8000);
      return false;
    }
    if (this.processManager.snapshot().running) {
      new Notice("PaperBrain is already running.");
      return false;
    }
    const completedScopes = [];
    for (const scope of ["config", "env", "llm"]) {
      const commandArgs = ["doctor", scope];
      const invocation = buildInvocation(this.settings, commandArgs, { existsSync: fs.existsSync });
      const result = this.processManager.start({
        invocation,
        commandArgs,
        spawnOptions: buildSpawnOptions(this.settings, invocation),
        timeoutMs: Math.max(3, Number(this.settings.cancelTimeoutSeconds || 20)) * 1000,
        context: { date: yesterday(), provider: this.settings.provider, mode: "doctor", preset: "daily", doctorScope: scope },
        notify: false,
      });
      if (!result.started) return false;
      const outcome = await result.completion;
      if (!outcome.ok) {
        if (completedScopes.length) this.processManager.appendLog(`doctor passed before failure: ${completedScopes.join(", ")}`);
        return false;
      }
      completedScopes.push(scope);
    }
    this.processManager.appendLog(`doctor passed: ${completedScopes.join(", ")}; live probes were not requested`);
    new Notice("PaperBrain setup validation passed.");
    return true;
  }
};

class PaperBrainConsoleView extends ItemView {
  constructor(leaf, plugin) {
    super(leaf);
    this.plugin = plugin;
    this.disposed = false;
    this.processUnsubscribe = null;
    this.installerUnsubscribe = null;
    this.runtime = plugin.processManager.snapshot();
    this.installerRuntime = plugin.backendInstaller.snapshot();
    this.state = null;
    this.stateFingerprint = "";
    this.pollInFlight = false;
    this.showAllLogs = false;
    this.activePanel = "run";
    this.pollTimer = null;
    this.panelScroll = {};
    this.renderedPanel = "";
    this.dateTouched = false;
    this.runHistory = [];
    this.briefHistory = [];
    this.briefCache = null;
    this.pendingTabFocus = "";
    const defaultDate = yesterday();
    const preset = presetById(plugin.settings.lastPreset || "daily");
    this.form = {
      date: defaultDate,
      provider: plugin.settings.provider || "openrouter",
      mode: preset.mode,
      preset: preset.id,
      arxivUrl: "",
      briefMode: "week",
      briefDate: defaultDate,
      generatePodcast: !!plugin.settings.generatePodcast,
      forceRun: false,
    };
  }

  get process() { return this.runtime.running; }
  get stopping() { return this.runtime.stopping; }
  get stdout() { return this.runtime.stdout || ""; }
  get stderr() { return this.runtime.stderr || ""; }
  get lastPayload() { return this.runtime.lastPayload; }
  get liveStage() { return this.runtime.stage || ""; }
  get liveMessage() { return this.runtime.latestOutput || ""; }
  get lastOutputLine() { return this.runtime.latestOutput || ""; }

  getViewType() {
    return VIEW_TYPE;
  }

  getDisplayText() {
    return "PaperBrain console";
  }

  getIcon() {
    return "brain-circuit";
  }

  async onOpen() {
    this.disposed = false;
    this.processUnsubscribe = this.plugin.processManager.subscribe((snapshot, event) => {
      this.runtime = snapshot;
      this.handleProcessEvent(event);
    });
    this.installerUnsubscribe = this.plugin.backendInstaller.subscribe((snapshot) => {
      this.installerRuntime = snapshot;
      if (!this.disposed) this.render();
    });
    this.restoreRunContext();
    await Promise.all([this.loadState({ force: true }), this.loadRunHistory()]);
    if (this.process) this.startPolling();
    this.render();
  }

  async onClose() {
    this.dispose();
    this.plugin.views.delete(this);
  }

  dispose() {
    if (this.disposed) return;
    this.disposed = true;
    this.stopPolling();
    if (this.processUnsubscribe) this.processUnsubscribe();
    this.processUnsubscribe = null;
    if (this.installerUnsubscribe) this.installerUnsubscribe();
    this.installerUnsubscribe = null;
  }

  restoreRunContext() {
    const context = this.runtime.context;
    if (!context) return;
    if (context.date) this.form.date = context.date;
    if (context.provider) this.form.provider = context.provider;
    if (context.mode) this.form.mode = context.mode;
    if (context.preset) this.form.preset = context.preset;
    if (typeof context.generatePodcast === "boolean") this.form.generatePodcast = context.generatePodcast;
    if (context.arxivUrl) this.form.arxivUrl = context.arxivUrl;
  }

  handleProcessEvent(event) {
    if (this.disposed) return;
    if (event === "started") this.startPolling();
    if (event === "finished") {
      this.stopPolling();
      const payload = this.lastPayload;
      if (payload && payload.date) {
        this.form.date = payload.date;
        this.dateTouched = false;
      }
      Promise.all([this.loadState({ force: true }), this.loadRunHistory(), this.loadPanelData()]).then(() => this.render());
      return;
    }
    if (["attach", "started", "stopping", "output", "stage"].includes(event)) this.render();
  }

  async loadState(options = {}) {
    if (this.disposed) return;
    const statePath = this.currentStatePath();
    if (!statePath) {
      this.state = null;
      this.stateFingerprint = "";
      return true;
    }
    try {
      const stat = await fs.promises.stat(statePath);
      const fingerprint = `${statePath}:${stat.mtimeMs}:${stat.size}`;
      if (!options.force && fingerprint === this.stateFingerprint) return false;
      this.state = JSON.parse(await fs.promises.readFile(statePath, "utf8"));
      this.stateFingerprint = fingerprint;
      return true;
    } catch (error) {
      if (error && error.code === "ENOENT") {
        const changed = this.state !== null || this.stateFingerprint !== "";
        this.state = null;
        this.stateFingerprint = "";
        return changed;
      }
      this.state = null;
      this.appendLog(`state read failed: ${error.message}`);
      return true;
    }
  }

  currentRunId() {
    return `${this.form.date}`;
  }

  vaultPath(...parts) {
    const root = textValue(this.plugin.settings.vaultPath);
    return root ? path.join(root, ...parts) : "";
  }

  currentRunDir() {
    return this.vaultPath("Run_Records", this.currentRunId());
  }

  currentStatePath() {
    const runDir = this.currentRunDir();
    return runDir ? path.join(runDir, "state.json") : "";
  }

  render() {
    if (this.disposed) return;
    this.capturePaneScroll();
    const focus = this.captureInputFocus();
    const root = this.containerEl.children[1];
    root.empty();
    root.addClass("paperbrain-console");
    this.renderTopbar(root);
    this.renderPanelTabs(root);
    const shell = root.createDiv({ cls: "paperbrain-shell" });
    const pane = shell.createDiv({ cls: "paperbrain-pane paperbrain-active-pane" });
    if (this.activePanel === "run") {
      this.renderControls(pane);
      this.renderRunHistory(pane);
    } else if (this.activePanel === "timeline") {
      this.renderMain(pane);
    } else if (this.activePanel === "briefs") {
      this.renderBriefs(pane);
    } else {
      this.renderDetails(pane);
    }
    this.restorePaneScroll(pane, this.activePanel);
    this.restoreInputFocus(focus);
    this.restoreTabFocus();
    this.renderedPanel = this.activePanel;
  }

  captureInputFocus() {
    const active = document.activeElement;
    if (!active || !this.containerEl.contains(active) || !active.dataset.paperbrainField) return null;
    return {
      key: active.dataset.paperbrainField,
      start: typeof active.selectionStart === "number" ? active.selectionStart : null,
      end: typeof active.selectionEnd === "number" ? active.selectionEnd : null,
    };
  }

  restoreInputFocus(focus) {
    if (!focus) return;
    requestAnimationFrame(() => {
      const input = this.containerEl.querySelector(`[data-paperbrain-field="${focus.key}"]`);
      if (!input) return;
      input.focus({ preventScroll: true });
      if (focus.start !== null && typeof input.setSelectionRange === "function") {
        input.setSelectionRange(focus.start, focus.end);
      }
    });
  }

  restoreTabFocus() {
    if (!this.pendingTabFocus) return;
    const panel = this.pendingTabFocus;
    this.pendingTabFocus = "";
    requestAnimationFrame(() => {
      const tab = this.containerEl.querySelector(`[data-paperbrain-panel="${panel}"]`);
      if (tab) tab.focus({ preventScroll: true });
    });
  }

  capturePaneScroll() {
    const pane = this.containerEl.querySelector(".paperbrain-pane");
    const key = this.renderedPanel || this.activePanel;
    if (pane && key) {
      this.panelScroll[key] = pane.scrollTop;
    }
  }

  restorePaneScroll(pane, key) {
    const scrollTop = this.panelScroll[key] || 0;
    requestAnimationFrame(() => {
      pane.scrollTop = scrollTop;
    });
  }

  async loadPanelData(panel = this.activePanel) {
    if (panel === "run") await this.loadRunHistory();
    if (panel === "briefs") await this.loadBriefData();
  }

  async loadBriefData() {
    const briefDate = this.form.briefDate || this.form.date || yesterday();
    const period = briefPeriod(this.form.briefMode || "week", briefDate);
    const [existing, summary, history] = await Promise.all([
      this.findBrief(period.label),
      this.readDailyDigestSummary(period.start, period.end),
      this.readBriefHistory(),
    ]);
    this.briefHistory = history;
    this.briefCache = { key: `${period.type}:${briefDate}`, existing, summary };
  }

  renderPanelTabs(root) {
    const tabs = root.createDiv({ cls: "paperbrain-tabs", attr: { role: "tablist", "aria-label": "PaperBrain views" } });
    const buttons = [];
    PANELS.forEach((panel, index) => {
      const button = tabs.createEl("button", {
        text: panel.label,
        attr: {
          role: "tab",
          type: "button",
          "aria-selected": String(this.activePanel === panel.id),
          tabindex: this.activePanel === panel.id ? "0" : "-1",
        },
      });
      button.dataset.paperbrainPanel = panel.id;
      buttons.push(button);
      if (this.activePanel === panel.id) button.addClass("is-active");
      button.addEventListener("click", async () => {
        this.activePanel = panel.id;
        await Promise.all([this.loadState(), this.loadPanelData(panel.id)]);
        this.render();
      });
      button.addEventListener("keydown", (event) => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
        event.preventDefault();
        const nextIndex = event.key === "Home"
          ? 0
          : event.key === "End"
            ? buttons.length - 1
            : (index + (event.key === "ArrowRight" ? 1 : -1) + PANELS.length) % PANELS.length;
        this.pendingTabFocus = PANELS[nextIndex].id;
        buttons[nextIndex].click();
      });
    });
  }

  renderTopbar(root) {
    const bar = root.createDiv({ cls: "paperbrain-topbar" });
    const title = bar.createDiv({ cls: "paperbrain-title" });
    title.createEl("strong", { text: "PaperBrain console" });
    const runtime = this.plugin.validateConfiguration(false).invocation;
    title.createEl("span", {
      text: `${this.plugin.settings.vaultPath} / ${runtime.mode === "cli" ? "CLI" : "Python backend"}`,
    });
    const right = bar.createDiv({ cls: "paperbrain-run-id" });
    right.setText(this.state ? `${this.state.run_id} / ${this.state.stage}` : `${this.currentRunId()} / idle`);
  }

  renderControls(parent) {
    const validation = this.plugin.validateConfiguration(false);
    if (!validation.ok && !this.process) {
      this.renderSetupGuide(parent, validation);
      return;
    }
    const section = parent.createDiv({ cls: "paperbrain-section" });
    section.createEl("h3", { text: "Run" });
    this.renderPresetSelect(section);
    this.field(section, "Date", "date", this.form.date, (value) => {
      this.form.date = value || yesterday();
      this.dateTouched = true;
      this.refreshAfterInput();
    }, { type: "date", cls: "paperbrain-date-input", fieldCls: "paperbrain-date-field" });
    this.select(section, "Provider", "provider", this.form.provider, ["openrouter", "doubao"], (value) => {
      this.form.provider = value;
      this.plugin.settings.provider = value;
      this.plugin.saveSettings();
      this.refreshAfterInput();
    });
    this.field(section, "arXiv URL", "arxivUrl", this.form.arxivUrl, (value) => {
      this.form.arxivUrl = value;
      this.refreshAfterInput();
    });

    const toggles = section.createDiv({ cls: "paperbrain-toggle-row" });
    const podcast = toggles.createDiv({ cls: "paperbrain-toggle-field" });
    podcast.createEl("span", { text: "Podcast" });
    const podcastButton = podcast.createEl("button", {
      cls: `paperbrain-icon-toggle ${this.form.generatePodcast ? "is-active" : ""}`,
      attr: {
        "aria-label": "Toggle podcast generation",
        "aria-pressed": String(this.form.generatePodcast),
        type: "button",
      },
    });
    setIcon(podcastButton, this.form.generatePodcast ? "check" : "circle");
    podcastButton.addEventListener("click", () => {
      this.form.generatePodcast = !this.form.generatePodcast;
      this.render();
    });
    const force = toggles.createDiv({ cls: "paperbrain-toggle-field" });
    force.createEl("span", { text: "Force" });
    const forceButton = force.createEl("button", {
      cls: `paperbrain-icon-toggle ${this.form.forceRun ? "is-active" : ""}`,
      attr: {
        "aria-label": "Toggle force refresh",
        "aria-pressed": String(this.form.forceRun),
        type: "button",
      },
    });
    setIcon(forceButton, this.form.forceRun ? "check" : "circle");
    forceButton.addEventListener("click", () => {
      this.form.forceRun = !this.form.forceRun;
      this.render();
    });

    const actions = section.createDiv({ cls: "paperbrain-actions" });
    const runBtn = actions.createEl("button", { text: this.stopping ? "Stopping" : this.process ? "Running" : "Run" });
    runBtn.addClass("paperbrain-primary");
    runBtn.disabled = !!this.process;
    runBtn.addEventListener("click", () => this.runSelected());
    const stopBtn = actions.createEl("button", { text: "Stop" });
    stopBtn.addClass("paperbrain-danger");
    stopBtn.disabled = !this.process || this.stopping;
    stopBtn.addEventListener("click", () => this.stopRun());

    const utility = parent.createDiv({ cls: "paperbrain-section" });
    utility.createEl("h3", { text: "Tools" });
    const utilityActions = utility.createDiv({ cls: "paperbrain-actions" });
    utilityActions.createEl("button", { text: "Doctor" }).addEventListener("click", () => this.runDoctor());
    utilityActions.createEl("button", { text: "Refresh" }).addEventListener("click", async () => {
      await this.loadState();
      this.render();
    });
    const openActions = utility.createDiv({ cls: "paperbrain-actions" });
    openActions.createEl("button", { text: "Digest" }).addEventListener("click", () => this.openArtifact("daily_digest"));
    openActions.createEl("button", { text: "Report" }).addEventListener("click", () => this.openArtifact("screening_report"));
    openActions.createEl("button", { text: "Index" }).addEventListener("click", () => this.runIndex());
  }

  renderSetupGuide(parent, validation) {
    const section = parent.createDiv({ cls: "paperbrain-section paperbrain-setup" });
    section.createEl("h3", { text: "Finish setup" });
    section.createEl("p", { cls: "paperbrain-muted", text: "Install the fixed PaperBrain backend into wd, then add your provider key and validate. Terminal installation is recommended when your shell provides network or proxy settings." });
    const backendReady = Boolean(detectBackendPath({
      savedPath: this.plugin.settings.backendPath,
      vaultPath: this.plugin.settings.vaultPath,
      existsSync: fs.existsSync,
    }));
    const pythonReady = Boolean(detectWdPython({
      savedPath: this.plugin.settings.pythonPath,
      env: process.env,
      existsSync: fs.existsSync,
    }).path);
    [
      ["1", "Backend runtime", backendReady || pythonReady ? "A local PaperBrain runtime was detected." : "Use the recommended terminal command or install inside Obsidian to create or reuse wd."],
      ["2", "Provider key", this.plugin.settings.installerManaged ? "Open the managed .env file and replace the placeholder key." : "API keys stay in a local .env file or operating-system environment, never in plugin settings."],
      ["3", "Provider diagnostics", "Validate setup runs doctor config, env, and llm locally without --live or model charges."],
    ].forEach(([numberText, title, detail]) => {
      const item = section.createDiv({ cls: "paperbrain-setup-step" });
      item.createEl("strong", { text: numberText, attr: { "aria-hidden": "true" } });
      const copy = item.createDiv();
      copy.createEl("b", { text: title });
      copy.createEl("span", { text: detail });
    });
    const errors = section.createDiv({ cls: "paperbrain-setup-errors", attr: { role: "status" } });
    validation.errors.forEach((error) => errors.createEl("div", { text: error }));
    const actions = section.createDiv({ cls: "paperbrain-actions paperbrain-actions-wide" });
    const manualInstallButton = actions.createEl("button", { text: "Terminal install (recommended)" });
    manualInstallButton.addClass("paperbrain-primary");
    manualInstallButton.disabled = this.installerRuntime.running || this.process;
    manualInstallButton.addEventListener("click", () => this.plugin.showManualBackendInstall());
    const installButton = actions.createEl("button", { text: this.installerRuntime.running ? "Installing backend" : "Install inside Obsidian" });
    installButton.disabled = this.installerRuntime.running || this.process;
    installButton.addEventListener("click", async () => {
      await this.plugin.installBackend();
      this.render();
    });
    if (this.installerRuntime.running) {
      const stopInstall = actions.createEl("button", { text: "Stop installation" });
      stopInstall.addClass("paperbrain-danger");
      stopInstall.disabled = this.installerRuntime.stopping;
      stopInstall.addEventListener("click", () => this.plugin.backendInstaller.stop());
    }
    actions.createEl("button", { text: "Detect again" }).addEventListener("click", async () => {
      const result = await this.plugin.detectSetup();
      this.form.provider = this.plugin.settings.provider;
      this.appendLog(`setup detection: backend=${result.backendPath ? "found" : "missing"}, wd=${result.pythonPath ? result.pythonSource : "missing"}`);
      this.render();
    });
    actions.createEl("button", { text: "Validate setup" }).addEventListener("click", async () => {
      await this.plugin.detectSetup();
      const current = this.plugin.validateConfiguration(false);
      if (!current.ok) {
        this.appendLog(`setup validation failed: ${current.errors.join(" ")}`);
        new Notice("PaperBrain setup is incomplete. See console details.", 7000);
        this.render();
        return;
      }
      await this.runDoctorSequence();
    });
    const recovery = section.createDiv({ cls: "paperbrain-actions paperbrain-actions-wide" });
    if (this.plugin.settings.installerManaged) {
      recovery.createEl("button", { text: "Open API key file" }).addEventListener("click", () => this.plugin.openManagedEnvFile());
    }
      recovery.createEl("button", { text: "Open settings" }).addEventListener("click", () => this.plugin.openSettings());
    recovery.createEl("button", { text: "Copy redacted diagnostics" }).addEventListener("click", () => this.copyDiagnostics());
    if (this.installerRuntime.logs) {
      const installStatus = section.createDiv({ cls: "paperbrain-install-status", attr: { role: "status", "aria-live": "polite" } });
      installStatus.createEl("strong", { text: `Backend installation: ${this.installerRuntime.stage}` });
      const installLog = installStatus.createEl("pre", { text: this.installerRuntime.logs });
      requestAnimationFrame(() => {
        installLog.scrollTop = installLog.scrollHeight;
      });
    }
  }

  renderPresetSelect(parent) {
    const field = parent.createDiv({ cls: "paperbrain-field" });
    field.createEl("label", { text: "Run mode" });
    const select = field.createEl("select");
    select.dataset.paperbrainField = "preset";
    PRESETS.forEach((preset) => {
      const item = select.createEl("option", { text: preset.label, value: preset.id });
      item.selected = preset.id === this.form.preset;
    });
    select.addEventListener("change", () => this.applyPreset(select.value));
  }

  renderMain(parent) {
    const timeline = parent.createDiv({ cls: "paperbrain-section" });
    timeline.createEl("h3", { text: "Timeline" });
    this.renderTimeline(timeline);

    const status = parent.createDiv({ cls: "paperbrain-section" });
    status.createEl("h3", { text: "Live status" });
    this.renderLiveStatus(status);

    const papers = parent.createDiv({ cls: "paperbrain-section" });
    papers.createEl("h3", { text: "Paper queue" });
    this.renderPaperTable(papers);
  }

  renderDetails(parent) {
    const artifacts = parent.createDiv({ cls: "paperbrain-section" });
    artifacts.createEl("h3", { text: "Artifacts" });
    this.renderArtifacts(artifacts);

    const retry = parent.createDiv({ cls: "paperbrain-section" });
    retry.createEl("h3", { text: "Retry panel" });
    this.renderRetryPanel(retry);

    const review = parent.createDiv({ cls: "paperbrain-section" });
    review.createEl("h3", { text: "Review queue" });
    this.renderReviewQueue(review);

    const diagnostics = parent.createDiv({ cls: "paperbrain-section" });
    diagnostics.createEl("h3", { text: "Diagnostics" });
    if (this.lastPayload) {
      diagnostics.createEl("div", {
        cls: "paperbrain-muted",
        text: `${this.lastPayload.command || "command"} / exit ${this.lastPayload.exit_code ?? ""}`,
      });
    } else {
      diagnostics.createEl("div", { cls: "paperbrain-muted", text: "No command output yet." });
    }
    diagnostics.createEl("button", { cls: "paperbrain-copy-button", text: "Copy redacted diagnostics" })
      .addEventListener("click", () => this.copyDiagnostics());

    const logs = parent.createDiv({ cls: "paperbrain-section" });
    const head = logs.createDiv({ cls: "paperbrain-inline-actions" });
    head.createEl("h3", { text: "Logs" });
    const toggle = head.createEl("button", { text: this.showAllLogs ? "Warnings" : "All" });
    toggle.addEventListener("click", () => {
      this.showAllLogs = !this.showAllLogs;
      this.render();
    });
    this.renderLogs(logs);
  }

  renderLiveStatus(parent) {
    const snapshot = this.activitySnapshot();
    const board = parent.createDiv({ cls: `paperbrain-status-board is-${snapshot.tone}` });
    const head = board.createDiv({ cls: "paperbrain-status-head" });
    const marker = head.createDiv({ cls: "paperbrain-status-marker" });
    marker.createEl("span");
    const title = head.createDiv();
    title.createEl("strong", { text: snapshot.title });
    title.createEl("span", { text: snapshot.subtitle });

    const metrics = board.createDiv({ cls: "paperbrain-status-metrics" });
    snapshot.metrics.forEach((metric) => {
      const item = metrics.createDiv({ cls: "paperbrain-status-metric" });
      item.createEl("strong", { text: metric.value });
      item.createEl("span", { text: metric.label });
    });

    const latest = board.createDiv({ cls: "paperbrain-status-latest" });
    latest.createEl("span", { text: snapshot.latestLabel });
    latest.createEl("strong", { text: snapshot.latestText });
  }

  activitySnapshot() {
    const rawStage = this.liveStage || (this.state ? this.state.stage : "idle");
    const stage = normalizeStageForUi(rawStage);
    const meta = STAGE_DETAILS[stage] || { label: titleCase(rawStage || "Idle"), detail: "Ready" };
    const papers = (this.state && this.state.papers) || [];
    const stats = this.queueStats(papers);
    const errors = (this.state && this.state.errors) || [];
    const warningCount = this.warningCount();
    const latestLog = this.latestStateLog();
    const latestText = this.lastOutputLine || logText(latestLog) || "No activity recorded yet.";
    const isDone = this.state && this.state.stage === "completed" && !this.process;
    const isError = errors.length || rawStage === "failed" || rawStage === "cancelled";
    const tone = isError ? "error" : this.process ? "running" : isDone ? "done" : "idle";
    const title = this.process
      ? `${meta.label} is running`
      : isDone
        ? "Run completed"
        : isError
          ? "Run needs attention"
          : `${meta.label || "Idle"} status`;
    const subtitle = STAGE_DETAILS[stage]?.queue || meta.detail || "Waiting for a run.";
    return {
      tone,
      title,
      subtitle,
      latestLabel: latestLog ? `${eventLabel(latestLog)} / ${latestLog.ts || latestLog.created_at || ""}` : "Output",
      latestText,
      metrics: [
        { label: "papers", value: String(stats.total) },
        { label: "digest", value: String(stats.digest) },
        { label: "deep", value: String(stats.deep) },
        { label: "pdfs", value: String(stats.pdfs) },
        { label: "notes", value: String(stats.notes) },
        { label: "warn", value: String(warningCount) },
        { label: "err", value: String(errors.length) },
      ],
    };
  }

  latestStateLog() {
    const logs = ((this.state && this.state.logs) || []).filter(Boolean);
    return logs.length ? logs[logs.length - 1] : null;
  }

  warningCount() {
    const stateLogs = ((this.state && this.state.logs) || []).map(logText);
    const stderrLines = this.stderr.split(/\r?\n/);
    return [...stateLogs, ...stderrLines].filter((line) => /warn|warning|cooldown|rate limit/i.test(line)).length;
  }

  queueStats(papers) {
    const stats = {
      total: papers.length,
      digest: 0,
      deep: 0,
      pdfs: 0,
      notes: 0,
      localPdfs: 0,
      missingNotes: 0,
      high: 0,
    };
    papers.forEach((paper) => {
      const score = queueScoreValue(paper);
      if (score >= 7) stats.high += 1;
      if (paper.in_daily_digest) stats.digest += 1;
      if (paper.selected_for_deep_analysis) stats.deep += 1;
      if (textValue(paper.pdf_url)) stats.pdfs += 1;
      if (this.existingLocalPath(paper.pdf_path || paper.local_pdf_path)) stats.localPdfs += 1;
      const notePath = this.existingLocalPath(paper.note_path);
      if (notePath) stats.notes += 1;
      if (paper.note_path && !notePath) stats.missingNotes += 1;
    });
    return stats;
  }

  renderTimeline(parent) {
    const current = normalizeStageForUi(this.liveStage || (this.state ? this.state.stage : "idle"));
    const currentIndex = STAGE_TO_INDEX[current] ?? -1;
    const grid = parent.createDiv({ cls: "paperbrain-timeline" });
    STAGES.forEach((stage, index) => {
      const step = grid.createDiv({ cls: "paperbrain-step" });
      const meta = STAGE_DETAILS[stage];
      const status = this.stageStatus(current, index, currentIndex);
      if (status.className) step.addClass(status.className);
      step.createEl("strong", { text: meta.label });
      step.createEl("span", { cls: "paperbrain-step-detail", text: meta.detail });
      const state = step.createEl("span", { cls: "paperbrain-step-state" });
      state.createEl("i", { cls: "paperbrain-step-dot" });
      state.createEl("span", { text: status.text });
    });
  }

  stageStatus(current, index, currentIndex) {
    if (current === "failed" || current === "cancelled") {
      return index <= currentIndex ? { className: "is-error", text: "attention", kind: "error" } : { className: "", text: "waiting", kind: "waiting" };
    }
    if (current === "completed" || index < currentIndex) {
      return { className: "is-done", text: "done", kind: "done" };
    }
    if (index === currentIndex) {
      return { className: "is-active", text: this.process ? "running" : "active", kind: "active" };
    }
    return { className: "", text: "waiting", kind: "waiting" };
  }

  renderPaperTable(parent) {
    const papers = [...((this.state && this.state.papers) || [])].sort((a, b) => queueScoreValue(b) - queueScoreValue(a));
    if (!papers.length) {
      this.renderQueueEmpty(parent);
      return;
    }
    this.renderQueueSummary(parent, papers);
    const table = parent.createEl("table", { cls: "paperbrain-table" });
    const head = table.createEl("thead").createEl("tr");
    ["Title", "Score", "Stage", "PDF", "Note", "Digest", "Deep", "Quality", "Action"].forEach((label) => head.createEl("th", { text: label }));
    const body = table.createEl("tbody");
    papers.forEach((paper) => {
      const pdfPath = this.existingLocalPath(paper.pdf_path || paper.local_pdf_path);
      const notePath = this.existingLocalPath(paper.note_path);
      const pdfUrl = textValue(paper.pdf_url);
      const pdfStatus = pdfPath ? "local" : pdfUrl ? "url" : "no";
      const noteStatus = notePath ? "yes" : paper.note_path ? "missing" : "no";
      const row = body.createEl("tr");
      row.createEl("td", { cls: "paperbrain-title-cell", text: paper.title || paper.short_title || "Untitled" });
      row.createEl("td", { text: formatQueueScore(paper) });
      row.createEl("td", { text: paper.screening_stage || paperStageHint(paper) });
      row.createEl("td").appendChild(this.badge(pdfStatus, !!pdfPath, pdfPath || pdfUrl));
      row.createEl("td").appendChild(this.badge(noteStatus, !!notePath, notePath || paper.note_path || ""));
      row.createEl("td").appendChild(this.badge(paper.in_daily_digest ? "yes" : "no", paper.in_daily_digest));
      row.createEl("td").appendChild(this.badge(paper.selected_for_deep_analysis ? "yes" : "no", paper.selected_for_deep_analysis));
      this.renderQualityBars(row.createEl("td"), paper);
      const actions = row.createEl("td", { cls: "paperbrain-inline-actions" });
      if (notePath) {
        actions.createEl("button", { text: "Note" }).addEventListener("click", () => this.openPath(notePath));
      }
      if (pdfPath) {
        actions.createEl("button", { text: "PDF" }).addEventListener("click", () => this.openPath(pdfPath));
      }
      actions.createEl("button", { text: "Retry" }).addEventListener("click", () => this.retryPaperMode(paper, "run"));
    });
    this.renderPaperCards(parent, papers);
  }

  renderPaperCards(parent, papers) {
    const cards = parent.createDiv({ cls: "paperbrain-paper-cards" });
    papers.forEach((paper) => {
      const card = cards.createDiv({ cls: "paperbrain-paper-card" });
      card.createEl("strong", { text: paper.title || paper.short_title || "Untitled" });
      const facts = card.createDiv({ cls: "paperbrain-paper-facts" });
      [
        ["Score", formatQueueScore(paper)],
        ["Stage", paper.screening_stage || paperStageHint(paper)],
        ["Digest", paper.in_daily_digest ? "yes" : "no"],
        ["Deep", paper.selected_for_deep_analysis ? "yes" : "no"],
      ].forEach(([label, value]) => {
        const fact = facts.createDiv();
        fact.createEl("span", { text: label });
        fact.createEl("b", { text: value });
      });
      const actions = card.createDiv({ cls: "paperbrain-inline-actions" });
      const notePath = this.existingLocalPath(paper.note_path);
      const pdfPath = this.existingLocalPath(paper.pdf_path || paper.local_pdf_path);
      if (notePath) actions.createEl("button", { text: "Note" }).addEventListener("click", () => this.openPath(notePath));
      if (pdfPath) actions.createEl("button", { text: "PDF" }).addEventListener("click", () => this.openPath(pdfPath));
      actions.createEl("button", { text: "Retry" }).addEventListener("click", () => this.retryPaperMode(paper, "run"));
    });
  }

  renderQueueEmpty(parent) {
    const stage = normalizeStageForUi(this.liveStage || (this.state ? this.state.stage : "idle"));
    const meta = STAGE_DETAILS[stage];
    const empty = parent.createDiv({ cls: "paperbrain-empty paperbrain-queue-empty" });
    empty.createEl("strong", { text: stage === "idle" ? "No run state loaded." : "No saved papers yet." });
    empty.createEl("span", {
      text: meta
        ? meta.queue
        : "Choose a run mode and start a command; the queue appears after PaperBrain writes papers to state.json.",
    });
  }

  renderQueueSummary(parent, papers) {
    const stats = this.queueStats(papers);
    const summary = parent.createDiv({ cls: "paperbrain-queue-summary" });
    [
      ["Total", stats.total],
      ["High", stats.high],
      ["Digest", stats.digest],
      ["Deep", stats.deep],
      ["Local PDFs", stats.localPdfs],
      ["Notes", stats.notes],
      ["Missing notes", stats.missingNotes],
    ].forEach(([label, value]) => {
      const item = summary.createDiv({ cls: "paperbrain-queue-stat" });
      item.createEl("strong", { text: String(value) });
      item.createEl("span", { text: label });
    });
  }

  renderQualityBars(parent, paper) {
    const fields = [
      ["Rel", "relevance"],
      ["Nov", "novelty"],
      ["Rig", "rigor"],
      ["Evd", "evidence"],
      ["Con", "confidence"],
    ];
    const wrap = parent.createDiv({ cls: "paperbrain-quality-bars" });
    fields.forEach(([label, key]) => {
      const value = Math.max(0, Math.min(10, qualityMetricValue(paper, key)));
      const bar = wrap.createDiv({ cls: "paperbrain-quality-bar" });
      bar.title = `${label}: ${value.toFixed(1)}`;
      bar.createEl("span", { text: label });
      const track = bar.createDiv({ cls: "paperbrain-quality-track" });
      const fill = track.createDiv({ cls: "paperbrain-quality-fill" });
      fill.style.width = `${value * 10}%`;
    });
  }

  renderArtifacts(parent) {
    const artifacts = (this.state && this.state.artifacts) || {};
    const entries = Object.entries(artifacts).filter(([, value]) => !!value);
    if (!entries.length) {
      parent.createDiv({ cls: "paperbrain-empty", text: "No artifacts yet." });
      return;
    }
    entries.forEach(([key, value]) => {
      const item = parent.createDiv({ cls: "paperbrain-artifact" });
      item.createEl("span", { text: key });
      const button = item.createEl("button", { text: "Open" });
      button.addEventListener("click", () => this.openPath(value));
    });
  }

  renderLogs(parent) {
    const lines = [];
    if (this.stderr.trim()) lines.push(this.stderr.trim());
    const stateLogs = ((this.state && this.state.logs) || []).map((log) => {
      return `${log.ts || log.created_at || ""} ${log.event_type || "log"} ${log.status || ""} ${log.stage || ""} ${log.message || ""}`.trim();
    });
    const filtered = this.showAllLogs
      ? stateLogs
      : stateLogs.filter((line) => /warn|error|fail|cancel/i.test(line));
    lines.push(...filtered.slice(-80));
    const log = parent.createDiv({ cls: "paperbrain-log" });
    log.setText(lines.filter(Boolean).join("\n") || "No warnings or errors.");
    requestAnimationFrame(() => {
      log.scrollTop = log.scrollHeight;
    });
  }

  renderRetryPanel(parent) {
    const papers = [...((this.state && this.state.papers) || [])]
      .sort((a, b) => number(b.score) - number(a.score))
      .slice(0, 8);
    if (!papers.length) {
      parent.createDiv({ cls: "paperbrain-empty", text: "No papers available for retry." });
      return;
    }
    const globalActions = parent.createDiv({ cls: "paperbrain-actions paperbrain-actions-wide" });
    globalActions.createEl("button", { text: "Rebuild index" }).addEventListener("click", () => this.runIndex());
    globalActions.createEl("button", { text: "Refresh state" }).addEventListener("click", async () => {
      await this.loadState();
      this.render();
    });

    papers.forEach((paper) => {
      const item = parent.createDiv({ cls: "paperbrain-retry-item" });
      item.createEl("span", { text: paper.short_title || paper.title || "Untitled" });
      const actions = item.createDiv({ cls: "paperbrain-inline-actions" });
      actions.createEl("button", { text: "PDF" }).addEventListener("click", () => this.retryPaperMode(paper, "deep"));
      actions.createEl("button", { text: "Screen" }).addEventListener("click", () => this.retryPaperMode(paper, "screen"));
      actions.createEl("button", { text: "Deep" }).addEventListener("click", () => this.retryPaperMode(paper, "deep"));
    });
  }

  renderReviewQueue(parent) {
    const items = this.reviewPapers();
    if (!items.length) {
      parent.createDiv({ cls: "paperbrain-empty", text: "No papers need manual review." });
      return;
    }
    items.slice(0, 12).forEach(({ paper, reasons }) => {
      const item = parent.createDiv({ cls: "paperbrain-review-item" });
      item.createEl("strong", { text: paper.short_title || paper.title || "Untitled" });
      item.createEl("span", { text: reasons.join(" / ") });
      const actions = item.createDiv({ cls: "paperbrain-inline-actions" });
      actions.createEl("button", { text: "Retry" }).addEventListener("click", () => this.retryPaperMode(paper, "run"));
      if (paper.note_path) {
        actions.createEl("button", { text: "Note" }).addEventListener("click", () => this.openPath(paper.note_path));
      }
    });
  }

  renderBriefs(parent) {
    const briefDate = this.form.briefDate || this.form.date || yesterday();
    this.form.briefDate = briefDate;
    const period = briefPeriod(this.form.briefMode || "week", briefDate);
    const cacheKey = `${period.type}:${briefDate}`;
    const cached = this.briefCache && this.briefCache.key === cacheKey ? this.briefCache : null;
    const existing = cached ? cached.existing : "";

    const controls = parent.createDiv({ cls: "paperbrain-section" });
    controls.createEl("h3", { text: "Briefs" });
    this.select(controls, "Period", "briefMode", this.form.briefMode || "week", ["week", "month"], async (value) => {
      this.form.briefMode = value;
      await this.loadBriefData();
      this.render();
    });
    this.field(controls, "Date", "briefDate", briefDate, async (value) => {
      this.form.briefDate = value || yesterday();
      await this.loadBriefData();
      this.render();
    }, { type: "date", cls: "paperbrain-date-input", fieldCls: "paperbrain-date-field" });
    const actions = controls.createDiv({ cls: "paperbrain-actions" });
    actions.createEl("button", { text: "Generate" }).addEventListener("click", () => this.runBrief(period));
    const openButton = actions.createEl("button", { text: "Open" });
    openButton.disabled = !existing;
    openButton.addEventListener("click", () => existing && this.openPath(existing));

    const summary = cached ? cached.summary : { daysFound: 0, highCount: 0, entries: [] };
    const metricsSection = parent.createDiv({ cls: "paperbrain-section" });
    metricsSection.createEl("h3", { text: period.label, cls: "paperbrain-date-text" });
    const metrics = metricsSection.createDiv({ cls: "paperbrain-status-metrics paperbrain-brief-metrics" });
    [
      { label: "days", value: `${summary.daysFound}/${period.days}` },
      { label: "papers", value: String(summary.entries.length) },
      { label: "high", value: String(summary.highCount) },
      { label: "brief", value: existing ? "ready" : "none" },
    ].forEach((metric) => {
      const item = metrics.createDiv({ cls: "paperbrain-status-metric" });
      item.createEl("strong", { text: metric.value });
      item.createEl("span", { text: metric.label });
    });

    const topSection = parent.createDiv({ cls: "paperbrain-section" });
    topSection.createEl("h3", { text: "Top papers" });
    const topEntries = summary.entries.slice(0, 8);
    if (!topEntries.length) {
      topSection.createDiv({ cls: "paperbrain-empty", text: "No daily digest entries found." });
    } else {
      topEntries.forEach((entry) => {
        const item = topSection.createDiv({ cls: "paperbrain-brief-item" });
        const meta = item.createDiv();
        meta.createEl("strong", { text: entry.title || "Untitled" });
        meta.createEl("span", { text: `${entry.date} / ${formatScore(entry.score)}`, cls: "paperbrain-date-text" });
        const itemActions = item.createDiv({ cls: "paperbrain-inline-actions" });
        if (entry.digestPath) {
          itemActions.createEl("button", { text: "Digest" }).addEventListener("click", () => this.openPath(entry.digestPath));
        }
        const externalUrl = safeExternalHttpUrl(entry.url);
        if (externalUrl) {
          itemActions.createEl("button", { text: "Web" }).addEventListener("click", () => {
            window.open(externalUrl, "_blank", "noopener,noreferrer");
          });
        }
      });
    }

    this.renderBriefHistory(parent);
  }

  renderBriefHistory(parent) {
    const section = parent.createDiv({ cls: "paperbrain-section" });
    section.createEl("h3", { text: "Research briefs" });
    const history = this.briefHistory.slice(0, 10);
    if (!history.length) {
      section.createDiv({ cls: "paperbrain-empty", text: "No research briefs found." });
      return;
    }
    history.forEach((item) => {
      const row = section.createDiv({ cls: "paperbrain-brief-item" });
      const meta = row.createDiv();
      meta.createEl("strong", { text: item.label, cls: "paperbrain-date-text" });
      meta.createEl("span", { text: item.modified, cls: "paperbrain-date-text" });
      const actions = row.createDiv({ cls: "paperbrain-inline-actions" });
      actions.createEl("button", { text: "Open" }).addEventListener("click", () => this.openPath(item.path));
    });
  }

  runBrief(period) {
    const args = ["brief", "--mode", period.type, "--date", this.form.briefDate || yesterday()];
    this.spawnPaperBrain(args);
  }

  async findBrief(label) {
    const root = this.vaultPath("Research_Briefs");
    if (!root) return "";
    const direct = path.join(root, `${label}-ResearchBrief.md`);
    try {
      await fs.promises.access(direct);
      return direct;
    } catch (_) {
      // Fall back to older brief filenames in the configured briefs directory.
    }
    try {
      const match = (await fs.promises.readdir(root)).find((name) => name.endsWith("-ResearchBrief.md") && name.includes(label));
      return match ? path.join(root, match) : "";
    } catch (error) {
      if (error.code !== "ENOENT") this.appendLog(`brief lookup failed: ${error.message}`);
      return "";
    }
  }

  async readBriefHistory() {
    const root = this.vaultPath("Research_Briefs");
    try {
      const names = (await fs.promises.readdir(root)).filter((name) => name.endsWith("-ResearchBrief.md"));
      const items = await Promise.all(names.map(async (name) => {
          const fullPath = path.join(root, name);
          const stat = await fs.promises.stat(fullPath);
          return {
            path: fullPath,
            label: name.replace(/-ResearchBrief\.md$/, ""),
            modified: new Date(stat.mtimeMs).toISOString().slice(0, 16).replace("T", " "),
            sort: stat.mtimeMs,
          };
        }));
      return items.sort((a, b) => b.sort - a.sort);
    } catch (error) {
      if (error.code !== "ENOENT") this.appendLog(`brief history read failed: ${error.message}`);
      return [];
    }
  }

  async readDailyDigestSummary(startDate, endDate) {
    const dailyRoot = this.vaultPath("Daily_Papers");
    if (!dailyRoot) return { daysFound: 0, highCount: 0, entries: [] };
    const entries = [];
    let daysFound = 0;
    for (const dateKey of dateRange(startDate, endDate)) {
      const digestPath = path.join(dailyRoot, `${dateKey}-PaperDigest.md`);
      const digestEntries = await this.readDailyDigestEntries(digestPath, dateKey);
      if (digestEntries === null) continue;
      daysFound += 1;
      entries.push(...digestEntries);
    }
    entries.sort((a, b) => number(b.score) - number(a.score));
    return {
      daysFound,
      highCount: entries.filter((entry) => number(entry.score) >= 8).length,
      entries,
    };
  }

  async readDailyDigestEntries(digestPath, dateKey) {
    try {
      const raw = await fs.promises.readFile(digestPath, "utf8");
      return raw.split(/\n(?=###\s+)/)
        .map((chunk) => {
          const match = chunk.match(/^###\s+(.+?)\s+\(Score:\s*([0-9]+(?:\.[0-9]+)?)\/10\)/m);
          if (!match) return null;
          const link = digestField(chunk, "Link");
          return {
            title: cleanDigestTitle(match[1]),
            score: number(match[2]),
            date: dateKey,
            url: firstUrl(link),
            digestPath,
          };
        })
        .filter(Boolean);
    } catch (error) {
      if (error.code === "ENOENT") return null;
      this.appendLog(`daily digest read failed: ${error.message}`);
      return null;
    }
  }

  field(parent, label, key, value, onChange, options = {}) {
    const field = parent.createDiv({ cls: "paperbrain-field" });
    if (options.fieldCls) field.addClass(options.fieldCls);
    field.createEl("label", { text: label });
    const input = field.createEl("input");
    input.type = options.type || "text";
    if (options.cls) input.addClass(options.cls);
    input.dataset.paperbrainField = key;
    input.value = value || "";
    input.addEventListener("input", () => { this.form[key] = input.value; });
    input.addEventListener("change", () => onChange(input.value));
  }

  select(parent, label, key, value, options, onChange) {
    const field = parent.createDiv({ cls: "paperbrain-field" });
    field.createEl("label", { text: label });
    const select = field.createEl("select");
    select.dataset.paperbrainField = key;
    options.forEach((option) => {
      const item = select.createEl("option", { text: optionLabel(option), value: option });
      item.selected = option === value;
    });
    select.addEventListener("change", () => onChange(select.value));
  }

  badge(text, good, title = "") {
    const badge = document.createElement("span");
    badge.className = `paperbrain-badge ${good ? "is-good" : "is-warn"}`;
    badge.textContent = text;
    if (title) badge.title = title;
    return badge;
  }

  existingLocalPath(value) {
    const raw = textValue(value);
    if (!raw) return "";
    const vaultRoot = this.plugin.settings.vaultPath;
    if (!path.isAbsolute(raw) && !vaultRoot) return "";
    const candidate = path.isAbsolute(raw) ? raw : path.join(vaultRoot, raw);
    try {
      return fs.existsSync(candidate) ? candidate : "";
    } catch (error) {
      return "";
    }
  }

  applyPreset(id) {
    const preset = PRESETS.find((item) => item.id === id);
    if (!preset) return;
    this.form.preset = id;
    this.form.mode = preset.mode;
    if (preset.generatePodcast !== null) {
      this.form.generatePodcast = !!preset.generatePodcast;
    }
    if (preset.clearArxiv) {
      this.form.arxivUrl = "";
    }
    this.plugin.settings.lastPreset = id;
    this.plugin.saveSettings();
    this.refreshAfterInput();
  }

  renderRunHistory(parent) {
    const section = parent.createDiv({ cls: "paperbrain-section" });
    section.createEl("h3", { text: "Run history" });
    const history = this.runHistory.slice(0, 12);
    if (!history.length) {
      section.createDiv({ cls: "paperbrain-empty", text: "No historical runs found." });
      return;
    }
    history.forEach((item) => {
      const row = section.createDiv({ cls: "paperbrain-history-item" });
      const meta = row.createDiv();
      meta.createEl("strong", { text: item.run_id || "unknown-run", cls: "paperbrain-date-text" });
      meta.createEl("span", { text: `${item.stage || "unknown"} / ${item.updated_at || item.date || ""}`, cls: "paperbrain-date-text" });
      const actions = row.createDiv({ cls: "paperbrain-inline-actions" });
      actions.createEl("button", { text: "Load" }).addEventListener("click", async () => {
        this.form.date = item.date || this.form.date;
        this.form.provider = item.provider || this.form.provider;
        const modes = item.run_modes || [];
        const singleOnly = modes.includes("single") && !modes.includes("daily");
        this.form.arxivUrl = singleOnly || (item.single_paper && !modes.length) ? this.firstPaperUrl(item) : "";
        this.activePanel = "timeline";
        await this.loadState();
        this.render();
      });
      if (item.artifacts && item.artifacts.daily_digest) {
        actions.createEl("button", { text: "Digest" }).addEventListener("click", () => this.openPath(item.artifacts.daily_digest));
      }
    });
  }

  async loadRunHistory() {
    this.runHistory = await this.readRunHistory();
  }

  async readRunHistory() {
    const root = this.vaultPath("Run_Records");
    const items = [];
    try {
      const entries = await fs.promises.readdir(root, { withFileTypes: true });
      for (const entry of entries) {
        if (entry.isDirectory()) {
          const statePath = path.join(root, entry.name, "state.json");
          const item = await this.readStateSummary(statePath);
          if (item) items.push(item);
        } else if (entry.isFile() && entry.name.endsWith("-run-state.json")) {
          const item = await this.readStateSummary(path.join(root, entry.name));
          if (item) items.push(item);
        }
      }
    } catch (error) {
      if (error.code !== "ENOENT") this.appendLog(`run history read failed: ${error.message}`);
    }
    return items.sort((a, b) => textValue(b.updated_at).localeCompare(textValue(a.updated_at)));
  }

  async readStateSummary(statePath) {
    try {
      const data = JSON.parse(await fs.promises.readFile(statePath, "utf8"));
      return {
        run_id: data.run_id || path.basename(path.dirname(statePath)),
        date: data.date || "",
        provider: data.provider || this.form.provider,
        providers: data.providers || [],
        run_modes: data.run_modes || [],
        single_paper: !!data.single_paper,
        stage: data.stage || "",
        updated_at: data.updated_at || data.created_at || "",
        artifacts: data.artifacts || {},
        papers: data.papers || [],
      };
    } catch (error) {
      return null;
    }
  }

  firstPaperUrl(item) {
    const paper = (item.papers || [])[0] || {};
    const arxivId = extractArxivId(paper.arxiv_id || paper.paper_id || paper.pdf_url || paper.url);
    return textValue(paper.url) || (arxivId ? `https://arxiv.org/abs/${arxivId}` : "") || textValue(paper.pdf_url);
  }

  reviewPapers() {
    return [...((this.state && this.state.papers) || [])]
      .map((paper) => {
        const reasons = [];
        const flags = Array.isArray(paper.red_flags) ? paper.red_flags : [];
        if (number(paper.confidence) > 0 && number(paper.confidence) < 5) reasons.push("low confidence");
        if (flags.length > 2) reasons.push("many red flags");
        if (number(paper.score) >= 7 && !this.existingLocalPath(paper.pdf_path || paper.local_pdf_path)) reasons.push("high score missing PDF");
        if (paper.selected_for_deep_analysis && !this.existingLocalPath(paper.note_path)) reasons.push("deep selected missing note");
        if (paper.should_rescreen && paper.screening_stage === "coarse_only") reasons.push("needs re-screen");
        return { paper, reasons };
      })
      .filter((item) => item.reasons.length)
      .sort((a, b) => number(b.paper.score) - number(a.paper.score));
  }

  refreshAfterInput() {
    this.loadState().then(() => this.render());
  }

  async runSelected() {
    const mode = this.form.mode;
    const args = [mode];
    if (mode === "index") {
      this.form.forceRun = false;
      await this.spawnPaperBrain(args);
      return;
    }
    const arxivUrl = this.form.arxivUrl.trim();
    const omitAutoArxivDate = mode !== "digest" && arxivUrl && !this.dateTouched;
    if (!omitAutoArxivDate) args.push("--date", this.form.date);
    args.push("--provider", this.form.provider);
    if (mode !== "digest") {
      if (!this.form.generatePodcast) args.push("--no-podcast");
      if (arxivUrl) args.push("--arxiv-url", arxivUrl);
    }
    if (this.form.forceRun && ["run", "fetch", "screen", "deep"].includes(mode)) {
      args.push("--force");
    }
    const force = this.form.forceRun;
    this.form.forceRun = false;
    await this.spawnPaperBrain(args, { force });
  }

  async runDoctor() {
    await this.runDoctorSequence();
  }

  runIndex() {
    this.form.mode = "index";
    this.spawnPaperBrain(["index"]);
  }

  stopRun() {
    this.plugin.processManager.requestStop();
  }

  async spawnPaperBrain(commandArgs, options = {}) {
    if (this.disposed) return;
    if (this.installerRuntime.running) {
      new Notice("Wait for backend installation to finish before running PaperBrain.");
      return null;
    }
    if (this.process) {
      new Notice("PaperBrain is already running.");
      return null;
    }
    const validation = this.plugin.validateConfiguration(false);
    if (!validation.ok) {
      this.activePanel = "run";
      this.appendLog(`configuration invalid: ${validation.errors.join(" ")}`);
      new Notice("PaperBrain setup needs attention. Open the console for details.", 8000);
      this.render();
      return null;
    }
    const requirements = runConfirmationRequirements(this.plugin.settings, {
      command: commandArgs[0],
      force: options.force || commandArgs.includes("--force"),
    });
    if (!options.skipConfirmation && (requirements.paidDisclosure || requirements.forceReset)) {
      const accepted = await confirmRun(this.app, {
        provider: this.form.provider,
        mode: commandArgs[0],
        podcast: this.form.generatePodcast && !commandArgs.includes("--no-podcast"),
        paidDisclosure: requirements.paidDisclosure,
        forceReset: requirements.forceReset,
      });
      if (!accepted) return null;
      if (requirements.paidDisclosure) {
        this.plugin.settings.paidRunDisclosureAccepted = true;
        await this.plugin.saveSettings();
      }
    }
    const invocation = buildInvocation(this.plugin.settings, commandArgs, { existsSync: fs.existsSync });
    const result = this.plugin.processManager.start({
      invocation,
      commandArgs,
      spawnOptions: buildSpawnOptions(this.plugin.settings, invocation),
      timeoutMs: Math.max(3, Number(this.plugin.settings.cancelTimeoutSeconds || 20)) * 1000,
      context: {
        date: this.form.date,
        provider: this.form.provider,
        mode: this.form.mode,
        preset: this.form.preset,
        arxivUrl: this.form.arxivUrl,
        generatePodcast: this.form.generatePodcast,
      },
    });
    if (!result.started && result.reason === "already-running") new Notice("PaperBrain is already running.");
    return result.completion;
  }

  async runDoctorSequence() {
    return this.plugin.validateSetup();
  }

  startPolling() {
    this.stopPolling();
    if (this.disposed) return;
    const poll = async () => {
      if (this.disposed || !this.process) {
        this.stopPolling();
        return;
      }
      if (!this.pollInFlight) {
        this.pollInFlight = true;
        try {
          const changed = await this.loadState();
          if (this.state && this.state.stage && this.state.stage !== "initialized") {
            this.plugin.processManager.setStage(this.state.stage);
          }
          if (changed) this.render();
        } finally {
          this.pollInFlight = false;
        }
      }
      if (!this.disposed && this.process) this.pollTimer = window.setTimeout(poll, 2000);
    };
    this.pollTimer = window.setTimeout(poll, 2000);
  }

  stopPolling() {
    if (this.pollTimer) {
      window.clearTimeout(this.pollTimer);
      this.pollTimer = null;
    }
  }

  openArtifact(key) {
    const artifacts = (this.state && this.state.artifacts) || {};
    if (!artifacts[key]) {
      new Notice(`No ${key} artifact for this run.`);
      return;
    }
    this.openPath(artifacts[key]);
  }

  openPath(value) {
    const relativePath = toVaultRelativePath(value, this.plugin.settings.vaultPath);
    if (!relativePath) {
      new Notice(`Artifact is outside the vault or missing: ${value}`);
      return;
    }
    const relative = normalizePath(relativePath);
    const file = this.app.vault.getAbstractFileByPath(relative);
    if (file) {
      this.app.workspace.getLeaf(true).openFile(file);
      return;
    }
    new Notice(`Artifact is outside the vault or missing: ${value}`);
  }

  retryPaper(paper) {
    this.retryPaperMode(paper, "run");
  }

  retryPaperMode(paper, mode) {
    const arxivId = extractArxivId(paper.arxiv_id || paper.paper_id || paper.pdf_url || paper.url);
    const url = textValue(paper.url) || (arxivId ? `https://arxiv.org/abs/${arxivId}` : "") || textValue(paper.pdf_url);
    if (!url) {
      new Notice("No retry URL or paper id is available.");
      return;
    }
    this.form.mode = mode;
    this.form.arxivUrl = url;
    this.activePanel = "run";
    this.render();
    new Notice(`Paper loaded for ${mode} retry.`);
  }

  copyDiagnostics() {
    const payload = {
      lastPayload: this.lastPayload,
      state: this.state
        ? {
            run_id: this.state.run_id,
            stage: this.state.stage,
            errors: this.state.errors || [],
            artifacts: this.state.artifacts || {},
          }
        : null,
      stderr: this.stderr.slice(-4000),
      stdout: this.stdout.slice(-4000),
      recentLogs: ((this.state && this.state.logs) || []).slice(-20),
    };
    const redacted = redactDiagnostics(payload, [
      this.plugin.settings.vaultPath,
      this.plugin.settings.backendPath,
      this.plugin.settings.configPath,
      this.plugin.settings.cliPath,
      this.plugin.settings.pythonPath,
    ]);
    navigator.clipboard.writeText(JSON.stringify(redacted, null, 2))
      .then(() => new Notice("Redacted PaperBrain diagnostics copied. Review before sharing."))
      .catch((error) => {
        this.appendLog(`clipboard copy failed: ${error.message}`);
        this.render();
      });
  }

  appendLog(line) {
    this.plugin.processManager.appendLog(line);
  }
}

class ArxivCategoryModal extends Modal {
  constructor(app, initial, onApply) {
    super(app);
    this.mode = initial.categoryMode === "all" ? "all" : "selected";
    this.selected = new Set(initial.categories || []);
    this.onApply = onApply;
    this.query = "";
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.empty();
    const shell = contentEl.createDiv({ cls: "paperbrain-category-modal" });
    const header = shell.createDiv({ cls: "paperbrain-category-header" });
    header.createEl("h2", { text: "Choose arXiv categories" });
    this.countEl = header.createEl("span", { cls: "paperbrain-count-badge" });

    const mode = shell.createDiv({ cls: "paperbrain-segmented", attr: { role: "group", "aria-label": "arXiv scope" } });
    this.selectedModeButton = mode.createEl("button", { text: "Selected categories" });
    this.allModeButton = mode.createEl("button", { text: "All arXiv" });
    this.selectedModeButton.addEventListener("click", () => this.setMode("selected"));
    this.allModeButton.addEventListener("click", () => this.setMode("all"));

    const toolbar = shell.createDiv({ cls: "paperbrain-category-toolbar" });
    const search = toolbar.createEl("input", {
      type: "search",
      placeholder: "Search code or category name",
      attr: { "aria-label": "Search arXiv categories" },
    });
    search.addEventListener("input", () => {
      this.query = search.value.trim().toLocaleLowerCase();
      this.renderCategoryList();
    });
    const reset = toolbar.createEl("button", {
      cls: "clickable-icon paperbrain-category-tool",
      attr: { "aria-label": "Restore default categories", title: "Restore default categories" },
    });
    setIcon(reset, "rotate-ccw");
    reset.addEventListener("click", () => {
      this.mode = "selected";
      this.selected = new Set(DEFAULT_CATEGORIES);
      this.renderCategoryList();
      this.updateModalState();
    });
    const clear = toolbar.createEl("button", {
      cls: "clickable-icon paperbrain-category-tool",
      attr: { "aria-label": "Clear category selection", title: "Clear category selection" },
    });
    setIcon(clear, "trash-2");
    clear.addEventListener("click", () => {
      this.mode = "selected";
      this.selected.clear();
      this.renderCategoryList();
      this.updateModalState();
    });

    this.listEl = shell.createDiv({ cls: "paperbrain-category-list" });
    const actions = shell.createDiv({ cls: "modal-button-container paperbrain-category-actions" });
    actions.createEl("button", { text: "Cancel" }).addEventListener("click", () => this.close());
    this.applyButton = actions.createEl("button", { text: "Apply", cls: "mod-cta" });
    this.applyButton.addEventListener("click", () => {
      if (this.mode === "selected" && !this.selected.size) {
        new Notice("Choose at least one arXiv category.");
        return;
      }
      this.onApply({ categoryMode: this.mode, categories: [...this.selected] });
      this.close();
    });
    this.renderCategoryList();
    this.updateModalState();
  }

  setMode(mode) {
    this.mode = mode === "all" ? "all" : "selected";
    this.renderCategoryList();
    this.updateModalState();
  }

  updateModalState() {
    if (!this.countEl) return;
    this.countEl.setText(this.mode === "all" ? "All categories" : `${this.selected.size} selected`);
    this.selectedModeButton.toggleClass("is-active", this.mode === "selected");
    this.allModeButton.toggleClass("is-active", this.mode === "all");
    this.applyButton.disabled = this.mode === "selected" && !this.selected.size;
  }

  renderCategoryList() {
    if (!this.listEl) return;
    this.listEl.empty();
    if (this.mode === "all") {
      this.listEl.createEl("p", {
        cls: "paperbrain-settings-note",
        text: "Every arXiv category submitted on the target date will be checked locally against your keywords.",
      });
      this.updateModalState();
      return;
    }

    let visibleCount = 0;
    const visibleGroups = filterCategoryGroups(this.query);
    for (const visibleGroup of visibleGroups) {
      const group = ARXIV_CATEGORY_GROUPS.find((item) => item.group === visibleGroup.group);
      const visible = visibleGroup.categories;
      visibleCount += visible.length;
      const details = this.listEl.createEl("details", { cls: "paperbrain-category-group" });
      details.open = Boolean(this.query) || visible.some((category) => this.selected.has(category.id));
      const summary = details.createEl("summary");
      const groupCheckbox = summary.createEl("input", { type: "checkbox", attr: { "aria-label": `Select ${group.group}` } });
      const selectedCount = group.categories.filter((category) => this.selected.has(category.id)).length;
      groupCheckbox.checked = selectedCount === group.categories.length;
      groupCheckbox.indeterminate = selectedCount > 0 && selectedCount < group.categories.length;
      groupCheckbox.addEventListener("click", (event) => event.stopPropagation());
      groupCheckbox.addEventListener("change", () => {
        this.selected = updateCategoryGroupSelection(this.selected, group.group, groupCheckbox.checked);
        this.renderCategoryList();
        this.updateModalState();
      });
      summary.createEl("span", { text: group.group });
      summary.createEl("small", { text: `${selectedCount}/${group.categories.length}` });

      const options = details.createDiv({ cls: "paperbrain-category-options" });
      for (const category of visible) {
        const label = options.createEl("label", { cls: "paperbrain-category-option" });
        const checkbox = label.createEl("input", { type: "checkbox" });
        checkbox.checked = this.selected.has(category.id);
        checkbox.addEventListener("change", () => {
          if (checkbox.checked) this.selected.add(category.id);
          else this.selected.delete(category.id);
          this.updateModalState();
          const nextSelectedCount = group.categories.filter((item) => this.selected.has(item.id)).length;
          groupCheckbox.checked = nextSelectedCount === group.categories.length;
          groupCheckbox.indeterminate = nextSelectedCount > 0 && nextSelectedCount < group.categories.length;
          summary.querySelector("small").setText(`${nextSelectedCount}/${group.categories.length}`);
        });
        label.createEl("code", { text: category.id });
        label.createEl("span", { text: category.name });
      }
    }
    if (!visibleCount) {
      this.listEl.createEl("p", { cls: "paperbrain-settings-note", text: "No matching arXiv categories." });
    }
    this.updateModalState();
  }
}

class PaperBrainSettingTab extends PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  createSection(parent, id, title, description, icon) {
    const section = parent.createEl("section", {
      cls: `paperbrain-settings-section paperbrain-settings-${id}`,
      attr: { "data-paperbrain-settings-section": id },
    });
    const heading = section.createDiv({ cls: "paperbrain-settings-section-heading" });
    const iconEl = heading.createSpan({ cls: "paperbrain-settings-section-icon" });
    setIcon(iconEl, icon);
    const copy = heading.createDiv();
    copy.createEl("h2", { text: title });
    copy.createEl("p", { text: description });
    return section;
  }

  loadDiscoveryDraft(force = false) {
    const configPath = this.plugin.discoveryConfigPath();
    const configBecameAvailable = this.discoveryReadState
      && !this.discoveryReadState.readable
      && fs.existsSync(configPath);
    if (force || configBecameAvailable || !this.discoveryDraft || this.discoverySourcePath !== configPath) {
      const state = readDiscoverySettings(configPath);
      this.discoverySourcePath = state.configPath;
      this.discoveryReadState = state;
      this.discoveryDraft = {
        keywords: [...state.keywords],
        categoryMode: state.categoryMode,
        categories: [...state.categories],
      };
    }
    return this.discoveryReadState;
  }

  addKeywordBatch(value) {
    const additions = parseKeywordBatch(value);
    if (!additions.length) return false;
    this.discoveryDraft.keywords = normalizeKeywords([...this.discoveryDraft.keywords, ...additions]);
    return true;
  }

  renderDiscoverySection(section) {
    const readState = this.loadDiscoveryDraft();
    const draft = this.discoveryDraft;
    const keywordSetting = new Setting(section)
      .setName("Interest keywords")
      .setDesc("Only locally matched papers enter model scoring.");
    const editor = keywordSetting.controlEl.createDiv({ cls: "paperbrain-keyword-editor" });
    const tags = editor.createDiv({ cls: "paperbrain-keyword-tags" });
    for (const keyword of draft.keywords) {
      const tag = tags.createSpan({ cls: "paperbrain-keyword-tag" });
      tag.createSpan({ text: keyword });
      const remove = tag.createEl("button", {
        cls: "clickable-icon paperbrain-keyword-remove",
        attr: { "aria-label": `Remove ${keyword}`, title: `Remove ${keyword}` },
      });
      setIcon(remove, "x");
      remove.addEventListener("click", () => {
        draft.keywords = draft.keywords.filter((value) => value !== keyword);
        this.display();
      });
    }
    const input = editor.createEl("input", {
      type: "text",
      cls: "paperbrain-keyword-input",
      placeholder: "Add keywords",
      attr: { "aria-label": "Add research keywords" },
    });
    const rerenderAndFocus = () => {
      this.display();
      requestAnimationFrame(() => {
        const nextInput = this.containerEl.querySelector(".paperbrain-keyword-input");
        if (nextInput) nextInput.focus();
      });
    };
    const commit = () => {
      if (!this.addKeywordBatch(input.value)) return;
      input.value = "";
      rerenderAndFocus();
    };
    input.addEventListener("keydown", (event) => {
      if (event.key !== "Enter") return;
      event.preventDefault();
      commit();
    });
    input.addEventListener("input", () => {
      if (input.value.includes(",") || /[\r\n]/.test(input.value)) commit();
    });
    input.addEventListener("paste", (event) => {
      const value = event.clipboardData && event.clipboardData.getData("text");
      if (!value || !/[,\r\n]/.test(value)) return;
      event.preventDefault();
      if (this.addKeywordBatch(value)) rerenderAndFocus();
    });

    const categorySummary = draft.categoryMode === "all"
      ? "All arXiv"
      : `${draft.categories.length} selected${draft.categories.length ? `: ${draft.categories.slice(0, 4).join(", ")}${draft.categories.length > 4 ? "..." : ""}` : ""}`;
    new Setting(section)
      .setName("arXiv categories")
      .setDesc(categorySummary)
      .addButton((button) => button
        .setButtonText("Choose categories")
        .onClick(() => {
          new ArxivCategoryModal(this.app, draft, (selection) => {
            draft.categoryMode = selection.categoryMode;
            draft.categories = [...selection.categories];
            this.display();
          }).open();
        }));

    const validated = validateDiscoverySettings(draft);
    const busyReason = this.plugin.discoverySaveBlockReason();
    const unavailableReason = readState.readable ? "" : readState.error;
    const status = unavailableReason || busyReason || validated.errors.join(" ");
    const save = new Setting(section)
      .setName("Discovery preferences")
      .setDesc(status || `Config: ${this.discoverySourcePath}`)
      .addButton((button) => button
        .setCta()
        .setButtonText("Save discovery preferences")
        .setDisabled(Boolean(status))
        .onClick(() => {
          const currentBlock = this.plugin.discoverySaveBlockReason();
          if (currentBlock) {
            new Notice(currentBlock);
            this.display();
            return;
          }
          try {
            writeDiscoverySettings(this.discoverySourcePath, draft);
            new Notice("Discovery preferences saved.");
            this.loadDiscoveryDraft(true);
            this.display();
          } catch (error) {
            new Notice(`Could not save discovery preferences: ${error.message}`);
            this.loadDiscoveryDraft(true);
            this.display();
          }
        }));
    save.settingEl.toggleClass("is-error", Boolean(unavailableReason || validated.errors.length));
    save.settingEl.toggleClass("is-busy", Boolean(busyReason));
  }

  display() {
    const { containerEl } = this;
    containerEl.empty();
    containerEl.addClass("paperbrain-settings-page");
    const discoverySection = this.createSection(
      containerEl,
      "discovery",
      "Research discovery",
      "Control which daily papers are checked locally before model scoring.",
      "search",
    );
    const runtimeSection = this.createSection(
      containerEl,
      "runtime",
      "Runtime & updates",
      "Validate the backend, install it, and keep PaperBrain current.",
      "activity",
    );
    const networkSection = this.createSection(
      containerEl,
      "network",
      "Network & provider",
      "Configure downloads, connectivity, and the default model provider.",
      "network",
    );
    const advancedSection = this.createSection(
      containerEl,
      "advanced-section",
      "Advanced",
      "Override detected paths and lower-level runtime behavior.",
      "settings-2",
    );
    const advanced = advancedSection.createEl("details", { cls: "paperbrain-settings-advanced" });
    advanced.createEl("summary", { text: "Show advanced settings" });
    this.renderDiscoverySection(discoverySection);
    const validation = this.plugin.validateConfiguration(false);
    new Setting(runtimeSection)
      .setName("Runtime status")
      .setDesc(validation.ok
        ? `${validation.invocation.mode === "cli" ? "CLI" : "Python script"} mode is ready.${validation.warnings[0] ? ` ${validation.warnings[0]}` : ""}`
        : validation.errors.join(" "))
      .addButton((button) => button
        .setButtonText("Detect again")
        .onClick(async () => {
          await this.plugin.detectSetup();
          this.display();
        }))
      .addButton((button) => button
        .setCta()
        .setButtonText("Validate setup")
        .onClick(async () => {
          await this.plugin.activateView();
          await this.plugin.validateSetup();
          this.display();
        }));
    const updateState = this.plugin.softwareUpdates || {};
    const updates = new Setting(runtimeSection)
      .setName("Software updates")
      .setDesc(this.plugin.softwareUpdateDescription())
      .addButton((button) => button
        .setCta()
        .setButtonText(updateState.checking ? "Checking" : "Check for updates")
        .setDisabled(this.plugin.softwareUpdatesBusy())
        .onClick(async () => {
          const checking = this.plugin.checkSoftwareUpdates();
          this.display();
          await checking;
          this.display();
        }));
    if (updateState.console && updateState.console.available) {
      updates.addButton((button) => button
        .setButtonText(updateState.console.updating ? "Updating Console" : "Update Console")
        .setDisabled(this.plugin.softwareUpdatesBusy())
        .onClick(async () => {
          const updating = this.plugin.updateConsole();
          this.display();
          await updating;
          this.display();
        }));
    }
    if (updateState.backend && updateState.backend.available) {
      updates.addButton((button) => button
        .setButtonText(updateState.backend.updating ? "Updating backend" : "Update backend")
        .setDisabled(this.plugin.softwareUpdatesBusy())
        .onClick(async () => {
          const updating = this.plugin.updateBackend();
          this.display();
          await updating;
          this.display();
        }));
    }
    new Setting(runtimeSection)
      .setName("Backend installation")
      .setDesc("Terminal installation is recommended when your shell supplies proxy or network settings. The existing in-app installer remains available.")
      .addButton((button) => button
        .setCta()
        .setButtonText("Show terminal command")
        .setDisabled(this.plugin.backendInstaller.snapshot().running)
        .onClick(() => this.plugin.showManualBackendInstall()))
      .addButton((button) => button
        .setButtonText(this.plugin.backendInstaller.snapshot().running ? "Installing" : "Install inside Obsidian")
        .setDisabled(this.plugin.backendInstaller.snapshot().running)
        .onClick(async () => {
          await this.plugin.activateView();
          await this.plugin.installBackend();
          this.display();
        }));
    new Setting(advanced)
      .setName("Backend directory")
      .setDesc("Folder containing script/paperbrain.py. Detection checks this folder and the current vault only.")
      .addText((input) => input
        .setValue(this.plugin.settings.backendPath)
        .onChange(async (value) => {
          this.plugin.settings.backendPath = value.trim();
          await this.plugin.saveSettings();
        }));
    new Setting(advanced)
      .setName("wd Python")
      .setDesc("Python executable from the existing wd Conda environment.")
      .addText((input) => input
        .setPlaceholder(process.platform === "win32" ? "...\\envs\\wd\\python.exe" : ".../envs/wd/bin/python")
        .setValue(this.plugin.settings.pythonPath)
        .onChange(async (value) => {
          this.plugin.settings.pythonPath = value.trim();
          await this.plugin.saveSettings();
        }));
    new Setting(networkSection)
      .setName("Dependency download source")
      .setDesc("Auto downloads one fixed 1.6 MB wheel from PyPI, Alibaba Cloud, USTC, and TUNA, verifies its hash, then uses the fastest working source.")
      .addDropdown((dropdown) => dropdown
        .addOption("auto", "Auto (fastest available)")
        .addOption("pypi", "Official PyPI")
        .addOption("aliyun", "Alibaba Cloud")
        .addOption("ustc", "USTC")
        .addOption("tuna", "Tsinghua TUNA")
        .addOption("custom", "Custom HTTPS mirror")
        .setValue(this.plugin.settings.dependencySource)
        .onChange(async (value) => {
          this.plugin.settings.dependencySource = value;
          await this.plugin.saveSettings();
          this.display();
        }));
    new Setting(networkSection)
      .setName("Network proxy")
      .setDesc("Applies to PaperBrain runs, diagnostics, and installation inside Obsidian. Terminal installation keeps the terminal's own environment.")
      .addDropdown((dropdown) => dropdown
        .addOption("inherit", "Inherit Obsidian environment")
        .addOption("manual", "Manual HTTP(S) proxy")
        .addOption("direct", "Direct connection")
        .setValue(this.plugin.settings.proxyMode)
        .onChange(async (value) => {
          this.plugin.settings.proxyMode = value;
          await this.plugin.saveSettings();
          this.display();
        }))
      .addButton((button) => button
        .setButtonText("Test connection")
        .setDisabled(this.plugin.backendInstaller.snapshot().running || this.plugin.processManager.snapshot().running)
        .onClick(async () => {
          await this.plugin.activateView();
          await this.plugin.testNetworkConnection();
          this.display();
        }));
    if (this.plugin.settings.proxyMode === "manual") {
      new Setting(networkSection)
        .setName("Proxy URL")
        .setDesc("HTTP or HTTPS origin with an explicit port. Credentials, paths, queries, and fragments are rejected.")
        .addText((input) => input
          .setPlaceholder("http://127.0.0.1:7890")
          .setValue(this.plugin.settings.proxyUrl)
          .onChange(async (value) => {
            this.plugin.settings.proxyUrl = value.trim();
            await this.plugin.saveSettings();
          }));
    }
    new Setting(networkSection)
      .setName("Default provider")
      .addDropdown((dropdown) => dropdown
        .addOption("openrouter", "OpenRouter")
        .addOption("doubao", "Doubao")
        .setValue(this.plugin.settings.provider)
        .onChange(async (value) => {
          this.plugin.settings.provider = value;
          await this.plugin.saveSettings();
        }));
    new Setting(networkSection)
      .setName("API key file")
      .setDesc("Open the local .env file used by OpenRouter or Doubao. API keys are never stored in Obsidian plugin settings.")
      .addButton((button) => button
        .setButtonText("Open .env file")
        .onClick(() => this.plugin.openManagedEnvFile()));
    if (this.plugin.settings.dependencySource === "custom") {
      new Setting(advanced)
        .setName("Custom dependency mirror")
        .setDesc("Credential-free HTTPS simple-index URL. It must end in /simple.")
        .addText((input) => input
          .setPlaceholder("https://mirror.example.org/pypi/simple")
          .setValue(this.plugin.settings.customDependencyIndex)
          .onChange(async (value) => {
            this.plugin.settings.customDependencyIndex = value.trim();
            await this.plugin.saveSettings();
          }));
    }
    new Setting(advanced)
      .setName("Conda executable")
      .setDesc("Optional absolute path to conda. Detection also checks the active environment, wd Python location, PATH, and common user installs.")
      .addText((input) => input
        .setPlaceholder(process.platform === "win32" ? "...\\Scripts\\conda.exe" : ".../bin/conda")
        .setValue(this.plugin.settings.condaPath)
        .onChange(async (value) => {
          this.plugin.settings.condaPath = value.trim();
          await this.plugin.saveSettings();
        }));
    new Setting(advanced)
      .setName("Execution mode")
      .setDesc("Auto uses a backend script when found, otherwise the installed PaperBrain CLI.")
      .addDropdown((dropdown) => dropdown
        .addOption("auto", "Auto")
        .addOption("cli", "Installed CLI")
        .addOption("python-script", "Python script")
        .setValue(this.plugin.settings.executionMode)
        .onChange(async (value) => {
          this.plugin.settings.executionMode = value;
          await this.plugin.saveSettings();
          this.display();
        }));
    new Setting(advanced)
      .setName("CLI executable")
      .setDesc("Optional absolute path or command name. Leave empty to use paperbrain from PATH.")
      .addText((input) => input
        .setPlaceholder("paperbrain")
        .setValue(this.plugin.settings.cliPath)
        .onChange(async (value) => {
          this.plugin.settings.cliPath = value.trim();
          await this.plugin.saveSettings();
        }));
    new Setting(advanced)
      .setName("Backend config override")
      .setDesc("Optional YAML path passed to CLI and Python script runs.")
      .addText((input) => input
        .setValue(this.plugin.settings.configPath)
        .onChange(async (value) => {
          this.plugin.settings.configPath = value.trim();
          await this.plugin.saveSettings();
        }));
    new Setting(advanced)
      .setName("Vault path override")
      .setDesc("Detected from the active desktop vault. Change only when outputs belong in another vault.")
      .addText((input) => input
        .setValue(this.plugin.settings.vaultPath)
        .onChange(async (value) => {
          this.plugin.settings.vaultPath = value.trim();
          await this.plugin.saveSettings();
        }));
    new Setting(advanced)
      .setName("Generate podcast by default")
      .addToggle((toggle) => toggle
        .setValue(!!this.plugin.settings.generatePodcast)
        .onChange(async (value) => {
          this.plugin.settings.generatePodcast = value;
          await this.plugin.saveSettings();
        }));
    new Setting(advanced)
      .setName("Cancel timeout seconds")
      .addText((text) => text
        .setValue(String(this.plugin.settings.cancelTimeoutSeconds))
        .onChange(async (value) => {
          this.plugin.settings.cancelTimeoutSeconds = Math.max(3, Number(value || 20));
          await this.plugin.saveSettings();
        }));
  }
}

class RunConfirmationModal extends Modal {
  constructor(app, details, resolve) {
    super(app);
    this.details = details;
    this.resolve = resolve;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.empty();
    contentEl.createEl("h2", { text: this.details.forceReset ? "Confirm forced run" : "Confirm model usage" });
    if (this.details.paidDisclosure) {
      contentEl.createEl("p", {
        text: "This is the first PaperBrain run that may call paid services. Your backend configuration controls the exact providers and limits.",
      });
    }
    if (this.details.forceReset) {
      contentEl.createEl("p", {
        text: "Force resets saved state for the selected date before rerunning the requested stages.",
      });
    }
    const list = contentEl.createEl("ul");
    list.createEl("li", { text: `Provider: ${this.details.provider}` });
    list.createEl("li", { text: `Mode: ${this.details.mode}` });
    list.createEl("li", { text: `Podcast: ${this.details.podcast ? "enabled" : "disabled"}` });
    list.createEl("li", { text: "Network search: may incur usage according to backend search settings" });
    const actions = contentEl.createDiv({ cls: "modal-button-container" });
    actions.createEl("button", { text: "Cancel" }).addEventListener("click", () => this.closeWith(false));
    const confirm = actions.createEl("button", { text: this.details.forceReset ? "Reset and run" : "Continue" });
    confirm.addClass("mod-cta");
    confirm.addEventListener("click", () => this.closeWith(true));
    requestAnimationFrame(() => confirm.focus());
  }

  closeWith(value) {
    if (this.resolve) this.resolve(value);
    this.resolve = null;
    this.close();
  }

  onClose() {
    this.contentEl.empty();
    if (this.resolve) this.resolve(false);
    this.resolve = null;
  }
}

function confirmRun(app, details) {
  return new Promise((resolve) => new RunConfirmationModal(app, details, resolve).open());
}

class BackendInstallConfirmationModal extends Modal {
  constructor(app, details, resolve) {
    super(app);
    this.details = details;
    this.resolve = resolve;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.empty();
    contentEl.createEl("h2", { text: `Install PaperBrain backend ${this.details.release.version}` });
    contentEl.createEl("p", {
      text: "PaperBrain will make the following local and network changes only after you continue:",
    });
    const list = contentEl.createEl("ul");
    if (this.details.condaPath) {
      list.createEl("li", { text: `Reuse the detected Conda installation: ${this.details.condaPath}.` });
    } else {
      const sizeMiB = Math.ceil(this.details.miniforgeAsset.size / 1024 / 1024);
      list.createEl("li", {
        text: `No Conda installation was found. Download verified Miniforge ${this.details.miniforgeRelease.version} (${sizeMiB} MiB) from conda-forge.`,
      });
      list.createEl("li", {
        text: `Install it privately under ${this.details.managedRuntimePath} without changing PATH or registering system Python.`,
      });
    }
    list.createEl("li", { text: "Create wd with Python 3.10 when absent, or reuse an existing wd only when it already has Python 3.9 or later and pip 24 or later." });
    list.createEl("li", { text: "An incompatible existing wd is never changed automatically; installation stops before backend files are downloaded." });
    list.createEl("li", { text: "Download the fixed wheel and locked dependency file from the PaperBrain GitHub Release." });
    list.createEl("li", { text: "Verify both downloads with embedded SHA-256 checksums before execution." });
    if (this.details.dependencyIndex.id === "auto") {
      list.createEl("li", { text: "Download and hash-check one fixed 1.6 MB probe wheel from official PyPI, Alibaba Cloud, USTC, and Tsinghua TUNA, then select the fastest working source." });
      list.createEl("li", { text: "Install all exact hash-locked dependencies from that one selected source into wd; sources are never mixed." });
    } else {
      list.createEl("li", { text: `Install exact hash-locked dependencies from ${this.details.dependencyIndex.label} (${this.details.dependencyIndex.url}) into wd; this may take several minutes.` });
    }
    list.createEl("li", { text: `Create configuration under ${this.details.configDir}; existing .env content is preserved.` });
    list.createEl("li", { text: `Write generated papers only to the active vault: ${this.details.vaultPath}.` });
    contentEl.createEl("p", {
      cls: "paperbrain-muted",
      text: "No API key is requested or stored by the plugin. You will add it to the local .env file after installation.",
    });
    const actions = contentEl.createDiv({ cls: "modal-button-container" });
    actions.createEl("button", { text: "Cancel" }).addEventListener("click", () => this.closeWith(false));
    const confirm = actions.createEl("button", { text: "Install backend" });
    confirm.addClass("mod-cta");
    confirm.addEventListener("click", () => this.closeWith(true));
    requestAnimationFrame(() => confirm.focus());
  }

  closeWith(value) {
    if (this.resolve) this.resolve(value);
    this.resolve = null;
    this.close();
  }

  onClose() {
    this.contentEl.empty();
    if (this.resolve) this.resolve(false);
    this.resolve = null;
  }
}

function confirmBackendInstall(app, details) {
  return new Promise((resolve) => new BackendInstallConfirmationModal(app, details, resolve).open());
}

class ManualBackendInstallModal extends Modal {
  constructor(app, details) {
    super(app);
    this.details = details;
    this.selectedPlatform = details.selectedPlatform;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.empty();
    contentEl.createEl("h2", { text: `Install PaperBrain backend ${this.details.backendVersion} in a terminal` });
    contentEl.createEl("p", {
      text: "Recommended: run the verified command in your own terminal so downloads inherit that shell's proxy and network environment. The command reuses Conda when available, otherwise installs private Miniforge, then creates or reuses wd.",
    });
    const platformField = contentEl.createDiv({ cls: "paperbrain-manual-install-field" });
    platformField.createEl("label", { text: "Operating system", attr: { for: "paperbrain-manual-platform" } });
    const platformSelect = platformField.createEl("select", { attr: { id: "paperbrain-manual-platform" } });
    for (const platform of this.details.platforms) {
      const option = platformSelect.createEl("option", { value: platform.id, text: platform.label });
      option.selected = platform.id === this.selectedPlatform;
    }
    const sourceText = this.details.dependencyIndex.id === "auto"
      ? "Auto source selection will download and hash-check the same pinned probe wheel from all four configured indexes, then use the fastest valid source."
      : `Dependencies will use ${this.details.dependencyIndex.label} (${this.details.dependencyIndex.url}).`;
    contentEl.createEl("p", { cls: "paperbrain-muted", text: sourceText });
    const commandArea = contentEl.createEl("textarea", {
      cls: "paperbrain-manual-install-command",
      attr: { "aria-label": "Backend terminal installation command", rows: "9", spellcheck: "false" },
    });
    commandArea.readOnly = true;
    const renderCommand = () => {
      commandArea.value = this.details.commands[this.selectedPlatform];
      commandArea.scrollTop = 0;
    };
    platformSelect.addEventListener("change", () => {
      this.selectedPlatform = platformSelect.value;
      renderCommand();
    });
    renderCommand();
    contentEl.createEl("p", {
      cls: "paperbrain-muted",
      text: "After the command completes, return to PaperBrain and select Detect again. Installer files are downloaded from the matching plugin Release and verified before execution.",
    });
    const actions = contentEl.createDiv({ cls: "modal-button-container" });
    actions.createEl("button", { text: "Close" }).addEventListener("click", () => this.close());
    const copyButton = actions.createEl("button", { text: "Copy command" });
    copyButton.addClass("mod-cta");
    copyButton.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(commandArea.value);
        new Notice("PaperBrain terminal installation command copied.");
      } catch (error) {
        new Notice(`Could not copy the command: ${error.message}`, 8000);
      }
    });
    requestAnimationFrame(() => copyButton.focus());
  }

  onClose() {
    this.contentEl.empty();
  }
}

function execFileText(executable, args) {
  return new Promise((resolve, reject) => {
    childProcess.execFile(executable, args, { windowsHide: true, encoding: "utf8", maxBuffer: 1024 * 1024 }, (error, stdout) => {
      if (error) reject(error);
      else resolve(stdout || "");
    });
  });
}

function execFileResult(executable, args, options = {}) {
  return new Promise((resolve, reject) => {
    try {
      childProcess.execFile(
        executable,
        args,
        { windowsHide: true, encoding: "utf8", maxBuffer: 1024 * 1024, ...options },
        (error, stdout, stderr) => resolve({ error, stdout: stdout || "", stderr: stderr || "" }),
      );
    } catch (error) {
      reject(error);
    }
  });
}

function parseDateUtc(dateText) {
  const match = textValue(dateText).match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (!match) return parseDateUtc(yesterday());
  return new Date(Date.UTC(Number(match[1]), Number(match[2]) - 1, Number(match[3])));
}

function formatDateUtc(date) {
  return date.toISOString().slice(0, 10);
}

function briefPeriod(mode, dateText) {
  const anchor = parseDateUtc(dateText);
  if (mode === "month") {
    const start = new Date(Date.UTC(anchor.getUTCFullYear(), anchor.getUTCMonth(), 1));
    const end = new Date(Date.UTC(anchor.getUTCFullYear(), anchor.getUTCMonth() + 1, 0));
    return {
      type: "month",
      label: formatDateUtc(start).slice(0, 7),
      start: formatDateUtc(start),
      end: formatDateUtc(end),
      days: dateRange(formatDateUtc(start), formatDateUtc(end)).length,
    };
  }
  const day = anchor.getUTCDay() || 7;
  const start = new Date(anchor);
  start.setUTCDate(anchor.getUTCDate() - day + 1);
  const end = new Date(start);
  end.setUTCDate(start.getUTCDate() + 6);
  const thursday = new Date(start);
  thursday.setUTCDate(start.getUTCDate() + 3);
  const yearStart = new Date(Date.UTC(thursday.getUTCFullYear(), 0, 1));
  const week = Math.ceil((((thursday - yearStart) / 86400000) + 1) / 7);
  return {
    type: "week",
    label: `${thursday.getUTCFullYear()}-W${String(week).padStart(2, "0")}`,
    start: formatDateUtc(start),
    end: formatDateUtc(end),
    days: 7,
  };
}

function dateRange(startDate, endDate) {
  const dates = [];
  const current = parseDateUtc(startDate);
  const end = parseDateUtc(endDate);
  while (current <= end) {
    dates.push(formatDateUtc(current));
    current.setUTCDate(current.getUTCDate() + 1);
  }
  return dates;
}

function digestField(text, label) {
  const pattern = new RegExp(`-\\s+\\*\\*[^*\\n]*${label}\\*\\*:\\s*([\\s\\S]*?)(?=\\n-\\s+\\*\\*|\\n---|$)`, "i");
  const match = String(text || "").match(pattern);
  return match ? match[1].replace(/\s+/g, " ").trim() : "";
}

function cleanDigestTitle(title) {
  return textValue(title).replace(/^[^\w]+/u, "").trim();
}

function firstUrl(text) {
  const match = textValue(text).match(/https?:\/\/[^)\s]+/);
  return match ? match[0] : "";
}

function number(value) {
  const n = Number(value);
  return Number.isFinite(n) ? n : 0;
}

function formatScore(value) {
  return number(value).toFixed(1);
}

function hasNumericValue(value) {
  const n = Number(value);
  return Number.isFinite(n);
}

function queueScoreValue(paper) {
  if (hasNumericValue(paper.score)) return number(paper.score);
  if (hasNumericValue(paper.coarse_score)) return number(paper.coarse_score);
  return 0;
}

function formatQueueScore(paper) {
  if (hasNumericValue(paper.score)) return formatScore(paper.score);
  if (hasNumericValue(paper.coarse_score)) return `${formatScore(paper.coarse_score)}c`;
  return "new";
}

function qualityMetricValue(paper, key) {
  if (hasNumericValue(paper[key])) return number(paper[key]);
  const fallback = {
    relevance: "coarse_relevance",
    rigor: "coarse_method_completeness",
    evidence: "coarse_evidence",
  }[key];
  return fallback && hasNumericValue(paper[fallback]) ? number(paper[fallback]) : 0;
}

function paperStageHint(paper) {
  if (paper.selected_for_deep_analysis) return "deep";
  if (paper.in_daily_digest) return "digest";
  if (hasNumericValue(paper.score)) return "screened";
  if (hasNumericValue(paper.coarse_score)) return paper.should_rescreen ? "coarse / stage2" : "coarse";
  return textValue(paper.source) || "fetched";
}

function textValue(value) {
  return typeof value === "string" ? value.trim() : "";
}

function extractArxivId(value) {
  const match = textValue(value).match(/(\d{4}\.\d{4,5})(?:v\d+)?/);
  return match ? match[1] : "";
}

function presetById(id) {
  return PRESETS.find((item) => item.id === id) || PRESETS[0];
}

function normalizeStageForUi(stage) {
  const value = textValue(stage);
  return stageAlias(value) || value || "idle";
}

function stageAlias(stage) {
  const value = textValue(stage);
  if (value === "fetched") return "fetch";
  if (value === "coarse_screened") return "coarse";
  if (value === "screened") return "screen";
  if (value === "deep_analyzed") return "deep";
  if (value === "digest_written") return "digest";
  if (STAGES.includes(value)) return value;
  return "";
}

function stageIndex(stage) {
  const value = normalizeStageForUi(stage);
  return STAGE_TO_INDEX[value] ?? -1;
}

function isTerminalStage(stage) {
  return ["completed", "failed", "cancelled"].includes(textValue(stage));
}

function titleCase(value) {
  const text = textValue(value);
  return text ? text.charAt(0).toUpperCase() + text.slice(1) : "";
}

function optionLabel(value) {
  const labels = { openrouter: "OpenRouter", doubao: "Doubao", week: "Week", month: "Month" };
  return labels[value] || titleCase(value);
}

function eventLabel(log) {
  return textValue(log.event_type || "log").replace(/_/g, " ");
}

function logText(log) {
  if (!log) return "";
  return `${log.message || ""} ${log.title || ""}`.trim() || eventLabel(log);
}

function lastNonEmptyLine(text) {
  const lines = String(text || "").split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  return lines.length ? lines[lines.length - 1] : "";
}

function inferStageFromOutput(text) {
  const value = String(text || "");
  for (const hint of OUTPUT_STAGE_HINTS) {
    if (hint.pattern.test(value)) return hint.stage;
  }
  return "";
}
