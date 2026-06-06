# PaperBrain 仓库全面检查与升级建议

生成时间: 2026-06-05 20:36, Asia/Shanghai  
仓库路径: `D:\PaperBrain`  
报告目标: 系统检查当前仓库存在的问题，并基于联网调研提出 15 条进一步完善与升级方案。

## 0. 核查范围与方法

本次检查覆盖:

- Python 主流程: `script/main.py`, `script/src/*.py`, `script/config/*.yaml`, `script/tests/*`
- Obsidian 插件: `obsidian-plugin/paperbrain/*` 与已安装副本 `.obsidian/plugins/paperbrain/*`
- Vault 数据: `Research_Notes`, `Daily_Papers`, `Research_Briefs`, `Research_Index`, `Run_Records`
- 生成物和缓存: `PDFs`, `Assets`, `Podcasts`, `Cache`, `.obsidian`, `.smart-env`
- Git 状态、对象大小、被跟踪的大文件、被跟踪但应忽略的文件
- 本地验证: `paperbrain.py check`, `paperbrain.py doctor`, `node --check`
- 联网调研: arXiv API 条款、Git LFS/DVC、Obsidian 插件/Bases、Ruff/pre-commit、OpenTelemetry、Phoenix/RAGAS/promptfoo、OpenRouter、SQLite FTS5、uv/pip-tools、GitHub security、Semantic Scholar/OpenAlex/Crossref、Pydantic settings 等官方或一手文档。

未执行的内容:

- 未执行真实 arXiv live probe 或真实 LLM probe, 因为这会触发外部网络/API 消耗。`doctor` 的非 live 检查已通过。
- 未修改业务代码。本报告是新增文件；另外运行 `doctor` 会刷新 `Cache/diagnostics/*.json`, 这是项目当前行为导致的生成物变更。

## 1. 一句话结论

当前 PaperBrain 的核心流水线是可运行的: `wd` 环境中 81 个测试通过、Python 编译/导入通过、非联网 `doctor` 通过、插件源文件和已安装副本一致、插件 JS 语法通过。主要风险不在“功能是否能跑”, 而在仓库治理、可复现环境、CI 防线、生成物入库、前端工程化、数据 schema 规范和 LLM 输出可验证性上。

## 2. 当前健康状态

### 2.1 验证结果

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| `D:\anaconda3\envs\wd\python.exe script\paperbrain.py check` | 通过 | 81 tests OK, compile/import OK, path writable |
| Ruff | 未实际执行 | `wd` 环境未安装 Ruff, `check` 在非 strict 模式下把 lint 标记为 missing 但仍通过 |
| `D:\anaconda3\envs\d2l\python.exe script\paperbrain.py check` | 失败 | 该环境缺少 `feedparser`, `arxiv`, `pymupdf`, `openai`, `edge-tts`, `python-dotenv` 等依赖。说明多环境漂移明显 |
| `node --check obsidian-plugin\paperbrain\main.js` | 通过 | 源插件 JS 语法有效 |
| `node --check .obsidian\plugins\paperbrain\main.js` | 通过 | 已安装插件 JS 语法有效 |
| 插件源和已安装副本哈希 | 一致 | `main.js`, `styles.css`, `manifest.json`, `README.md` 均一致 |
| `paperbrain.py doctor` | 通过 | config/env/arxiv/llm/obsidian 非 live 检查 OK |

### 2.2 Git 与仓库规模

| 指标 | 当前值 |
| --- | --- |
| Git tracked files | 864 |
| Git object database | 1.44 GiB |
| tracked `PDFs` | 88 files, 1177.71 MiB |
| tracked `Podcasts` | 34 files, 89.29 MiB |
| tracked `Assets` | 88 files, 56.69 MiB |
| tracked `.smart-env` | 253 files, 47.85 MiB |
| tracked `Cache` | 25 files, 27.43 MiB |
| tracked `.obsidian` | 69 files, 26.62 MiB |
| tracked `Run_Records` | 76 files, 2.78 MiB |

当前最大的 tracked 文件示例:

