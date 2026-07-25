"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const { EventEmitter } = require("node:events");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");

const { BackendInstaller, managedCondaExecutable } = require("../src/backend-installer");
const { MINIFORGE_RELEASE, resolveMiniforgeAsset } = require("../src/miniforge-release");

function sha(bytes) {
  return crypto.createHash("sha256").update(bytes).digest("hex");
}

function fixtureRelease(wheel, requirements, probe = Buffer.from("probe-wheel")) {
  return {
    repository: "example/PaperBrain",
    version: "0.3.7",
    tag: "backend-0.3.7",
    dependencyProbe: { requirement: "probe-package==1.0.0", sha256: sha(probe) },
    assets: {
      wheel: { name: "paperbrain-0.3.7-py3-none-any.whl", sha256: sha(wheel) },
      requirements: { name: "requirements.lock", sha256: sha(requirements) },
    },
  };
}

const TUNA_INDEX = Object.freeze({
  id: "tuna",
  label: "Tsinghua TUNA",
  url: "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple",
});
const PYPI_INDEX = Object.freeze({
  id: "pypi",
  label: "Official PyPI",
  url: "https://pypi.org/simple",
});
const ALIYUN_INDEX = Object.freeze({
  id: "aliyun",
  label: "Alibaba Cloud",
  url: "https://mirrors.aliyun.com/pypi/simple",
});
const USTC_INDEX = Object.freeze({
  id: "ustc",
  label: "USTC",
  url: "https://mirrors.ustc.edu.cn/pypi/simple",
});
const AUTO_INDEX = Object.freeze({
  id: "auto",
  label: "Automatic (fastest available)",
  candidates: [PYPI_INDEX, ALIYUN_INDEX, USTC_INDEX, TUNA_INDEX],
});

function compatibleRuntime(python = [3, 10, 14], pip = "24.3.1") {
  return JSON.stringify({ python, pip });
}

function completedChild(stdout = "", stderr = "", onStart = () => {}) {
  const child = new EventEmitter();
  child.stdout = new EventEmitter();
  child.stderr = new EventEmitter();
  child.pid = 1234;
  child.kill = () => {
    process.nextTick(() => child.emit("close", null, "SIGTERM"));
    return true;
  };
  onStart();
  process.nextTick(() => {
    if (stdout) child.stdout.emit("data", Buffer.from(stdout));
    if (stderr) child.stderr.emit("data", Buffer.from(stderr));
    child.emit("close", 0, null);
  });
  return child;
}

async function temporaryRoot(t) {
  const root = await fs.promises.mkdtemp(path.join(os.tmpdir(), "paperbrain-installer-test-"));
  t.after(() => fs.promises.rm(root, { recursive: true, force: true }));
  return root;
}

test("an existing Conda installation is preferred and its Python 3.9 wd environment is reused", async (t) => {
  const root = await temporaryRoot(t);
  const wheel = Buffer.from("wheel");
  const requirements = Buffer.from("requirements");
  const release = fixtureRelease(wheel, requirements);
  const envPath = path.join(root, "existing-conda", "envs", "wd");
  const calls = [];
  const spawn = (executable, args) => {
    calls.push({ executable, args });
    if (args[0] === "--version") return completedChild("conda 26.3.1\n");
    if (args[0] === "env") return completedChild(JSON.stringify({ envs: [envPath] }));
    if (args[0] === "-c") return completedChild(compatibleRuntime([3, 9, 18]));
    if (args[0] === "bootstrap") {
      return completedChild(JSON.stringify({
        ok: true,
        command: "bootstrap",
        config_path: path.join(root, "config", "config.yaml"),
        env_path: path.join(root, "config", ".env"),
      }));
    }
    return completedChild();
  };
  const installer = new BackendInstaller({
    spawn,
    download: async (url) => url.endsWith("requirements.lock") ? requirements : wheel,
  });
  const result = await installer.install({
    condaExecutable: path.join(root, "conda"),
    configDir: path.join(root, "config"),
    vaultPath: path.join(root, "vault"),
    release,
    dependencyIndex: TUNA_INDEX,
  });

  assert.equal(result.ok, true);
  assert.equal(result.condaManaged, false);
  assert.equal(result.envPath, envPath);
  assert.equal(calls.some((call) => call.args[0] === "create"), false);
  assert.equal(calls[0].executable, path.join(root, "conda"));
  const dependencyCall = calls.find((call) => call.args[0] === "-m" && call.args[1] === "pip" && call.args.includes("--require-hashes"));
  assert.equal(dependencyCall.args[dependencyCall.args.indexOf("--index-url") + 1], TUNA_INDEX.url);
  assert.equal(dependencyCall.args.includes("--extra-index-url"), false);
});

