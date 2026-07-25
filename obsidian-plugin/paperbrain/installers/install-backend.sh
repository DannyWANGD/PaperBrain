#!/usr/bin/env bash
set -Eeuo pipefail

BACKEND_VERSION="0.3.7"
BACKEND_TAG="backend-0.3.7"
BACKEND_REPOSITORY="DannyWANGD/PaperBrain"
WHEEL_NAME="paperbrain-0.3.7-py3-none-any.whl"
WHEEL_SHA256="4f9485b3a69f9217bcfa6aeacc900e02b2ac9ed2ad14d6a49fd299d082dc9ea2"
REQUIREMENTS_NAME="requirements.lock"
REQUIREMENTS_SHA256="2a7394540a7552cd1bbbb88e9c440ae3c493e25e5d30a7c8300281831d30de7c"
PROBE_REQUIREMENT="openai==2.46.0"
PROBE_SHA256="672381db55efb3a1e2610f29304c130cccdd0b319bace4d492b2443cb64c1e7c"
MINIFORGE_VERSION="26.3.2-2"
MINIFORGE_REPOSITORY="conda-forge/miniforge"

usage() {
  printf '%s\n' "Usage: bash install-backend.sh --vault <absolute-path> [--index-url auto|https://.../simple]"
}

VAULT_PATH=""
INDEX_URL="auto"
while [ "$#" -gt 0 ]; do
  case "$1" in
    --vault)
      [ "$#" -ge 2 ] || { usage >&2; exit 2; }
      VAULT_PATH="$2"
      shift 2
      ;;
    --index-url)
      [ "$#" -ge 2 ] || { usage >&2; exit 2; }
      INDEX_URL="$2"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

[ -n "$VAULT_PATH" ] || { printf 'The --vault path is required.\n' >&2; exit 2; }
[ -d "$VAULT_PATH" ] || { printf 'Vault directory does not exist: %s\n' "$VAULT_PATH" >&2; exit 2; }
if [ "$INDEX_URL" != "auto" ]; then
  case "$INDEX_URL" in
    https://*/simple|https://*/simple/) ;;
    *) printf 'The dependency index must be auto or a credential-free HTTPS URL ending in /simple.\n' >&2; exit 2 ;;
  esac
  case "$INDEX_URL" in
    *'@'*|*'?'*|*'#'*) printf 'The dependency index must not contain credentials, a query, or a fragment.\n' >&2; exit 2 ;;
  esac
fi

# BRAT can replace the plugin directory while a terminal still points at its
# old inode. Conda subprocesses need a live working directory.
cd "$HOME"

RUNTIME_ROOT="$HOME/.paperbrain/runtime/miniforge3"
CONFIG_DIR="$HOME/.paperbrain/config"
TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/paperbrain-install.XXXXXX")"
managed_runtime_incomplete=0
cleanup() {
  rm -rf "$TEMP_DIR"
  if [ "$managed_runtime_incomplete" = "1" ]; then
    rm -rf "$RUNTIME_ROOT"
  fi
}
trap cleanup EXIT

download_file() {
  local url="$1"
  local destination="$2"
  if command -v curl >/dev/null 2>&1; then
    curl --fail --location --retry 2 --connect-timeout 20 --output "$destination" "$url"
  elif command -v wget >/dev/null 2>&1; then
    wget --tries=3 --timeout=20 --output-document="$destination" "$url"
  else
    printf 'curl or wget is required.\n' >&2
    return 1
  fi
}

sha256_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    printf 'sha256sum or shasum is required.\n' >&2
    return 1
  fi
}

verify_file() {
  local file="$1"
  local expected="$2"
  local actual
  actual="$(sha256_file "$file")"
  [ "$actual" = "$expected" ] || {
    printf 'SHA-256 verification failed for %s.\n' "$(basename "$file")" >&2
    return 1
  }
}

CONDA_PATH=""
if command -v conda >/dev/null 2>&1; then
  CONDA_PATH="$(command -v conda)"
else
  for candidate in \
    "$HOME/miniforge3/bin/conda" \
    "$HOME/mambaforge/bin/conda" \
    "$HOME/anaconda3/bin/conda" \
    "$HOME/miniconda3/bin/conda" \
    "$RUNTIME_ROOT/bin/conda"; do
    if [ -x "$candidate" ]; then
      CONDA_PATH="$candidate"
      break
    fi
  done
fi

