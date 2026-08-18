---
name: pluginName
version: 1.0.0
type: requestHandler   # requestHandler | protocolBinding | storageBackend | notificationHandler | scriptExtension | other
acmecseVersion: ">=2026.05"
author: yourName
license: MIT   # must match the LICENSE file in this folder
---

# pluginName

One-line description of what this plugin does.

## Installation

Copy `pluginName.py` into your ACME CSE's configured plugin directory.

## Configuration

Describe any `acme.ini` settings, environment variables, or other configuration
this plugin reads. If none, say so explicitly.

## Usage

Describe what the plugin does once loaded — what it hooks into, what triggers it,
and any behavior the user should expect.

## Testing

`<descriptive-name>.hurl` contains example requests that exercise this plugin.
Run with:

    hurl <descriptive-name>.hurl

## Notes

Anything else worth mentioning — known limitations, related plugins, etc.
