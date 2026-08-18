# ACME CSE Community Plugins

Community-contributed plugins for [ACME CSE](https://github.com/ankraft/ACME-oneM2M-CSE), the open-source oneM2M CSE implementation.

Each subfolder in this repository is a self-contained plugin — a request handler, protocol binding, or other extension for the ACME CSE. Browse the list below, grab what you need, and drop it into your CSE's plugin directory.

## Available Plugins

| Name | Type | Description | License |
|------|------|--------------|---------|
| [PushoverTriggerRequestHandler](PushoverTriggerRequestHandler/) | requestHandler | Sends `TriggerRequest` notifications via [Pushover](https://pushover.net) | BSD-3-Clause |
## Structure

Every plugin lives in its own top-level folder, named after the plugin itself:

```
<pluginName>/
├── README.md           # plugin metadata (YAML frontmatter) + usage docs
├── LICENSE             # the plugin author's chosen license
├── <pluginName>.py     # the plugin module
└── ... other files...  # extra files to use together with the plugin
```

The plugin's `README.md` starts with a YAML frontmatter block carrying its metadata:

```yaml
---
name: pluginName
version: 1.0.0
type: requestHandler
acmecseVersion: ">=2026.05"
author: yourName
license: MIT
---
```

## Installing a Plugin

Copy the plugin's `.py` file into your ACME CSE's configured plugin directory. See the plugin's own `README.md` for any additional configuration steps.

## Licensing

Each plugin is licensed independently by its author — check the plugin's own `LICENSE` file before use. The repository infrastructure itself (this README, templates, tooling) is licensed under the top-level [LICENSE](LICENSE) (BSD 3-Clause).

## Contributing

Contributions are welcome. To add a plugin:

1. Copy [`TEMPLATE_README.md`](TEMPLATE_README.md) to `<pluginName>/README.md` and fill it in, including the frontmatter block.
2. Add your `LICENSE` file, plugin module, and a `.hurl` file with example requests demonstrating its use.
3. Open a pull request adding the new top-level folder following the structure above.
