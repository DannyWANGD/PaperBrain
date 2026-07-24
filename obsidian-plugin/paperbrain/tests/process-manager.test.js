"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const { EventEmitter } = require("node:events");

const { ProcessManager } = require("../src/process-manager");

class FakeChild extends EventEmitter {
  constructor() {
    super();
    this.stdout = new EventEmitter();
    this.stderr = new EventEmitter();
    this.killed = false;
  }

  kill() {
    this.killed = true;
  }
}

function invocation(args = ["script.py", "run"]) {
  return { executable: "python", args, prefixArgs: ["script.py"], cwd: "backend" };
}

function validPayload(command = "run") {
  return JSON.stringify({ ok: true, command, exit_code: 0, backend_version: "0.3.1", date: "2026-07-22" });
}

test("unsubscribing a view does not terminate the active process and a new view can attach", () => {
  const child = new FakeChild();
  const manager = new ProcessManager({ spawn: () => child });
  let firstEvents = 0;
  const unsubscribe = manager.subscribe(() => { firstEvents += 1; });
  manager.start({ invocation: invocation(), commandArgs: ["run"], spawnOptions: {}, context: { date: "2026-07-22", mode: "run" } });
  unsubscribe();
  child.stdout.emit("data", "working\n");
  assert.equal(child.killed, false);
  assert.equal(firstEvents, 2);
  let attached;
  manager.subscribe((snapshot) => { attached = snapshot; });
  assert.equal(attached.running, true);
  assert.equal(attached.context.date, "2026-07-22");
  assert.equal(attached.latestOutput, "working");
});

test("only one active process is allowed", () => {
  const child = new FakeChild();
  let spawnCount = 0;
  const manager = new ProcessManager({ spawn: () => { spawnCount += 1; return child; } });
  assert.equal(manager.start({ invocation: invocation(), commandArgs: ["run"], spawnOptions: {} }).started, true);
  assert.equal(manager.start({ invocation: invocation(), commandArgs: ["run"], spawnOptions: {} }).started, false);
  assert.equal(spawnCount, 1);
});

test("manager-owned diagnostic lines remain separated across view lifecycles", () => {
  const manager = new ProcessManager({ spawn: () => new FakeChild() });
  manager.appendLog("first diagnostic");
  manager.appendLog("second diagnostic");
  assert.equal(manager.snapshot().stderr, "first diagnostic\nsecond diagnostic");
});

test("stop requests soft cancellation before the timeout kills the main process", () => {
  const active = new FakeChild();
  const cancel = new FakeChild();
  const timers = [];
  let calls = 0;
  const manager = new ProcessManager({
    spawn: () => (++calls === 1 ? active : cancel),
    setTimeout: (callback) => { timers.push(callback); return timers.length; },
    clearTimeout: () => {},
  });
  manager.start({ invocation: invocation(), commandArgs: ["run"], spawnOptions: {}, timeoutMs: 3000 });
  assert.equal(manager.requestStop(), true);
  assert.deepEqual(manager.cancelInvocation.args.slice(-3), ["cancel", "--reason", "plugin_stop"]);
  assert.equal(active.killed, false);
  timers[0]();
  assert.equal(active.killed, true);
});

test("plugin unload terminates active and cancellation helper processes", () => {
  const active = new FakeChild();
  const cancel = new FakeChild();
  let calls = 0;
  const manager = new ProcessManager({ spawn: () => (++calls === 1 ? active : cancel), setTimeout: () => 1, clearTimeout: () => {} });
  manager.start({ invocation: invocation(), commandArgs: ["run"], spawnOptions: {} });
  manager.requestStop();
  manager.dispose();
  assert.equal(active.killed, true);
  assert.equal(cancel.killed, true);
});

test("a command completes and retains its final result without any view subscription", async () => {
  const child = new FakeChild();
  const notices = [];
  const manager = new ProcessManager({ spawn: () => child, onNotice: (notice) => notices.push(notice) });
  const result = manager.start({ invocation: invocation(), commandArgs: ["run"], spawnOptions: {} });
  child.stdout.emit("data", validPayload());
  child.emit("close", 0, null);
  const outcome = await result.completion;
  assert.equal(outcome.ok, true);
  assert.equal(manager.snapshot().lastPayload.date, "2026-07-22");
  assert.equal(manager.snapshot().running, false);
  assert.equal(notices.at(-1).ok, true);
});
