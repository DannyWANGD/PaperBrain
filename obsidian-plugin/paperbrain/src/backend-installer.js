"use strict";

const crypto = require("crypto");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { backendAssetUrl } = require("./backend-release");
const { miniforgeAssetUrl } = require("./miniforge-release");
const { boundedAppend, cliExecutableForEnv, parseCondaEnvironmentList, parsePayload, pythonExecutableForEnv } = require("./runtime");

class BackendInstaller {
  constructor(options = {}) {
    this.spawn = options.spawn;
    this.download = options.download;
    this.fs = options.fs || fs.promises;
    this.platform = options.platform || process.platform;
    this.arch = options.arch || process.arch;
    this.path = options.pathApi || path;
    this.os = options.osApi || os;
    this.now = options.now || Date.now;
    this.listeners = new Set();
    this.child = null;
    this.commandEnv = null;
    this.downloadOptions = null;
    this.disposed = false;
    this.state = this.emptyState();
  }

  emptyState() {
    return {
      running: false,
      stopping: false,
      stage: "idle",
      logs: "",
      error: "",
      result: null,
    };
  }

  snapshot() {
    return { ...this.state, result: this.state.result ? { ...this.state.result } : null };
  }

  subscribe(listener) {
    this.listeners.add(listener);
    listener(this.snapshot(), "attach");
    return () => this.listeners.delete(listener);
  }

  emit(event) {
    const snapshot = this.snapshot();
    for (const listener of this.listeners) listener(snapshot, event);
  }

  setStage(stage, message) {
    this.state.stage = stage;
    if (message) this.appendLog(message, false);
    this.emit("stage");
  }

  appendLog(message, emit = true) {
    const line = String(message || "").trimEnd();
    if (!line) return;
    this.state.logs = boundedAppend(this.state.logs, `${this.state.logs ? "\n" : ""}${line}`, 200000);
    if (emit) this.emit("output");
  }