- `PDFs/RynnBrain Open Embodied Foundation Models.pdf`: 63.18 MiB
- `PDFs/ACEBrain0 Spatial Intelligence as a Shared Scaffold for Universal Embodiments.pdf`: 48.74 MiB
- `PDFs/DynaFLIP Rethinking Robotics Perception via TriModalDynamics Guided Representation.pdf`: 48.67 MiB
- `Cache/pdfs/2605.23699.pdf`: 21.90 MiB
- `Assets/ULTRA Unified Multimodal Control for Autonomous Humanoid WholeBody LocoManipulation_arch.png`: 14.02 MiB

### 2.3 Vault 数据完整性

| 检查项 | 结果 |
| --- | --- |
| `Research_Notes/*.md` | 88 篇 |
| frontmatter | 88/88 存在 |
| frontmatter YAML | 88/88 可解析 |
| duplicate `paper_id` | 0 |
| duplicate arXiv ID | 0 |
| `Run_Records/*/state.json` | 11 个 |
| run stages | 10 completed, 1 initialized |
| run states with errors | 0 |
| PDFs / Assets / Podcasts | 88 / 88 / 34 |

一个结构性问题: 研究笔记 frontmatter 中有 `aliases`, `paper_id`, `arxiv_id`, `publication_date`, `score`, `tags` 等字段，但没有统一的 `title` 或 `short_title` 字段。Obsidian 内部可以靠文件名和 alias 工作，但对 Bases、外部索引、导出、API 查询会不够友好。

## 3. 主要问题清单

### P1. 仓库把大量生成物和本地状态纳入 Git, 长期会拖慢一切

证据:

- Git object database 为 1.44 GiB。
- tracked PDF 合计约 1.18 GiB, MP3 约 89 MiB, Assets 约 56 MiB, `.smart-env` 约 48 MiB, Cache 约 27 MiB。
- `Cache/diagnostics/*.json` 是运行 `doctor` 会刷新的生成物, 但当前被 Git 跟踪, 所以一次健康检查就会污染工作区。
- `.smart-env/event_logs/event_logs.ajson` 当前处于 modified 状态, 也属于本地事件日志。

影响:

- clone、diff、status、备份、CI checkout 都会越来越慢。
- 每次运行可能把缓存/诊断/插件状态写成 Git 变更, 让真正的代码变更被噪声淹没。
- PDF/MP3 这类二进制大文件不适合普通 Git diff 和历史存储。

建议:

- 把 `PDFs`, `Podcasts`, `Assets`, `Cache`, `.smart-env`, `.obsidian/workspace.json`, `.obsidian/plugins/*/data.json`, `__pycache__`, `*.egg-info` 从普通 Git 中迁出。
- 对需要保留的 PDF/图片/音频使用 Git LFS 或 DVC。GitHub 官方文档说明 Git LFS 用 pointer 文件引用大文件本体；DVC 官方文档说明可以用 remote storage 同步大文件和目录。
- 保留一个轻量 manifest, 例如 `artifacts/index.jsonl`: `paper_id`, `sha256`, `local_path`, `source_url`, `license`, `created_at`, `size`, `kind`。

参考:

- GitHub Git LFS: https://docs.github.com/repositories/working-with-files/managing-large-files/about-git-large-file-storage
- DVC remote storage: https://dvc.org/doc/user-guide/data-management/remote-storage

### P1. `.gitignore` 太窄, 且存在已被跟踪的 ignored 文件

证据:

- 当前 `.gitignore` 只覆盖 `__pycache__/`, `*.pyc`, `.env`, `.DS_Store`, `.vscode/`, `paperbrain.log`, `temp_pdfs/`, plugin `data.json`, copilot index。
- `git ls-files -ci --exclude-standard` 显示 13 个“已经被跟踪但现在匹配 ignore”的文件, 包括:
  - `.obsidian/plugins/dataview/data.json`
  - `.obsidian/plugins/floating-toc/data.json`
  - `.obsidian/plugins/highlightr-plugin/data.json`
  - `.obsidian/plugins/obsidian42-brat/data.json`
  - `.obsidian/plugins/smart-connections/data.json`
  - 根目录 `__pycache__/*.pyc`

影响:

- `.gitignore` 对已经被 Git 跟踪的文件无效, 必须从 index 中移除才会停止追踪。
- Obsidian 插件 `data.json` 往往是用户配置, 有潜在 token、路径、隐私偏好或本地状态。

建议:

