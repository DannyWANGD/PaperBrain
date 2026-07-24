"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const { EventEmitter } = require("node:events");
const https = require("node:https");

const {
  downloadHttpsBuffer,
  inheritedProxyUrl,
  proxyForDownload,
  validateTargetUrl,
} = require("../src/proxy-download");

function response(statusCode, headers = {}, chunks = []) {
  const stream = new EventEmitter();
  stream.statusCode = statusCode;
  stream.headers = headers;
  stream.resume = () => {};
  stream.destroy = (error) => process.nextTick(() => stream.emit("error", error));
  stream.send = () => {
    for (const chunk of chunks) stream.emit("data", Buffer.from(chunk));
    stream.emit("end");
  };
  return stream;
}

function mockHttpsGet(t, responses, calls) {
  const original = https.get;
  const restore = () => { https.get = original; };
  t.after(restore);
  https.get = (target, options, callback) => {
    const request = new EventEmitter();
    request.setTimeout = () => {};
    request.destroy = (error) => process.nextTick(() => request.emit("error", error));
    calls.push({ target: target.href, options });
    const next = responses.shift();
    process.nextTick(() => {
      callback(next);
      process.nextTick(() => next.send());
    });
    return request;
  };
  return restore;
}

test("inherited proxy selection accepts only credential-free HTTP(S) values", () => {
  assert.equal(inheritedProxyUrl({
    HTTPS_PROXY: "http://proxy.example:8080",
    HTTP_PROXY: "http://fallback.example:8081",
  }), "http://proxy.example:8080");
  assert.equal(inheritedProxyUrl({ HTTPS_PROXY: "http://user:password@proxy.example:8080" }), "");
  assert.equal(inheritedProxyUrl({ ALL_PROXY: "socks5://proxy.example:1080" }), "");
  assert.equal(proxyForDownload({ proxyMode: "direct", env: { HTTPS_PROXY: "http://proxy.example:8080" } }), "");
  assert.equal(proxyForDownload({ proxyMode: "manual", proxyUrl: "http://127.0.0.1:7890" }), "http://127.0.0.1:7890");
});

test("proxy-aware downloader follows HTTPS redirects and returns bounded bytes", async (t) => {
  const calls = [];
  mockHttpsGet(t, [
    response(302, { location: "https://assets.example/file.whl" }),
    response(200, { "content-length": "5" }, ["wheel"]),
  ], calls);

  const bytes = await downloadHttpsBuffer("https://github.example/release", {
    proxyMode: "manual",
    proxyUrl: "http://127.0.0.1:7890",
    maxBytes: 1024,
  });

  assert.equal(bytes.toString(), "wheel");
  assert.deepEqual(calls.map((call) => call.target), [
    "https://github.example/release",
    "https://assets.example/file.whl",
  ]);
  assert.ok(calls.every((call) => call.options.agent));
  assert.ok(calls.every((call) => call.options.rejectUnauthorized));
});

test("downloader rejects insecure targets, redirects, and oversized responses", async (t) => {
  assert.throws(() => validateTargetUrl("http://example.com/file"), /HTTPS/);
  const redirectCalls = [];
  const restoreRedirect = mockHttpsGet(t, [response(302, { location: "http://example.com/file" })], redirectCalls);
  await assert.rejects(
    downloadHttpsBuffer("https://example.com/start", { proxyMode: "direct" }),
    /HTTPS/,
  );
  restoreRedirect();

  const sizeCalls = [];
  mockHttpsGet(t, [response(200, { "content-length": "4096" })], sizeCalls);
  await assert.rejects(
    downloadHttpsBuffer("https://example.com/file", { proxyMode: "direct", maxBytes: 2048 }),
    /limit is 2048/,
  );
});