  async install(plan) {
    if (this.disposed) return { ok: false, reason: "disposed" };
    if (this.state.running) return { ok: false, reason: "already-running" };
    this.state = { ...this.emptyState(), running: true, stage: "starting" };
    this.emit("started");
    let tempDir = "";
    const installContext = { managedRootCreated: false, managedRuntimeReady: false };
    try {
      this.validatePlan(plan);
      this.commandEnv = { ...(plan.environment || process.env) };
      this.downloadOptions = {
        proxyMode: plan.proxyMode || "inherit",
        proxyUrl: plan.proxyUrl || "",
        env: this.commandEnv,
      };
      tempDir = await this.fs.mkdtemp(this.path.join(this.os.tmpdir(), "paperbrain-installer-"));
      const conda = await this.ensureConda(plan, tempDir, installContext);
      this.setStage("detecting", "Checking the selected Conda installation for a wd environment.");
      const managedEnvRoot = conda.managed ? plan.miniforge.installDir : "";
      let envPath = await this.findWdEnvironment(conda.executable, managedEnvRoot);
      if (!envPath) {
        this.setStage("environment", "Creating the isolated Conda environment wd with Python 3.10.");
        const destination = conda.managed
          ? ["--prefix", this.path.join(plan.miniforge.installDir, "envs", "wd")]
          : ["--name", "wd"];
        await this.runCommand(conda.executable, [
          "create", "--yes", ...destination,
          "--override-channels", "--channel", "https://conda.anaconda.org/conda-forge", "python=3.10", "pip>=24",
        ]);
        envPath = await this.findWdEnvironment(conda.executable, managedEnvRoot);
      } else {
        this.appendLog(`Reusing existing wd environment: ${envPath}`);
      }
      if (!envPath) throw new Error("Conda did not report a wd environment after creation.");

      const pythonPath = pythonExecutableForEnv(envPath, this.platform, this.path);
      const cliPath = cliExecutableForEnv(envPath, this.platform, this.path);
      await this.validateWdRuntime(pythonPath);
      const downloaded = {};
      for (const [key, asset] of Object.entries(plan.release.assets)) {
        this.setStage("download", `Downloading ${asset.name} from the fixed PaperBrain ${plan.release.version} release.`);
        const target = await this.downloadVerifiedAsset(backendAssetUrl(asset, plan.release), asset, tempDir);
        downloaded[key] = target;
      }

      const dependencyIndex = await this.selectDependencyIndex(plan, pythonPath, tempDir);
      this.setStage("dependencies", `Installing locked Python dependencies from ${dependencyIndex.label} into wd.`);
      await this.runCommand(pythonPath, [
        "-m", "pip", "install", "--disable-pip-version-check",
        "--index-url", dependencyIndex.url, "--require-hashes", "-r", downloaded.requirements,
      ]);
      this.setStage("backend", `Installing PaperBrain backend ${plan.release.version} into wd.`);
      await this.runCommand(pythonPath, [
        "-m", "pip", "install", "--disable-pip-version-check", "--no-deps", "--force-reinstall", downloaded.wheel,
      ]);
      this.setStage("configuration", "Creating the user-owned configuration without overwriting an existing .env file.");
      const bootstrap = await this.runCommand(cliPath, ["bootstrap", "--config-dir", plan.configDir, "--vault", plan.vaultPath]);
      const payload = parsePayload(bootstrap.stdout);
      if (!payload || payload.ok !== true || payload.command !== "bootstrap") {
        throw new Error("The installed backend did not return a valid bootstrap result.");
      }

      this.state.result = {
        ok: true,
        version: plan.release.version,
        envPath,
        pythonPath,
        cliPath,
        condaPath: conda.executable,
        condaManaged: conda.managed,
        managedRuntimePath: conda.managed ? plan.miniforge.installDir : "",
        dependencySource: dependencyIndex.id,
        dependencyIndexUrl: dependencyIndex.url,
        configPath: payload.config_path,
        envFilePath: payload.env_path,
      };
      this.state.stage = "completed";
      this.appendLog("PaperBrain backend installation completed.", false);
      return this.state.result;
    } catch (error) {
      this.state.error = error && error.message ? error.message : String(error);
      this.state.stage = this.state.stopping ? "cancelled" : "failed";
      this.appendLog(`Installation ${this.state.stopping ? "cancelled" : "failed"}: ${this.state.error}`, false);
      return { ok: false, reason: this.state.stopping ? "cancelled" : "failed", error: this.state.error };
    } finally {
      this.child = null;
      if (installContext.managedRootCreated && !installContext.managedRuntimeReady) {
        try {
          await this.fs.rm(plan.miniforge.installDir, { recursive: true, force: true });
          await this.fs.rm(`${plan.miniforge.installDir}.paperbrain-installing`, { force: true });
          this.appendLog("Removed the incomplete managed Miniforge installation.", false);
        } catch (error) {
          this.appendLog(`Incomplete runtime cleanup failed: ${error.message}`, false);
        }
      }
      if (tempDir) {
        try {
          await this.fs.rm(tempDir, { recursive: true, force: true });
        } catch (error) {
          this.appendLog(`Temporary installer cleanup failed: ${error.message}`, false);
        }
      }
      this.state.running = false;
      this.state.stopping = false;
      this.commandEnv = null;
      this.downloadOptions = null;
      this.emit("finished");
    }
  }

