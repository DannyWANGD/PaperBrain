const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const test = require("node:test");

const {
  normalizeCategories,
  normalizeKeywords,
  parseKeywordBatch,
  readDiscoverySettings,
  validateDiscoverySettings,
  writeDiscoverySettings,
} = require("../src/discovery-settings");
const {
  ARXIV_CATEGORY_GROUPS,
  ARXIV_CATEGORY_IDS,
  DEFAULT_CATEGORIES,
  filterCategoryGroups,
  updateCategoryGroupSelection,
} = require("../src/arxiv-categories");

function withConfig(content, callback) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "paperbrain-discovery-"));
  const configPath = path.join(directory, "config.yaml");
  fs.writeFileSync(configPath, content, "utf8");
  try {
    callback(configPath);
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
}

test("the bundled category catalog is complete enough for every official top-level group", () => {
  assert.deepEqual(
    ARXIV_CATEGORY_GROUPS.map((group) => group.group),
    [
      "Computer Science",
      "Economics",
      "Electrical Engineering and Systems Science",
      "Mathematics",
      "Physics",
      "Quantitative Biology",
      "Quantitative Finance",
      "Statistics",
    ],
  );
  assert.equal(ARXIV_CATEGORY_IDS.size, ARXIV_CATEGORY_GROUPS.flatMap((group) => group.categories).length);
  assert.equal(ARXIV_CATEGORY_IDS.size, 155);
  for (const category of DEFAULT_CATEGORIES) assert.ok(ARXIV_CATEGORY_IDS.has(category));
  for (const category of ["cs.RO", "econ.EM", "eess.SY", "math.OC", "quant-ph", "q-bio.CB", "q-fin.MF", "stat.ML"]) {
    assert.ok(ARXIV_CATEGORY_IDS.has(category));
  }
});

test("keyword and category normalization trims and deduplicates values", () => {
  assert.deepEqual(normalizeKeywords([" VLA ", "vla", "World Model", ""]), ["VLA", "World Model"]);
  assert.deepEqual(parseKeywordBatch(" VLA, World Model\nVLA\r\nRobot Manipulation "), [
    "VLA",
    "World Model",
    "Robot Manipulation",
  ]);
  assert.deepEqual(normalizeCategories(["cs.RO", "invalid", "cs.RO", "stat.ML"]), ["cs.RO", "stat.ML"]);
});

test("category search checks codes and names without flattening groups", () => {
  const robotics = filterCategoryGroups("robotics");
  const code = filterCategoryGroups("stat.ml");

  assert.deepEqual(robotics.map((group) => group.group), ["Computer Science"]);
  assert.deepEqual(robotics[0].categories.map((category) => category.id), ["cs.RO"]);
  assert.deepEqual(code[0].categories.map((category) => category.id), ["stat.ML"]);
});

test("group selection applies to the complete group even after filtering", () => {
  const selected = updateCategoryGroupSelection(new Set(["stat.ML"]), "Economics", true);
  const cleared = updateCategoryGroupSelection(selected, "Economics", false);

  assert.ok(selected.has("econ.EM"));
  assert.ok(selected.has("econ.GN"));
  assert.ok(selected.has("econ.TH"));
  assert.ok(selected.has("stat.ML"));
  assert.equal(cleared.has("econ.EM"), false);
  assert.ok(cleared.has("stat.ML"));
});

test("discovery validation rejects empty keywords and selected categories", () => {
  const result = validateDiscoverySettings({ keywords: [], categoryMode: "selected", categories: [] });
  assert.equal(result.ok, false);
  assert.equal(result.errors.length, 2);
});

test("all category mode still requires a keyword but not selected categories", () => {
  const result = validateDiscoverySettings({ keywords: ["robot"], categoryMode: "all", categories: [] });
  assert.equal(result.ok, true);
});

test("a missing config reports its resolved path and cannot be saved", () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "paperbrain-discovery-missing-"));
  const configPath = path.join(directory, "config.yaml");
  try {
    const state = readDiscoverySettings(configPath);
    assert.equal(state.readable, false);
    assert.equal(state.configPath, configPath);
    assert.match(state.error, /config was not found/);
    assert.throws(
      () => writeDiscoverySettings(configPath, {
        keywords: ["robot"],
        categoryMode: "selected",
        categories: ["cs.RO"],
      }),
      /config was not found/,
    );
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
});