if [ -z "$CONDA_PATH" ]; then
  os_name="$(uname -s)"
  arch_name="$(uname -m)"
  case "$os_name/$arch_name" in
    Darwin/x86_64)
      miniforge_name="Miniforge3-26.3.2-2-MacOSX-x86_64.sh"
      miniforge_sha256="a755192103de19bb2782685ac78820c2e00702e5f33e6e4f0a3bf3c214f45d69"
      ;;
    Darwin/arm64)
      miniforge_name="Miniforge3-26.3.2-2-MacOSX-arm64.sh"
      miniforge_sha256="2657d94152343cff7c06159ac9fc09624d7879fa9575c5a0a324c571c4df0ade"
      ;;
    Linux/x86_64)
      miniforge_name="Miniforge3-26.3.2-2-Linux-x86_64.sh"
      miniforge_sha256="42260ffe3830fb953d5eee1bbb32229ff06aa7c3833c1ed7a9a0420a95685d94"
      ;;
    Linux/aarch64|Linux/arm64)
      miniforge_name="Miniforge3-26.3.2-2-Linux-aarch64.sh"
      miniforge_sha256="f4096a92482b30f04534cddb63d8bc929118318deffac71d90fb89dc52359d22"
      ;;
    *)
      printf 'Automatic Miniforge installation is unavailable for %s/%s.\n' "$os_name" "$arch_name" >&2
      exit 1
      ;;
  esac
  if [ -e "$RUNTIME_ROOT" ]; then
    printf 'The managed runtime path exists but does not contain Conda: %s\n' "$RUNTIME_ROOT" >&2
    exit 1
  fi
  miniforge_installer="$TEMP_DIR/$miniforge_name"
  miniforge_url="https://github.com/$MINIFORGE_REPOSITORY/releases/download/$MINIFORGE_VERSION/$miniforge_name"
  printf 'Downloading Miniforge %s...\n' "$MINIFORGE_VERSION"
  download_file "$miniforge_url" "$miniforge_installer"
  verify_file "$miniforge_installer" "$miniforge_sha256"
  mkdir -p "$(dirname "$RUNTIME_ROOT")"
  managed_runtime_incomplete=1
  bash "$miniforge_installer" -b -p "$RUNTIME_ROOT"
  CONDA_PATH="$RUNTIME_ROOT/bin/conda"
  "$CONDA_PATH" --version
  printf '{\n  "owner": "PaperBrain",\n  "miniforgeVersion": "%s",\n  "platform": "%s",\n  "arch": "%s"\n}\n' \
    "$MINIFORGE_VERSION" "$os_name" "$arch_name" > "$RUNTIME_ROOT/.paperbrain-managed.json"
  managed_runtime_incomplete=0
fi

"$CONDA_PATH" --version
env_list="$TEMP_DIR/conda-envs.json"
find_wd_environment() {
  local base_root
  local base_python
  "$CONDA_PATH" env list --json > "$env_list"
  base_root="$("$CONDA_PATH" info --base)"
  base_python="$base_root/bin/python"
  [ -x "$base_python" ] || { printf 'Conda base Python was not found: %s\n' "$base_python" >&2; return 1; }
  "$base_python" -c 'import json, os, sys; sys.stdout.write(next((p for p in json.load(open(sys.argv[1], encoding="utf-8"))["envs"] if os.path.basename(os.path.normpath(p)).lower() == "wd"), ""))' "$env_list"
}
env_path="$(find_wd_environment)"
if [ -z "$env_path" ]; then
  printf 'Creating wd with Python 3.10 and pip 24 or later...\n'
  "$CONDA_PATH" create --yes --name wd --override-channels --channel https://conda.anaconda.org/conda-forge 'python=3.10' 'pip>=24'
  env_path="$(find_wd_environment)"
fi
[ -n "$env_path" ] || { printf 'Conda did not report a wd environment.\n' >&2; exit 1; }
python_path="$env_path/bin/python"
paperbrain_path="$env_path/bin/paperbrain"
"$python_path" -c 'import pip, sys; assert sys.version_info >= (3, 9), "PaperBrain requires Python 3.9 or later"; major = int(pip.__version__.split(".")[0]); assert major >= 24, "PaperBrain requires pip 24 or later"; print(f"Using Python {sys.version.split()[0]} and pip {pip.__version__}")'