  validatePlan(plan) {
    if (!plan || !plan.release || !plan.configDir || !plan.vaultPath) {
      throw new Error("The backend installation plan is incomplete.");
    }
    for (const asset of Object.values(plan.release.assets || {})) {
      if (!asset.name || !/^[a-f0-9]{64}$/.test(asset.sha256 || "")) {
        throw new Error(`The backend release manifest is incomplete for ${asset.name || "an asset"}.`);
      }
    }
    const dependencyIndex = plan.dependencyIndex || {};
    if (dependencyIndex.id === "auto") {
      const candidates = Array.isArray(dependencyIndex.candidates) ? dependencyIndex.candidates : [];
      const probe = plan.release.dependencyProbe || {};
      if (candidates.length < 2 || candidates.some((index) => !index.id || !index.label || !validDependencyIndexUrl(index.url))) {
        throw new Error("The automatic dependency source candidates are invalid.");
      }
      if (!/^[A-Za-z0-9][A-Za-z0-9._-]*==[A-Za-z0-9][A-Za-z0-9._+-]*$/.test(probe.requirement || "")
          || !/^[a-f0-9]{64}$/.test(probe.sha256 || "")) {
        throw new Error("The automatic dependency source probe is not pinned and checksummed.");
      }
    } else if (!dependencyIndex.id || !dependencyIndex.label || !validDependencyIndexUrl(dependencyIndex.url)) {
      throw new Error("The dependency download source is invalid. Choose a credential-free HTTPS mirror ending in /simple.");
    }
    if (!plan.condaExecutable) {
      const miniforge = plan.miniforge || {};
      const asset = miniforge.asset || {};
      if (!miniforge.release || !miniforge.installDir || !asset.name || !/^[a-f0-9]{64}$/.test(asset.sha256 || "")) {
        throw new Error(`Automatic Miniforge installation is not available for ${this.platform}/${this.arch}.`);
      }
    }
  }

  async ensureConda(plan, tempDir, context) {
    if (plan.condaExecutable) {
      this.setStage("runtime", `Using the detected Conda executable: ${plan.condaExecutable}`);
      await this.runCommand(plan.condaExecutable, ["--version"]);
      return { executable: plan.condaExecutable, managed: false };
    }

    const root = plan.miniforge.installDir;
    const executable = managedCondaExecutable(root, this.platform, this.path);
    if (await this.exists(executable)) {
      this.setStage("runtime", `Reusing PaperBrain-managed Miniforge at ${root}.`);
      await this.runCommand(executable, ["--version"]);
      return { executable, managed: true };
    }

    const installingMarker = `${root}.paperbrain-installing`;
    const managedMarker = this.path.join(root, ".paperbrain-managed.json");
    const interruptedInstall = await this.exists(installingMarker);
    if (await this.exists(root)) {
      if (interruptedInstall || await this.exists(managedMarker)) {
        this.setStage("runtime", "Removing an incomplete PaperBrain-managed Miniforge runtime before retrying.");
        await this.fs.rm(root, { recursive: true, force: true });
        await this.fs.rm(installingMarker, { force: true });
      } else {
        throw new Error(`The managed runtime directory already exists but is not owned by PaperBrain: ${root}`);
      }
    } else if (interruptedInstall) {
      await this.fs.rm(installingMarker, { force: true });
    }

    context.managedRootCreated = true;
    await this.fs.mkdir(this.path.dirname(root), { recursive: true });
    await this.fs.writeFile(installingMarker, "PaperBrain managed installation in progress\n", { flag: "wx" });
    const asset = plan.miniforge.asset;
    this.setStage("runtime", `No Conda installation was found. Downloading verified Miniforge ${plan.miniforge.release.version}.`);
    const installer = await this.downloadVerifiedAsset(
      miniforgeAssetUrl(asset, plan.miniforge.release), asset, tempDir,
    );
    this.setStage("runtime", "Installing Miniforge in PaperBrain's private runtime directory without changing PATH.");
    if (this.platform === "win32") {
      await this.runCommand(installer, [
        "/InstallationType=JustMe",
        "/RegisterPython=0",
        "/S",
        `/D=${root}`,
      ]);
    } else {
      await this.runCommand("/bin/bash", [installer, "-b", "-p", root]);
    }
    if (!await this.exists(executable)) throw new Error("Miniforge installation completed without a usable Conda executable.");
    await this.runCommand(executable, ["--version"]);
    await this.fs.rm(installingMarker, { force: true });
    await this.fs.writeFile(managedMarker, JSON.stringify({
      owner: "PaperBrain",
      miniforgeVersion: plan.miniforge.release.version,
      platform: this.platform,
      arch: this.arch,
    }, null, 2));
    context.managedRuntimeReady = true;
    this.appendLog(`Miniforge ${plan.miniforge.release.version} is ready at ${root}.`);
    return { executable, managed: true };
  }