test("automatic source selection probes real wheels and uses only the fastest verified source", async (t) => {
  const root = await temporaryRoot(t);
  const wheel = Buffer.from("wheel");
  const requirements = Buffer.from("requirements");
  const probe = Buffer.from("probe-wheel");
  const release = fixtureRelease(wheel, requirements, probe);
  const envPath = path.join(root, "existing-conda", "envs", "wd");
  const calls = [];
  const clock = [0, 210, 210, 300, 300, 345, 345, 405];
  const spawn = (executable, args) => {
    calls.push({ executable, args });
    if (args[0] === "--version") return completedChild("conda 26.3.1\n");
    if (args[0] === "env") return completedChild(JSON.stringify({ envs: [envPath] }));
    if (args[0] === "-c") return completedChild(compatibleRuntime([3, 9, 18]));
    if (args[0] === "-m" && args[1] === "pip" && args[2] === "download") {
      const destination = args[args.indexOf("--dest") + 1];
      return completedChild("", "", () => {
        fs.mkdirSync(destination, { recursive: true });
        fs.writeFileSync(path.join(destination, "probe-package-1.0.0-py3-none-any.whl"), probe);
      });
    }
    if (args[0] === "bootstrap") {
      return completedChild(JSON.stringify({
        ok: true,
        command: "bootstrap",
        config_path: path.join(root, "config", "config.yaml"),
        env_path: path.join(root, "config", ".env"),
      }));
    }
    return completedChild();
  };
  const installer = new BackendInstaller({
    spawn,
    now: () => clock.shift(),
    download: async (url) => url.endsWith("requirements.lock") ? requirements : wheel,
  });
  const result = await installer.install({
    condaExecutable: path.join(root, "conda"),
    configDir: path.join(root, "config"),
    vaultPath: path.join(root, "vault"),
    release,
    dependencyIndex: AUTO_INDEX,
  });

  assert.equal(result.ok, true);
  assert.equal(result.dependencySource, "ustc");
  assert.equal(result.dependencyIndexUrl, USTC_INDEX.url);
  const probes = calls.filter((call) => call.args[0] === "-m" && call.args[2] === "download");
  assert.equal(probes.length, 4);
  assert.equal(probes.every((call) => call.args.includes("--no-cache-dir")), true);
  assert.equal(probes.every((call) => call.args.includes("probe-package==1.0.0")), true);
  const dependencyCall = calls.find((call) => call.args[0] === "-m" && call.args[2] === "install" && call.args.includes("--require-hashes"));
  assert.equal(dependencyCall.args[dependencyCall.args.indexOf("--index-url") + 1], USTC_INDEX.url);
  assert.equal(dependencyCall.args.includes(PYPI_INDEX.url), false);
});

test("installation downloads and child processes share the selected proxy environment", async (t) => {
  const root = await temporaryRoot(t);
  const wheel = Buffer.from("wheel");
  const requirements = Buffer.from("requirements");
  const release = fixtureRelease(wheel, requirements);
  const envPath = path.join(root, "envs", "wd");
  const spawnOptions = [];
  const downloadOptions = [];
  const spawn = (executable, args, options) => {
    spawnOptions.push(options);
    if (args[0] === "--version") return completedChild("conda 26.3.1\n");
    if (args[0] === "env") return completedChild(JSON.stringify({ envs: [envPath] }));
    if (args[0] === "-c") return completedChild(compatibleRuntime([3, 9, 18]));
    if (args[0] === "bootstrap") {
      return completedChild(JSON.stringify({
        ok: true,
        command: "bootstrap",
        config_path: path.join(root, "config", "config.yaml"),
        env_path: path.join(root, "config", ".env"),
      }));
    }
    return completedChild();
  };
  const installer = new BackendInstaller({
    spawn,
    download: async (url, options) => {
      downloadOptions.push(options);
      return url.endsWith("requirements.lock") ? requirements : wheel;
    },
  });
  const environment = {
    PATH: "bin",
    HTTP_PROXY: "http://127.0.0.1:7890",
    HTTPS_PROXY: "http://127.0.0.1:7890",
  };

  const result = await installer.install({
    condaExecutable: path.join(root, "conda"),
    configDir: path.join(root, "config"),
    vaultPath: path.join(root, "vault"),
    release,
    dependencyIndex: TUNA_INDEX,
    environment,
    proxyMode: "manual",
    proxyUrl: "http://127.0.0.1:7890",
  });

  assert.equal(result.ok, true);
  assert.ok(spawnOptions.length > 0);
  assert.ok(spawnOptions.every((options) => options.env.HTTPS_PROXY === environment.HTTPS_PROXY));
  assert.equal(downloadOptions.length, 2);
  assert.ok(downloadOptions.every((options) => options.proxyMode === "manual"));
  assert.ok(downloadOptions.every((options) => options.proxyUrl === "http://127.0.0.1:7890"));
  assert.ok(downloadOptions.every((options) => options.env.HTTPS_PROXY === environment.HTTPS_PROXY));
});

