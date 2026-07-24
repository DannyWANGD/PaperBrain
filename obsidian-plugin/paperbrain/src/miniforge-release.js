"use strict";

const MINIFORGE_RELEASE = Object.freeze({
  repository: "conda-forge/miniforge",
  version: "26.3.2-2",
  tag: "26.3.2-2",
  assets: Object.freeze({
    "win32-x64": Object.freeze({
      name: "Miniforge3-26.3.2-2-Windows-x86_64.exe",
      sha256: "088884aafcbf2e3355671d4e9b227b0d1cfb278e3bbe74ba2ad213c553874d70",
      size: 79227640,
    }),
    "darwin-x64": Object.freeze({
      name: "Miniforge3-26.3.2-2-MacOSX-x86_64.sh",
      sha256: "a755192103de19bb2782685ac78820c2e00702e5f33e6e4f0a3bf3c214f45d69",
      size: 61243225,
    }),
    "darwin-arm64": Object.freeze({
      name: "Miniforge3-26.3.2-2-MacOSX-arm64.sh",
      sha256: "2657d94152343cff7c06159ac9fc09624d7879fa9575c5a0a324c571c4df0ade",
      size: 54147762,
    }),
    "linux-x64": Object.freeze({
      name: "Miniforge3-26.3.2-2-Linux-x86_64.sh",
      sha256: "42260ffe3830fb953d5eee1bbb32229ff06aa7c3833c1ed7a9a0420a95685d94",
      size: 106038245,
    }),
    "linux-arm64": Object.freeze({
      name: "Miniforge3-26.3.2-2-Linux-aarch64.sh",
      sha256: "f4096a92482b30f04534cddb63d8bc929118318deffac71d90fb89dc52359d22",
      size: 93869432,
    }),
  }),
});

function miniforgeAssetUrl(asset, release = MINIFORGE_RELEASE) {
  return `https://github.com/${release.repository}/releases/download/${release.tag}/${asset.name}`;
}

function resolveMiniforgeAsset(platform = process.platform, arch = process.arch, release = MINIFORGE_RELEASE) {
  return release.assets[`${platform}-${arch}`] || null;
}

module.exports = { MINIFORGE_RELEASE, miniforgeAssetUrl, resolveMiniforgeAsset };