  async downloadVerifiedAsset(url, asset, tempDir) {
    const bytes = await this.download(url, this.downloadOptions || {});
    const actual = crypto.createHash("sha256").update(bytes).digest("hex");
    if (actual !== asset.sha256) throw new Error(`SHA-256 verification failed for ${asset.name}.`);
    const target = this.path.join(tempDir, asset.name);
    await this.fs.writeFile(target, bytes, { flag: "wx" });
    this.appendLog(`Verified ${asset.name}: ${actual}`);
    return target;
  }

  async exists(target) {
    try {
      await this.fs.access(target);
      return true;
    } catch (_) {
      return false;
    }
  }

  async findWdEnvironment(condaExecutable, requiredRoot = "") {
    const result = await this.runCommand(condaExecutable, ["env", "list", "--json"]);
    return parseCondaEnvironmentList(result.stdout)
      .find((entry) => this.path.basename(entry).toLowerCase() === "wd" && this.isWithinRoot(entry, requiredRoot)) || "";
  }

  async selectDependencyIndex(plan, pythonPath, tempDir) {
    if (plan.dependencyIndex.id !== "auto") return plan.dependencyIndex;
    const successful = [];
    for (const candidate of plan.dependencyIndex.candidates) {
      this.setStage("source-probe", `Testing an actual package download from ${candidate.label}.`);
      const started = this.now();
      try {
        await this.probeDependencyIndex(pythonPath, candidate, plan.release.dependencyProbe, tempDir);
        const elapsedMs = Math.max(1, this.now() - started);
        successful.push({ ...candidate, elapsedMs });
        this.appendLog(`${candidate.label} probe passed in ${elapsedMs} ms.`);
      } catch (error) {
        if (this.state.stopping) throw error;
        this.appendLog(`${candidate.label} probe failed: ${error.message}`);
      }
    }
    if (!successful.length) {
      throw new Error("No dependency source passed the real package download and SHA-256 probe. Choose a working source in settings and retry.");
    }
    successful.sort((left, right) => left.elapsedMs - right.elapsedMs);
    const selected = successful[0];
    this.appendLog(`Selected ${selected.label} (${selected.elapsedMs} ms) for the hash-locked dependency installation.`);
    return selected;
  }

  async probeDependencyIndex(pythonPath, candidate, probe, tempDir) {
    const probeDir = this.path.join(tempDir, `source-probe-${candidate.id}`);
    await this.fs.mkdir(probeDir, { recursive: true });
    await this.runCommand(pythonPath, [
      "-m", "pip", "download", "--disable-pip-version-check", "--no-deps",
      "--only-binary=:all:", "--no-cache-dir", "--timeout", "20", "--retries", "1",
      "--dest", probeDir, "--index-url", candidate.url, probe.requirement,
    ]);
    const files = await this.fs.readdir(probeDir);
    if (files.length !== 1) throw new Error("The source probe did not produce exactly one wheel.");
    const bytes = await this.fs.readFile(this.path.join(probeDir, files[0]));
    const actual = crypto.createHash("sha256").update(bytes).digest("hex");
    if (actual !== probe.sha256) throw new Error("The source probe wheel failed SHA-256 verification.");
  }