- 扩展 `.gitignore`:
  - `Cache/`
  - `PDFs/`
  - `Podcasts/`
  - `Assets/` 或至少 `Assets/*_arch.*`
  - `Run_Records/` 或仅保留精选样例
  - `.smart-env/`
  - `.obsidian/workspace*.json`
  - `.obsidian/plugins/**/data.json`
  - `script/paperbrain.egg-info/`
  - `**/__pycache__/`
- 后续用非破坏性、可审查的 commit 把这些文件从 Git index 迁出。

### P1. CI 当前没有真正执行 lint/format, 也没有覆盖插件语法和仓库治理

证据:

- `.github/workflows/paperbrain-check.yml` 只安装 `script/requirements.txt`, 没有安装 `.[dev]` 或 Ruff。
- `paperbrain.py check` 在 Ruff 缺失且非 `--strict-lint` 时仍然 `ok: true`。
- 当前本地 `wd` 环境也显示 Ruff missing。
- CI 未执行 `node --check obsidian-plugin/paperbrain/main.js`。
- CI 未检查插件源目录和 `.obsidian/plugins/paperbrain` 已安装副本是否一致。
- CI 未检查大文件预算、tracked ignored 文件、secret scanning、frontmatter schema。

影响:

- “CI 绿”不能代表风格、格式、JS 语法、插件同步、仓库卫生都健康。
- `paperbrain.py check` 的语义容易被误解: 它叫 check, 但在默认模式下 lint 可缺席。

建议:

- CI 改为安装 dev 依赖并执行:
  - `python script/paperbrain.py check --strict-lint`
  - `node --check obsidian-plugin/paperbrain/main.js`
  - plugin hash sync check
  - tracked large file budget check
  - `git ls-files -ci --exclude-standard` 必须为空
  - frontmatter schema check
- pre-commit 中加入大文件、密钥、YAML、JSON、JS syntax、Ruff format/check。

参考:

- Ruff linter: https://docs.astral.sh/ruff/linter/
- pre-commit: https://pre-commit.com/
- GitHub security features: https://docs.github.com/code-security/getting-started/github-security-features

### P1. 环境可复现性不足, `requirements.txt` 与 `pyproject.toml` 双源维护

证据:

- `pyproject.toml` 和 `script/requirements.txt` 都列依赖, 容易漂移。
- 没有 lockfile。
- `wd` 环境可运行, `d2l` 环境缺少关键依赖。说明“机器上某个环境能跑”没有被固化成可复现状态。

影响:

- 新机器、CI、未来自己恢复环境时, 可能安装到不同依赖版本。
- LLM/PDF/HTML 解析工具版本漂移会直接影响输出结果。

建议:

- 选择单一依赖入口:
  - 推荐 `pyproject.toml` 作为唯一源。
  - 用 `uv.lock` 或 `pip-tools` 生成锁定文件。
- CI 使用 `uv sync --locked` 或 `pip-sync`。
- 把 dev tools 也纳入 dependency group, 例如 Ruff、pre-commit、pytest 或 unittest runner 辅助工具。

参考:

- uv lockfile: https://docs.astral.sh/uv/guides/projects/
- uv locking and syncing: https://docs.astral.sh/uv/concepts/projects/sync/
- pip-tools `pip-compile`: https://pip-tools.readthedocs.io/en/stable/cli/pip-compile/

### P1. PDF 下载路径需要更强的安全和资源保护边界

证据:

- `script/main.py:162-273` 的 `download_pdf` 只检查 URL scheme, 域名白名单被注释掉。
- 下载时没有显式最大文件大小限制。
- 对任意 HTTP(S) URL 发起请求, 本地个人工具风险较低, 但仍有 SSRF/内网请求/超大文件消耗/非 PDF 内容伪装的可能。
- 当前会验证 `%PDF-` header, 这是好点, 但可以更早用 Content-Type 和 Content-Length 拦截。

建议:

- 默认只允许 `arxiv.org`, `export.arxiv.org`, `huggingface.co`, `openreview.net`, `aclweb.org` 等明确信任域。
- 对单文件大小设置上限, 如 100 MiB 或可配置。
- 先 HEAD 检查 Content-Type 和 Content-Length, 失败时再 GET, 并在 streaming 中累计字节数。
- 保存 `source_url`, `sha256`, `license_hint`, `downloaded_at`。

参考:

