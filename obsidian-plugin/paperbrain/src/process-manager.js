"use strict";

const {
  boundedAppend,
  buildSiblingInvocation,
  isCurrentProcess,
  mergeFailurePayload,
  parsePayload,
  processOutcome,
} = require("./runtime");

class ProcessManager {
  constructor(options = {}) {
    this.spawn = options.spawn;
    this.setTimeout = options.setTimeout || setTimeout;
    this.clearTimeout = options.clearTimeout || clearTimeout;
    this.inferStage = options.inferStage || (() => "");
    this.onNotice = options.onNotice || (() => {});
    this.listeners = new Set();
    this.process = null;
    this.cancelProcess = null;
    this.processToken = 0;
    this.stopTimer = null;
    this.invocation = null;
    this.cancelInvocation = null;
    this.spawnOptions = null;
    this.context = null;
    this.running = false;
    this.stopping = false;
    this.stdout = "";
    this.stderr = "";
    this.lastPayload = null;
    this.stage = "";
    this.latestOutput = "";
    this.completion = null;
  }

  snapshot() {
    return {
      running: this.running,
      stopping: this.stopping,
      stdout: this.stdout,
      stderr: this.stderr,
      lastPayload: this.lastPayload,
      stage: this.stage,
      latestOutput: this.latestOutput,
      context: this.context ? { ...this.context } : null,
    };
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

  appendLog(line) {
    this.stderr = boundedAppend(this.stderr, `${this.stderr ? "\n" : ""}${line}`);
    this.latestOutput = String(line || "").trim() || this.latestOutput;
    this.emit("output");
  }

  updateOutput(kind, value) {
    const text = String(value || "");
    if (!text) return;
    if (kind === "stdout") this.stdout = boundedAppend(this.stdout, text);
    else this.stderr = boundedAppend(this.stderr, text);
    const line = text.split(/\r?\n/).map((item) => item.trim()).filter(Boolean).pop();
    if (line) this.latestOutput = line;
    const inferred = this.inferStage(text);
    if (inferred) this.stage = inferred;
    this.emit("output");
  }

  setStage(stage) {
    const next = String(stage || "").trim();
    if (!next || next === this.stage) return false;
    this.stage = next;
    this.emit("stage");
    return true;
  }

  start({ invocation, commandArgs, spawnOptions, context = {}, timeoutMs = 20000, notify = true }) {
    if (this.running) return { started: false, reason: "already-running", completion: this.completion };
    this.stdout = "";
    this.stderr = "";
    this.lastPayload = null;
    this.stage = "";
    this.latestOutput = "";
    this.stopping = false;
    this.invocation = invocation;
    this.cancelInvocation = buildSiblingInvocation(invocation, ["cancel", "--reason", "plugin_stop"]);
    this.spawnOptions = spawnOptions;
    this.context = { ...context, command: commandArgs[0], commandArgs: [...commandArgs], timeoutMs };
    const token = this.processToken + 1;
    this.processToken = token;
    let child;
    try {
      child = this.spawn(invocation.executable, invocation.args, spawnOptions);
    } catch (error) {
      const outcome = processOutcome({ error, payload: null, stderr: "", expectedCommand: commandArgs[0] });
      this.lastPayload = mergeFailurePayload(null, commandArgs[0], outcome, null, null);
      this.stderr = `spawn failed: ${error.message}`;
      this.onNotice({ ok: false, message: "PaperBrain could not start. Open the console for details." });
      this.emit("finished");
      return { started: false, reason: "spawn-error", outcome, completion: Promise.resolve(outcome) };
    }
    this.process = child;
    this.running = true;
    this.emit("started");
    child.stdout.on("data", (data) => this.updateOutput("stdout", data));
    child.stderr.on("data", (data) => this.updateOutput("stderr", data));
    let resolveCompletion;
    this.completion = new Promise((resolve) => { resolveCompletion = resolve; });
    let settled = false;
    const finalize = ({ code = null, signal = null, error = null }) => {
      if (settled) return;
      settled = true;
      const ownsSlot = isCurrentProcess(this.process, this.processToken, child, token);
      const payload = parsePayload(this.stdout);
      const outcome = processOutcome({ code, signal, error, payload, stderr: this.stderr, expectedCommand: commandArgs[0] });
      if (!ownsSlot) {
        resolveCompletion(outcome);
        return;
      }
      this.clearStopTimer();
      this.lastPayload = outcome.ok ? payload : mergeFailurePayload(payload, commandArgs[0], outcome, code, signal);
      if (!outcome.ok) this.stderr = boundedAppend(this.stderr, `\n${outcome.reason}: ${outcome.message}`);
      this.process = null;
      this.invocation = null;
      this.cancelInvocation = null;
      this.running = false;
      this.stopping = false;
      this.stage = "";
      if (notify || !outcome.ok) {
        this.onNotice(outcome.ok
          ? { ok: true, message: outcome.message }
          : { ok: false, message: "PaperBrain stopped with an error. Open the console for details." });
      }
      this.emit("finished");
      resolveCompletion(outcome);
    };
    child.once("error", (error) => finalize({ error }));
    child.once("close", (code, signal) => finalize({ code, signal }));
    return { started: true, completion: this.completion };
  }

  requestStop() {
    if (!this.running || this.stopping) return false;
    const activeProcess = this.process;
    const activeToken = this.processToken;
    this.stopping = true;
    this.emit("stopping");
    if (this.cancelInvocation) {
      try {
        const cancel = this.spawn(this.cancelInvocation.executable, this.cancelInvocation.args, this.spawnOptions);
        this.cancelProcess = cancel;
        let failed = false;
        cancel.once("error", (error) => {
          failed = true;
          if (this.cancelProcess === cancel) this.cancelProcess = null;
          this.appendLog(`cancel request failed: ${error.message}`);
          this.onNotice({ ok: false, message: "PaperBrain cancellation request failed. See console details." });
        });
        cancel.once("close", (code) => {
          if (this.cancelProcess === cancel) this.cancelProcess = null;
          if (failed) return;
          if (code === 0) this.onNotice({ ok: true, message: "PaperBrain cancellation requested." });
          else {
            this.appendLog(`cancel command exited with code ${code}`);
            this.onNotice({ ok: false, message: "PaperBrain cancellation command failed. See console details." });
          }
        });
      } catch (error) {
        this.appendLog(`cancel request failed: ${error.message}`);
        this.onNotice({ ok: false, message: "PaperBrain cancellation request failed. See console details." });
      }
    }
    this.clearStopTimer();
    this.stopTimer = this.setTimeout(() => {
      this.stopTimer = null;
      if (isCurrentProcess(this.process, this.processToken, activeProcess, activeToken)) {
        this.appendLog("hard stop after cancellation timeout");
        try {
          activeProcess.kill();
          this.onNotice({ ok: false, message: "PaperBrain was stopped after the cancellation timeout." });
        } catch (error) {
          this.appendLog(`hard stop failed: ${error.message}`);
        }
      }
    }, Math.max(3000, Number(this.context && this.context.timeoutMs) || 20000));
    return true;
  }

  clearStopTimer() {
    if (!this.stopTimer) return;
    this.clearTimeout(this.stopTimer);
    this.stopTimer = null;
  }

  dispose(reason = "plugin unload") {
    this.clearStopTimer();
    this.processToken += 1;
    const active = this.process;
    const cancel = this.cancelProcess;
    this.process = null;
    this.cancelProcess = null;
    this.running = false;
    this.stopping = false;
    if (active) {
      this.stderr = boundedAppend(this.stderr, `\nterminating active process: ${reason}`);
      try { active.kill(); } catch (_) {}
    }
    if (cancel) {
      try { cancel.kill(); } catch (_) {}
    }
    this.emit("disposed");
  }
}

module.exports = { ProcessManager };