  async validateWdRuntime(pythonPath) {
    this.setStage("environment", "Checking that wd uses a compatible Python and pip before downloading backend files.");
    const code = [
      "import json, sys",
      "import pip",
      "print(json.dumps({'python': [sys.version_info.major, sys.version_info.minor, sys.version_info.micro], 'pip': pip.__version__}))",
    ].join("; ");
    const result = await this.runCommand(pythonPath, ["-c", code]);
    const payload = parsePayload(result.stdout);
    if (!payload || !Array.isArray(payload.python) || typeof payload.pip !== "string") {
      throw new Error("Could not determine the Python and pip versions in wd. No backend files were downloaded.");
    }
    const pythonVersion = payload.python.map((part) => Number(part) || 0);
    const pythonText = pythonVersion.join(".");
    if (compareVersion(pythonVersion, [3, 9, 0]) < 0) {
      throw new Error(`Existing wd uses Python ${pythonText}. PaperBrain requires Python 3.9 or later. The installer did not modify wd or download backend files. Upgrade or recreate wd yourself, then retry.`);
    }
    if (compareVersion(parseVersion(payload.pip), [24, 0, 0]) < 0) {
      throw new Error(`Existing wd uses pip ${payload.pip}. PaperBrain requires pip 24 or later. The installer did not modify wd or download backend files. Upgrade pip in wd yourself, then retry.`);
    }
    this.appendLog(`Compatible wd runtime detected: Python ${pythonText}, pip ${payload.pip}.`);
  }

  isWithinRoot(target, requiredRoot) {
    if (!requiredRoot) return true;
    const relative = this.path.relative(this.path.resolve(requiredRoot), this.path.resolve(target));
    return relative !== "" && relative !== ".." && !relative.startsWith(`..${this.path.sep}`) && !this.path.isAbsolute(relative);
  }

  runCommand(executable, args) {
    if (this.state.stopping) return Promise.reject(new Error("Installation cancelled."));
    this.appendLog(`$ ${executable} ${args.join(" ")}`);
    return new Promise((resolve, reject) => {
      let stdout = "";
      let stderr = "";
      let settled = false;
      const child = this.spawn(executable, args, {
        windowsHide: true,
        env: { ...(this.commandEnv || process.env) },
      });
      this.child = child;
      child.stdout.on("data", (data) => {
        const text = String(data);
        stdout = boundedAppend(stdout, text);
        this.appendLog(text.trimEnd());
      });
      child.stderr.on("data", (data) => {
        const text = String(data);
        stderr = boundedAppend(stderr, text);
        this.appendLog(text.trimEnd());
      });
      child.once("error", (error) => {
        if (settled) return;
        settled = true;
        if (this.child === child) this.child = null;
        reject(error);
      });
      child.once("close", (code, signal) => {
        if (settled) return;
        settled = true;
        if (this.child === child) this.child = null;
        if (code === 0 && !signal) resolve({ stdout, stderr });
        else reject(new Error(lastLine(stderr) || `${executable} exited with ${signal || code}.`));
      });
    });
  }

  stop() {
    if (!this.state.running || this.state.stopping) return false;
    this.state.stopping = true;
    this.emit("stopping");
    if (this.child) this.child.kill();
    return true;
  }

  dispose() {
    this.disposed = true;
    this.state.stopping = true;
    if (this.child) this.child.kill();
    this.child = null;
    this.listeners.clear();
  }
}

function managedCondaExecutable(root, platform = process.platform, pathApi = path) {
  return platform === "win32"
    ? pathApi.join(root, "Scripts", "conda.exe")
    : pathApi.join(root, "bin", "conda");
}

function lastLine(value) {
  return String(value || "").split(/\r?\n/).map((line) => line.trim()).filter(Boolean).at(-1) || "";
}

function parseVersion(value) {
  return String(value || "").split(".").slice(0, 3).map((part) => Number.parseInt(part, 10) || 0);
}

function compareVersion(left, right) {
  for (let index = 0; index < Math.max(left.length, right.length); index += 1) {
    const difference = (left[index] || 0) - (right[index] || 0);
    if (difference) return difference;
  }
  return 0;
}

function validDependencyIndexUrl(value) {
  try {
    const parsed = new URL(String(value || ""));
    return parsed.protocol === "https:"
      && !parsed.username && !parsed.password && !parsed.search && !parsed.hash
      && /\/simple\/?$/i.test(parsed.pathname);
  } catch (_) {
    return false;
  }
}

module.exports = { BackendInstaller, compareVersion, managedCondaExecutable, validDependencyIndexUrl };