test("an existing wd below Python 3.9 stops before any backend download", async (t) => {
  const root = await temporaryRoot(t);
  const envPath = path.join(root, "envs", "wd");
  let downloads = 0;
  const calls = [];
  const installer = new BackendInstaller({
    spawn: (executable, args) => {
      calls.push({ executable, args });
      if (args[0] === "--version") return completedChild("conda test\n");
      if (args[0] === "env") return completedChild(JSON.stringify({ envs: [envPath] }));
      if (args[0] === "-c") return completedChild(compatibleRuntime([3, 8, 20]));
      return completedChild();
    },
    download: async () => { downloads += 1; return Buffer.from("unexpected"); },
  });
  const result = await installer.install({
    condaExecutable: "conda",
    configDir: path.join(root, "config"),
    vaultPath: path.join(root, "vault"),
    release: fixtureRelease(Buffer.from("wheel"), Buffer.from("requirements")),
    dependencyIndex: TUNA_INDEX,
  });

  assert.equal(result.ok, false);
  assert.match(result.error, /Python 3\.8\.20/);
  assert.match(result.error, /did not modify wd or download backend files/);
  assert.equal(downloads, 0);
  assert.equal(calls.some((call) => call.args[0] === "install"), false);
  assert.equal(calls.some((call) => call.args[0] === "create"), false);
});

test("missing Conda installs verified Miniforge privately before creating wd", async (t) => {
  const root = await temporaryRoot(t);
  const managedRoot = path.join(root, "runtime", "miniforge3");
  const envPath = path.join(managedRoot, "envs", "wd");
  const externalWd = path.join(root, "external-conda", "envs", "wd");
  const wheel = Buffer.from("wheel");
  const requirements = Buffer.from("requirements");
  const miniforge = Buffer.from("miniforge-installer");
  const release = fixtureRelease(wheel, requirements);
  const miniforgeRelease = {
    repository: "conda-forge/miniforge",
    version: "test",
    tag: "test",
    assets: {},
  };
  const asset = { name: "Miniforge3-test-Windows-x86_64.exe", sha256: sha(miniforge), size: miniforge.length };
  let wdCreated = false;
  const calls = [];
  const spawn = (executable, args) => {
    calls.push({ executable, args });
    if (String(executable).endsWith(asset.name)) {
      const installDir = args.find((value) => value.startsWith("/D=")).slice(3);
      return completedChild("", "", () => {
        fs.mkdirSync(path.dirname(managedCondaExecutable(installDir, "win32")), { recursive: true });
        fs.writeFileSync(managedCondaExecutable(installDir, "win32"), "fake conda");
      });
    }
    if (args[0] === "--version") return completedChild("conda test\n");
    if (args[0] === "env") return completedChild(JSON.stringify({ envs: wdCreated ? [externalWd, envPath] : [externalWd] }));
    if (args[0] === "create") {
      wdCreated = true;
      return completedChild();
    }
    if (args[0] === "bootstrap") {
      return completedChild(JSON.stringify({
        ok: true,
        command: "bootstrap",
        config_path: path.join(root, "config", "config.yaml"),
        env_path: path.join(root, "config", ".env"),
      }));
    }
    if (args[0] === "-c") return completedChild(compatibleRuntime());
    return completedChild();
  };
  const installer = new BackendInstaller({
    spawn,
    platform: "win32",
    arch: "x64",
    download: async (url) => {
      if (url.endsWith(asset.name)) return miniforge;
      return url.endsWith("requirements.lock") ? requirements : wheel;
    },
  });
  const result = await installer.install({
    condaExecutable: "",
    configDir: path.join(root, "config"),
    vaultPath: path.join(root, "vault"),
    release,
    dependencyIndex: TUNA_INDEX,
    miniforge: { release: miniforgeRelease, asset, installDir: managedRoot },
  });

  assert.equal(result.ok, true);
  assert.equal(result.condaManaged, true);
  assert.equal(result.condaPath, managedCondaExecutable(managedRoot, "win32"));
  assert.equal(fs.existsSync(path.join(managedRoot, ".paperbrain-managed.json")), true);
  assert.equal(fs.existsSync(`${managedRoot}.paperbrain-installing`), false);
  assert.equal(calls.some((call) => call.args[0] === "create"), true);
  const createCall = calls.find((call) => call.args[0] === "create");
  assert.deepEqual(createCall.args.slice(0, 5), ["create", "--yes", "--prefix", envPath, "--override-channels"]);
  assert.equal(createCall.args[createCall.args.indexOf("--channel") + 1], "https://conda.anaconda.org/conda-forge");
  assert.equal(createCall.args.includes("pip>=24"), true);
  assert.equal(calls.findIndex((call) => String(call.executable).endsWith(asset.name)) < calls.findIndex((call) => call.args[0] === "create"), true);
});