- arXiv API 条款鼓励链接 abstract 页面, 并限制 PDF/source 的再分发: https://info.arxiv.org/help/api/tou.html

### P1. LLM 输出仍有大量 regex/宽松 JSON 修复, 应引入 schema 级约束

证据:

- `script/src/analyser.py` 中 metadata JSON 提取依赖多段正则修复。
- screening prompt 要求 JSON, 但当前更像“提示约束 + 清洗”, 不是 API 层 schema。
- OpenRouter 文档支持对兼容模型使用 `response_format.type=json_schema`, 并可用 provider `require_parameters` 只选择支持指定参数的 provider。

影响:

- 模型偶发输出格式漂移时, pipeline 会进入不可预期的 regex 修补路径。
- 难以把“模型错误”和“解析器错误”精确区分。

建议:

- 为 coarse screening、detailed screening、metadata extraction、alias generation 定义 JSON Schema。
- 当 OpenRouter provider 支持 structured outputs 时强制 schema；不支持时明确 fallback 并记录原因。
- 对 schema validation fail 的输出保存到 `Run_Records/<date>/bad_outputs/` 作为回归样本。

参考:

- OpenRouter structured outputs: https://openrouter.ai/docs/features/structured-outputs
- OpenRouter provider routing: https://openrouter.ai/docs/features/provider-routing

### P2. 主流程和分析器文件过大, 修改成本已经偏高

证据:

- `script/main.py`: 1299 lines。
- `script/src/analyser.py`: 1455 lines。
- `obsidian-plugin/paperbrain/main.js`: 1507 lines。

影响:

- 每次新增功能都容易碰到跨阶段状态、选择逻辑、LLM 调用、PDF 处理、写入 Obsidian 的耦合。
- 测试虽然覆盖不少 helper, 但整体结构对未来并发、重试、可观测性、插件协议升级不够友好。

建议:

- 拆分 Python:
  - `pipeline/stages/fetch.py`
  - `pipeline/stages/screen.py`
  - `pipeline/stages/deep.py`
  - `pipeline/stages/digest.py`
  - `llm/client.py`
  - `llm/schemas.py`
  - `artifacts/pdf_store.py`
  - `state/selection.py`
- 拆分插件:
  - view state
  - run form
  - timeline
  - artifacts/history
  - settings
  - process bridge

### P2. `RunState.run_id()` 现在只返回日期, provider/single-paper 维度被压扁

证据:

- `script/src/paths.py:145-146`: `run_id(self, date_key, provider, single_paper=False)` 返回 `str(date_key)`。

优点:

- 同一天的 daily/single/preserved deep 能合并到统一状态, 这是近期功能的合理需求。

风险:

- 同一天用不同 provider 重跑, provider 维度会在同一个 run folder 中混合。
- 插件历史和诊断中可能出现“date 是唯一 run id, 但内部 provider/modes 多源”的语义复杂性。

建议:

- 保留 date-level canonical state, 但增加 `provider_runs` 子结构:
  - `provider_runs.openrouter.started_at`
  - `provider_runs.doubao.started_at`
  - `provider_runs.<provider>.model_usage`
  - `provider_runs.<provider>.stages`
- 插件 UI 显示“日期主状态 + provider 子记录”, 避免误判。

### P2. 研究笔记 schema 缺少显式 `title` 字段

证据:

- 88 篇 `Research_Notes/*.md` frontmatter 都能解析, 但没有统一 `title`。
- 单篇示例 `ACEBrain0.md` 有 `aliases`, `paper_id`, `arxiv_id`, `publication_date`, `score` 等字段, 但没有 `title`。

影响:

- Obsidian 内部链接没问题, 但 Bases、外部导出、SQLite/JSONL 索引、引用生成都会更依赖文件名。
- 文件名后续重命名会影响 title 的稳定性。

建议:

- 新增统一字段:
  - `title`
  - `short_title`
  - `canonical_title`
  - `source_title`
  - `note_version`
- 给历史 88 篇跑一次非破坏性迁移, 从 alias 或正文标题回填。

参考:

- Obsidian Bases 支持基于 note properties 构建动态视图: https://docs.obsidian.md/plugins/guides/bases-view

### P2. 插件是单文件 CommonJS, 缺少 TypeScript/build/test 工程化

证据:

