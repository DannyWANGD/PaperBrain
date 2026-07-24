"use strict";

const https = require("https");
const { HttpsProxyAgent } = require("https-proxy-agent");
const { normalizeProxyUrl } = require("./runtime");

const REDIRECT_CODES = new Set([301, 302, 303, 307, 308]);

function inheritedProxyUrl(env = process.env) {
  for (const key of ["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"]) {
    const value = String((env && env[key]) || "").trim();
    if (!value) continue;
    try {
      const parsed = new URL(value);
      if (["http:", "https:"].includes(parsed.protocol) && parsed.hostname && !parsed.username && !parsed.password) {
        return value;
      }
    } catch (_) {
      // Ignore malformed inherited proxy variables.
    }
  }
  return "";
}

function proxyForDownload(options = {}) {
  if (options.proxyMode === "direct") return "";
  if (options.proxyMode === "manual") {
    const proxyUrl = normalizeProxyUrl(options.proxyUrl);
    if (!proxyUrl) throw new Error("The configured manual proxy URL is invalid.");
    return proxyUrl;
  }
  return inheritedProxyUrl(options.env);
}

function validateTargetUrl(value) {
  const parsed = new URL(String(value || ""));
  if (parsed.protocol !== "https:" || parsed.username || parsed.password) {
    throw new Error("Downloads require a credential-free HTTPS URL.");
  }
  return parsed;
}

function downloadHttpsBuffer(url, options = {}) {
  const maxRedirects = Math.max(0, Number(options.maxRedirects) || 5);
  const maxBytes = Math.max(1024, Number(options.maxBytes) || 200 * 1024 * 1024);
  const timeoutMs = Math.max(1000, Number(options.timeoutMs) || 30000);
  const proxyUrl = proxyForDownload(options);
  const agent = proxyUrl ? new HttpsProxyAgent(proxyUrl) : undefined;

  const requestOnce = (currentUrl, redirectCount, seen) => new Promise((resolve, reject) => {
    let target;
    try {
      target = validateTargetUrl(currentUrl);
    } catch (error) {
      reject(error);
      return;
    }
    if (seen.has(target.href)) {
      reject(new Error("Download redirect loop detected."));
      return;
    }
    seen.add(target.href);

    const request = https.get(target, {
      agent,
      headers: {
        Accept: "application/octet-stream,application/json;q=0.9,*/*;q=0.8",
        "User-Agent": "PaperBrain-Obsidian/0.5.1",
      },
      rejectUnauthorized: true,
    }, (response) => {
      const statusCode = Number(response.statusCode || 0);
      const location = response.headers.location;
      if (REDIRECT_CODES.has(statusCode) && location) {
        response.resume();
        if (redirectCount >= maxRedirects) {
          reject(new Error(`Download exceeded ${maxRedirects} redirects.`));
          return;
        }
        let nextUrl;
        try {
          nextUrl = new URL(location, target).href;
          validateTargetUrl(nextUrl);
        } catch (error) {
          reject(error);
          return;
        }
        requestOnce(nextUrl, redirectCount + 1, seen).then(resolve, reject);
        return;
      }
      if (statusCode < 200 || statusCode >= 300) {
        response.resume();
        reject(new Error(`Download returned HTTP ${statusCode}.`));
        return;
      }

      const declaredLength = Number(response.headers["content-length"] || 0);
      if (declaredLength > maxBytes) {
        response.resume();
        reject(new Error(`Download declared ${declaredLength} bytes; limit is ${maxBytes}.`));
        return;
      }
      const chunks = [];
      let bytesRead = 0;
      response.on("data", (chunk) => {
        bytesRead += chunk.length;
        if (bytesRead > maxBytes) {
          response.destroy(new Error(`Download exceeded the ${maxBytes}-byte limit.`));
          return;
        }
        chunks.push(chunk);
      });
      response.once("error", reject);
      response.once("end", () => resolve(Buffer.concat(chunks)));
    });
    request.setTimeout(timeoutMs, () => request.destroy(new Error(`Download timed out after ${timeoutMs} ms.`)));
    request.once("error", reject);
  });

  return requestOnce(validateTargetUrl(url).href, 0, new Set());
}

module.exports = {
  downloadHttpsBuffer,
  inheritedProxyUrl,
  proxyForDownload,
  validateTargetUrl,
};