test("read and write update only discovery fields while preserving comments and unrelated config", () => {
  withConfig(
    [
      "# user-owned config",
      "openrouter:",
      "  api_key: ${OPENROUTER_API_KEY}",
      "search:",
      "  # keep this comment",
      "  keywords: [robot]",
      "  max_results: 50",
      "  arxiv_categories: [cs.RO]",
      "obsidian:",
      "  vault_path: /tmp/vault",
      "",
    ].join("\n"),
    (configPath) => {
      const before = readDiscoverySettings(configPath);
      assert.equal(before.ok, true);
      assert.deepEqual(before.keywords, ["robot"]);

      writeDiscoverySettings(configPath, {
        keywords: ["VLA", "World Model"],
        categoryMode: "all",
        categories: ["cs.RO", "stat.ML"],
      });
      const text = fs.readFileSync(configPath, "utf8");
      const after = readDiscoverySettings(configPath);
      assert.match(text, /# user-owned config/);
      assert.match(text, /# keep this comment/);
      assert.match(text, /api_key: \$\{OPENROUTER_API_KEY\}/);
      assert.match(text, /vault_path: \/tmp\/vault/);
      assert.match(text, /max_results: 50/);
      assert.match(text, /arxiv_page_size: 200/);
      assert.deepEqual(after.keywords, ["VLA", "World Model"]);
      assert.equal(after.categoryMode, "all");
      assert.deepEqual(after.categories, ["cs.RO", "stat.ML"]);
    },
  );
});

test("invalid discovery update leaves the config untouched", () => {
  withConfig("search:\n  keywords: [robot]\n  arxiv_categories: [cs.RO]\n", (configPath) => {
    const before = fs.readFileSync(configPath, "utf8");
    assert.throws(
      () => writeDiscoverySettings(configPath, { keywords: [], categoryMode: "selected", categories: [] }),
      /at least one research keyword/,
    );
    assert.equal(fs.readFileSync(configPath, "utf8"), before);
  });
});

test("saving discovery preferences does not mask an invalid existing page size", () => {
  withConfig(
    "search:\n  keywords: [robot]\n  arxiv_categories: [cs.RO]\n  arxiv_page_size: 0\n",
    (configPath) => {
      writeDiscoverySettings(configPath, {
        keywords: ["VLA"],
        categoryMode: "selected",
        categories: ["cs.RO"],
      });
      assert.match(fs.readFileSync(configPath, "utf8"), /arxiv_page_size: 0/);
    },
  );
});

test("a malformed search section is reported without modifying the config", () => {
  withConfig("search: invalid\nprovider: openrouter\n", (configPath) => {
    const before = fs.readFileSync(configPath, "utf8");
    const state = readDiscoverySettings(configPath);
    assert.equal(state.readable, false);
    assert.match(state.error, /search.*YAML mapping/);
    assert.throws(
      () => writeDiscoverySettings(configPath, {
        keywords: ["robot"],
        categoryMode: "selected",
        categories: ["cs.RO"],
      }),
      /search.*YAML mapping/,
    );
    assert.equal(fs.readFileSync(configPath, "utf8"), before);
  });
});

test("failed atomic replacement restores the original config", () => {
  withConfig("search:\n  keywords: [robot]\n  arxiv_categories: [cs.RO]\n", (configPath) => {
    const before = fs.readFileSync(configPath, "utf8");
    let renameCount = 0;
    const failingFs = {
      ...fs,
      renameSync(source, destination) {
        renameCount += 1;
        if (renameCount === 2) throw new Error("replacement failed");
        return fs.renameSync(source, destination);
      },
    };

    assert.throws(
      () => writeDiscoverySettings(configPath, {
        keywords: ["VLA"],
        categoryMode: "selected",
        categories: ["cs.RO"],
      }, { fsApi: failingFs }),
      /replacement failed/,
    );
    assert.equal(fs.readFileSync(configPath, "utf8"), before);
    assert.deepEqual(fs.readdirSync(path.dirname(configPath)), ["config.yaml"]);
  });
});
