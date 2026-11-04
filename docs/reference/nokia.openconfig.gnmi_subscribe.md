# Ansible Module: nokia.openconfig.gnmi_subscribe

**Retrieve configuration and state using gNMI Subscribe**

!!! note "Notes"

    Requires the [`nokia.openconfig.grpc`](nokia.openconfig.grpc.md) connection.

    Check mode is supported. The task is skipped and no Subscribe RPC is sent (use [nokia.openconfig.gnmi_get](nokia.openconfig.gnmi_get.md) for read-only checks).

    The Subscribe RPC is a bidirectional stream. The connection sends the `SubscribeRequest`, and in `POLL` mode one `Poll` after the initial synchronization, then reads responses until the subscription completes.

    `ONCE` completes with the `sync_response` of the target, `POLL` with the second `sync_response`. If [`duration`](#param-duration) expires first, the task fails.

    `STREAM` is closed by the client when [`duration`](#param-duration) expires, and the task returns the notifications received until then. With [`config_subscription`](#param-config-subscription) and no [`duration`](#param-duration), the task returns as soon as the target reports a `sync_done` with `done=true` after the initial synchronization.

## Synopsis

* Sends a gNMI `SubscribeRequest` and collects the responses.
* Option names are the `SubscriptionList` and `Subscription` fields in snake_case, and the values follow the gNMI 0.10.0 protobuf messages. Enum values are case-insensitive.
* `ONCE` returns the merged object tree, like [nokia.openconfig.gnmi_get](nokia.openconfig.gnmi_get.md).
* `STREAM` collects notifications until [`duration`](#param-duration) expires. `POLL` sends one Poll after the initial synchronization and returns both rounds.

## Parameters

| Parameter | Type | Comments |
| --- | --- | --- |
| path {#param-path} | list | Paths to subscribe to, `Subscription.path`. Every path uses the same [`stream_mode`](#param-stream-mode), [`sample_interval`](#param-sample-interval), [`heartbeat_interval`](#param-heartbeat-interval) and [`suppress_redundant`](#param-suppress-redundant).<br/>Mutually exclusive with [`subscription`](#param-subscription). |
| subscription {#param-subscription} | list | Subscriptions with individual settings, `SubscriptionList.subscription`. Each entry has `path` and optionally `stream_mode`, `sample_interval`, `heartbeat_interval` and `suppress_redundant`, with the same meaning as the top-level options.<br/>The 1.0.0 keys `mode`, `sampleInterval`, `heartbeatInterval` and `suppressRedundant` were removed in 2.0.0.<br/>Mutually exclusive with [`path`](#param-path). |
| origin {#param-origin} | str | Origin of the paths, `Path.origin`, for example `openconfig` or `rfc7951`. Set on [`prefix`](#param-prefix) if given, otherwise on each path that does not name its own origin.<br/>With an origin, element names keep their YANG module prefix.<br/>Defaults to the `gnmi_origin` option of the connection. An empty string sends the paths without origin. |
| prefix {#param-prefix} | str | Common prefix for all paths, `SubscriptionList.prefix`.<br/>**Default:** `''` |
| target {#param-target} | str | Target name set on the prefix, `Path.target`. |
| model {#param-model} | str | Restricts the subscription to a model by name, `SubscriptionList.use_models`. |
| mode {#param-mode} | str | Subscription mode, `SubscriptionList.mode`.<br/>One of `STREAM`, `ONCE`, `POLL`.<br/>The default changed from `ONCE` to `STREAM` in 2.0.0, matching the default of the gNMI specification.<br/>**Default:** `STREAM` |
| stream_mode {#param-stream-mode} | str | Mode of each subscription if [`mode=STREAM`](#param-mode), `Subscription.mode`.<br/>One of `SAMPLE`, `ON_CHANGE`, `TARGET_DEFINED`. Defaults to `SAMPLE`. |
| sample_interval {#param-sample-interval} | str | Sample interval as Go duration, for example `10s`, `Subscription.sample_interval`.<br/>Omitted or `0s` lets the target choose. |
| heartbeat_interval {#param-heartbeat-interval} | str | Heartbeat interval as Go duration, `Subscription.heartbeat_interval`. |
| suppress_redundant {#param-suppress-redundant} | bool | Suppress updates of unchanged values, `Subscription.suppress_redundant`. |
| updates_only {#param-updates-only} | bool | Do not send the initial state, only changes after the synchronization, `SubscriptionList.updates_only`. |
| allow_aggregation {#param-allow-aggregation} | bool | Allow the target to aggregate elements that are marked as eligible for aggregation in the schema. |
| qos {#param-qos} | int | DSCP marking of the subscription, `SubscriptionList.qos`. |
| encoding {#param-encoding} | str | Overrides the encoding of the connection, `SubscriptionList.encoding`. Either `JSON` or `JSON_IETF`. |
| depth {#param-depth} | int | Limits the depth of the returned subtrees using the gNMI Depth extension, `Depth.level`. `0` means no limit. |
| config_subscription {#param-config-subscription} | bool | Subscribe to configuration nodes only, using the gNMI ConfigSubscription extension (`ConfigSubscriptionStart`).<br/>SR OS supports the extension with [`mode=STREAM`](#param-mode) only.<br/>The target reports each commit with a `sync_done` extension, returned in R`extensions` with `commit_confirm_id`, `server_commit_id` and `done`.<br/>With [`mode=STREAM`](#param-mode) and no [`duration`](#param-duration), the subscription ends when the target reports `done=true`, at the latest when the command timeout of the connection expires.<br/>**Default:** `false` |
| duration {#param-duration} | int | Time in seconds to collect responses. A task cannot keep a subscription open, so a `STREAM` subscription always ends.<br/>For `STREAM` the subscription is closed when it expires. For `ONCE` and `POLL` it is a timeout.<br/>Defaults to `20`, except for [`config_subscription`](#param-config-subscription) in `STREAM` mode, see there.<br/>Must be lower than the `persistent_command_timeout` of the connection. |

## Examples

```yaml
- name: Get the system configuration using Subscribe ONCE (SR OS)
  nokia.openconfig.gnmi_subscribe:
    mode: once
    path:
      - /configure/system

- name: Get the system information using Subscribe ONCE (SR Linux)
  nokia.openconfig.gnmi_subscribe:
    mode: once
    path:
      - /system/information

- name: Collect management port statistics for 5 seconds (SR OS)
  nokia.openconfig.gnmi_subscribe:
    prefix: /state
    path:
      - /port[port-id=A/1]/statistics
    stream_mode: sample
    sample_interval: 1s
    duration: 5

- name: Collect management interface statistics for 5 seconds (SR Linux)
  nokia.openconfig.gnmi_subscribe:
    path:
      - /interface[name=mgmt0]/statistics
    stream_mode: sample
    sample_interval: 1s
    duration: 5

- name: Sample OpenConfig interface counters every 10 seconds for 30 seconds
  nokia.openconfig.gnmi_subscribe:
    origin: openconfig
    path:
      - /interfaces/interface/state/counters
    stream_mode: sample
    sample_interval: 10s
    duration: 30

- name: Collect configuration changes for 60 seconds (SR OS)
  nokia.openconfig.gnmi_subscribe:
    path:
      - /configure/system
    stream_mode: on_change
    config_subscription: true
    duration: 60
  register: commits

- name: Collect configuration changes for 60 seconds (SR Linux)
  nokia.openconfig.gnmi_subscribe:
    path:
      - /interface[name=ethernet-1/1]
    stream_mode: on_change
    config_subscription: true
    duration: 60
  register: commits
```
## Return Values

| Parameter | Type | Comments |
| --- | --- | --- |
| output {#return-output} | str |  - For `ONCE`, the merged object tree as JSON string. - For `STREAM` and `POLL`, a JSON string with a list of notifications,<br/>**Returned:** success<br/>**Sample:** `[{"prefix":"/state/port[port-id=1/1/c1/1]/ethernet/statistics","timestamp":"2020-02-18T00:19:34.954275","values":{"in-octets":"0"}}]` |
| extensions {#return-extensions} | list |  - Extensions returned in the `SubscribeResponse` messages, using<br/>**Returned:** success<br/>**Sample:** `[{"config_subscription":{"sync_done":{"commit_confirm_id":"c1","server_commit_id":"17","done":true}}}]` |

*New in version 1.0.0*