release_base="https://github.com/$BACKEND_REPOSITORY/releases/download/$BACKEND_TAG"
wheel_path="$TEMP_DIR/$WHEEL_NAME"
requirements_path="$TEMP_DIR/$REQUIREMENTS_NAME"
printf 'Downloading and verifying PaperBrain backend %s...\n' "$BACKEND_VERSION"
download_file "$release_base/$WHEEL_NAME" "$wheel_path"
verify_file "$wheel_path" "$WHEEL_SHA256"
download_file "$release_base/$REQUIREMENTS_NAME" "$requirements_path"
verify_file "$requirements_path" "$REQUIREMENTS_SHA256"

if [ "$INDEX_URL" = "auto" ]; then
  best_url=""
  best_label=""
  best_elapsed=""
  while IFS='|' read -r source_label source_url; do
    probe_dir="$TEMP_DIR/probe-${source_label%% *}"
    rm -rf "$probe_dir"
    mkdir -p "$probe_dir"
    start_ns="$("$python_path" -c 'import time; print(time.monotonic_ns())')"
    printf 'Testing %s...\n' "$source_label"
    if "$python_path" -m pip download --disable-pip-version-check --no-deps --only-binary=:all: --no-cache-dir --timeout 20 --retries 1 --dest "$probe_dir" --index-url "$source_url" "$PROBE_REQUIREMENT"; then
      probe_count="$(find "$probe_dir" -maxdepth 1 -type f | wc -l | tr -d ' ')"
      probe_file="$(find "$probe_dir" -maxdepth 1 -type f | head -n 1)"
      if [ "$probe_count" = "1" ] && [ -n "$probe_file" ] && [ "$(sha256_file "$probe_file")" = "$PROBE_SHA256" ]; then
        end_ns="$("$python_path" -c 'import time; print(time.monotonic_ns())')"
        elapsed="$((end_ns - start_ns))"
        if [ -z "$best_elapsed" ] || [ "$elapsed" -lt "$best_elapsed" ]; then
          best_elapsed="$elapsed"
          best_url="$source_url"
          best_label="$source_label"
        fi
      else
        printf '%s failed the wheel hash probe.\n' "$source_label" >&2
      fi
    else
      printf '%s was unavailable.\n' "$source_label" >&2
    fi
  done <<'SOURCES'
Official PyPI|https://pypi.org/simple
Alibaba Cloud|https://mirrors.aliyun.com/pypi/simple
USTC|https://mirrors.ustc.edu.cn/pypi/simple
Tsinghua TUNA|https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
SOURCES
  [ -n "$best_url" ] || { printf 'No dependency source passed the download and SHA-256 probe.\n' >&2; exit 1; }
  INDEX_URL="$best_url"
  printf 'Selected %s for dependency installation.\n' "$best_label"
fi

"$python_path" -m pip install --disable-pip-version-check --index-url "$INDEX_URL" --require-hashes -r "$requirements_path"
"$python_path" -m pip install --disable-pip-version-check --no-deps --force-reinstall "$wheel_path"
mkdir -p "$CONFIG_DIR"
bootstrap_output="$("$paperbrain_path" bootstrap --config-dir "$CONFIG_DIR" --vault "$VAULT_PATH")"
printf '%s\n' "$bootstrap_output"
config_path="$(printf '%s' "$bootstrap_output" | "$python_path" -c 'import json, sys; data=json.load(sys.stdin); assert data.get("ok") is True and data.get("command") == "bootstrap" and data.get("config_path"); print(data["config_path"])')"
receipt_path="$HOME/.paperbrain/runtime/terminal-install.json"
managed_runtime_path=""
case "$CONDA_PATH" in
  "$RUNTIME_ROOT"/*) managed_runtime_path="$RUNTIME_ROOT" ;;
esac
"$python_path" -c 'import json, os, sys; target=sys.argv[1]; os.makedirs(os.path.dirname(target), exist_ok=True); data={"backendVersion": sys.argv[2], "condaPath": sys.argv[3], "envPath": sys.argv[4], "pythonPath": sys.argv[5], "cliPath": sys.argv[6], "configPath": sys.argv[7], "managedRuntimePath": sys.argv[8]}; json.dump(data, open(target, "w", encoding="utf-8"), indent=2)' \
  "$receipt_path" "$BACKEND_VERSION" "$CONDA_PATH" "$env_path" "$python_path" "$paperbrain_path" "$config_path" "$managed_runtime_path"
printf '\nPaperBrain backend %s is ready. Return to Obsidian and select Detect again.\n' "$BACKEND_VERSION"