- 插件使用 `main.js` 直接维护, 1507 行。
- 没有 `package.json`, `tsconfig`, build step 或单元测试。
- 当前 `manifest.json` 版本为 `0.1.0`, `README`/主项目版本为 `PaperBrain 2.0` / `pyproject 0.3.0`, 版本语义不统一。

影响:

- 小改动可以很快, 但大型 UI 和状态机演进时缺乏类型保护。
- Obsidian API 变动、DOM 事件、路径处理、process bridge 都缺少类型提示和测试。

建议:

- 引入最小 TypeScript 插件工程:
  - `src/main.ts`
  - `src/view/*.ts`
  - `src/bridge/process.ts`
  - `npm run build`
  - `npm run check`
- CI 执行 build 和 `node --check`。
- 同步 `manifest.json` 版本和 Python 包版本, 或明确区分 plugin version 与 pipeline version。

参考:

- Obsidian manifest schema: https://docs.obsidian.md/Reference/Manifest
- Obsidian plugin build guide: https://docs.obsidian.md/Plugins/Getting%20started/Build%20a%20plugin

### P2. 文档有轻微漂移和路径不一致

证据:

- `SECURITY.md:37` 建议 `pip install --upgrade -r requirements.txt`, 但实际依赖文件是 `script/requirements.txt`。
- README 中 `script/config/.env.example` 实际存在, 这一点是正确的。
- `script/paperbrain.egg-info/PKG-INFO` 中的 README 快照可能已经和实际 README 漂移。

建议:

- 把安装、运行、doctor/check、plugin sync、artifact policy 放入一个 `docs/operations.md`。
- 对 README 中的命令做 CI smoke test, 至少验证路径存在。
- 生成包 metadata 不应长期手改或入库。

### P2. 安全边界总体可接受, 但应把“已验证无泄漏”转成自动化

证据:

- `script/.env` 存在且包含非空本地值, 但没有被 Git 跟踪。
- `.gitignore` 的 `.env` 规则正在保护该文件。
- 当前仍有多个 Obsidian plugin `data.json` 被跟踪, 这类文件可能包含本地配置或隐私信息。

建议:

- 加入 secret scanning/pre-commit hook。
- CI 中禁止 tracked `.env`, `data.json`, token-like patterns。
- 对本地 `.env` 做仅键名/非空状态检查, 不输出值。

参考:

- GitHub Secret Protection 和 Code Security: https://docs.github.com/code-security/getting-started/github-security-features
- Dependabot alerts: https://docs.github.com/en/code-security/concepts/supply-chain-security/about-dependabot-alerts

### P3. 当前测试很实用, 但缺少“端到端样本”和“LLM 回归评估”

证据:

- 81 个 tests 通过, 包含 identity、state、digest、brief、scraper mock、pipeline helper、doctor 等。
- Live network/LLM probes 被正确排除在 unit tests 外。
- 但 prompt/schema/link/resource quality 没有系统化 golden set。

建议:

- 建立 20 篇固定 paper fixture:
  - 5 篇强相关
  - 5 篇弱相关
  - 5 篇边界案例
  - 5 篇容易误判或 PDF 异常案例
- 每次 prompt/model/routing 改动后跑离线回归:
  - 是否选中
  - score 偏差
  - JSON schema pass rate
  - link valid rate
  - note section completeness

参考:

- promptfoo: https://www.promptfoo.dev/docs/intro/
- RAGAS metrics: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/
- Phoenix tracing/evaluation: https://arize.com/docs/phoenix

## 4. 15 条进一步完善与升级方案

### 1. 建立“代码仓库 + 研究资产库”双层架构

方案:

- Git 只存代码、配置模板、少量 fixtures、报告和索引 manifest。
- PDF/MP3/大图/大缓存迁移到 Git LFS 或 DVC remote。
- 每个 artifact 保留 `sha256`, `paper_id`, `source_url`, `license`, `size`, `created_by`, `created_at`。
- Obsidian 里仍保持本地文件可点开, 但 Git 只追踪 pointer 或 manifest。

启发:

- 这会把 PaperBrain 从“巨大 vault 仓库”升级成“可同步、可重建、可迁移的个人研究资产系统”。

参考:

- Git LFS: https://docs.github.com/repositories/working-with-files/managing-large-files/about-git-large-file-storage
- DVC remote storage: https://dvc.org/doc/user-guide/data-management/remote-storage