test("a failed checksum prevents package installation", async (t) => {
  const root = await temporaryRoot(t);
  const release = fixtureRelease(Buffer.from("expected"), Buffer.from("requirements"));
  const envPath = path.join(root, "envs", "wd");
  const calls = [];
  const installer = new BackendInstaller({
    spawn: (executable, args) => {
      calls.push({ executable, args });
      if (args[0] === "--version") return completedChild("conda test\n");
      if (args[0] === "env") return completedChild(JSON.stringify({ envs: [envPath] }));
      if (args[0] === "-c") return completedChild(compatibleRuntime());
      return completedChild();
    },
    download: async () => Buffer.from("tampered"),
  });
  const result = await installer.install({
    condaExecutable: "conda",
    configDir: path.join(root, "config"),
    vaultPath: path.join(root, "vault"),
    release,
    dependencyIndex: TUNA_INDEX,
  });

  assert.equal(result.ok, false);
  assert.match(result.error, /SHA-256 verification failed/);
  assert.equal(calls.some((call) => call.args[0] === "-m" && call.args[1] === "pip"), false);
});

test("stop during a download prevents package installation and finishes as cancelled", async (t) => {
  const root = await temporaryRoot(t);
  const wheel = Buffer.from("wheel");
  const requirements = Buffer.from("requirements");
  const release = fixtureRelease(wheel, requirements);
  const envPath = path.join(root, "envs", "wd");
  const calls = [];
  let releaseDownload;
  const downloadStarted = new Promise((resolve) => { releaseDownload = resolve; });
  let finishDownload;
  const pendingDownload = new Promise((resolve) => { finishDownload = resolve; });
  const installer = new BackendInstaller({
    spawn: (executable, args) => {
      calls.push({ executable, args });
      if (args[0] === "--version") return completedChild("conda test\n");
      if (args[0] === "env") return completedChild(JSON.stringify({ envs: [envPath] }));
      if (args[0] === "-c") return completedChild(compatibleRuntime());
      return completedChild();
    },
    download: async () => {
      releaseDownload();
      return pendingDownload;
    },
  });
  const installation = installer.install({
    condaExecutable: "conda",
    configDir: path.join(root, "config"),
    vaultPath: path.join(root, "vault"),
    release,
    dependencyIndex: TUNA_INDEX,
  });
  await downloadStarted;
  assert.equal(installer.stop(), true);
  finishDownload(wheel);
  const result = await installation;

  assert.equal(result.ok, false);
  assert.equal(result.reason, "cancelled");
  assert.equal(calls.some((call) => call.args[0] === "-m" && call.args[1] === "pip"), false);
});

test("the embedded Miniforge manifest covers supported desktop architectures", () => {
  for (const [platform, arch] of [
    ["win32", "x64"], ["darwin", "x64"], ["darwin", "arm64"], ["linux", "x64"], ["linux", "arm64"],
  ]) {
    const asset = resolveMiniforgeAsset(platform, arch, MINIFORGE_RELEASE);
    assert.ok(asset, `${platform}/${arch} should be supported`);
    assert.match(asset.sha256, /^[a-f0-9]{64}$/);
    assert.ok(asset.size > 50 * 1024 * 1024);
  }
  assert.equal(resolveMiniforgeAsset("win32", "arm64", MINIFORGE_RELEASE), null);
});
