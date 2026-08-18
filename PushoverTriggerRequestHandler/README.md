---
name: PushoverTriggerRequestHandler
version: 1.0.0
type: requestHandler
acmecseVersion: ">2026.05"
author: Andreas Kraft
license: BSD-3-Clause
---

# PushoverTriggerRequestHandler

A `<TriggerRequest>` handler that sends notifications via [Pushover](https://pushover.net) instead of an actual NSE endpoint. This lets a `<TriggerRequest>` resource result in a push notification to a phone or desktop, which is convenient for testing, demos, or lightweight deployments that don't have a real Notification Server Entity available.

## Installation

Copy `PushoverTriggerRequestHandler.py` into your ACME CSE's **external** plugin directory (not the implementation's internal one) - see [Plugin Directories](https://acmecse.net/plugins/PluginsOverview/#plugin-directories) in the ACME CSE documentation for details.

## Configuration

Add a `[TriggerHandler.pushover]` section to your `acme.ini`:

```ini
[TriggerHandler.pushover]
userKey=<Pushover user or group key>
appToken=<Pushover application token>
domain=<Domain for validating M2M-EXT-ID values, default: notification.example.com>
```

`domain` is optional and defaults to `notification.example.com` if not set.

`userKey` and `appToken` can also be overridden per `<TriggerRequest>` resource via labels, and the notification text can be customized per resource via the `message` and `title` labels. Supported labels:

| Label | Description | Default |
|-------|-------------|---------|
| `userKey` | Pushover user or group key | value from `[TriggerHandler.pushover]` |
| `appToken` | Pushover application token | value from `[TriggerHandler.pushover]` |
| `message` | Notification message text | derived from the `<TriggerRequest>`'s trigger purpose |
| `title` | Notification title | `TriggerRequest` |

See the plugin's docstring for further implementation details.

## Usage

Once installed and configured, `<TriggerRequest>` resources whose `mei` (M2M-EXT-ID) ends with the configured `domain` are routed through this handler, which sends a Pushover notification and updates the `<TriggerRequest>`'s trigger status accordingly. Any of `userKey`, `appToken`, `message`, or `title` can be overridden per resource via labels - see the table above - e.g.:

```
lbl: ["message:Hello, oneM2M!", "title:Notification from ACME CSE"]
```

## Testing

`sendTriggerNotification.hurl` contains example requests - registering an `<AE>`, creating a `<TriggerRequest>` to trigger a Pushover notification, then cleaning up - using [Hurl](https://hurl.dev), the command-line HTTP testing tool from Orange.

Shared values (host, port, release version, authorization) live in `hurl.vars`. Fill in your own `authorization` value there, then run:

```
hurl --variables-file hurl.vars sendTriggerNotification.hurl
```

## Notes

Requires a valid Pushover account, application token, and user/group key. See [pushover.net](https://pushover.net) to obtain these.