### 2. 用 lockfile 固化 PaperBrain 运行环境

方案:

- 以 `pyproject.toml` 为唯一依赖源。
- 引入 `uv.lock` 或 `requirements.lock.txt`。
- CI 和插件 doctor 都显示 lockfile 状态。
- `paperbrain.py check` 增加 `dependency_lock_ok`。

启发:

- 你的系统输出依赖 PDF parser、HTML parser、OpenAI SDK、edge-tts 等版本。锁定环境就是锁定研究记录的可复现性。

参考:

- uv project lockfile: https://docs.astral.sh/uv/guides/projects/
- uv sync: https://docs.astral.sh/uv/concepts/projects/sync/

### 3. 把 `check` 升级为真正的质量闸门

方案:

- 默认 CI 使用 `--strict-lint`。
- 安装 dev 依赖, 让 Ruff 缺失变成失败。
- 加入 JS syntax, plugin sync hash, large-file budget, ignored-tracked file check, markdown/frontmatter schema check。
- 对 `doctor` 写入 `Cache/diagnostics` 的行为做隔离: 默认写入 ignored cache 或 `--no-write`。

启发:

- 现在的 `check` 已经是很好的骨架, 下一步是让它从“项目自检”变成“仓库健康守门员”。

参考:

- Ruff: https://docs.astral.sh/ruff/linter/
- pre-commit: https://pre-commit.com/

### 4. 引入 Typed Config 与 schema migration

方案:

- 用 Pydantic 或 dataclass schema 描述 `config.yaml`, `prompts.yaml`, `tags.yaml`。
- 对阈值、模型列表、URL、folder、超时、权重总和进行类型校验。
- 增加 `config_version` 和迁移器。
- 插件 UI 读取 doctor schema, 显示配置错误。

启发:

- 现在 YAML 灵活, 但越灵活越容易“看起来能跑, 实际某个 key 拼错”。类型化配置能把运行时错误前移。

参考:

- Pydantic settings: https://docs.pydantic.dev/usage/settings/

### 5. 用 OpenRouter structured outputs 重写评分与元数据提取

方案:

- coarse screening、stage-2 screening、metadata extraction、alias generation 全部定义 JSON Schema。
- 请求中使用 `response_format.type=json_schema`。
- provider routing 中按需设置 `require_parameters: true`。
- 保存 schema fail 样本, 自动生成 prompt regression case。

启发:

- 这会让“LLM 输出”从文本清洗问题变成可验证的数据契约问题。

参考:

- OpenRouter structured outputs: https://openrouter.ai/docs/features/structured-outputs
- OpenRouter provider routing: https://openrouter.ai/docs/features/provider-routing

### 6. 建一个 LLM 回归评估台

方案:

- 固定一组 paper fixtures。
- 每次 prompt/model/routing 改动后跑:
  - score stability
  - selected/deep/digest decision stability
  - JSON parse/schema pass
  - note section coverage
  - hallucinated URL rate
  - resource link validity
- 用 promptfoo 做 CLI/CI 评估, 用 RAGAS/Phoenix 做 RAG 和 trace 层评估。

启发:

- 你已经在做“自动研究助理”, 下一步需要“自动研究助理的考试系统”。

参考:

- promptfoo: https://www.promptfoo.dev/docs/intro/
- RAGAS metrics: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/
- Phoenix: https://arize.com/docs/phoenix

### 7. 加入 OpenTelemetry 风格的本地 trace

方案:

- 每个 run 生成 trace:
  - fetch
  - coarse screening
  - PDF excerpt
  - rigorous screening
  - deep analysis round 1
  - refinement
  - round 2 resources
  - link validation
  - digest/index/podcast
- 每个 span 记录耗时、模型、token/cost、retry、fallback、异常、artifact path。
- 初期可以写 JSONL, 后续可接 Phoenix 或 OTLP。

启发:

- 现在 RunState 记录“发生了什么”, trace 会进一步告诉你“为什么慢、为什么贵、为什么失败”。

参考:

- OpenTelemetry Python instrumentation: https://opentelemetry.io/docs/languages/python/instrumentation/
- Phoenix tracing: https://arize.com/docs/phoenix

### 8. 建立本地学术知识图谱

方案:

