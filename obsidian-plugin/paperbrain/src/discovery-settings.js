const fs = require("fs");
const os = require("os");
const path = require("path");
const YAML = require("yaml");
const {
  ARXIV_CATEGORY_IDS,
  DEFAULT_CATEGORIES,
  DEFAULT_KEYWORDS,
} = require("./arxiv-categories");

function textValue(value) {
  return typeof value === "string" ? value.trim() : "";
}

function defaultConfigPath(homeDir = os.homedir()) {
  return path.join(homeDir, ".paperbrain", "config", "config.yaml");
}

function resolveDiscoveryConfigPath(configPath, homeDir = os.homedir(), pathApi = path) {
  const configured = textValue(configPath);
  return configured ? pathApi.resolve(configured) : defaultConfigPath(homeDir);
}

function normalizeKeywords(values) {
  const normalized = [];
  const seen = new Set();
  for (const raw of Array.isArray(values) ? values : []) {
    const value = textValue(raw);
    const key = value.toLocaleLowerCase();
    if (!value || seen.has(key)) continue;
    seen.add(key);
    normalized.push(value);
  }
  return normalized;
}

function parseKeywordBatch(value) {
  return normalizeKeywords(String(value || "").split(/[,\r\n]+/));
}

function normalizeCategories(values) {
  const normalized = [];
  const seen = new Set();
  for (const raw of Array.isArray(values) ? values : []) {
    const value = textValue(raw);
    if (!value || seen.has(value) || !ARXIV_CATEGORY_IDS.has(value)) continue;
    seen.add(value);
    normalized.push(value);
  }
  return normalized;
}

function validateDiscoverySettings(value) {
  const keywords = normalizeKeywords(value && value.keywords);
  const categoryMode = value && value.categoryMode === "all" ? "all" : "selected";
  const categories = normalizeCategories(value && value.categories);
  const errors = [];
  if (!keywords.length) errors.push("Add at least one research keyword.");
  if (categoryMode === "selected" && !categories.length) errors.push("Choose at least one arXiv category.");
  return { ok: errors.length === 0, errors, keywords, categoryMode, categories };
}

function readDiscoverySettings(configPath, options = {}) {
  const fsApi = options.fsApi || fs;
  const resolvedPath = resolveDiscoveryConfigPath(configPath, options.homeDir, options.pathApi || path);
  if (!fsApi.existsSync(resolvedPath)) {
    return {
      ok: false,
      readable: false,
      configPath: resolvedPath,
      error: `PaperBrain config was not found: ${resolvedPath}`,
      keywords: [...DEFAULT_KEYWORDS],
      categoryMode: "selected",
      categories: [...DEFAULT_CATEGORIES],
    };
  }
  try {
    const document = YAML.parseDocument(fsApi.readFileSync(resolvedPath, "utf8"));
    if (document.errors.length) throw document.errors[0];
    const config = document.toJS() || {};
    if (config.search != null && (typeof config.search !== "object" || Array.isArray(config.search))) {
      throw new Error("'search' must be a YAML mapping");
    }
    const search = config.search && typeof config.search === "object" ? config.search : {};
    const values = validateDiscoverySettings({
      keywords: search.keywords || DEFAULT_KEYWORDS,
      categoryMode: search.arxiv_category_mode,
      categories: search.arxiv_categories || DEFAULT_CATEGORIES,
    });
    return { ...values, ok: values.ok, readable: true, configPath: resolvedPath, error: values.errors.join(" ") };
  } catch (error) {
    return {
      ok: false,
      readable: false,
      configPath: resolvedPath,
      error: `PaperBrain config could not be read: ${error.message}`,
      keywords: [...DEFAULT_KEYWORDS],
      categoryMode: "selected",
      categories: [...DEFAULT_CATEGORIES],
    };
  }
}

function replaceFileFromTemp(fsApi, targetPath, tempPath) {
  const backupPath = `${targetPath}.${process.pid}.${Date.now()}.paperbrain-backup`;
  let movedOriginal = false;
  let installedReplacement = false;
  try {
    fsApi.renameSync(targetPath, backupPath);
    movedOriginal = true;
    fsApi.renameSync(tempPath, targetPath);
    installedReplacement = true;
  } catch (error) {
    if (fsApi.existsSync(tempPath)) fsApi.unlinkSync(tempPath);
    if (movedOriginal && !installedReplacement && fsApi.existsSync(backupPath) && !fsApi.existsSync(targetPath)) {
      fsApi.renameSync(backupPath, targetPath);
    }
    throw error;
  }
  try {
    fsApi.unlinkSync(backupPath);
  } catch (_) {
    // The replacement is committed. A stale backup is safer than reporting a false write failure.
  }
}

function writeDiscoverySettings(configPath, value, options = {}) {
  const fsApi = options.fsApi || fs;
  const pathApi = options.pathApi || path;
  const resolvedPath = resolveDiscoveryConfigPath(configPath, options.homeDir, pathApi);
  const validated = validateDiscoverySettings(value);
  if (!validated.ok) throw new Error(validated.errors.join(" "));
  if (!fsApi.existsSync(resolvedPath)) throw new Error(`PaperBrain config was not found: ${resolvedPath}`);

  const document = YAML.parseDocument(fsApi.readFileSync(resolvedPath, "utf8"));
  if (document.errors.length) throw document.errors[0];
  const config = document.toJS() || {};
  if (config.search != null && (typeof config.search !== "object" || Array.isArray(config.search))) {
    throw new Error("'search' must be a YAML mapping");
  }
  if (!document.get("search")) document.set("search", {});
  document.setIn(["search", "keywords"], validated.keywords);
  document.setIn(["search", "arxiv_category_mode"], validated.categoryMode);
  document.setIn(["search", "arxiv_categories"], validated.categories);
  if (document.getIn(["search", "arxiv_page_size"]) == null) {
    document.setIn(["search", "arxiv_page_size"], 200);
  }

  const tempPath = `${resolvedPath}.${process.pid}.${Date.now()}.tmp`;
  fsApi.writeFileSync(tempPath, String(document), "utf8");
  replaceFileFromTemp(fsApi, resolvedPath, tempPath);
  return {
    ok: true,
    configPath: resolvedPath,
    keywords: validated.keywords,
    categoryMode: validated.categoryMode,
    categories: validated.categories,
  };
}

module.exports = {
  defaultConfigPath,
  normalizeCategories,
  normalizeKeywords,
  parseKeywordBatch,
  readDiscoverySettings,
  resolveDiscoveryConfigPath,
  validateDiscoverySettings,
  writeDiscoverySettings,
};
