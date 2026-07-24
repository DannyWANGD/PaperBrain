# PaperBrain Console

**简体中文** | [English](README_EN.md)

PaperBrain Console 是 [PaperBrain Python 流水线](https://github.com/DannyWANGD/PaperBrain)
的 Obsidian 桌面控制台，用于安装后端、启动或停止任务、查看运行状态，以及打开写入当前
vault 的摘要、研究笔记、PDF、图像和音频。

插件需要启动本地进程，因此仅支持 Obsidian 桌面版。插件 `0.5.0` 的安装器固定使用
PaperBrain 后端 `0.3.6`。

## 快速开始

1. 安装并启用 BRAT，选择 **Add beta plugin**，输入
   `https://github.com/DannyWANGD/obsidian-paperbrain`。
2. 启用 **PaperBrain Console**，打开控制台并选择推荐的
   **Terminal install (recommended)**。
3. 选择 Windows、macOS 或 Linux，复制命令并在自己的终端中执行。完成后返回插件，
   选择 **Detect again**。
4. 选择 **Open API key file**，填写 API Key 并保存。
5. 选择 **Validate setup**。验证通过后选择运行模式并点击 **Run**。

也可以选择 **Install inside Obsidian** 完成原有的一键安装。两种方式都会优先复用现有
Conda；没有可用 Conda 时安装独立 Miniforge，均不需要 Python 源码仓库或预装 Python。

## 系统要求

- Obsidian 桌面版 1.5.0 或更高版本
- 约 1 GB 可用磁盘空间
- 安装时可访问 GitHub Releases、conda-forge 和至少一个 Python 包索引
- OpenRouter 或豆包账号及 API Key

高级用户也可自行配置 PaperBrain 0.3.x 后端和 Python 3.9 或更高版本。

## 安装插件

推荐使用 BRAT，它会从同一个 GitHub Release 自动安装和更新插件。

如需手动安装，从 [Releases](https://github.com/DannyWANGD/obsidian-paperbrain/releases)
下载同一版本的 `main.js`、`manifest.json` 和 `styles.css`，放入
`<vault>/.obsidian/plugins/paperbrain/` 后重载 Obsidian。`checksums.txt` 仅用于校验；
GitHub 自动生成的 Source code 压缩包不能替代这三个运行文件。

## 后端安装

推荐选择 **Terminal install (recommended)**，复制当前系统的命令并在自己的终端执行。
这样下载会继承该终端中的 `HTTP_PROXY`、`HTTPS_PROXY` 等网络环境。命令先从对应的插件
Release 下载 `install-backend.ps1`（Windows）或 `install-backend.sh`（macOS/Linux），
校验固定 SHA-256 后才执行。

不希望使用终端时，可选择 **Install inside Obsidian**。两种安装方式都会：

1. 检测并优先复用现有 Conda。
2. 创建或复用名为 `wd` 的环境。新环境使用 Python 3.10；现有环境必须是
   Python 3.9 或更高版本且 pip 不低于 24，否则安装会在下载后端前停止。
3. 如果没有可用 Conda，从 conda-forge 下载并校验 Miniforge 26.3.2-2，安装到
   `~/.paperbrain/runtime/miniforge3`。该安装不修改系统 PATH、不初始化 shell，
   也不需要管理员权限。
4. 从 `backend-0.3.6` Release 下载 wheel 与哈希锁定依赖，并校验 SHA-256。
5. 在默认 **Auto** 模式下，从官方 PyPI、阿里云、USTC 和清华 TUNA 分别下载同一个
   1.6 MB 探测 wheel。只有通过 SHA-256 的源参与测速，完整依赖只从最快的合格源安装，
   不会混用多个索引。也可在设置中手动固定一个源。
6. 在 `~/.paperbrain/config` 创建配置并指向当前 vault。已有配置和 `.env` 不会被覆盖。

终端方式以用户执行复制的命令作为确认；Obsidian 内安装会显示确认窗口。临时文件会在
安装结束或失败后清理。终端安装完成后选择 **Detect again**，插件会自动记录 `wd` 中的
Python、CLI 和默认配置路径。

| 内容 | Windows | macOS / Linux |
| --- | --- | --- |
| 私有 Miniforge | `%USERPROFILE%\.paperbrain\runtime\miniforge3` | `~/.paperbrain/runtime/miniforge3` |
| 配置与 API Key | `%USERPROFILE%\.paperbrain\config` | `~/.paperbrain/config` |
| 生成内容 | 当前 Obsidian vault | 当前 Obsidian vault |

卸载私有运行时前先关闭 Obsidian，再删除 `~/.paperbrain/runtime/miniforge3`。仅在确认不再
需要配置和 API Key 时删除 `~/.paperbrain/config`。不要删除插件只是复用的外部 Conda。

## API Key 与设置

**Open API key file** 会打开 `~/.paperbrain/config/.env`。只需填写实际使用的供应商：

```env
OPENROUTER_API_KEY=your_openrouter_api_key
# DOUBAO_API_KEY=your_doubao_api_key
```

API Key 不会写入 Obsidian 的插件设置。**Validate setup** 会执行本地的
`doctor config`、`doctor env` 和 `doctor llm`，但不会添加 `--live`，因此不会调用模型。

常用设置：

- **Dependency download source**：默认 Auto，也可固定 PyPI、阿里云、USTC、TUNA 或一个
  不含凭据的 HTTPS simple index。
- **Network proxy**：默认继承启动 Obsidian 时的代理环境；也可填写无凭据、带端口的
  `http://` 或 `https://` 代理，或选择 Direct 清除代理。**Test connection** 会先测试
  插件下载器，检测到后端时再测试 Hugging Face 和 arXiv，不调用模型。
- **Default provider**：新任务默认使用的模型供应商。
- **API key file**：随时打开本地 `.env` 文件；API Key 不写入 Obsidian 插件设置。
- **Advanced**：源码后端、CLI、配置路径、vault、Podcast 和取消超时等高级选项。

## 数据、网络与费用

- 插件本身没有遥测、广告或付费功能，只保存本地运行设置。
- 插件会启动本地后端进程，并读取当前 vault 中的运行记录和生成内容。
- 后端会访问 arXiv、Hugging Face 和所选模型供应商。根据任务类型，论文元数据、PDF 文本
  或渲染页面可能发送给模型供应商并产生费用。
- 后端会向配置的 vault 写入摘要、笔记、PDF、资源、索引、缓存和运行记录。请备份重要 vault。

权限、网络边界和安全报告方式见 [SECURITY.md](SECURITY.md)。插件代码采用 MIT License；
后端、论文、模型服务及生成或下载的内容遵循各自的许可证和服务条款。

## 兼容性

| 插件 | 后端 | Obsidian |
| --- | --- | --- |
| 0.5.0 | 安装器固定 0.3.6；运行时接受 0.3.1 至小于 0.4.0 | 1.5.0 或更高版本，桌面版 |

## 故障排查

- **终端安装失败**：保留终端输出，确认代理和 GitHub 可访问后重新执行同一命令。
- **Obsidian 内安装失败**：保持控制台打开并重试 **Install inside Obsidian**，查看失败阶段和最后一条错误。
- **所有包索引均失败**：确认网络允许访问所选索引，或在设置中手动固定可用源。
- **找不到 `paperbrain`**：将 CLI executable 设置为 `wd` 中 `paperbrain` 的绝对路径。
- **验证失败**：确认 **Vault path** 与后端实际 vault 一致，并检查
  `~/.paperbrain/config/.env` 中的 API Key。
- **Python-script 模式失败**：确认后端目录包含 `script/paperbrain.py`。

## 可选配套插件

PaperBrain Console 不依赖其他 Obsidian 插件。以下插件可按需搭配：

| 插件 | ID | 用途 |
| --- | --- | --- |
| BRAT | `obsidian42-brat` | 从 GitHub Release 安装和更新 PaperBrain |
| Dataview | `dataview` | 查询论文属性并构建阅读与复现队列 |
| Audio Player | `obsidian-audio-player` | 播放生成的 Podcast 音频 |
| floating toc | `floating-toc` | 导航长篇研究笔记和简报 |
| Highlightr | `highlightr-plugin` | 手工标记证据与复核重点 |
| Style Settings | `obsidian-style-settings` | 调整 Obsidian 主题 |
| Immersive Translate | `immersive-translate` | 翻译生成的研究笔记 |
| Smart Connections | `smart-connections` | 探索笔记之间的语义关系 |
| Copilot | `copilot` | 围绕 vault 内容继续提问 |
| Claudian | `realclaudian` | 在 vault 中运行编码代理工作流 |
| Translay Translator | `aqu-translay-translator` | 翻译笔记与界面文本 |
| Components | `components` | 构建可复用的 Obsidian 内容组件 |

安装方式与注意事项见[配套插件说明](docs/COMPANION_PLUGINS.md)。

## 开发与发布

```bash
npm ci
npm run check
```

源码位于 `src/`，构建产物 `main.js` 由 Release 工作流生成。发布标签必须与
`manifest.json` 版本一致，Release 必须包含 `main.js`、`manifest.json`、`styles.css`、
`install-backend.ps1`、`install-backend.sh` 和 `checksums.txt`。

开发与发布政策见 [CONTRIBUTING.md](CONTRIBUTING.md)、[SECURITY.md](SECURITY.md) 和
[CHANGELOG.md](CHANGELOG.md)。