- 用 `paper_id` 作为节点。
- 增加 citation edges、related works、shared method、shared dataset、same institution、code/dataset/project page edges。
- 数据源:
  - Semantic Scholar recommendations/citations
  - OpenAlex works/cited_by
  - Crossref DOI metadata
- Obsidian 中渲染成 topic map、citation path、research lineage。

启发:

- PaperBrain 不只要“读今天的论文”, 还可以变成“知道一个想法从哪里来、往哪里去”的研究导航仪。

参考:

- Semantic Scholar API: https://www.semanticscholar.org/product/api
- OpenAlex works: https://developers.openalex.org/api-entities/works/get-content
- Crossref REST API: https://www.crossref.org/documentation/retrieve-metadata/rest-api/

### 9. 用 SQLite FTS5 做本地全文检索底座

方案:

- 把 notes、abstracts、screening reasons、limitations、innovation、open questions、resource links、run logs 建成 SQLite。
- 使用 FTS5 支持关键词检索、BM25 排序、字段过滤。
- 后续叠加 embedding 检索, 但先用 FTS5 获得可解释、低成本、可离线的搜索。

启发:

- 对个人研究库, 很多问题不需要一上来就向量数据库。FTS5 足够快、可控、可调试。

参考:

- SQLite FTS5: https://www.sqlite.org/fts5.html

### 10. 把 PaperDigest 升级为“研究决策日志”

方案:

- 每个 digest entry 增加:
  - selected_reason
  - rejected_reason
  - score dimensions
  - confidence
  - red_flags
  - what evidence changed between coarse and rigorous
  - whether PDF context was used
- 对每日入选/未入选做短小复盘。

启发:

- 这会让 PaperBrain 不只是产出结果, 还能积累你自己的研究品味和筛选标准。

### 11. 构建模型能力注册表和预算控制层

方案:

- 为每个模型记录:
  - supports JSON schema
  - supports vision
  - supports reasoning
  - max context
  - observed fail rate
  - average latency
  - cost per successful paper
  - allowed tasks
- 配置每日预算、每篇预算、超时降级策略。
- 利用 OpenRouter routing 和 reasoning 参数, 对不同阶段设定不同 effort。

启发:

- 现在模型列表在 config 里, 下一步应升级为“模型运营系统”: 知道何时用快模型, 何时用强模型, 何时停止花钱。

参考:

- OpenRouter provider routing: https://openrouter.ai/docs/features/provider-routing
- OpenRouter reasoning tokens: https://openrouter.ai/docs/guides/best-practices/reasoning-tokens

### 12. 把 Obsidian 插件升级成 TypeScript 模块化控制台

方案:

- 用 TypeScript 拆分 `main.js`。
- 加入 build/check 脚本。
- 对 process bridge、state parser、timeline stage reducer 写单元测试。
- 设置页加“Validate paths”和“Run doctor”按钮, 结果结构化展示。

启发:

- 当前插件已经很实用, 但它会越来越像一个本地应用。TypeScript 化会显著降低 UI 迭代的心理负担。

参考:

- Obsidian plugin guide: https://docs.obsidian.md/Plugins/Getting%20started/Build%20a%20plugin
- Obsidian manifest: https://docs.obsidian.md/Reference/Manifest

### 13. 为 Obsidian Bases 设计研究工作台

方案:

- 标准化 note properties:
  - `title`
  - `short_title`
  - `paper_id`
  - `publication_date`
  - `reading_status`
  - `repro_status`
  - `code_status`
  - `dataset_status`
  - `next_action`
  - `priority_score`
- 建立多个 Base:
  - 今日待读
  - 高价值未复现
  - 有代码可跑
  - 有开放问题
  - 未来 7 天复习

启发:

- 这会把 Vault 从“笔记集合”升级为“研究操作系统”。

参考:

- Obsidian Bases view: https://docs.obsidian.md/plugins/guides/bases-view

### 14. 按 arXiv API 条款做集中式礼貌抓取层

方案:

- 全局单连接、单速率 limiter。
- 把 API fetch、PDF fetch、retry、cooldown 收敛到统一 `network/polite_client.py`。
- 对所有 arXiv legacy API 请求保持至少 3 秒间隔。
- 记录 User-Agent 和 contact。
- 默认优先链接 abstract 页面, PDF 只为个人研究缓存。

启发:

