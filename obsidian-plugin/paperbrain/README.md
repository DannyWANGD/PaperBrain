# PaperBrain Console Plugin

This is the Obsidian desktop control surface for the local PaperBrain Python pipeline.

The plugin does not contain the Python backend. It expects a local PaperBrain checkout and calls:

```powershell
python script\paperbrain.py ...
```

Local development source lives here:

```text
obsidian-plugin/paperbrain/
```

The local Obsidian runtime copy lives here:

```text
.obsidian/plugins/paperbrain/
```

Use `sync_plugin.ps1` from `obsidian-plugin/` to copy the current source files into the vault plugin directory.