- 当前已经有 cooldown 和 fallback, 但可以进一步变成可审计、可证明遵守条款的抓取层。

参考:

- arXiv API Terms of Use: https://info.arxiv.org/help/api/tou.html

### 15. 做“主动学习与复现循环”

方案:

- Round 2 资源路线图之后, 自动生成:
  - 3 个主动回忆问题
  - 1 个最小复现实验
  - 1 个 90 分钟阅读任务
  - 1 个 1-2 周实验任务
  - 复习日期
- 每周 Research Brief 汇总:
  - 本周掌握的概念
  - 尚未回答的问题
  - 值得复现实验
  - 和已有研究方向的关系

启发:

- PaperBrain 最有潜力的升级不是“多总结一点”, 而是把阅读变成一个持续学习和实验推进系统。

## 5. 推荐执行顺序

### 第一阶段: 仓库治理和质量闸门

1. 扩展 `.gitignore`。
2. 制定 artifact policy。
3. 从 Git index 中迁出已跟踪的 cache、pyc、plugin data、smart-env、egg-info。
4. CI 安装 dev 依赖, 启用 `check --strict-lint`。
5. 增加 `node --check` 和 plugin sync hash check。
6. 增加 large-file budget check。

### 第二阶段: 可复现和 schema 化

1. 引入 lockfile。
2. 统一 `pyproject.toml` 和 requirements。
3. Pydantic config schema。
4. note frontmatter schema。
5. OpenRouter structured outputs。
6. prompt/model regression fixtures。

### 第三阶段: 研究能力升级

1. SQLite FTS5 本地索引。
2. citation graph enrichment。
3. OpenTelemetry/Phoenix traces。
4. Obsidian Bases 工作台。
5. 主动学习与复现循环。

## 6. 本次检查中的积极发现

- `script/.env` 存在且有非空值, 但没有被 Git 跟踪, 这是正确的安全边界。
- `Research_Notes` 没有发现重复 `paper_id` 或重复 arXiv ID。
- `Run_Records` 当前没有错误记录。
- 插件源目录和已安装目录哈希一致。
- `--force` preservation、Research Brief、Round 2 resources 等近期功能已经有相应测试基础。
- `doctor`/`check` 的结构已经很适合作为未来质量平台的核心。

## 7. 联网参考来源

- arXiv API Terms of Use: https://info.arxiv.org/help/api/tou.html
- GitHub Git LFS: https://docs.github.com/repositories/working-with-files/managing-large-files/about-git-large-file-storage
- DVC Remote Storage: https://dvc.org/doc/user-guide/data-management/remote-storage
- uv project lockfile: https://docs.astral.sh/uv/guides/projects/
- uv locking and syncing: https://docs.astral.sh/uv/concepts/projects/sync/
- pip-tools pip-compile: https://pip-tools.readthedocs.io/en/stable/cli/pip-compile/
- Ruff linter: https://docs.astral.sh/ruff/linter/
- pre-commit: https://pre-commit.com/
- GitHub security features: https://docs.github.com/code-security/getting-started/github-security-features
- Dependabot alerts: https://docs.github.com/en/code-security/concepts/supply-chain-security/about-dependabot-alerts
- Obsidian manifest: https://docs.obsidian.md/Reference/Manifest
- Obsidian build a plugin: https://docs.obsidian.md/Plugins/Getting%20started/Build%20a%20plugin
- Obsidian Bases view: https://docs.obsidian.md/plugins/guides/bases-view
- OpenTelemetry Python instrumentation: https://opentelemetry.io/docs/languages/python/instrumentation/
- Phoenix docs: https://arize.com/docs/phoenix
- RAGAS metrics: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/
- promptfoo intro: https://www.promptfoo.dev/docs/intro/
- OpenRouter structured outputs: https://openrouter.ai/docs/features/structured-outputs
- OpenRouter provider routing: https://openrouter.ai/docs/features/provider-routing
- OpenRouter reasoning tokens: https://openrouter.ai/docs/guides/best-practices/reasoning-tokens
- SQLite FTS5: https://www.sqlite.org/fts5.html
- Semantic Scholar API: https://www.semanticscholar.org/product/api
- OpenAlex Works API: https://developers.openalex.org/api-entities/works/get-content
- Crossref REST API: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- Pydantic settings: https://docs.pydantic.dev/usage/settings/
